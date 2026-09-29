# Fase 9 · Entrega

**Qué se consigue:** el vídeo aprobado guardado como entregable, con sus fuentes, listo para usar.
**Qué necesita la persona:** decir que lo aprueba y qué versión (p. ej. la de 1.2x).
**Coste:** nada.

## Pasos

1. Copiar la versión aprobada a entregables:
   `python3 tools/approve_video.py --video .tmp/renders/<flujo>/<nombre>.mp4 --flow <flujo>`
   Si ya existe un archivo con ese nombre, es un vídeo aprobado antes (quizá ya publicado): **no sustituirlo sin preguntar**. Si la persona lo confirma, `--replace`.
2. Si va a una web, ofrecer una versión optimizada (H.264, sin audio, arranque rápido):
   `cd renderer && npx remotion ffmpeg -i <entrada.mp4> -an -c:v libx264 -preset slow -crf 24 -pix_fmt yuv420p -movflags +faststart -tune animation <salida-web.mp4>`
   Suele quedar en 1-2 MB por minuto a 1440×800. Como imagen de portada, el primer frame (`tools/render_still.py --frame 0`).
3. Actualizar `entregables/README.md`: qué vídeo es, qué flujo enseña, qué versión y dónde se usa.
4. **Guardar el trabajo (opcional).** Si la persona usa git, proponer un commit con el MP4 aprobado, el guion y las escenas que lo producen. **Nunca subir nada a internet (push, publicar) sin que la persona lo pida expresamente.** Recordarle que su copia del kit contiene su producto: si la sube a GitHub, en un repositorio **privado**.
5. Marcar el vídeo en `PROGRESO.md`, sección "Vídeos".

## Siguiente vídeo

Volver a la fase 6 (si el flujo aún no tiene escenas) o a la fase 7 (si ya las tiene). Cada vídeo nuevo es más rápido: las escenas se reutilizan y las reglas de vídeo ya incluyen las correcciones de los anteriores.
