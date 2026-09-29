#!/usr/bin/env python3
"""Lista los vídeos y escenas registrados en Remotion (id, tamaño, duración).

Uso:
  python3 tools/list_compositions.py
"""
import re

from _common import emit, fail, require_renderer, run_renderer, tail


def main():
    require_renderer()
    res = run_renderer(["remotion", "compositions", "src/index.ts"], timeout=600)
    if res.returncode != 0:
        fail(tail(res.stderr) or tail(res.stdout))
    comps = []
    for line in res.stdout.splitlines():
        m = re.match(r"^\s*(\S+)\s+(\d+)\s+(\d+)x(\d+)\s+(\d+)\s+\(([\d.]+) sec\)", line)
        if m:
            comps.append({"id": m.group(1), "fps": int(m.group(2)), "width": int(m.group(3)),
                          "height": int(m.group(4)), "frames": int(m.group(5)), "seconds": float(m.group(6))})
    emit({"ok": True, "compositions": comps, "raw": None if comps else tail(res.stdout)})


if __name__ == "__main__":
    main()
