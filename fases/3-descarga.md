# Fase 3 · Descargar las pantallas

**Qué se consigue:** una imagen PNG (a doble resolución) de cada pantalla del inventario en `referencia/<seccion>/capturas/`, y una galería para verlas todas.
**Qué necesita la persona:** nada, salvo esperar. Con cientos de pantallas puede llevar un rato.
**Coste:** con token, 1 llamada por cada 20 pantallas. Con MCP, 1 llamada por pantalla.

Todo el progreso se guarda en el inventario tras cada pantalla o lote: si la sesión se corta, se vuelve a lanzar y sigue donde lo dejó. Esta fase se puede retomar en cualquier sesión nueva, aunque Claude no recuerde la conversación anterior.

## Pasos (ruta con token)

1. `python3 tools/inventory.py status`: cuántas quedan.
2. `python3 tools/figma_download.py --limit 200`
3. Repetir hasta que no queden pendientes. Si responde con `rate_limited`, **parar sin reintentar en bucle**: explicar a la persona que Figma pide una pausa y que se puede seguir más tarde (o mañana) sin perder nada.
4. Las que queden en error: `figma_download.py --retry-errors` una vez. Si siguen fallando, suelen ser frames vacíos u ocultos; dejarlas como error y anotarlo.

## Pasos (ruta solo MCP)

1. `python3 tools/inventory.py next --limit 20`
2. Por cada pantalla: `get_screenshot` del MCP de Figma con su `nodeId`. Si la respuesta trae una URL de imagen, guardarla con `python3 tools/save_screenshot.py --id <id> --url "<url>"`. Si el MCP devuelve la imagen solo dentro del chat, sin URL ni archivo, **esta ruta no puede guardar a disco**: explicarlo y volver a la ruta con token.
3. Límite prudente: no más de ≈150 capturas por sesión, con una pausa breve cada ~10. Si aparece un error de límite, parar inmediatamente; el inventario ya está guardado.

## Al terminar (las dos rutas)

1. `python3 tools/build_gallery.py --open`: abre `referencia/galeria.html` en el navegador. Enseñársela a la persona: es la primera vez que ve todo su producto junto.
2. Informar: cuántas se han descargado, cuántas han fallado y cuántas quedan.

## Fuera de esta fase, a propósito

El código de las pantallas (`get_design_context`) y los recursos gráficos **no** se descargan en bloque: se piden pantalla a pantalla solo cuando esa pantalla se va a construir (fase 6). Así se gastan las llamadas justas.

## Terminada cuando

No quedan pendientes (las de error, anotadas) y la persona ha visto la galería. Anotar la fecha de cierre en `PROGRESO.md`.
