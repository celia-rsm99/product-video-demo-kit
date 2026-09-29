import { z } from "zod";

/**
 * El contrato del guion. Un vídeo es un JSON (renderer/scripts/<flujo>/<nombre>.json)
 * que cumple este esquema. Contenido (`data`) y escenas (`scenes`) van por
 * separado: hacer otra versión de un vídeo con otros datos ficticios es copiar
 * el JSON y cambiar solo `data` (y el `id`), sin tocar ningún componente.
 */

export const CaptionCue = z.object({
  fromFrame: z.number().int().nonnegative(),
  toFrame: z.number().int().positive(),
  text: z.string(),
});
export type CaptionCue = z.infer<typeof CaptionCue>;

export const CursorPoint = z.object({
  /** Porcentaje del ancho del vídeo: 0 = borde izquierdo, 100 = derecho. */
  x: z.number().min(0).max(100),
  /** Porcentaje del alto del vídeo. */
  y: z.number().min(0).max(100),
  /** Frame (local a la escena) en el que el cursor llega a este punto. */
  frame: z.number().int().nonnegative(),
});
export type CursorPoint = z.infer<typeof CursorPoint>;

export const CursorScript = z.object({
  points: z.array(CursorPoint).min(1),
  /** Frames (locales a la escena) en los que el cursor hace clic. */
  clickFrames: z.array(z.number().int().nonnegative()).default([]),
});
export type CursorScript = z.infer<typeof CursorScript>;

export const Person = z.object({
  id: z.string(),
  firstName: z.string(),
  lastName: z.string(),
  role: z.string().optional(),
  company: z.string().optional(),
  location: z.string().optional(),
  /** Ruta dentro de renderer/public/ (p. ej. "personas/ana-lopez.jpg"). Sin foto se dibujan iniciales. */
  avatarUrl: z.string().optional(),
});
export type Person = z.infer<typeof Person>;

export const Company = z.object({
  id: z.string(),
  name: z.string(),
  /** Ruta dentro de renderer/public/. Sin logo se dibuja un monograma de color. */
  logoUrl: z.string().optional(),
});
export type Company = z.infer<typeof Company>;

export const Scene = z.object({
  id: z.string().regex(/^[A-Za-z0-9-]+$/, "solo letras, números y guiones"),
  /** Nombre registrado en src/lib/componentRegistry.ts, p. ej. "ejemplo/ListadoProyectos". */
  component: z.string(),
  durationInFrames: z.number().int().positive(),
  captions: z.array(CaptionCue).default([]),
  cursor: CursorScript.optional(),
  /** Props propias de la escena (textos, timings, qué fila se pulsa...). */
  props: z.record(z.string(), z.any()).default({}),
});
export type Scene = z.infer<typeof Scene>;

export const VideoScript = z.object({
  id: z.string().regex(/^[A-Za-z0-9-]+$/, "solo letras, números y guiones (Remotion lo usa como id de composición)"),
  /** Carpeta del flujo en renderer/src/flows/ y renderer/scripts/. */
  flow: z.string(),
  title: z.string().optional(),
  fps: z.number().int().positive().default(30),
  width: z.number().int().positive().default(1440),
  height: z.number().int().positive().default(800),
  captionStyle: z
    .object({ burnIn: z.boolean().default(false) })
    .default({ burnIn: false }),
  /** Datos ficticios que usan las escenas. Nunca personas o empresas reales. */
  data: z.object({
    user: Person,
    people: z.array(Person).default([]),
    companies: z.array(Company).default([]),
    /** Cualquier otro dato ficticio propio de tu producto (proyectos, facturas, tareas...). */
    extra: z.record(z.string(), z.any()).default({}),
  }),
  scenes: z.array(Scene).min(1),
});
export type VideoScript = z.infer<typeof VideoScript>;

/** Lo que recibe cada componente de escena. */
export type SceneProps<P = Record<string, unknown>> = P & {
  data: VideoScript["data"];
  cursor?: CursorScript;
};

export const totalDuration = (script: VideoScript) =>
  script.scenes.reduce((sum, s) => sum + s.durationInFrames, 0);
