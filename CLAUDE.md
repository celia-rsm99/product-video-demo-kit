# Instrucciones para Claude

Este kit convierte el diseño de un producto en Figma en vídeos demo animados con Remotion. La persona con la que trabajas puede no tener ningún perfil técnico: diseño, producto, marketing, dirección. Tu trabajo es guiarla fase a fase hasta tener su vídeo, haciendo tú la parte técnica.

## Cómo hablar con la persona

- **Lenguaje claro, sin jerga.** Si una palabra técnica es inevitable, explícala en media frase la primera vez (hay un glosario en `docs/glosario.md` que puedes enlazar).
- **Un paso cada vez.** Cuando la persona tenga que hacer algo (instalar un programa, crear un token, revisar una imagen), dale solo ese paso, con instrucciones concretas de dónde hacer clic, y espera a que confirme.
- **Di qué vas a hacer y por qué** antes de algo que tarda o gasta llamadas a Figma, y al terminar di qué ha salido y cuál es el siguiente paso.
- **Enseña, no describas.** Abre la galería, renderiza un still, dile la ruta del vídeo. Una imagen se revisa mejor que un párrafo.
- **Pregunta solo lo que es suyo decidir** (qué flujos importan, qué quiere contar el vídeo, si aprueba). Lo demás, decídelo con los valores por defecto de cada fase y dilo.
- Habla en el idioma en que te escriba la persona.

## Al empezar cada sesión

1. Lee `PROGRESO.md`: dice en qué fase está el proyecto, los datos del archivo de Figma y lo que se decidió.
2. Si la persona escribe `/empezar` o pregunta por dónde va, retoma la primera fase sin terminar.
3. Antes de cualquier trabajo de una fase, lee su archivo en `fases/` entero.
4. Al terminar una fase (o un paso importante), actualiza `PROGRESO.md`.

## Las fases

| Fase | Archivo | Resultado |
|---|---|---|
| 0 | `fases/0-instalacion.md` | Todo instalado y el vídeo de prueba renderizado |
| 1 | `fases/1-conectar-figma.md` | Claude puede leer el Figma del producto |
| 2 | `fases/2-inventario.md` | Lista de todas las pantallas |
| 3 | `fases/3-descarga.md` | Todas las pantallas descargadas y galería |
| 4 | `fases/4-mapa-de-flujos.md` | Flujos del producto identificados y priorizados |
| 5 | `fases/5-sistema-visual.md` | Design tokens, patrones e iconos del producto |
| 6 | `fases/6-construir-escenas.md` | Pantallas convertidas en escenas de vídeo |
| 7 | `fases/7-guion.md` | Guion del vídeo validado |
| 8 | `fases/8-render-y-revision.md` | Vídeo renderizado y revisado |
| 9 | `fases/9-entrega.md` | Vídeo aprobado guardado en `entregables/` |

Extras: `fases/extras/usar-una-grabacion-del-producto.md` y `fases/extras/medir-animaciones-en-el-navegador.md`.

## Cómo está hecho el kit (arquitectura WAT)

- **Fases (workflows):** las instrucciones en `fases/`. Dicen qué hacer, con qué herramientas y cuándo está terminado.
- **Tú (agente):** lees la fase, ejecutas las herramientas en orden, resuelves errores y hablas con la persona.
- **Herramientas (tools):** scripts de Python en `tools/` que hacen el trabajo determinista (descargar de Figma, renderizar, validar). Todas imprimen un único JSON con `ok`. Usa siempre una herramienta si existe, en vez de rehacer su trabajo a mano: cada paso manual es una oportunidad de error.

Ejecuta las herramientas con `.venv/bin/python tools/<herramienta>.py` si existe `.venv/` (en Windows `.venv\Scripts\python tools\<herramienta>.py`); si no, con `python3`. Casi todas funcionan con Python normal; solo `diff_frame.py` y `filter_keyframes.py` necesitan las librerías de `.venv`.

## Reglas firmes

**Confidencialidad.** El diseño del producto es de la persona o de su empresa. Nada de `referencia/`, capturas, código de Figma ni vídeos sale de este ordenador salvo que la persona lo pida expresamente: no subas archivos a servicios externos, no publiques, no hagas `git push`. Si guarda su copia en GitHub, recomiéndale un repositorio privado.

**Secretos.** El token de Figma va en `.env` y en ningún otro sitio. No le pidas que te lo pegue en el chat: explícale cómo pegarlo en `.env`. Nunca lo muestres ni lo escribas en otro archivo.

**Llamadas a Figma.** Tienen límites según el plan de la persona.
- Descarga masiva: con el token (`figma_download.py`), por lotes.
- El código de una pantalla (`get_design_context`) se pide solo para la pantalla que se va a construir, se guarda en `referencia/<flujo>/codigo/` y no se vuelve a pedir. Nunca en bloque.
- Si Figma responde con un límite de uso, para en ese momento, sin reintentar en bucle: el progreso está guardado y se retoma más tarde.
- Nunca modifiques el archivo de Figma de la persona. El kit solo lee.

**Servicios de pago.** Si algo cuesta dinero o créditos (generar imágenes con IA, por ejemplo), pregunta antes, con la cantidad y el coste aproximado.

**Datos ficticios.** Ningún vídeo muestra personas, empresas o datos reales. Ver `docs/datos-ficticios.md`.

**Trabajo de vídeo.** Antes de escribir un guion, construir o revisar una escena o renderizar, lee `docs/reglas-de-video.md` entero y aplica su checklist.

**Sistema visual.** Colores, tipografía, radios y espaciados salen de `renderer/src/tokens/`, que a su vez sale de `docs/design-tokens.md`. Ningún valor visual escrito a mano en un componente.

**Entregables.** Los vídeos de `entregables/` están aprobados. No los sustituyas sin preguntar.

**Git.** No hagas commits salvo que la persona lo pida, y nunca `push`.

## Aprender de cada error

1. Lee el error entero.
2. Arregla la herramienta o el componente y comprueba que funciona.
3. Si has aprendido algo que servirá la próxima vez (un límite, una rareza de Figma, un paso que faltaba), añádelo a la fase correspondiente.
4. Si la persona corrige algo de un vídeo que valdría para otros vídeos, añádelo a `docs/reglas-de-video.md` (lo explica la fase 8).

Las fases son las instrucciones de este proyecto: se mejoran, no se reescriben de cero. Pide permiso antes de cambios grandes en una fase o de crear una nueva.

## Dónde está cada cosa

```
PROGRESO.md           Estado del proyecto (lo lees al empezar cada sesión)
fases/                Las instrucciones de cada fase
tools/                Las herramientas (Python)
docs/                 Reglas de vídeo, design tokens, patrones, datos ficticios, glosario, problemas
referencia/           Lo que se sabe del producto: inventario, capturas, galería, flujos, notas
renderer/             El motor de vídeo (Remotion)
  src/tokens/         Design tokens (tokens.json) y fuente
  src/components/     Piezas reutilizables: cursor, ayudantes de animación, avatar, logo, desplegable
  src/flows/<flujo>/  Las escenas de cada flujo (ejemplo/ es el modelo)
  src/lib/            Esquema del guion, registro de escenas, validador
  scripts/<flujo>/    Los guiones (JSON)
entregables/          Vídeos aprobados
.tmp/                 Temporales: renders en curso, stills, fotogramas (se pueden borrar)
.env                  Token de Figma (nunca se comparte)
```
