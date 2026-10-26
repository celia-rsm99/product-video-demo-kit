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
- [ ] Cada momento compuesto para lo que se cuenta: pieza mínima primero, que crece o suma otra pieza real cuando la historia introduce algo nuevo (25).
- [ ] Datos ficticios según `docs/datos-ficticios.md`.

**Además, en vídeos explicativos con voz** (`fases/extras/video-explicativo-con-voz.md`), plano a plano:

- [ ] Una pieza real por plano, entera y grande; como mucho 8-10 palabras de interfaz legibles y nada quieto y lleno de texto más de 3-4 s (26, 35).
- [ ] Cada plano demuestra para qué le sirve la función a quien lo ve, no solo que existe (27).
- [ ] Efectos de sonido en el frame de la acción que se ve, repasados tras cada cambio de imagen (28).
- [ ] Voz, música e imágenes generadas, apuntadas en el `PLAN.md` con herramienta, ajustes y texto (29).
- [ ] Transiciones como movimientos de una sola cámara, sin fundidos cruzados y siempre con algo opaco en plano (30, 32).
- [ ] Para redes, el frame 0 ya enseña el gancho (31).
- [ ] La cámara deriva siempre y hace como mucho un movimiento por frase (32).
- [ ] Formato estrecho (4:5, 9:16): escala con margen para la cámara y zonas seguras respetadas (33).
- [ ] Subtítulos, si se piden: texto del guion, pegados a la voz y sin repetir lo que ya dice la tipografía (34).

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

**24. Desactivados por defecto.** `captionStyle.burnIn: false` en el guion. Si la persona pide quitar los subtítulos "en general", se quitan de todas las escenas de ese vídeo, no solo de la que se mencionó. Cuando sí se piden (habitual en vídeos para redes, que se ven sin sonido), ver la regla 34.

## Composición

**25. La pantalla se compone por lo que se cuenta, no por cómo es el producto.** Cada momento empieza con la pieza mínima que lo explica, sola, sin columnas ni paneles que no hablen de eso. Cuando la historia introduce algo nuevo relacionado, la pieza que ya está crece y la nueva pieza real entra dentro o al lado, en vez de cortar a otra pantalla. Si la historia habla de dos cosas a la vez (una petición y su efecto), van en el mismo encuadre aunque en el producto estén separadas. Lo que se inventa es la composición; el aspecto de cada pieza es siempre el de tu producto. *Por qué:* es lo que una grabación no puede hacer y lo que hace que el vídeo cuente una historia en vez de enseñar pantallas. *Cómo:* una prop en la pieza para cada forma en que tenga que crecer (p. ej. `chat` de 0 a 1 que ensancha la tarjeta), animando su ancho nativo y una escala que lo compense para que todo siga cabiendo y centrado.

## Vídeos explicativos con voz

Vídeos que cuentan una historia (qué es el producto, por qué sirve, una función nueva para redes) con locución y música, en vez de recorrer un flujo con el cursor. Todas las reglas anteriores siguen valiendo; estas se suman. El proceso está en `fases/extras/video-explicativo-con-voz.md`.

**26. Una idea por plano, y nada metido en una caja.** Cada plano enseña una sola pieza real del producto, entera (sus cuatro bordes, esquinas y relleno a la vista) y grande, legible en un móvil. Ni la pantalla entera dentro de una ventana con zoom (se lee "todo muy contenido en una caja"), ni pantallas completas en 3D con piezas separándose (demasiada interfaz moviéndose a la vez). Matices que salieron de rondas reales:
- *El titular no es obligatorio ni tiene sitio fijo.* Algunos planos necesitan un texto corto de 2-4 palabras y otros se explican solos. "Titular a la izquierda, animación a la derecha" en todos los planos se lee como plantilla.
- *Nada de literal y pobre.* Tres funciones resueltas con una caja de texto, dos filas y un mensaje en miniatura se ven baratas. O cada función se enseña de una en una y con tiempo, o se cuenta con otro recurso (tipografía, por ejemplo).
- *El montaje rápido funciona a propósito.* Muchos cortes seguidos (seis en dos segundos) se leen como energía si cada pieza es entera, grande y entra en movimiento. Lo pobre son las piezas pequeñas y quietas, no que sean muchas.
- *Abrir solo con tipografía es genérico.* Mejor un solo objeto real y grande (el campo de búsqueda, por ejemplo) que cada verbo de la voz transforma un instante.
- *Nada asoma por el borde.* Un panel que se ve a medias para sugerir que hay más se lee como componente cortado. Si un componente vive dentro de una pantalla larga, se renderiza suelto, no se recorta a ojo. Única excepción: el primer plano al que se llega moviendo la cámara (regla 32).
- *Color de acento solo en la palabra clave y en el elemento del que habla la voz.* Los pop-ups salen solos, sin el fondo atenuado de la regla 7: aquí no hay pantalla detrás.

**27. Cada plano enseña para qué le sirve la función a quien lo ve, no solo que existe.** Una lista con tres filas dice "hay una lista"; lo que convence es el volumen (la tabla llena y creciendo), que el producto sigue trabajando solo y que cada fila trae su porqué. *Cómo:* antes de diseñar un plano, escribir en una línea qué resuelve (ahorro de tiempo, confianza, escala, control) y elegir la parte del componente real que lo demuestra. *Encuadre:* la porción más pequeña de la pantalla en la que todo lo visible aporta algo a esa frase. A veces son dos paneles (una conversación con la lista de personas al lado dice a quién se escribe y que hay más); lo que no aporta (navegación, campos vacíos) se queda fuera.

**28. Los efectos de sonido van atados a la acción que se ve.** El tecleo suena solo mientras se ve escribir; clics, pops y whooshes caen en el frame del clic, del cambio o del movimiento que los causa. Cada vez que cambia la imagen de un tramo, se repasa su lista de efectos a la vez, no después: un tecleo heredado de una versión anterior que suena sobre una pantalla quieta es el fallo típico.

**29. Todo lo generado (voz, música, imágenes) queda apuntado en el momento.** En el `PLAN.md` del vídeo o en un `ORIGEN.md` junto al archivo: herramienta y modelo, voz (nombre e id), ajustes, texto o prompt exacto, id de la creación en el servicio y el postproceso (p. ej. "acelerada un 8 %"). Sin eso, cambiar una palabra de la locución semanas después obliga a adivinar con qué voz se hizo, y la nueva toma no casa.

**30. Las transiciones son movimientos de una cámara, no objetos que se mueven solos.** Si cada pieza entra y sale con sus propios giros desde el centro, se ve que "solo se mueven los componentes, no el mundo".
- *Una sola cámara para todo lo que hay en plano.* Las piezas se colocan en un mismo espacio (una delante, otra 1.500 px detrás) y se anima la cámara. Perspectiva, paralaje (lo cercano pasa rápido, lo lejano casi no se mueve), foco y curva de velocidad salen de ella y casan solos. El fondo se mueve con la cámara; la viñeta no, es de la lente.
- *Movimientos que funcionan:* grúa (arranca pegada a la pieza, por debajo, enorme y desenfocada, y retrocede hasta dejarla plana y enfocada), la misma grúa al revés para cerrar, un giro rápido sobre sí misma con estelas en el fondo, y una pieza que se transforma en la siguiente (un mensaje que vuela al hilo y se convierte en su burbuja).
- *Los rótulos van en pantalla, fuera del espacio 3D.* El contraste entre el mundo que se mueve y el texto quieto es lo que se lee como cámara.
- *Plano cuando hay que leer.* El movimiento termina antes de que se escriba algo o aterrice un elemento en su sitio.
- *Nada de fundidos cruzados entre dos pantallas.* Dos capas semitransparentes se ven sucias. La saliente se transforma en la entrante o sale por el movimiento de cámara.
*Cómo, en Remotion:* `perspective()` dentro de `transform`, con `transform-origin` en el centro de la pantalla. La distorsión curva de un gran angular no se puede hacer con CSS.

**31. En un vídeo para redes, el frame 0 ya enseña el gancho.** Las redes reproducen el vídeo solo y sin sonido desde el primer frame, y los primeros tres segundos deciden si alguien sigue mirando. Un frame 0 con el fondo vacío y el logo apareciendo hacia el segundo 1 se pierde. *Cómo:* la animación de entrada arranca ya empezada: en el frame 0 hay texto legible y la pieza principal a medio animar. El gancho es el mismo; solo se adelanta su arranque. El audio no se mueve.

**32. La cámara nunca se para, pero hace como mucho un movimiento por frase.** Un plano que aterriza y se queda clavado se lee como una diapositiva.
- *Deriva siempre.* Un avance y un deslizamiento lentos y constantes (del orden de 0,04-0,08 % de zoom y 0,3-1 px por frame), también mientras se escribe o se lee.
- *Un movimiento por frase.* Irse a un plano general inclinado y volver en 1,5 s es "mucho movimiento en muy poco tiempo"; queda mejor un solo retroceso lento. Cada movimiento va atado a lo que dice la voz: acercarse al resultado cuando la voz lo nombra, seguir una tarjeta que se arrastra.
- *Repertorio que funciona:* subir desde abajo inclinada y quedar recta antes de leer, retroceso rápido para salir, plano general inclinado para enseñar volumen, barrido lateral que enlaza con la entrada de la pantalla siguiente, y bajar de una pantalla a la siguiente.
- *En cada cambio siempre hay algo opaco en plano.* Al bajar de una pantalla a otra, la saliente sale por arriba mientras la entrante ya asoma por abajo, las dos opacas. Ni fundido ni un frame vacío entre las dos.
- *Desenfoque de movimiento solo en las salidas rápidas.* En un movimiento que llega a algo que leer, convierte la pieza en una mancha.
- *Una pieza que se convierte en otra cae exactamente sobre su sitio* (una tarjeta que encoge hasta que su foto cae sobre la foto de su fila en la tabla, y se disuelve en ella). Las posiciones se miden en el diseño, no a ojo.
- *Cortar bordes vale en un primer plano al que se llega moviendo la cámara* desde la pieza entera. Un recorte quieto sigue leyéndose como componente cortado (regla 26).
*Cómo:* una función de cámara por tramo que suma los movimientos clave (con easing) y una deriva constante encima, y un contenedor que filma a sus hijos girando sobre el centro de la pantalla. Lo que va en pantalla y tiene que apuntar a algo del mundo (un elemento que vuela a su sitio) proyecta su destino con la misma cámara.

**33. Formato estrecho (4:5 o 9:16): el encaje se decide antes de construir y la cámara necesita margen.**
- *Escala con margen.* Una pieza que llena justo el ancho útil se sale por un lado en cuanto la cámara se acerca o deriva. Dejar aire (1,9× en vez de 2×). Las piezas anchas (tablas, conversaciones) se rehacen más anchas en nativo y más bajas, para caber en alto a menos escala.
- *Centrar en el área útil, no en el frame.* En 9:16 la interfaz de Reels, TikTok o LinkedIn tapa unos 240 px arriba, 420 abajo y 120 a la derecha (en 1080×1920). En 4:5 (1080×1350) el feed no tapa nada: 60 px de margen y dos bandas, una para la pieza y otra para los subtítulos.
- *Moverse en alto.* En vertical sobra recorrido en altura y falta en anchura: las transiciones son subidas y bajadas de cámara entre zonas apiladas, y la deriva es vertical. Las zonas se colocan a menos de un frame de distancia, para que la pieza que sale y la que entra compartan plano.
- *Comprobar con guías.* Una segunda composición del mismo vídeo con las zonas seguras dibujadas encima, para revisar stills.

**34. Subtítulos, cuando se piden: el texto del guion pegado a la voz, y nada que diga lo mismo dos veces.**
- *Texto del guion, no de la transcripción.* La transcripción automática parte palabras ("follow -up") y junta frases con comas. Cada palabra del guion se empareja en orden con las de la voz por su forma normalizada, y así cada palabra tiene sus frames.
- *Trozos cortos* (2-6 palabras, cortados a mano), la palabra que suena en el color de acento, y el primer trozo ya visible en el frame 0 (regla 31).
- *Sin duplicados.* Con subtítulos sobran los titulares. Donde la tipografía grande ya dice el texto (el cierre, la llamada a la acción), los subtítulos se ocultan.

**35. Muy, muy simple: un foco por plano y las ideas contadas con imagen, no leídas.** El fallo típico es pasar diez de treinta segundos en la misma pantalla, llena de texto y casi sin animación.
- *Un foco y pocas palabras.* Como mucho 8-10 palabras de interfaz legibles por plano (los subtítulos no cuentan). Lo que no habla de la frase se quita, aunque esté en la pantalla real: un diálogo cuya consecuencia ya se ve, descripciones, pasos de más, la mitad de una tabla.
- *Ninguna pantalla quieta y llena de texto más de 3-4 s.* Si la voz dedica varias frases al mismo componente, sus ideas se convierten en imagen (las opciones de un diálogo salen volando y se vuelven tarjetas, cada una con una línea por la que caen mensajes hacia su destinatario; "parar solo esta" es cortar esa línea mientras las otras siguen). El componente real aparece solo en el momento de actuar. Un plano de paso que solo enseña un dato no pasa de ~1,5 s.
- *El sentido del dibujo se lee solo.* Los mensajes caen hacia quien los recibe, como a una bandeja de entrada; si "suben" hacia él, no se entiende quién escribe a quién.
- *Estados en el formato del producto.* Un "(en pausa)" en texto gris pasa a la etiqueta de estado real (Activo, En pausa, Parado).
- *Lo pequeño se dibuja a su tamaño final, no se escala.* Una casilla de 14 px escalada 1,8× se ve como un cuadradito raro.
- *Lo que no aporta sale del plano,* como el tablero que quedaba detrás de un diálogo: se desvanece mientras el diálogo sale.
Inventar la composición (líneas, mensajes volando, marcas sobre las tarjetas) es aceptable si las piezas son del producto (regla 25), pero se dice al enseñar el render.

## Método de trabajo

- **Ver lo que la persona vio.** Con feedback sobre un MP4, sacar imágenes en cada segundo citado (`tools/extract_frames.py`) antes de tocar nada: el guion y el render pueden no coincidir.
- **Comprobar con imágenes antes del render completo.** `tools/render_still.py` sobre la composición de escena suelta (`<id-guion>--<id-escena>`), en cada frame de clic y a ambos lados de cada corte.
- **Editar el guion sin reformatearlo entero.** Si se modifica el JSON con un script, cambiar solo las claves necesarias y conservar el formato compacto existente, para que el cambio sea legible en git.

---

## Reglas añadidas en este proyecto

<!-- Claude añade aquí las nuevas, numeradas desde 36, con vídeo y fecha. -->
