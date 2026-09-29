# Fase 8 · Renderizar y revisar

**Qué se consigue:** el MP4 del vídeo, revisado ronda a ronda hasta que la persona lo da por bueno.
**Qué necesita la persona:** ver el vídeo y dar feedback, idealmente como lista numerada con el segundo ("0:12 el ratón va demasiado rápido").
**Coste:** nada. Cada render tarda unos minutos.

## Render

1. Repasar el checklist de `docs/reglas-de-video.md` escena por escena.
2. `python3 tools/render_video.py --composition <id> --output .tmp/renders/<flujo>/<id>.mp4`
3. `python3 tools/probe_video.py .tmp/renders/<flujo>/<id>.mp4`: duración, resolución y fps esperados.
4. Decirle a la persona la ruta del archivo para que lo vea.

## Revisión de fidelidad (antes de enseñarlo)

- Un still en el frame correspondiente a cada captura clave, comparado con ella (`tools/diff_frame.py` como ayuda, juicio visual como criterio).
- En el frame de cada clic, el cursor sobre su objetivo.
- En cada corte de escena, el último frame de la escena anterior y el primero de la siguiente: cursor en el mismo sitio y sin fundido. Un still en el frame del clic no ve la continuidad: hay que mirar los dos lados del corte.
- Las escenas construidas "solo desde captura" reciben una revisión extra con la persona.

## Ronda de feedback

1. **Leer `docs/reglas-de-video.md` entero.** La mitad de los puntos de una ronda suelen ser una regla que ya está ahí.
2. **Ver lo que la persona vio:** `python3 tools/extract_frames.py --video <mp4> --times "0:12,0:26" --out-dir .tmp/stills/<flujo>/feedback` en cada segundo citado.
3. **Reescribir cada punto como secuencia en pantalla**: qué pasa, en qué orden, dónde empieza y acaba el cursor. Si el punto cruza un corte, dónde está el cursor en el último frame de la escena N y en el primero de la N+1. Esta lista va en la respuesta, para que la persona vea cómo se ha entendido cada punto.
4. **Implementar.** Editar el guion sin reformatearlo entero.
5. **Pasada de hermanos:** aplicar el mismo arreglo a todas las instancias del elemento corregido en el vídeo y repasar el checklist en las escenas tocadas.
6. **Verificar con stills antes de renderizar:** en cada escena cuyo diseño cambió, volver a medir **todos** sus objetivos de clic, no solo el del punto de feedback; y comprobar los dos lados de cada corte tocado.
7. **Renderizar al mismo archivo** que la versión anterior. Después, sacar imágenes en los segundos citados y comprobar que cada punto está resuelto (el tiempo puede haberse desplazado: buscar el momento equivalente, no el mismo segundo).
8. **Responder** con cada punto: su secuencia, qué se ha cambiado y en qué segundo del nuevo render se ve.
9. **Aprender:** si una corrección valdría para otros vídeos, añadirla numerada al final de `docs/reglas-de-video.md` y a su checklist, con vídeo y fecha. Así el siguiente vídeo ya sale bien a la primera.

## Variantes

- **Velocidad** (post-proceso, no toca el guion): `python3 tools/speed_variant.py --video <mp4> --factor 1.2`.
- **Sin subtítulos:** no es una variante; se hace en el guion (`captionStyle.burnIn: false`) y se vuelve a renderizar.
- **Vertical (9:16) o cuadrado (1:1):** pedir a Claude una composición con `CameraFrame` (`renderer/src/components/CameraFrame.tsx`), que recorta la interfaz ya construida enfocando la zona importante de cada escena, sin rehacerla. Comprobar que nada importante queda fuera del encuadre.

## Terminada cuando

La persona dice que el vídeo está bien. Pasar a la fase 9.
