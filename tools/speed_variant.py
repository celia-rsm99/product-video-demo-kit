#!/usr/bin/env python3
"""Crea una versión acelerada de un vídeo (p. ej. 1.2x), sin audio.

Uso:
  python3 tools/speed_variant.py --video .tmp/renders/x/y.mp4 --factor 1.2

Guarda al lado: y__1.2x.mp4. Es un post-proceso: el guion no se toca.
"""
import argparse

from _common import emit, fail, repo_path, rel, require_renderer, run_renderer, tail


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", required=True)
    parser.add_argument("--factor", type=float, required=True)
    args = parser.parse_args()
    require_renderer()
    video = repo_path(args.video)
    if not video.exists():
        fail(f"no existe el vídeo: {video}")
    if not 0.25 <= args.factor <= 4:
        fail("--factor tiene que estar entre 0.25 y 4")
    out = video.with_name(f"{video.stem}__{args.factor:g}x{video.suffix}")
    # El ffmpeg que trae Remotion no incluye los filtros setpts/fps: se reescala el
    # tiempo de entrada (-itsscale) y se fija la cadencia de salida (-r) en su lugar.
    res = run_renderer(["remotion", "ffmpeg", "-y", "-itsscale", f"{1 / args.factor:.6f}", "-i", str(video),
                        "-r", "30", "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", str(out)], timeout=1800)
    if res.returncode != 0:
        fail(tail(res.stderr))
    emit({"ok": True, "output": rel(out)})


if __name__ == "__main__":
    main()
