# Extra · Vídeo explicativo con voz

**Cuándo:** cuando el vídeo **cuenta una historia** en vez de recorrer un flujo con el cursor: qué es el producto, por qué sirve, una función nueva para redes, ventas o una presentación. Lleva locución y música, dura 30-60 s y se construye frase a frase.
**Qué necesita:** las fases 0 a 6 hechas para los flujos que van a salir (las piezas del vídeo son las escenas y componentes ya construidos). Una voz: grabada por la persona o generada con un servicio de voz por IA (de pago: preguntar antes, con el coste). Música opcional, con licencia que permita usarla.

## La idea que lo hace funcionar

**Tu producto es material, no una grabación** (regla 25 de `docs/reglas-de-video.md`). Cada pieza es un componente real del producto con datos ficticios, pero qué hay en pantalla, de qué tamaño y cuándo lo decide la frase que dice la voz. Ejemplo: mientras la voz habla de los filtros, se ve solo la tarjeta de filtros, grande; cuando dice "¿quieres cambiar algo? Pídeselo al asistente", la tarjeta crece hacia un lado, entra el chat real dentro, se escribe la petición y el filtro cambia, petición y efecto en el mismo encuadre. Esa pantalla no existe en el producto, y ninguna grabación podría enseñarla.

Este vídeo no usa un guion JSON como los demos: es un componente propio con su `<Composition>` en `Root.tsx`, y su "guion" es el texto de la locución.

## Pasos

1. **Leer `docs/reglas-de-video.md` entero**, en especial la 25 y la sección "Vídeos explicativos con voz" (26-35) con su checklist.

2. **Brief en tres líneas**, con la persona: para quién es, qué tiene que pensar al terminar de verlo y dónde se publica. Eso decide el formato:
   - web o presentación: 1920×1080, ≈60 s;
   - redes: 4:5 (1080×1350) con subtítulos y ≈30-45 s. 9:16 (1080×1920) solo si se pide para Reels o TikTok. Encaje en la regla 33 y gancho en el frame 0 en la regla 31.

3. **Texto de la locución, frase a frase.** Una idea por frase, unas 20 frases por minuto. La persona lo aprueba antes de seguir: todo el montaje se ancla a él. Si el producto tiene cosas que no se pueden prometer, se apuntan aquí y mandan sobre el texto.

4. **Plan frase a frase** en `renderer/src/flows/<video>/PLAN.md`. Una tabla: frase → qué se ve → qué le resuelve a quien lo ve (regla 27: ahorro, confianza, escala, control) → pieza real de la que sale. Para cada frase decidir:
   - la **pieza mínima** que la cuenta;
   - si **crece o suma otra pieza** cuando la voz introduce algo nuevo, en vez de cortar;
   - qué piezas que el producto tiene separadas conviene **juntar** en un encuadre;
   - si hay un **hilo** que une planos (la misma persona ficticia pasando de una pantalla a la siguiente);
   - cómo **entra y sale**: movimiento de cámara o una pieza que se transforma en la siguiente, nunca un fundido cruzado (regla 30).
   Enseñar el plan a la persona y ajustarlo antes de construir: es lo más barato de cambiar.

5. **La voz.**
   - **Grabada:** en un sitio sin eco, móvil a un palmo, una frase por toma con un segundo de silencio antes y después. Se guarda en `renderer/public/<video>/audio/vo.wav`.
   - **Generada con IA** (preguntar antes: cuesta dinero o créditos). Se manda **dirigida, nunca en un bloque**: un párrafo por frase, puntos suspensivos para las pausas con peso y MAYÚSCULAS para el énfasis. Si el modelo acepta etiquetas de tono (como `[warm]` o `[confident]` en algunos de ElevenLabs), como mucho una por frase y solo donde cambia el tono. El mismo texto en un bloque y sin dirección suele salir plano. Ante la duda, dos tomas con distinta estabilidad (p. ej. 0,5 y 0,4) para que la persona elija.
   - **Apuntarlo todo en el `PLAN.md` en cuanto se genera** (regla 29): servicio y modelo, voz (nombre e id), ajustes, texto exacto, id de la creación y el postproceso.
   - Una voz algo lenta se puede acelerar un 5-10 % al reproducirla (`playbackRate` de `<Audio>` en Remotion). Se apunta, y el paso 6 lo tiene en cuenta.
   - **Cambiar una frase después:** generar o grabar varias tomas que incluyan la frase anterior y la siguiente, para que la entonación case, y empalmar cortando en mitad de las pausas.

6. **Anclar todo a la voz.** `tools/transcribe_words.py renderer/public/<video>/audio/vo.wav renderer/src/flows/<video>/voWords.json --idioma <es|en…>` saca el momento de cada palabra (en local; la primera vez hay que instalar `faster-whisper`, lo explica la herramienta). Un `timeline.ts` convierte palabras en frames, y **ningún tiempo del vídeo se escribe a mano**: si la voz cambia, el montaje se mueve con ella.
   ```ts
   import rawWords from "./voWords.json";
   export const FPS = 30;
   export const VO_RATE = 1;   // 1.08 si la voz se reproduce un 8 % más rápida
   export const VO_OFFSET = 6; // la voz entra unos frames después del gancho (regla 31)
   const norm = (s: string) => s.toLowerCase().normalize("NFD").replace(/[^a-z0-9']/g, ""); // sin tildes ni signos
   const WORDS = (rawWords as [string, number, number][])
     .filter(([w]) => norm(w) !== "")
     .map(([w, s, e]) => ({
       norm: norm(w),
       start: Math.round((s / VO_RATE) * FPS) + VO_OFFSET,
       end: Math.round((e / VO_RATE) * FPS) + VO_OFFSET,
     }));
   /** Frame en el que empieza a sonar `frase` (la primera vez a partir de la palabra `desde`). */
   export const at = (frase: string, desde = 0) => {
     const partes = frase.split(" ").map(norm);
     for (let i = desde; i <= WORDS.length - partes.length; i++) {
       if (partes.every((p, k) => WORDS[i + k].norm === p)) return WORDS[i].start;
     }
     throw new Error(`no encuentro "${frase}" en la locución`);
   };
   export const DURATION = WORDS[WORDS.length - 1].end + 45; // 1,5 s de cierre
   ```
   Y luego, en el montaje, `const T = { filtros: at("los filtros"), asistente: at("pídeselo al asistente") }`.

7. **Construir las piezas** en `renderer/src/flows/<video>/pieces.tsx`:
   - importar tal cual las piezas sueltas de las escenas ya construidas (fase 6) y de `renderer/src/components/`;
   - lo que solo existe dentro de una escena completa, **copiarlo** aquí y adaptarlo; las escenas de vídeos aprobados no se editan;
   - colores, tipografía y radios de `renderer/src/tokens/`, como siempre;
   - cada pieza a su tamaño nativo y entera (regla 26), con una prop para cada forma en que tenga que crecer o cambiar (p. ej. `chat` de 0 a 1 que ensancha la tarjeta).

8. **La cámara** en `renderer/src/flows/<video>/camera.tsx` (reglas 30 y 32): una función que, para cada frame, da la posición, la escala y los giros de la cámara sumando los movimientos clave del tramo (con easing) y una deriva lenta constante encima; y un contenedor que aplica eso a todo lo que hay dentro, con `perspective()` en el `transform` y el `transform-origin` en el centro de la pantalla. El fondo se mueve con la misma cámara; titulares, subtítulos y píldoras van fuera, en pantalla.

9. **Componer por frase**, un archivo por tramo si el vídeo es largo (apertura, medio, cierre). La cámara mueve el mundo, las piezas crecen y se combinan según la frase, y cada momento se ata a `at("…")`.

10. **Música y efectos** (opcional, pero suben mucho el resultado). Música sin voces, a volumen bajo y más baja todavía mientras habla la voz (el `volume` de `<Audio>` acepta una función del frame). Efectos cortos (pop, whoosh, click) en el frame de la acción que se ve; el tecleo, solo mientras se ve escribir (regla 28). Archivos en `renderer/public/<video>/audio/`, con su origen y licencia apuntados (regla 29).

11. **Subtítulos**, si se piden o si va a redes (regla 34): el texto del guion, no el de la transcripción, emparejado palabra a palabra con `voWords.json`, en trozos de 2-6 palabras y con la palabra que suena en el color de acento.

12. **Registrar** el vídeo con su propia `<Composition>` en `renderer/src/Root.tsx`, fuera del bucle de guiones, con la duración de `timeline.ts`. En formato estrecho, una segunda composición `<video>--guias` con las zonas seguras dibujadas, para revisar stills.

13. **Revisar por tramos.** Stills en cada frase con `tools/render_still.py`, y tramos con `tools/render_video.py --composition <video> --frames 0-299 --con-audio --output .tmp/renders/<video>/tramo.mp4` antes del render completo. **Sin `--con-audio` el vídeo sale mudo.** El feedback sigue `fases/8-render-y-revision.md`, y cada cambio de imagen obliga a repasar los efectos (regla 28).

14. **Aprobar y entregar** como en `fases/9-entrega.md`, y cerrar el `PLAN.md` con lo aprobado y lo descartado: es la referencia del siguiente vídeo.

## Salida

`renderer/src/flows/<video>/` con `PLAN.md`, `timeline.ts`, `voWords.json`, piezas, cámara y tramos; el audio en `renderer/public/<video>/audio/` con su origen apuntado; la composición en `Root.tsx`; el MP4 aprobado en `entregables/`.

## Problemas conocidos

- **El vídeo sale mudo:** falta `--con-audio` en `render_video.py`. En Remotion Studio sí suena, porque la opción solo afecta al render.
- **`at("…")` no encuentra una frase:** la transcripción la escribió de otra forma (un número en cifras, una palabra partida). Mirar `voWords.json` y usar la forma que aparece ahí.
- **Una palabra que rueda dentro de una ventana con `overflow: hidden` queda más alta que el texto de al lado:** el navegador toma como línea base el borde inferior de la caja. Poner las dos mitades en cajas con la misma altura de línea y `alignItems: "flex-start"` en vez de `baseline`.
