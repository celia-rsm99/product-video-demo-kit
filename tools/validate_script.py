#!/usr/bin/env python3
"""Valida un guion JSON antes de renderizar (esquema + reglas que el esquema no ve).

Uso:
  python3 tools/validate_script.py renderer/scripts/<flujo>/<nombre>.json

Devuelve {"ok", "id", "scenes", "warnings"} o {"ok": false, "errors"|"error"}.
Los avisos (warnings) no bloquean, pero cada uno hay que revisarlo:
suelen ser una regla de docs/reglas-de-video.md.
"""
import json
import sys

from _common import emit, fail, repo_path, require_renderer, run_renderer, tail


def main():
    if len(sys.argv) != 2:
        fail("uso: validate_script.py <ruta/al/guion.json>")
    path = repo_path(sys.argv[1])
    if not path.exists():
        fail(f"no existe el guion: {path}")
    require_renderer()
    res = run_renderer(["tsx", "src/lib/validate-cli.ts", str(path)], timeout=300)
    lines = (res.stdout or "").strip().splitlines()
    try:
        payload = json.loads(lines[-1])
    except (IndexError, json.JSONDecodeError):
        fail(tail(res.stderr) or tail(res.stdout) or "el validador no devolvió nada")
    emit(payload)


if __name__ == "__main__":
    main()
