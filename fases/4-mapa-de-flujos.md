# Fase 4 · Mapa de flujos

**Qué se consigue:** entender qué tareas se pueden hacer en el producto, con qué pantallas y en qué orden. Queda escrito en `referencia/FLUJOS.md` y `referencia/flujos.json`, y se ve en la pestaña "Flujos" de la galería.
**Qué necesita la persona:** conocer su producto. Claude propone y la persona corrige.
**Coste:** nada (se trabaja sobre las capturas ya descargadas).

## Pasos

1. Mirar las capturas sección a sección (las secciones de Figma suelen corresponder ya a funcionalidades). Leer los nombres de los frames: muchas veces cuentan la historia ("Listado vacío", "Listado con filtros", "Modal crear").
2. Proponer una lista de flujos. Un flujo es una tarea completa con principio y final, contada desde el punto de vista de quien usa el producto ("Crear un proyecto y asignar responsable", no "Pantalla de proyectos"). Para cada flujo:
   - nombre corto y una frase que lo describe;
   - las pantallas en orden (node ids), con una nota cuando una pantalla es un estado intermedio ("desplegable abierto");
   - huecos: pasos que faltan en Figma (p. ej. un estado de carga que no está diseñado).
3. Preguntar a la persona, sin tecnicismos: "¿Esto es así? ¿Falta algún paso? ¿Qué flujos son los más importantes para enseñar en vídeo?". Pedir que marque 1-3 flujos prioritarios.
4. Escribir `referencia/flujos.json`:
   ```json
   {"flujos": [{"slug": "crear-proyecto", "nombre": "Crear un proyecto",
                "descripcion": "…", "prioridad": 1,
                "pantallas": ["12:1", {"id": "12:7", "nota": "desplegable abierto"}, "12:9"]}]}
   ```
5. Escribir `referencia/FLUJOS.md` con lo mismo en prosa, más los huecos detectados y cómo se resolverán (construir desde captura, pedir a la persona una captura del producto real, o inventarlo con el sistema visual si es un estado trivial).
6. Crear `referencia/<slug-del-flujo>/notas.md` para cada flujo prioritario: qué se ve en cada pantalla, qué comportamiento se deduce, dudas abiertas.
7. `python3 tools/build_gallery.py --open` y revisar juntos la pestaña "Flujos".

## Si hay grabaciones del producto

Un vídeo del producto real en uso ayuda mucho a entender el orden y los estados intermedios. Ver `fases/extras/usar-una-grabacion-del-producto.md`.

## Terminada cuando

La persona reconoce su producto en la pestaña "Flujos" y hay al menos un flujo prioritario elegido. Anotar en `PROGRESO.md` cuáles.
