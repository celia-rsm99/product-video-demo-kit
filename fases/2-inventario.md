# Fase 2 · Inventario de pantallas

**Qué se consigue:** una lista de todas las pantallas del archivo de Figma, agrupadas por sección, en `referencia/_inventario.json`. Es la fuente de verdad del progreso de descarga.
**Qué necesita la persona:** decir qué páginas de Figma interesan (a veces hay páginas de pruebas, archivo antiguo o componentes que no hacen falta).
**Coste:** 1 llamada con token. Con MCP, unas pocas llamadas de `get_metadata`.

## Pasos (ruta con token)

1. `python3 tools/figma_inventory.py --file "<URL>" --dry-run`
2. Enseñar a la persona, en lenguaje claro, qué se ha encontrado: páginas del archivo, secciones y cuántas pantallas tiene cada una. Preguntar qué páginas incluir. Si hay muchas pantallas pequeñas que no son pantallas (piezas, iconos), subir `--min-width`.
3. Crear el inventario de verdad con las páginas elegidas:
   `python3 tools/figma_inventory.py --file "<URL>" --pages "App,Onboarding"`
4. `python3 tools/inventory.py status` para confirmar el total.

## Pasos (ruta solo MCP)

1. `get_metadata` sobre el archivo para listar páginas. **Ojo:** en archivos grandes, la llamada sin `nodeId` puede devolver solo algunas páginas. Si faltan páginas que la persona sabe que existen, pedirle la URL de una sección o página (lleva `node-id=` en la URL) y recorrer desde ese node id hacia abajo.
2. Recorrer página → secciones → frames. Cada frame de primer nivel dentro de una sección (o suelto en la página) de ancho ≥ 320 px es una pantalla. Ignorar componentes.
3. Escribir un JSON con el formato de entrada de `tools/inventory.py` (ver su cabecera) y ejecutar:
   `python3 tools/inventory.py init --file-key <KEY> --file-name "<nombre>" --from .tmp/secciones.json`

## Notas

- Volver a ejecutar el inventario más adelante (p. ej. porque el diseño ha crecido) **conserva el progreso**: las pantallas ya descargadas siguen marcadas como hechas.
- La key del archivo es la parte de la URL después de `/design/` o `/file/`.

## Terminada cuando

`inventory.py status` enseña el total de pantallas y la persona está de acuerdo con lo que entra. Anotar en `PROGRESO.md` el total y la fecha.
