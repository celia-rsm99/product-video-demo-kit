# Glosario

Palabras que vas a ver durante el proceso, explicadas sin tecnicismos.

- **Claude Code**: el asistente con el que hablas. Lee las instrucciones del kit, ejecuta las herramientas y te va guiando.
- **Figma**: donde está diseñado tu producto. El kit lee de ahí las pantallas; nunca modifica tu archivo.
- **Archivo de Figma / página / sección / frame**: un archivo tiene páginas; en una página, los diseñadores agrupan las pantallas en secciones; cada pantalla es un *frame*.
- **Node id**: el identificador de cada elemento de Figma (p. ej. `12:345`). Sirve para volver a una pantalla exacta sin buscarla.
- **Token personal de Figma**: una contraseña de solo lectura que creas en tu cuenta de Figma para que el kit pueda descargar pantallas. Va en el archivo `.env` y nunca se comparte.
- **MCP de Figma**: la conexión oficial entre Claude y Figma. Permite a Claude leer el diseño y el código de una pantalla concreta.
- **Inventario**: la lista de todas las pantallas de tu archivo, con cuáles están descargadas. Vive en `referencia/_inventario.json`.
- **Flujo**: una tarea completa que alguien hace en tu producto, de principio a fin (p. ej. "crear un proyecto"). Un vídeo suele enseñar un flujo.
- **Design tokens**: los valores básicos del diseño con nombre: colores, tamaños de letra, radios de las esquinas, espaciados.
- **Patrón de interacción**: cómo se comporta algo cuando lo usas: cómo se abre un menú, cómo carga una lista.
- **Remotion**: la herramienta que convierte código en vídeo. Cada pantalla del vídeo se dibuja con código, por eso se ve nítida y se puede corregir al detalle.
- **Escena**: un trozo del vídeo que enseña una pantalla (o un momento de una pantalla).
- **Guion**: un archivo que describe el vídeo: qué escenas, en qué orden, cuánto dura cada una, qué datos ficticios usan y por dónde va el cursor. Vive en `renderer/scripts/`.
- **Frame (fotograma)**: cada imagen del vídeo. A 30 fps, 30 frames son un segundo.
- **fps**: fotogramas por segundo.
- **Composición**: lo que Remotion sabe renderizar. Cada guion crea una composición para el vídeo entero y otra por cada escena suelta.
- **Remotion Studio**: una ventana del navegador donde puedes ver el vídeo y moverte por él antes de renderizarlo.
- **Renderizar**: generar el archivo de vídeo final (MP4) a partir del guion.
- **Still**: una sola imagen de un frame, para revisar un momento concreto sin renderizar todo.
- **Entregable**: un vídeo que has aprobado. Se guarda en `entregables/`.
