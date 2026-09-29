#!/usr/bin/env python3
"""Lista todas las pantallas de un archivo de Figma y crea el inventario (fase 2, ruta con token).

Recorre páginas → secciones → frames. Cada frame de primer nivel dentro de
una sección (o suelto en la página) cuenta como pantalla. Los componentes y
los frames pequeños (iconos, piezas sueltas) se ignoran.

Uso:
  python3 tools/figma_inventory.py --file "https://www.figma.com/design/XXXX/Mi-app" \
      [--pages "App,Onboarding"] [--min-width 320] [--dry-run]

--dry-run: enseña lo que encontraría sin escribir el inventario (para revisarlo con la persona antes).
Coste: 1 llamada a la API de Figma.
"""
import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

from _common import emit, fail
from figma_api import get, parse_file_key


def box(node):
    b = node.get("absoluteBoundingBox") or {}
    return round(b.get("width") or 0), round(b.get("height") or 0)


def walk_section(node, min_w, out):
    for child in node.get("children", []):
        t = child.get("type")
        if t == "SECTION":
            walk_section(child, min_w, out)
        elif t == "FRAME" and child.get("visible", True):
            w, h = box(child)
            if w >= min_w:
                out.append({"id": child["id"], "name": child["name"], "w": w, "h": h})


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True, help="URL del archivo de Figma o su key")
    parser.add_argument("--pages", help="Nombres de páginas a incluir, separados por comas (por defecto, todas)")
    parser.add_argument("--min-width", type=int, default=320)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    key = parse_file_key(args.file)
    data = get(f"/files/{key}", {"depth": 5})
    if "_http_error" in data:
        fail(f"error {data['_http_error']} leyendo el archivo", detail=data["_body"])

    wanted = {p.strip().lower() for p in args.pages.split(",")} if args.pages else None
    sections = []
    for page in data.get("document", {}).get("children", []):
        if wanted and page["name"].strip().lower() not in wanted:
            continue
        loose = []
        for node in page.get("children", []):
            t = node.get("type")
            if t == "SECTION":
                screens = []
                walk_section(node, args.min_width, screens)
                if screens:
                    sections.append({"id": node["id"], "name": node["name"], "page": page["name"], "screens": screens})
            elif t == "FRAME" and node.get("visible", True):
                w, h = box(node)
                if w >= args.min_width:
                    loose.append({"id": node["id"], "name": node["name"], "w": w, "h": h})
        if loose:
            sections.append({"id": page["id"], "name": f"{page['name']} (sueltas)", "page": page["name"], "screens": loose})

    total = sum(len(s["screens"]) for s in sections)
    summary = [{"page": s["page"], "section": s["name"], "screens": len(s["screens"])} for s in sections]
    all_pages = [p["name"] for p in data.get("document", {}).get("children", [])]
    if args.dry_run or total == 0:
        emit({"ok": total > 0, "dry_run": True, "file_name": data.get("name"), "file_key": key,
              "pages_in_file": all_pages, "total_screens": total, "sections": summary,
              "error": None if total else "no he encontrado pantallas; revisa --pages o --min-width"})
        return

    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as f:
        json.dump({"sections": sections}, f, ensure_ascii=False)
        tmp = f.name
    res = subprocess.run([sys.executable, str(Path(__file__).parent / "inventory.py"), "init",
                          "--file-key", key, "--file-name", data.get("name", key), "--from", tmp],
                         capture_output=True, text=True)
    Path(tmp).unlink(missing_ok=True)
    try:
        inner = json.loads(res.stdout.strip().splitlines()[-1])
    except Exception:
        fail("no se pudo escribir el inventario", detail=res.stderr[-2000:])
    emit({**inner, "pages_in_file": all_pages, "sections_found": summary})


if __name__ == "__main__":
    main()
