# Fase 5 · Sistema visual (design tokens, patrones e iconos)

**Qué se consigue:** los colores, la tipografía, los radios, los espaciados y los iconos de tu producto, documentados en `docs/design-tokens.md` y aplicados en `renderer/src/tokens/tokens.json`, más los primeros patrones de interacción en `docs/patrones.md`. A partir de aquí, cualquier escena se ve como tu producto.
**Qué necesita la persona:** revisar la pestaña "Sistema visual" de la galería y decir si reconoce su producto.
**Coste:** unas 5-15 llamadas al MCP de Figma.

## Pasos

1. **Elegir 3-5 pantallas representativas** de los flujos prioritarios: una con la barra lateral y la cabecera, una con tabla o lista, una con formulario, un modal. Así salen casi todos los tokens con pocas llamadas.
2. **Variables de Figma:** `get_variable_defs` del MCP sobre cada una. Si el archivo usa variables o estilos, esta es la fuente más fiable (`[figma-variable]`).
3. **Código de las pantallas:** `get_design_context` sobre esas mismas pantallas. Guardar lo que devuelve en `referencia/<flujo>/codigo/<node-id>.txt` para no volver a pedirlo. Del código salen los valores concretos (`[code]`):
   - colores: buscar `#xxxxxx`, `rgb(...)` y variables `var(--nombre, valor)`;
   - tipografía, radios, espaciados: contar qué tamaños de letra, pesos, interlineados, `border-radius` y `gap`/`padding` se repiten más. Los valores frecuentes son tokens; los que salen una vez suelen ser excepciones.
4. **Escribir `docs/design-tokens.md`** con cada valor, su uso y su etiqueta de fuente. Seguir las reglas del propio documento: si un token sale con dos valores, decidir si es por contexto o una ambigüedad, y documentarlo así. Nunca quedarse con un valor sin decirlo.
5. **Aplicarlo en el código:**
   - `renderer/src/tokens/tokens.json`: sustituir los valores de ejemplo. Se pueden renombrar o añadir claves, pero entonces hay que actualizar los componentes que usen las antiguas (buscar en `renderer/src`). Cambiar `_nota` para que ya no empiece por "PLANTILLA".
   - `renderer/src/tokens/fonts.ts`: la fuente del producto (ver el comentario del archivo; si no es de Google Fonts, `docs/solucion-de-problemas.md`).
   - `video.width`/`height`: el tamaño de las pantallas de Figma (p. ej. 1440×900) si difiere de 1440×800; ajustar también los guiones.
6. **Iconos:** buscar en Figma la página o sección de iconos del sistema de diseño (suele llamarse "Icons", "Iconografía" o estar en una página "Design System"). Exportar como SVG los que usan los flujos prioritarios (`get_design_context` o descarga de recursos del MCP) y guardarlos en `renderer/src/icons/`. El código que genera Figma para una pantalla a veces trae un cuadrado de color donde va el icono: el icono se reconstruye desde el sistema de diseño, no desde ese cuadrado.
7. **Patrones:** con las capturas y el código, anotar en `docs/patrones.md` los comportamientos que ya se ven (cómo son los modales, los menús, los estados de carga, los mensajes de confirmación), con la plantilla del documento.
8. **Comprobación visual:**
   - `python3 tools/build_gallery.py --open` → pestaña "Sistema visual". Preguntar a la persona si reconoce sus colores y su tipografía.
   - Renderizar un still del vídeo de ejemplo (`tools/render_still.py --composition demo-ejemplo--modal --frame 130 --output .tmp/stills/ejemplo/tokens.png`): la app ficticia de ejemplo ya sale con la piel de tu producto. Es una forma rápida de ver que los tokens funcionan juntos.

## Terminada cuando

La persona reconoce su producto en la galería y en el still. `tokens.json` ya no es la plantilla. Marcar en `PROGRESO.md`.
