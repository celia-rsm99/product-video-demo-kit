# Extra · Medir animaciones en el producto real

**Cuándo:** cuando ya se sabe *qué* se mueve (por Figma o por una grabación) pero falta el número exacto (duración, curva, si de verdad anima o cambia al instante) y el detalle importa para que el vídeo no se sienta ni más lento ni más rápido que el producto.
**No como primer paso:** Figma y las grabaciones ya dan casi todo. Esto es para rellenar huecos puntuales.

Necesita que la persona tenga sesión iniciada en su producto en el navegador. Se puede hacer con **Claude en Chrome** (la extensión de navegador de Anthropic) o a mano con las herramientas de desarrollo del navegador.

## Pasos

1. Elegir 1-4 animaciones sin medida, buscando en `docs/patrones.md` y en las `notas.md` de los flujos frases como "estimado" o duraciones sin fuente.
2. Escribir **un solo prompt autocontenido** para Claude en Chrome (no comparte esta conversación), con: el objetivo, dónde navegar en el producto, qué elemento o interacción buscar, qué extraer y el formato de respuesta. Qué pedir:
   - si puede ejecutar JavaScript: `getComputedStyle(elemento)` → `transitionProperty`, `transitionDuration`, `transitionTimingFunction`, `animationName`, `animationDuration`, `animationTimingFunction`, `backdropFilter`;
   - si no: DevTools → Elements → Styles/Computed, o More tools → Animations;
   - el mecanismo real: transición CSS, `@keyframes`, animación por JavaScript, espera de red, o "sin animación, cambio instantáneo";
   - si no puede disparar la interacción, que busque igualmente la regla CSS en las hojas de estilo.
   Formato: un bloque por animación, con valores exactos o "no se pudo determinar".
3. La persona ejecuta el prompt y pega la respuesta en esta conversación.
4. **Contrastar, no promediar.** Lo medido en el producto manda: si contradice una lectura hecha a partir de un vídeo, se corrige la lectura, no se ignora la diferencia (caso típico: lo que en un vídeo parecía texto escribiéndose resulta ser una espera y una aparición instantánea).
5. Anotar en `docs/patrones.md` (y en las notas del flujo) con la etiqueta **"Medido en el navegador (fecha)"** y el mecanismo real.
