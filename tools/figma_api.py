"""Cliente mínimo de la API REST de Figma (solo lectura), sin dependencias externas.

Lee FIGMA_TOKEN de .env. Respeta los límites de uso: si Figma responde 429,
espera lo que indique la cabecera Retry-After (tope 120 s) y reintenta.
"""
from __future__ import annotations

import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request

from _common import fail, load_env

API = "https://api.figma.com/v1"


def token() -> str:
    t = load_env().get("FIGMA_TOKEN")
    if not t:
        fail("falta FIGMA_TOKEN en .env. Sigue la fase 1 (fases/1-conectar-figma.md) para crear un token personal.")
    return t


def parse_file_key(url_or_key: str) -> str:
    """Acepta la URL de un archivo de Figma o directamente su key."""
    m = re.search(r"figma\.com/(?:file|design|proto|board)/([A-Za-z0-9]+)", url_or_key)
    return m.group(1) if m else url_or_key.strip()


def get(path: str, params: dict | None = None, max_retries: int = 4) -> dict:
    url = f"{API}{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"X-Figma-Token": token()})
    for attempt in range(max_retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", "ignore")[:500]
            if e.code == 429 and attempt < max_retries:
                wait = min(int(e.headers.get("Retry-After", "30") or 30), 120)
                time.sleep(wait)
                continue
            if e.code == 403:
                fail("Figma ha rechazado el token (403). Comprueba que está bien copiado en .env, que no ha "
                     "caducado y que tu cuenta tiene acceso a este archivo.", detail=body)
            if e.code == 404:
                fail("Figma no encuentra el archivo (404). Revisa la URL o que tengas acceso a él.", detail=body)
            if e.code == 429:
                fail("Figma sigue limitando las llamadas (429) tras varios reintentos. Para aquí y retoma más tarde: "
                     "el progreso está guardado.", rate_limited=True, detail=body)
            return {"_http_error": e.code, "_body": body}
        except urllib.error.URLError as e:
            if attempt < max_retries:
                time.sleep(5)
                continue
            fail(f"no se puede conectar con Figma: {e.reason}")
    return {}


def download(url: str, max_retries: int = 1) -> bytes | None:
    for attempt in range(max_retries + 1):
        try:
            with urllib.request.urlopen(url, timeout=120) as resp:
                return resp.read()
        except Exception:
            if attempt < max_retries:
                time.sleep(2)
    return None


PNG_HEADER = b"\x89PNG\r\n\x1a\n"


def is_valid_png(data: bytes | None) -> bool:
    # Se comprueba la cabecera, no el tamaño: un icono legítimo puede pesar < 1 KB.
    return bool(data) and len(data) > 100 and data[:8] == PNG_HEADER
