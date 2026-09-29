import type { CSSProperties, ReactNode } from "react";
import { useCurrentFrame } from "remotion";
import { fadeIn, slideUp } from "./animation";

/**
 * Aparece en `at`. Antes de `at` NO ocupa espacio (no se monta): úsalo para
 * elementos que de verdad no existen todavía, p. ej. un mensaje nuevo en un chat.
 */
export const Reveal: React.FC<{ at: number; children: ReactNode; style?: CSSProperties }> = ({
  at,
  children,
  style,
}) => {
  const frame = useCurrentFrame();
  if (frame < at) return null;
  return (
    <div style={{ opacity: fadeIn(frame, at), transform: `translateY(${slideUp(frame, at)}px)`, ...style }}>
      {children}
    </div>
  );
};

/**
 * Aparece en `at` pero reserva su hueco desde el frame 0. Úsalo dentro de
 * modales, tarjetas o cualquier caja de tamaño fijo: si los elementos se
 * montaran de uno en uno, la caja crecería a saltos (docs/reglas-de-video.md).
 */
export const FadeInPlace: React.FC<{ at: number; children: ReactNode; style?: CSSProperties }> = ({
  at,
  children,
  style,
}) => {
  const frame = useCurrentFrame();
  return <div style={{ opacity: fadeIn(frame, at), ...style }}>{children}</div>;
};
