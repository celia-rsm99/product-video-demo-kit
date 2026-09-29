#!/usr/bin/env python3
"""Comprueba que el ordenador tiene todo lo necesario (fase 0).

Uso:
  python3 tools/check_setup.py

Devuelve {"ok": bool, "checks": [{"name", "ok", "detail", "fix"}], "pending": [...]}.
`ok` es true solo si todo lo obligatorio está listo. Las comprobaciones
opcionales no bloquean.
"""
import subprocess
import sys

from _common import REPO_ROOT, RENDERER_DIR, emit, load_env, which, npx

checks = []


def add(name, ok, detail="", fix="", required=True):
    checks.append({"name": name, "ok": ok, "detail": detail, "fix": fix, "required": required})


def version_of(cmd):
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return (out.stdout or out.stderr).strip()
    except Exception:
        return None


# Python
py = sys.version_info
add("Python 3.9 o superior", py >= (3, 9), f"{py.major}.{py.minor}.{py.micro}",
    "Instala Python desde https://www.python.org/downloads/")

# Node
node_v = version_of(["node", "--version"]) if which("node") else None
node_ok = False
if node_v and node_v.startswith("v"):
    try:
        node_ok = int(node_v[1:].split(".")[0]) >= 18
    except ValueError:
        pass
add("Node.js 18 o superior", node_ok, node_v or "no instalado",
    "Instala la versión LTS desde https://nodejs.org")

add("npm", which("npm") or which("npm.cmd"), "", "Viene con Node.js: reinstala Node desde https://nodejs.org")

# Dependencias de Remotion
add("Remotion instalado (renderer/node_modules)", (RENDERER_DIR / "node_modules" / "remotion").exists(), "",
    "Ejecuta el instalador (instalar.command en Mac, o `npm install` dentro de renderer/)")

# Dependencias de Python (solo para comparar imágenes; opcionales)
missing = []
for mod in ("PIL", "numpy", "skimage"):
    try:
        __import__(mod)
    except ImportError:
        missing.append(mod)
add("Librerías de Python para comparar imágenes", not missing,
    "faltan: " + ", ".join(missing) if missing else "",
    "Ejecuta el instalador; o `python3 -m pip install -r tools/requirements.txt` dentro de un entorno virtual",
    required=False)

# Figma
env = load_env()
add("Token de Figma en .env (FIGMA_TOKEN)", bool(env.get("FIGMA_TOKEN")),
    "", "Fase 1: crea un token personal en Figma y pégalo en .env", required=False)

claude_ok = which("claude")
figma_mcp = False
if claude_ok:
    out = version_of(["claude", "mcp", "list"]) or ""
    figma_mcp = "figma" in out.lower()
add("Servidor MCP de Figma conectado a Claude Code", figma_mcp,
    "" if claude_ok else "no encuentro el comando `claude` (normal si usas la app de escritorio)",
    "Fase 1: `claude mcp add --transport http figma https://mcp.figma.com/mcp` y luego /mcp para iniciar sesión",
    required=False)

pending = [c["name"] for c in checks if not c["ok"] and c["required"]]
emit({"ok": not pending, "checks": checks, "pending": pending,
      "error": None if not pending else "faltan requisitos: " + "; ".join(pending)})
