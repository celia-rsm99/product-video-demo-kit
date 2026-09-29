#!/usr/bin/env python3
"""Renderiza un vídeo completo a MP4.

Uso:
  python3 tools/render_video.py --composition <id-del-guion> --output .tmp/renders/<flujo>/<nombre>.mp4

El id de composición es el `id` del guion JSON (ver tools/list_compositions.py).
Tarda aproximadamente lo que dura el vídeo multiplicado por 2-5, según el ordenador.
"""
import argparse

from _common import emit, fail, repo_path, rel, require_renderer, run_renderer, tail


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--composition", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    require_renderer()

    out = repo_path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    res = run_renderer(["remotion", "render", "src/index.ts", args.composition, str(out)])
    if res.returncode != 0:
        fail(tail(res.stderr) or tail(res.stdout))
    emit({"ok": True, "composition": args.composition, "output": rel(out)})


if __name__ == "__main__":
    main()
