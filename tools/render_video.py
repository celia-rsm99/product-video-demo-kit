#!/usr/bin/env python3
"""Renderiza un vídeo completo a MP4.

Uso:
  python3 tools/render_video.py --composition <id-del-guion> --output .tmp/renders/<flujo>/<nombre>.mp4

El id de composición es el `id` del guion JSON (ver tools/list_compositions.py).
Tarda aproximadamente lo que dura el vídeo multiplicado por 2-5, según el ordenador.

Los vídeos demo salen mudos. Para un vídeo con voz o música, añadir --con-audio.
Para revisar un tramo sin renderizar todo, --frames 0-299.
"""
import argparse

from _common import emit, fail, repo_path, rel, require_renderer, run_renderer, tail


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--composition", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--con-audio", action="store_true", help="incluir la pista de audio (vídeos con voz o música)")
    parser.add_argument("--frames", help="solo un tramo, p. ej. 0-299")
    args = parser.parse_args()
    require_renderer()

    out = repo_path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["remotion", "render", "src/index.ts", args.composition, str(out)]
    if args.frames:
        cmd.append(f"--frames={args.frames}")
    if args.con_audio:
        cmd.append("--muted=false")
    res = run_renderer(cmd)
    if res.returncode != 0:
        fail(tail(res.stderr) or tail(res.stdout))
    emit({"ok": True, "composition": args.composition, "output": rel(out), "audio": args.con_audio})


if __name__ == "__main__":
    main()
