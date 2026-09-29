#!/usr/bin/env python3
"""Compare a rendered still against a reference PNG (regression aid, not a pass/fail gate).

Usage:
  tools/diff_frame.py <rendered.png> <reference.png> [--heatmap out.png]

Content is deliberately fictional and icons may be reconstructed, so an exact
pixel match is not the goal — use the similarity score to catch layout/spacing/proportion
regressions across edits to the same scene, and do the actual fidelity judgment by eye
(ver fases/8-render-y-revision.md).

Prints a single JSON object to stdout:
  {"ok": bool, "similarity": float, "size_mismatch": bool, "heatmap": str|None, "error": str|None}
"""
import argparse
import json
import sys
from pathlib import Path

try:
    import numpy as np
    from PIL import Image
    from skimage.metrics import structural_similarity as ssim
except ImportError as exc:  # pragma: no cover
    print(json.dumps({"ok": False, "error": f"missing dependency: {exc}. Run: pip install -r tools/requirements.txt"}))
    sys.exit(1)


def fail(message: str) -> None:
    print(json.dumps({"ok": False, "error": message}))
    sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("rendered")
    parser.add_argument("reference")
    parser.add_argument("--heatmap", help="Optional path to write a difference heatmap PNG")
    args = parser.parse_args()

    rendered_path, reference_path = Path(args.rendered), Path(args.reference)
    if not rendered_path.exists():
        fail(f"rendered image not found: {rendered_path}")
    if not reference_path.exists():
        fail(f"reference image not found: {reference_path}")

    rendered = Image.open(rendered_path).convert("RGB")
    reference = Image.open(reference_path).convert("RGB")

    size_mismatch = rendered.size != reference.size
    if size_mismatch:
        rendered = rendered.resize(reference.size)

    rendered_arr = np.asarray(rendered)
    reference_arr = np.asarray(reference)

    score, diff = ssim(rendered_arr, reference_arr, channel_axis=-1, full=True)

    heatmap_path = None
    if args.heatmap:
        heatmap_arr = (255 - (diff.mean(axis=-1) * 255)).astype(np.uint8)
        Image.fromarray(heatmap_arr).save(args.heatmap)
        heatmap_path = str(Path(args.heatmap).resolve())

    print(json.dumps({
        "ok": True,
        "similarity": round(float(score), 4),
        "size_mismatch": size_mismatch,
        "heatmap": heatmap_path,
    }))


if __name__ == "__main__":
    main()
