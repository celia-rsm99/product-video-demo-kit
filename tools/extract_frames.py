#!/usr/bin/env python3
"""Saca imágenes de un vídeo en los segundos indicados (para ver lo que la persona vio al dar feedback).

Uso:
  python3 tools/extract_frames.py --video .tmp/renders/x/y.mp4 --times "0:12,0:26.5,41" \
      --out-dir .tmp/stills/x/feedback

Acepta "mm:ss", "mm:ss.d" o segundos. Usa el ffmpeg que trae Remotion.
"""
import argparse

from _common import emit, fail, repo_path, rel, require_renderer, run_renderer, tail


def to_seconds(t: str) -> float:
    t = t.strip()
    if ":" in t:
        m, s = t.split(":", 1)
        return int(m) * 60 + float(s)
    return float(t)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", required=True)
    parser.add_argument("--times", required=True)
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()
    require_renderer()

    video = repo_path(args.video)
    if not video.exists():
        fail(f"no existe el vídeo: {video}")
    out_dir = repo_path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    saved = []
    for raw in args.times.split(","):
        sec = to_seconds(raw)
        out = out_dir / f"t{sec:06.2f}s.png"
        res = run_renderer(["remotion", "ffmpeg", "-y", "-ss", str(sec), "-i", str(video), "-frames:v", "1", str(out)], timeout=120)
        if res.returncode != 0 or not out.exists():
            fail(f"no se pudo extraer el segundo {raw}", detail=tail(res.stderr))
        saved.append({"time": raw.strip(), "seconds": sec, "image": rel(out)})
    emit({"ok": True, "frames": saved})


if __name__ == "__main__":
    main()
