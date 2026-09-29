# Fase 1 · Conectar Figma

**Qué se consigue:** Claude puede leer el archivo de Figma de tu producto.
**Qué necesita la persona:** una cuenta de Figma con acceso al archivo del producto y la URL de ese archivo.
**Coste:** nada. Las llamadas a Figma tienen límites según tu plan; el kit está hecho para gastar las mínimas.

Hay dos conexiones y conviene tener las dos:

| | Token personal (API REST) | MCP de Figma |
|---|---|---|
| Para qué | Descargar muchas pantallas de golpe (fases 2 y 3) | Leer el diseño, el código y las variables de una pantalla concreta (fases 5 y 6) |
| Llamadas | ≈1 por cada 20 pantallas | 1 por pantalla |
| Configuración | Crear un token y pegarlo en `.env` | Un comando y un inicio de sesión |

Si la persona no quiere crear un token, la fase 3 se puede hacer solo con el MCP, pantalla a pantalla (más lento y gasta muchas más llamadas).

## Pasos

### 1. La URL del archivo

Pedir a la persona la URL del archivo de Figma (en Figma: botón **Share** → **Copy link**, o copiar la barra del navegador). Anotarla en `PROGRESO.md`, sección "Mi proyecto". Si el producto está repartido en varios archivos, anotar todos y trabajar de uno en uno.

### 2. Token personal (recomendado)

Guiar a la persona paso a paso:

1. En Figma, abrir el menú de la cuenta (su foto, arriba a la izquierda) → **Settings** → pestaña **Security**.
2. En **Personal access tokens**, **Generate new token**.
3. Nombre: `product-video-demo-kit`. Caducidad: la que prefiera. Permisos: **File content → Read-only** (el resto se puede dejar sin acceso).
4. Copiar el token (Figma solo lo enseña una vez).
5. Copiar `.env.example` como `.env` si no existe, y pegar el token en la línea `FIGMA_TOKEN=`.

**Claude no pide que le peguen el token en el chat, y no puede leer `.env`** (está bloqueado en `.claude/settings.json` para proteger el token). La persona lo pega directamente en `.env`: explicarle cómo abrirlo (en la barra lateral del editor, o con TextEdit/Bloc de notas; en Mac, los archivos que empiezan por punto se ven en el Finder con Cmd+Shift+.). Si lo pega en el chat igualmente, pedirle que lo pegue también en `.env` y recomendarle revocar ese token en Figma y crear otro, porque ya ha quedado escrito en la conversación.

Comprobar: `python3 tools/figma_inventory.py --file "<URL>" --dry-run` (1 llamada). Si devuelve el nombre del archivo y sus páginas, funciona.

### 3. MCP de Figma

1. Si usa Claude Code en la terminal: `claude mcp add --transport http figma https://mcp.figma.com/mcp`. En la app de escritorio o en el IDE, lo mismo desde la configuración de MCP, o preguntar a Claude cómo hacerlo en esa versión.
2. Escribir `/mcp` en Claude Code, elegir `figma` y completar el inicio de sesión en el navegador.
3. Comprobar con la herramienta `whoami` del MCP de Figma (no gasta cuota): dice con qué cuenta y qué tipo de asiento se ha conectado. Anotarlo en `PROGRESO.md`. **Con asiento de solo lectura (View) o plan gratuito, el MCP da muy pocas llamadas**: avisar a la persona y apoyarse en el token para todo lo que se pueda.

## Terminada cuando

Hay URL anotada y al menos una de las dos conexiones funciona (idealmente las dos). Marcar la fase en `PROGRESO.md`.
