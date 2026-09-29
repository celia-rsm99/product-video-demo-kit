"""Utilidades compartidas por las herramientas del kit.

Todas las herramientas imprimen UN objeto JSON por stdout ({"ok": true, ...} o
{"ok": false, "error": "..."}) para que Claude pueda leer el resultado sin
ambigüedad, y salen con código 1 si algo falla.
"""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
RENDERER_DIR = REPO_ROOT / "renderer"
REFERENCIA_DIR = REPO_ROOT / "referencia"
INVENTARIO = REFERENCIA_DIR / "_inventario.json"
IS_WINDOWS = os.name == "nt"


def emit(payload: dict) -> None:
    print(json.dumps(payload, ensure_ascii=False))
    if not payload.get("ok", False):
        sys.exit(1)


def fail(message: str, **extra) -> None:
    emit({"ok": False, "error": message, **extra})


def load_env() -> dict:
    """Lee .env de la raíz del proyecto (formato CLAVE=valor). No falla si no existe."""
    env = {}
    path = REPO_ROOT / ".env"
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def npx() -> str:
    return "npx.cmd" if IS_WINDOWS else "npx"


def require_renderer() -> None:
    if not RENDERER_DIR.exists():
        fail(f"no encuentro la carpeta renderer/ en {RENDERER_DIR}")
    if not (RENDERER_DIR / "node_modules").exists():
        fail("faltan las dependencias de Remotion: ejecuta la fase 0 (instalación) o `npm install` dentro de renderer/")


def run_renderer(args: list, timeout: int = 1800) -> subprocess.CompletedProcess:
    """Ejecuta `npx <args>` dentro de renderer/."""
    return subprocess.run([npx()] + args, cwd=RENDERER_DIR, capture_output=True, text=True, timeout=timeout)


def tail(text: str, n: int = 4000) -> str:
    return (text or "").strip()[-n:]


def repo_path(p: str) -> Path:
    """Ruta relativa a la raíz del proyecto (o absoluta) → Path absoluto."""
    path = Path(p)
    return path if path.is_absolute() else (REPO_ROOT / path).resolve()


def rel(p: Path) -> str:
    try:
        return str(Path(p).resolve().relative_to(REPO_ROOT)).replace("\\", "/")
    except ValueError:
        return str(p)


def which(cmd: str) -> bool:
    return shutil.which(cmd) is not None
