import { interpolate } from "remotion";

/**
 * Ayudantes de animación compartidos. Si una animación se usa en más de un
 * sitio, vive aquí: así todas las instancias de un mismo elemento se animan
 * igual (docs/reglas-de-video.md, regla de hermanos).
 */

/**
 * Texto que se escribe letra a letra. Devuelve el trozo visible en `frame`.
 * `charsPerFrame` 0.8 ≈ 24 caracteres por segundo a 30 fps: se lee como
 * alguien escribiendo rápido sin que parezca un volcado.
 */
export const typewriter = (text: string, frame: number, startFrame: number, charsPerFrame = 0.8) => {
  const n = Math.max(0, Math.floor((frame - startFrame) * charsPerFrame));
  return text.slice(0, Math.min(n, text.length));
};

/** Frame en el que `typewriter` termina de escribir `text`. Úsalo para encadenar la siguiente acción. */
export const typewriterEnd = (text: string, startFrame: number, charsPerFrame = 0.8) =>
  startFrame + Math.ceil(text.length / charsPerFrame);

/** Escala de un botón al pulsarlo: baja a 0.94 y vuelve, en 8 frames. */
export const pressScale = (frame: number, pressFrame?: number) => {
  if (pressFrame === undefined) return 1;
  return interpolate(frame, [pressFrame, pressFrame + 3, pressFrame + 8], [1, 0.94, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
};

/** Opacidad 0 → 1 a partir de `at`, en `duration` frames. */
export const fadeIn = (frame: number, at: number, duration = 8) =>
  interpolate(frame, [at, at + duration], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

/** Desplazamiento vertical que acompaña a fadeIn (entra desde `distance` px más abajo). */
export const slideUp = (frame: number, at: number, duration = 8, distance = 8) =>
  interpolate(frame, [at, at + duration], [distance, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

/** ¿Está el cursor pasando por encima de algo entre estos frames? Útil para estados hover. */
export const isBetween = (frame: number, from?: number, to?: number) =>
  from !== undefined && frame >= from && (to === undefined || frame < to);
