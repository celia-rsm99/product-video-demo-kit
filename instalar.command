#!/bin/bash
# Instalador del kit para Mac y Linux. En Mac se puede abrir con doble clic.
# Instala Remotion (vídeo) y las librerías de Python en carpetas del propio kit:
# no toca nada más del ordenador.

cd "$(dirname "$0")" || exit 1

ok()   { printf "  \033[32m✓\033[0m %s\n" "$1"; }
bad()  { printf "  \033[31m✗\033[0m %s\n" "$1"; }
step() { printf "\n\033[1m%s\033[0m\n" "$1"; }
finish() { echo; read -r -p "Pulsa Enter para cerrar esta ventana." _; exit "$1"; }

step "1/4 · Comprobando Node.js y Python"
if command -v node >/dev/null 2>&1; then ok "Node.js $(node --version)"; else
  bad "Falta Node.js. Instálalo (versión LTS) desde https://nodejs.org y vuelve a abrir este instalador."; finish 1; fi
if command -v python3 >/dev/null 2>&1; then ok "$(python3 --version)"; else
  bad "Falta Python. Instálalo desde https://www.python.org/downloads/ y vuelve a abrir este instalador."; finish 1; fi

step "2/4 · Instalando Remotion (puede tardar unos minutos)"
if (cd renderer && npm install --no-audit --no-fund); then ok "Remotion instalado"; else
  bad "No se pudo instalar Remotion. Copia el error de arriba y pégaselo a Claude."; finish 1; fi

step "3/4 · Instalando las librerías de Python"
if [ ! -d .venv ]; then python3 -m venv .venv || { bad "No se pudo crear el entorno de Python."; finish 1; }; fi
if .venv/bin/python -m pip install --quiet --upgrade pip && .venv/bin/python -m pip install --quiet -r tools/requirements.txt; then
  ok "Librerías de Python instaladas"; else
  bad "No se pudieron instalar las librerías de Python (son opcionales: solo sirven para comparar imágenes)."; fi

step "4/4 · Preparando la configuración"
if [ ! -f .env ]; then cp .env.example .env && ok "Creado el archivo .env (el token de Figma se pega ahí en la fase 1)"; else ok ".env ya existía"; fi

echo
.venv/bin/python tools/check_setup.py >/dev/null 2>&1 && ok "Todo listo. Vuelve a Claude Code y escribe /empezar." \
  || ok "Instalación terminada. Vuelve a Claude Code y escribe /empezar: Claude revisará lo que falte."
finish 0
