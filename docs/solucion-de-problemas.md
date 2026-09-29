# Solución de problemas

Si algo falla, díselo a Claude tal cual: lee el error y normalmente sabe qué hacer. Estos son los casos conocidos.

## Instalación

- **"node: command not found" o "npm: command not found"**: falta Node.js. Instala la versión LTS desde https://nodejs.org y cierra y vuelve a abrir la terminal (o Claude Code).
- **"python3: command not found"**: instala Python desde https://www.python.org/downloads/. En Windows, marca "Add Python to PATH" en el instalador.
- **En Mac, "no se puede abrir instalar.command porque procede de un desarrollador no identificado"**: clic derecho sobre el archivo → Abrir → Abrir. Solo la primera vez.
- **El render se queda parado la primera vez**: Remotion descarga un navegador interno la primera vez (≈100 MB). Espera unos minutos con buena conexión.

## Figma

- **Error 403 con el token**: el token está mal copiado, ha caducado o no tiene permiso de lectura de archivos. Crea uno nuevo (fase 1) y sustitúyelo en `.env`.
- **Error 404**: la URL del archivo no es correcta o tu cuenta no tiene acceso a ese archivo.
- **Error 429 (demasiadas llamadas)**: Figma limita cuántas llamadas se pueden hacer por minuto y por día, según tu plan y tu tipo de asiento. Para y retoma más tarde: el inventario guarda el progreso y la descarga sigue donde se quedó.
- **El MCP de Figma no aparece o pide iniciar sesión**: en Claude Code, escribe `/mcp`, elige `figma` y sigue el inicio de sesión en el navegador.
- **El MCP de Figma se queda sin llamadas enseguida**: con asiento de solo lectura o plan gratuito, las llamadas del MCP son muy pocas. Usa la ruta del token para la descarga masiva y guarda el MCP para leer las pocas pantallas que vas a construir.
- **Una pantalla sale como imagen de 1×1 píxel o vacía**: suele ser un frame vacío u oculto en Figma. Queda marcada como error y no bloquea el resto.

## Vídeo

- **La letra sale con otra fuente**: la fuente de tu producto tiene que estar cargada. Si está en Google Fonts, se cambia en `renderer/src/tokens/fonts.ts`. Si es una fuente propia, pon los archivos `.woff2` en `renderer/public/fuentes/` y pide a Claude que la cargue con `@remotion/fonts` (`loadFont` con `staticFile`).
- **"Componente no registrado"**: la escena existe pero falta añadirla a `componentRegistry.ts` y `registeredNames.ts`.
- **El cursor hace clic al lado del botón**: el diseño cambió después de medir. Pide a Claude que vuelva a medir los objetivos con imágenes (regla 18).
- **El vídeo pesa demasiado para la web**: pide a Claude una versión comprimida (H.264, CRF 24, `-movflags +faststart`). Suele quedar en 1-2 MB por minuto a 1440×800.
