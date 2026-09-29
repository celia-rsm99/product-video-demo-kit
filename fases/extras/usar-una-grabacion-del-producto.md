# Extra · Usar una grabación del producto

**Cuándo:** para entender el orden real de un flujo y sus estados intermedios (cargas, menús abiertos, transiciones) que no están en Figma. Muy útil en la fase 4 y cuando se construye una escena desde captura.
**Qué necesita la persona:** grabar su pantalla usando el producto (en Mac, Cmd+Shift+5; en Windows, Win+Alt+R) y dejar el archivo en `.tmp/grabaciones/`.

## Pasos

1. Sacar fotogramas a 10 por segundo:
   `cd renderer && npx remotion ffmpeg -i ../.tmp/grabaciones/<video>.mov -r 10 ../.tmp/frames/<nombre>/%05d.png`
   (Crear antes la carpeta `.tmp/frames/<nombre>/`. El ffmpeg de Remotion no trae el filtro `fps`: por eso se usa `-r 10`.)
2. Quedarse solo con los fotogramas donde la interfaz cambia:
   `python3 tools/filter_keyframes.py .tmp/frames/<nombre> .tmp/keyframes/<nombre> --fps 10`
   Suele reducir cientos de fotogramas a unas decenas. `manifest.json` dice en qué segundo está cada uno.
3. Mirar los fotogramas clave en orden y describir en las `notas.md` del flujo qué pasa, con los segundos: eso da duraciones aproximadas (contando fotogramas) y los estados intermedios.
4. Las duraciones sacadas de un vídeo son aproximadas. Si una importa de verdad, medirla (`medir-animaciones-en-el-navegador.md`).

Los fotogramas y la grabación se quedan en `.tmp/` (no se guardan en git). Si un fotograma sirve como referencia permanente, copiarlo a `referencia/<flujo>/capturas-producto/`.
