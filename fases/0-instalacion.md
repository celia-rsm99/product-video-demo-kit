# Fase 0 · Instalación

**Qué se consigue:** el ordenador tiene todo lo necesario y el vídeo de prueba del kit se renderiza.
**Qué necesita la persona:** unos 15 minutos y conexión a internet.
**Coste:** nada.

## Pasos

1. Ejecutar `python3 tools/check_setup.py` (en Windows, `python tools/check_setup.py`) y leer el resultado.
2. Por cada comprobación obligatoria que falle, explicar a la persona qué es y cómo instalarlo, **de una en una**, esperando a que confirme:
   - **Node.js**: versión LTS desde https://nodejs.org (instalador normal, siguiente-siguiente). En Mac con Homebrew, `brew install node` también vale.
   - **Python**: https://www.python.org/downloads/ (en Windows, marcar "Add Python to PATH").
   Después de instalar algo, la persona tiene que cerrar y volver a abrir Claude Code para que se detecte.
3. Instalar las dependencias del kit:
   - Mac/Linux: `./instalar.command` (o doble clic en `instalar.command` desde el Finder).
   - Windows: `cd renderer && npm install`, y después `python -m venv .venv` y `.venv\Scripts\python -m pip install -r tools/requirements.txt`.
4. Volver a ejecutar `tools/check_setup.py` hasta que `ok` sea `true`. Las comprobaciones opcionales (Figma) se resuelven en la fase 1.
5. **Prueba de humo:** renderizar el vídeo de ejemplo:
   `python3 tools/render_video.py --composition demo-ejemplo --output .tmp/renders/ejemplo/demo-ejemplo.mp4`
   La primera vez Remotion descarga un navegador interno y tarda más. Comprobar con `tools/probe_video.py` que dura ≈12 s a 1440×800 y decirle a la persona dónde está el archivo para que lo abra.
6. Opcional pero recomendable: enseñarle Remotion Studio (`cd renderer && npm run studio`), que abre el navegador con el vídeo para moverse por él.

## Terminada cuando

`check_setup.py` devuelve `ok: true` y el vídeo de ejemplo se ha renderizado y la persona lo ha visto. Marcar la fase en `PROGRESO.md`.

## Si algo falla

Ver `docs/solucion-de-problemas.md`, sección Instalación.
