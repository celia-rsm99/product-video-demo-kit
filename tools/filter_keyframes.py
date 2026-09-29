#!/usr/bin/env python3
"""Reduce a raw video-frame dump to the keyframes where the UI actually changed.

Usage:
  tools/filter_keyframes.py <frames_dir> <output_dir> [--fps 10] [--threshold 0.985] [--resize-width 480]

Compares every frame against the last *kept* frame (not just the previous frame),
so a slow drift across many near-identical frames still gets caught instead of
each tiny step passing individually. Images are downscaled before comparing
(--resize-width) purely for speed — the copied output keeps full resolution.
Always keeps the first and last frame so the start/end state of the recording
isn't lost even if nothing changed.

Writes the curated subset to <output_dir> (renamed with an order index +
timestamp) plus a manifest.json describing what was kept and why.

Prints a single JSON summary object to stdout:
  {"ok": bool, "input_frames": int, "kept_frames": int, "reduction_pct": float,
   "output_dir": str, "manifest": str, "error": str|None}
"""
import argparse
import json
import shutil
import sys
from pathlib import Path

try:
    import numpy as np
    from PIL import Image
    from skimage.metrics import structural_similarity as ssim
except ImportError as exc:  # pragma: no cover
    print(json.dumps({"ok": False, "error": f"missing dependency: {exc}. Run: pip install -r tools/requirements.txt"}))
    sys.exit(1)

FRAME_EXTENSIONS = {".jpg", ".jpeg", ".png"}


def fail(message: str) -> None:
    print(json.dumps({"ok": False, "error": message}))
    sys.exit(1)


def load_for_compare(path: Path, resize_width: int) -> np.ndarray:
    img = Image.open(path).convert("RGB")
    if img.width > resize_width:
        ratio = resize_width / img.width
        img = img.resize((resize_width, max(1, round(img.height * ratio))))
    return np.asarray(img)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("frames_dir")
    parser.add_argument("output_dir")
    parser.add_argument("--fps", type=float, default=10.0, help="Frame rate the frames were exported at (used for manifest timestamps only)")
    parser.add_argument("--threshold", type=float, default=0.985, help="SSIM similarity to the last kept frame below which a new frame is kept")
    parser.add_argument("--resize-width", type=int, default=480, help="Width frames are downscaled to before comparing (speed only, output stays full-res)")
    args = parser.parse_args()

    frames_dir = Path(args.frames_dir)
    output_dir = Path(args.output_dir)
    if not frames_dir.is_dir():
        fail(f"frames dir not found: {frames_dir}")

    frames = sorted(p for p in frames_dir.iterdir() if p.suffix.lower() in FRAME_EXTENSIONS)
    if not frames:
        fail(f"no frames found in {frames_dir}")

    output_dir.mkdir(parents=True, exist_ok=True)

    kept = []
    last_kept_arr = None
    for i, frame_path in enumerate(frames):
        arr = load_for_compare(frame_path, args.resize_width)
        is_last = i == len(frames) - 1

        similarity = None
        if last_kept_arr is not None:
            similarity = float(ssim(arr, last_kept_arr, channel_axis=-1))

        if last_kept_arr is None or similarity < args.threshold or is_last:
            kept.append({
                "source": frame_path.name,
                "frame_index": i,
                "timestamp_s": round(i / args.fps, 3),
                "similarity_to_previous_kept": round(similarity, 4) if similarity is not None else None,
            })
            last_kept_arr = arr

    manifest = []
    for order, entry in enumerate(kept):
        dest_name = f"{order:04d}_t{entry['timestamp_s']:.2f}s{Path(entry['source']).suffix.lower()}"
        shutil.copy2(frames_dir / entry["source"], output_dir / dest_name)
        manifest.append({**entry, "kept_as": dest_name})

    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2))

    print(json.dumps({
        "ok": True,
        "input_frames": len(frames),
        "kept_frames": len(kept),
        "reduction_pct": round(100 * (1 - len(kept) / len(frames)), 1),
        "output_dir": str(output_dir.resolve()),
        "manifest": str(manifest_path.resolve()),
    }))


if __name__ == "__main__":
    main()
