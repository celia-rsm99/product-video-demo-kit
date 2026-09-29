#!/usr/bin/env python3
"""Comprueba un MP4 renderizado: duración, resolución, fps y códec.

Uso:
  python3 tools/probe_video.py .tmp/renders/<flujo>/<nombre>.mp4

Usa el ffprobe que trae Remotion, así que no hace falta instalar ffmpeg.
"""
import json
import sys

from _common import emit, fail, repo_path, rel, require_renderer, run_renderer, tail


def main():
    if len(sys.argv) != 2:
        fail("uso: probe_video.py <video.mp4>")
    video = repo_path(sys.argv[1])
    if not video.exists():
        fail(f"no existe el vídeo: {video}")
    require_renderer()
    res = run_renderer(["remotion", "ffprobe", "-v", "error", "-print_format", "json", "-show_streams", "-show_format", str(video)], timeout=120)
    if res.returncode != 0:
        fail(tail(res.stderr) or tail(res.stdout))
    try:
        info = json.loads(res.stdout[res.stdout.index("{"):])
    except ValueError:
        fail("no se pudo leer la salida de ffprobe", raw=tail(res.stdout))
    v = next((s for s in info.get("streams", []) if s.get("codec_type") == "video"), {})
    num, _, den = (v.get("r_frame_rate") or "0/1").partition("/")
    emit({"ok": True, "video": rel(video),
          "seconds": round(float(info.get("format", {}).get("duration", 0)), 2),
          "width": v.get("width"), "height": v.get("height"),
          "fps": round(float(num) / float(den or 1), 2) if num else None,
          "codec": v.get("codec_name"),
          "has_audio": any(s.get("codec_type") == "audio" for s in info.get("streams", [])),
          "size_mb": round(video.stat().st_size / 1_000_000, 2)})


if __name__ == "__main__":
    main()
