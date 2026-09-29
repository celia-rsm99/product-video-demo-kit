#!/usr/bin/env python3
"""Inventario de pantallas de Figma: la única fuente de verdad del progreso de descarga.

El inventario vive en referencia/_inventario.json. Cada pantalla tiene
status "pending" | "done" | "error", y se guarda en disco tras cada cambio,
así que la descarga se puede cortar y retomar otro día sin perder nada.

Uso:
  # Crear/actualizar desde un JSON de secciones (lo prepara Claude a partir de
  # get_metadata del MCP, o lo genera figma_inventory.py):
  python3 tools/inventory.py init --file-key KEY --file-name "Mi app" --from secciones.json [--force]

  python3 tools/inventory.py status                 # cuántas quedan, por sección
  python3 tools/inventory.py next --limit 20        # siguientes pendientes
  python3 tools/inventory.py mark --id 12:34 --status done --local-path referencia/x/capturas/12-34_x.png

Formato de entrada de `init --from` (el mismo que produce figma_inventory.py):
  {"sections": [{"id": "1:2", "name": "Onboarding", "page": "App",
                 "screens": [{"id": "3:4", "name": "Bienvenida", "w": 1440, "h": 900}]}]}
"""
import argparse
import json
import re
import unicodedata
from collections import Counter
from datetime import date

from _common import INVENTARIO, emit, fail, rel, REFERENCIA_DIR


def slugify(text: str, max_len: int = 60) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    return (text[:max_len].rstrip("-")) or "sin-nombre"


def screen_filename(screen: dict) -> str:
    return f"{screen['id'].replace(':', '-').replace(';', '_')}_{slugify(screen['name'], 50)}.png"


def load() -> dict:
    if not INVENTARIO.exists():
        fail("todavía no hay inventario (referencia/_inventario.json). Ejecuta la fase 2.")
    return json.loads(INVENTARIO.read_text(encoding="utf-8"))


def save(data: dict) -> None:
    INVENTARIO.parent.mkdir(parents=True, exist_ok=True)
    tmp = INVENTARIO.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(INVENTARIO)


def all_screens(data: dict):
    for section in data["sections"]:
        for screen in section["screens"]:
            yield section, screen


def find(data: dict, node_id: str):
    for section, screen in all_screens(data):
        if screen["id"] == node_id:
            return section, screen
    return None, None


def target_path(section: dict, screen: dict) -> str:
    return f"{section['target_dir']}/{screen_filename(screen)}"


def cmd_init(args):
    src = json.loads(open(args.from_file, encoding="utf-8").read())
    previous = {}
    if INVENTARIO.exists():
        if not args.force:
            old = load()
            if old.get("file_key") != args.file_key:
                fail("ya existe un inventario de OTRO archivo de Figma. Usa --force para sustituirlo "
                     "(se perderá el progreso) o mueve el actual.")
        old = load()
        previous = {s["id"]: s for _, s in all_screens(old)}

    used_slugs = Counter()
    sections = []
    for sec in src["sections"]:
        slug = slugify(sec["name"])
        used_slugs[slug] += 1
        if used_slugs[slug] > 1:
            slug = f"{slug}-{used_slugs[slug]}"
        target_dir = rel(REFERENCIA_DIR / slug / "capturas")
        screens = []
        for sc in sec["screens"]:
            prev = previous.get(sc["id"], {})
            screens.append({
                "id": sc["id"],
                "name": sc["name"],
                "w": sc.get("w"),
                "h": sc.get("h"),
                "status": prev.get("status", "pending"),
                "local_path": prev.get("local_path"),
            })
        sections.append({"id": sec.get("id"), "name": sec["name"], "page": sec.get("page"),
                         "slug": slug, "target_dir": target_dir, "screens": screens})

    data = {"file_key": args.file_key, "file_name": args.file_name,
            "generated": date.today().isoformat(), "sections": sections}
    save(data)
    counts = Counter(s["status"] for _, s in all_screens(data))
    emit({"ok": True, "inventory": rel(INVENTARIO), "sections": len(sections),
          "screens": sum(counts.values()), "by_status": dict(counts)})


def cmd_status(_args):
    data = load()
    counts = Counter(s["status"] for _, s in all_screens(data))
    per_section = []
    for section in data["sections"]:
        c = Counter(s["status"] for s in section["screens"])
        per_section.append({"section": section["name"], "slug": section["slug"], **{k: c.get(k, 0) for k in ("done", "pending", "error")}})
    emit({"ok": True, "file_name": data.get("file_name"), "total": sum(counts.values()),
          "done": counts.get("done", 0), "pending": counts.get("pending", 0), "error": counts.get("error", 0),
          "sections": per_section})


def cmd_next(args):
    data = load()
    wanted = {"pending"} | ({"error"} if args.include_errors else set())
    out = []
    for section, screen in all_screens(data):
        if screen["status"] in wanted:
            out.append({"id": screen["id"], "name": screen["name"], "section": section["name"],
                        "target": target_path(section, screen)})
            if len(out) >= args.limit:
                break
    emit({"ok": True, "file_key": data["file_key"], "count": len(out), "screens": out})


def cmd_mark(args):
    data = load()
    section, screen = find(data, args.id)
    if screen is None:
        fail(f"no encuentro la pantalla {args.id} en el inventario")
    screen["status"] = args.status
    if args.local_path is not None:
        screen["local_path"] = args.local_path
    save(data)
    emit({"ok": True, "id": args.id, "status": args.status})


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("init")
    p.add_argument("--file-key", required=True)
    p.add_argument("--file-name", required=True)
    p.add_argument("--from", dest="from_file", required=True)
    p.add_argument("--force", action="store_true")
    p.set_defaults(func=cmd_init)
    p = sub.add_parser("status")
    p.set_defaults(func=cmd_status)
    p = sub.add_parser("next")
    p.add_argument("--limit", type=int, default=20)
    p.add_argument("--include-errors", action="store_true")
    p.set_defaults(func=cmd_next)
    p = sub.add_parser("mark")
    p.add_argument("--id", required=True)
    p.add_argument("--status", required=True, choices=["pending", "done", "error"])
    p.add_argument("--local-path")
    p.set_defaults(func=cmd_mark)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
