#!/usr/bin/env python3
"""Renderiza un solo frame a PNG, para revisar una escena sin renderizar todo el vídeo.

Uso:
  python3 tools/render_still.py --composition <id-guion>--<id-escena> --frame 60 \
      --output .tmp/stills/<flujo>/<nombre>.png

Con la composición de escena suelta ("<id-guion>--<id-escena>") el frame es
local a esa escena: el mismo número que aparece en el guion JSON.
"""
import argparse

from _common import emit, fail, repo_path, rel, require_renderer, run_renderer, tail


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--composition", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--frame", type=int, default=0)
    args = parser.parse_args()
    require_renderer()

    out = repo_path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    res = run_renderer(["remotion", "still", "src/index.ts", args.composition, str(out), "--frame", str(args.frame)], timeout=600)
    if res.returncode != 0:
        fail(tail(res.stderr) or tail(res.stdout))
    emit({"ok": True, "composition": args.composition, "frame": args.frame, "output": rel(out)})


if __name__ == "__main__":
    main()
