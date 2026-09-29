#!/usr/bin/env python3
"""Descarga por lotes las pantallas pendientes del inventario como PNG a 2x (fase 3, ruta con token).

Reanudable: solo procesa pantallas "pending" y guarda el inventario tras cada
lote. Si se corta, volver a ejecutarlo sigue donde lo dejó.

Uso:
  python3 tools/figma_download.py [--limit 200] [--batch 20] [--scale 2] [--retry-errors]

Coste: 1 llamada a la API de Figma por lote (20 pantallas por defecto) + las
descargas de las imágenes (no cuentan contra el límite de Figma).
"""
import argparse
import time

from _common import REPO_ROOT, emit
from figma_api import download, get, is_valid_png
from inventory import all_screens, load, save, target_path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=200, help="Máximo de pantallas en esta tanda")
    parser.add_argument("--batch", type=int, default=20, help="Pantallas por llamada a Figma")
    parser.add_argument("--scale", type=float, default=2)
    parser.add_argument("--retry-errors", action="store_true", help="Reintentar también las marcadas como error")
    args = parser.parse_args()

    data = load()
    key = data["file_key"]
    wanted = {"pending"} | ({"error"} if args.retry_errors else set())
    queue = [(sec, sc) for sec, sc in all_screens(data) if sc["status"] in wanted][: args.limit]

    done = errors = calls = 0
    error_ids = []
    batch = args.batch
    i = 0
    while i < len(queue):
        chunk = queue[i : i + batch]
        ids = ",".join(sc["id"] for _, sc in chunk)
        res = get(f"/images/{key}", {"ids": ids, "format": "png", "scale": args.scale})
        calls += 1
        if "_http_error" in res or res.get("err"):
            # Un lote demasiado grande puede agotar el tiempo de render de Figma: se parte en dos.
            if batch > 1:
                batch = max(1, batch // 2)
                continue
            for _, sc in chunk:
                sc["status"] = "error"
                error_ids.append(sc["id"])
                errors += 1
            save(data)
            i += len(chunk)
            continue

        urls = res.get("images", {})
        for sec, sc in chunk:
            url = urls.get(sc["id"])
            png = download(url) if url else None
            if is_valid_png(png):
                out = REPO_ROOT / target_path(sec, sc)
                out.parent.mkdir(parents=True, exist_ok=True)
                out.write_bytes(png)
                sc["status"] = "done"
                sc["local_path"] = target_path(sec, sc)
                done += 1
            else:
                sc["status"] = "error"
                error_ids.append(sc["id"])
                errors += 1
        save(data)
        i += len(chunk)
        time.sleep(1)

    remaining = sum(1 for _, sc in all_screens(data) if sc["status"] == "pending")
    emit({"ok": True, "downloaded": done, "errors": errors, "error_ids": error_ids[:50],
          "pending_left": remaining, "figma_calls": calls})


if __name__ == "__main__":
    main()
