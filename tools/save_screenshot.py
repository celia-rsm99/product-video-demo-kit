#!/usr/bin/env python3
"""Guarda UNA pantalla del inventario a partir de una URL de imagen (fase 3, ruta MCP).

Para cuando la captura viene del MCP de Figma (get_screenshot) en vez del
token: descarga la URL, comprueba que es un PNG válido, lo guarda en su
carpeta y marca la pantalla como hecha en el inventario. Si falla dos veces,
la marca como error para seguir con la siguiente sin bloquearse.

Uso:
  python3 tools/save_screenshot.py --id 12:34 --url "https://..."
  python3 tools/save_screenshot.py --id 12:34 --file ruta/a/imagen.png   # si ya está en disco
"""
import argparse
from pathlib import Path

from _common import REPO_ROOT, emit, fail
from figma_api import download, is_valid_png
from inventory import find, load, save, target_path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", required=True)
    src = parser.add_mutually_exclusive_group(required=True)
    src.add_argument("--url")
    src.add_argument("--file")
    args = parser.parse_args()

    data = load()
    section, screen = find(data, args.id)
    if screen is None:
        fail(f"no encuentro la pantalla {args.id} en el inventario")

    png = download(args.url) if args.url else Path(args.file).read_bytes()
    if not is_valid_png(png):
        screen["status"] = "error"
        save(data)
        fail("lo descargado no es un PNG válido; pantalla marcada como error", id=args.id)

    out = REPO_ROOT / target_path(section, screen)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(png)
    screen["status"] = "done"
    screen["local_path"] = target_path(section, screen)
    save(data)
    emit({"ok": True, "id": args.id, "saved": screen["local_path"]})


if __name__ == "__main__":
    main()
