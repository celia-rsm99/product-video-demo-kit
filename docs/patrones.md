# Patrones de interacción de tu producto

Cómo se comporta tu producto: qué pasa cuando se hace clic, cómo se abre un modal, cómo carga una lista, cómo responde un chat. Se rellena en la fase 5 y se amplía en la fase 6 cada vez que se construye una pantalla con un comportamiento nuevo. Las escenas citan el patrón que reproducen.

Describir solo lo **observable** en las capturas, el código de Figma o el producto real, con su fuente. Nunca inventar un comportamiento porque "suele ser así".

## Plantilla de patrón

```
## N. Nombre del patrón

**Visto en:** flujo / pantallas (ids de Figma)
**Secuencia:** qué pasa, en orden, desde la acción del usuario hasta el estado final.
**Tiempos:** duraciones y curvas, con su fuente ([devtools], [code], estimado de vídeo).
**Cómo se reproduce en el kit:** componentes/ayudantes que lo implementan.
```

---

## Regla general para predecir tiempos sin medirlos

Si no hay medida del producto real, primero averiguar con qué está construido el componente:

- **Librerías de componentes (Material UI, Chakra, Radix, Headless UI…)** traen duraciones por defecto de su tema. En Material UI: ≈225 ms al entrar y ≈195 ms al salir para modales y fundidos de pantalla, ≈150 ms para cambios pequeños (interruptores, hover), con curva `cubic-bezier(0.4, 0, 0.2, 1)`. Suponer los valores por defecto de la librería es mejor apuesta que estimar a ojo.
- **Componentes a medida con utilidades CSS (Tailwind y similares)** muchas veces cambian **al instante**, sin transición, aunque en un vídeo comprimido parezca que animan.

Un vídeo grabado a pocos fotogramas por segundo engaña: algo que parece una animación de escritura puede ser una espera de red seguida de una aparición instantánea. Si el detalle importa, medirlo (`fases/extras/medir-animaciones-en-el-navegador.md`).

---

## Patrones de tu producto

<!-- Claude añade aquí los patrones, numerados. -->
