# Fase 7 · Escribir el guion

**Qué se consigue:** el guion del vídeo (`renderer/scripts/<flujo>/<nombre>.json`), validado y visible en Remotion Studio.
**Qué necesita la persona:** decir qué quiere contar, dónde se va a usar el vídeo y aprobar el guion en palabras antes de que se programe.
**Coste:** nada.

## Pasos

1. **Leer `docs/reglas-de-video.md` entero.** El guion tiene que cumplir su checklist desde la primera versión.
2. **Preguntar lo imprescindible** (con valores por defecto para no bloquear):
   - ¿Qué debe entender quien vea el vídeo? (una frase)
   - ¿Dónde se va a usar? Web (por defecto: horizontal, al tamaño de las pantallas, sin subtítulos, en bucle), redes (vertical 9:16 o cuadrado 1:1), onboarding, presentación.
   - Duración objetivo (por defecto 20-45 s).
3. **Guion en palabras.** Escribir la secuencia escena a escena, en lenguaje claro: qué pantalla, qué pasa, en qué orden, dónde empieza y dónde acaba el cursor, qué clic provoca el paso a la siguiente escena. Enseñárselo a la persona y ajustarlo **antes** de tocar el JSON. Es mucho más barato corregir aquí.
   Para cada escena, piensa primero qué tiene que entender quien lo ve y compón la pantalla para eso (regla 25 de `docs/reglas-de-video.md`): no hace falta enseñar la pantalla completa del producto si una sola tarjeta lo cuenta mejor.
4. **Datos ficticios** según `docs/datos-ficticios.md`: usuario, personas, empresas y lo propio del producto (en `data.extra`).
5. **Escribir el JSON** siguiendo `renderer/src/lib/schema.ts` (el guion de ejemplo `renderer/scripts/ejemplo/demo-ejemplo.json` sirve de modelo):
   - el `id` en minúsculas con guiones, p. ej. `crear-proyecto-v1`;
   - cada escena con su componente registrado, su duración en frames (30 = 1 s), sus props y su cursor;
   - el primer punto del cursor de cada escena = el último de la anterior.
6. **Validar:** `python3 tools/validate_script.py renderer/scripts/<flujo>/<nombre>.json`. Tiene que dar `ok`. Revisar cada aviso (`warnings`): casi siempre es una regla de vídeo.
7. **Registrar** el guion en `renderer/src/scripts.ts` (import + añadirlo a la lista).
8. **Medir los clics:** por cada clic, un still en su frame sobre la composición de la escena suelta (`<id>--<escena>`) y comprobar que el cursor cae sobre el objetivo. Si no, leer la posición real en la imagen y corregir el guion (regla 18).
9. **Previsualizar** en Remotion Studio (`cd renderer && npm run studio`) y que la persona lo vea antes del render completo.

## Otra versión con otros datos

Para hacer una variante (otro sector, otros nombres): copiar el JSON, cambiar solo `data` y el `id`, validar y registrar. Ningún componente se toca.

## Terminada cuando

El guion valida, los clics caen en su sitio y la persona ha visto la previsualización. Pasar a la fase 8.
