# Reglas de vídeo

Claude lee este archivo entero antes de escribir un guion, construir una escena, revisar o renderizar un vídeo. Cada regla salió de una corrección real sobre un vídeo demo ya hecho y se aplica por defecto a todos los vídeos nuevos, no solo al que la originó.

**Este archivo es tuyo y crece contigo.** Cuando corrijas algo en una ronda de feedback y sea algo que valdría para otros vídeos, Claude lo añade al final, numerado, con el vídeo y la fecha (ver `fases/8-render-y-revision.md`).

## Checklist antes de cada render completo

Repasar escena por escena. Entre paréntesis, la regla detallada.

- [ ] Esperas y cargas: la duración más corta que aún se lee como cambio de estado (1, 2).
- [ ] Todo lo que se escribe se ve escribirse, y la siguiente acción espera a que termine (3).
- [ ] Cada cambio que el guion cuenta tiene un cambio visible en pantalla, con el patrón real del producto (4, 5).
- [ ] Desplegables y menús se abren anclados bajo su botón, y el cursor baja hasta la opción y la pincha (6).
- [ ] Modales y asistentes: pantalla real atenuada detrás, tamaño final desde el frame 0 (7, 8).
- [ ] Barra lateral y cabecera completas, con fondos de tarjeta y lienzo iguales a la referencia (9, 10).
- [ ] Listas, tablas y bandejas con filas suficientes para llenar la pantalla (11).
- [ ] La misma animación en cada instancia de un elemento repetido (12).
- [ ] Texto largo recortado con "…", sin saltos de línea que muevan el diseño (13).
- [ ] Sin guiones largos ni medios (— –) en ningún texto visible (14).
- [ ] Cursor: visible si hay clics, sin etiqueta, movimiento que se lee como deslizamiento, empieza donde acabó la escena anterior, y cada objetivo medido en una imagen tras cualquier cambio de diseño (15, 16, 17, 18).
- [ ] Cada cambio de escena lo provoca un clic visible, con corte seco y sin fundido (19, 20).
- [ ] El estado final coincide con lo que el vídeo ha enseñado; nada de progreso inventado (21).
- [ ] Si una pantalla cambia según a quién se selecciona, cambia todo lo que depende de esa selección (22).
- [ ] Nada de secciones con título y sin contenido (23).
- [ ] Subtítulos desactivados salvo que se pidan; si se quitan, se quitan en todo el vídeo (24).
- [ ] Datos ficticios según `docs/datos-ficticios.md`.

---

## Ritmo y tiempo

**1. No copiar los tiempos de espera reales.** Una pantalla de carga debe durar lo mínimo para que se lea como cambio de estado (≈0,5-0,7 s), no lo que tarda de verdad el producto. *Por qué:* un vídeo demo enseña el producto de la forma más clara y rápida posible; no es una grabación realista.

**2. Calcular el tiempo de lectura hacia atrás.** Acortar una espera no basta: hay que mirar cuánto tiempo queda en pantalla el resultado antes del siguiente evento fijo (un clic, un cambio de escena). Si el resultado solo se ve un segundo, se recorta la espera lo suficiente para dejar ≈3 s de lectura, o se retrasa el siguiente evento.

**3. Lo que se escribe, se ve escribirse.** Si el guion dice que alguien escribe algo, se ve letra a letra en su campo (`typewriter` en `renderer/src/components/animation.ts`), y en un chat el mensaje se envía después, no aparece ya en el hilo. La siguiente acción (clic, guardar, cambio de escena) espera a que termine de escribirse (`typewriterEnd`).

## Fidelidad al producto

**4. Un cambio que se cuenta necesita un cambio visible.** Si el guion o un subtítulo dice "añade X como obligatorio", la pantalla tiene que enseñarlo, con el patrón que usa el producto real. Antes de inventar un visual, buscar la pantalla correspondiente en `referencia/` (la galería ayuda).

**5. Un destello que no aporta información se quita.** Un aviso o notificación que desaparece antes de poder leerse y no dice nada que el resto de la escena no diga ya, se elimina, no se acelera. La pregunta es "¿esto informa?", no "¿esto está en el producto?".

**6. Los desplegables se anclan a su botón con CSS.** Menú en `position: absolute` dentro de un contenedor `position: relative` que envuelve al botón (componente `AnchoredPopover`). Nunca coordenadas medidas a mano sobre la escena: en cuanto el botón se mueve, el menú queda flotando en otro sitio. Y un valor nunca cambia sin que el menú se haya visto abierto y el cursor haya elegido la opción.

**7. Detrás de un modal, la pantalla real atenuada.** Nunca un color plano. Se reutiliza la escena real congelada (`<Freeze>` de Remotion) debajo de una capa oscura semitransparente.

**8. Una caja de tamaño fijo reserva su espacio desde el frame 0.** Si los elementos de un modal o tarjeta aparecen de uno en uno montándose, la caja crece a saltos. Dentro de cajas fijas se usa `FadeInPlace` (ocupa su hueco, invisible hasta su momento); `Reveal` solo para cosas que de verdad no existen todavía, como un mensaje nuevo en un chat.

**9. El chrome recibe la misma fidelidad que el contenido.** La barra lateral, la cabecera y el bloque del usuario están siempre en pantalla aunque nunca sean el foco: foto y logo del usuario, y elementos de navegación coherentes con el tema del vídeo (no "Facturas de marzo" en un vídeo sobre contratación).

**10. Lienzo y tarjetas tienen colores distintos.** Una pantalla completa suele ser un fondo gris (lienzo) con paneles blancos (tarjetas), cada uno con su borde y su radio. Si una columna hereda el color del lienzo, toda la pantalla se convierte en una mancha plana sin estructura. Comparar siempre con la captura de referencia.

**11. Una lista de "varios" enseña varios.** Tablas, bandejas de entrada, tableros y listas llevan filas suficientes para llenar la pantalla desde la primera versión, aunque la escena solo interactúe con una. Una lista con una sola fila se lee como "solo hay uno".

**12. Lo que se arregla en uno, se arregla en todos.** Si un botón tiene efecto de pulsación, todos los botones equivalentes lo tienen. Cualquier comportamiento que se añade a una instancia se extrae a un ayudante compartido (`animation.ts`) en ese momento, para que ninguna instancia se quede atrás.

**13. El texto variable se recorta.** Cualquier celda o fila con texto de longitud variable lleva el estilo `truncate` (`renderer/src/components/text.ts`) y `minWidth: 0` en su contenedor flex. Sin eso, un valor largo ensancha la columna y desalinea esa fila respecto a las demás.

**14. Sin guiones largos ni medios (— –).** En ningún texto que se lea en pantalla: mensajes, subtítulos, etiquetas. Se reescribe con punto, coma o una conjunción. El validador avisa si encuentra alguno.

## Cursor

**15. Sin etiqueta junto al cursor.** Se ve el ratón, no un subtítulo que lo persigue. El componente `Cursor` ya no la dibuja.

**16. El desplazamiento se tiene que leer.** Un salto corto con algo pasando por el camino (un menú que se abre) necesita más frames, no menos: ≈25-35 frames para un desplazamiento normal. Una distancia corta en píxeles no implica que el viaje pueda ser instantáneo.

**17. El cursor continúa entre escenas.** El primer punto de cada escena es el último punto de la anterior, nunca vuelve a una posición por defecto. El validador avisa si hay un salto.

**18. Los objetivos de clic se miden en una imagen, no de cabeza.** Tras cualquier cambio de diseño en una escena (una fila más, un panel más ancho, otro texto), se renderiza una imagen en el frame del clic (`tools/render_still.py`), se lee la posición real del objetivo y se actualiza el guion. Coordenadas heredadas de una versión anterior del diseño caen en el botón equivocado.

## Escenas y cortes

**19. Cada corte tiene una causa visible.** Si la escena siguiente la provoca un botón o enlace que ya está en pantalla, el cursor hace clic en él antes del corte. Una escena que simplemente aparece se lee como un salto sin motivo.

**20. Corte seco, sin fundido ni negro entre escenas del mismo flujo.** Un corte con el cursor en su sitio se lee como la misma pantalla que continúa; un fundido se lee como un salto en el tiempo. Solo se usa transición si el guion la pide.

**21. El estado final no cambia sin enseñarlo.** Si al final se vuelve a una pantalla ya vista, se ve igual que antes salvo por los cambios que el vídeo ha mostrado. Nada de mover elementos o avanzar estados que no se vieron.

**22. Si algo varía según una selección, varía todo lo que depende de ella.** En una pantalla donde se elige entre varias personas o cuentas para enseñar que el contenido cambia, cambian nombre, foto y contenido personalizado, y no se queda ningún bloque fijo cerca que contradiga lo que se demuestra.

**23. Sin títulos huérfanos.** Una sección con título y sin nada debajo es un hueco visible. Se rellena con lo que muestra la referencia.

## Subtítulos

**24. Desactivados por defecto.** `captionStyle.burnIn: false` en el guion. Si la persona pide quitar los subtítulos "en general", se quitan de todas las escenas de ese vídeo, no solo de la que se mencionó.

## Método de trabajo

- **Ver lo que la persona vio.** Con feedback sobre un MP4, sacar imágenes en cada segundo citado (`tools/extract_frames.py`) antes de tocar nada: el guion y el render pueden no coincidir.
- **Comprobar con imágenes antes del render completo.** `tools/render_still.py` sobre la composición de escena suelta (`<id-guion>--<id-escena>`), en cada frame de clic y a ambos lados de cada corte.
- **Editar el guion sin reformatearlo entero.** Si se modifica el JSON con un script, cambiar solo las claves necesarias y conservar el formato compacto existente, para que el cambio sea legible en git.

---

## Reglas añadidas en este proyecto

<!-- Claude añade aquí las nuevas, numeradas desde 25, con vídeo y fecha. -->
