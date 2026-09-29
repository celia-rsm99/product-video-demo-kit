# Fase 6 · Construir las escenas

**Qué se consigue:** cada pantalla de los flujos prioritarios convertida en una escena de Remotion que se ve como tu producto y se maneja con datos del guion.
**Qué necesita la persona:** revisar cada escena al lado de su captura y decir si algo no cuadra.
**Coste:** 1-2 llamadas al MCP de Figma por pantalla (el código de esa pantalla, solo si no está ya guardado).

Se construye flujo a flujo y pantalla a pantalla, empezando por el flujo de prioridad 1. El flujo de ejemplo (`renderer/src/flows/ejemplo/`) sirve de modelo: cómo se lee `data`, cómo se usa `AppShell`, cómo se pulsa un botón y cómo se abre un modal con la pantalla atenuada detrás.

## Pasos, por cada pantalla

1. **Leer:** la captura (`referencia/<seccion>/capturas/`), su código si ya está en `referencia/<flujo>/codigo/` (si no, `get_design_context` y guardarlo ahí) y las `notas.md` del flujo.
2. **Clasificar:** qué patrón de `docs/patrones.md` reproduce. Si ninguno encaja, describir el nuevo en `patrones.md` primero.
3. **Comprobar qué hay de verdad en Figma:** si algo visible en el producto real no aparece en el frame de Figma (un componente que se añadió en código y nunca se diseñó), no se inventa: se construye desde una captura del producto real (ver abajo).
4. **Construir el componente** en `renderer/src/flows/<flujo>/<NombreEscena>.tsx`:
   - todos los valores visuales desde `renderer/src/tokens` (nunca un color o tamaño escrito a mano; si falta uno, volver a la fase 5 y añadirlo al documento primero);
   - todo el contenido desde props y `data` del guion: **ningún nombre, empresa o texto de ejemplo escrito dentro del componente**;
   - el chrome común del producto (barra lateral, cabecera) como un componente propio del flujo, igual que `AppShell` en el ejemplo, reutilizado por todas las escenas;
   - animaciones con los ayudantes compartidos (`typewriter`, `pressScale`, `FadeInPlace`, `AnchoredPopover`, `truncate`...);
   - quitar cualquier texto de relleno de Figma ("Lorem ipsum", "Label", nombres repetidos) y convertirlo en prop.
5. **Registrar** la escena en `renderer/src/lib/componentRegistry.ts` **y** en `renderer/src/lib/registeredNames.ts` con el nombre `"<flujo>/<NombreEscena>"`.
6. **Probar:** añadir la escena a un guion de trabajo (`renderer/scripts/<flujo>/borrador.json`, importado en `renderer/src/scripts.ts`) y renderizar un still:
   `python3 tools/render_still.py --composition borrador-<flujo>--<escena> --frame 0 --output .tmp/stills/<flujo>/<escena>.png`
7. **Comparar** con la captura: `python3 tools/diff_frame.py <still> <captura>` da una puntuación de parecido como ayuda (no es un aprobado/suspenso: los datos son otros a propósito). El juicio de verdad es visual: poner las dos imágenes una al lado de la otra y revisar estructura, colores de lienzo y tarjetas, tipografía, espaciados e iconos. Enseñárselo a la persona.
8. **Anotar** en `referencia/<flujo>/notas.md` que la pantalla ya tiene escena, con su origen: `figma (node-id)` o `solo captura`.

## Construir desde una captura (sin Figma)

Para un componente o pantalla que existe en el producto pero no en Figma:

1. Pedir a la persona una captura del producto real (y, si puede, un vídeo corto de cómo se comporta).
2. Analizar la imagen: posiciones, colores, tipografía, textos.
3. Ajustar cada valor observado al token existente más cercano. Nunca un valor nuevo si hay uno parecido.
4. Buscar el patrón más parecido en `docs/patrones.md`; si ninguno encaja, preguntar antes de inventar un lenguaje visual nuevo.
5. Anotarlo como `solo captura` en las notas y documentar los valores nuevos como `[png-estimated]`.
6. Revisión explícita con la persona: una imagen fija no dice cómo se comporta (¿reacciona al instante o al soltar?, ¿tiene estado de error?).

## Terminada cuando

Todas las pantallas del flujo prioritario tienen escena, cada una revisada al lado de su captura. Marcar el flujo en `PROGRESO.md`. Se puede pasar a la fase 7 con un flujo terminado y volver aquí para el siguiente.
