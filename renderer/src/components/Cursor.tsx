import { Easing, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import type { CursorScript } from "../lib/schema";
import { colors } from "../tokens";

/** Frames máximos que tarda un desplazamiento; si hay más margen, el cursor espera quieto y luego se mueve. */
const MAX_TRAVEL_FRAMES = 30;
const PRESS_DOWN = 3;
const PRESS_UP = 6;
const RIPPLE_FRAMES = 16;

const ease = Easing.bezier(0.45, 0, 0.2, 1);

const positionAt = (points: CursorScript["points"], frame: number) => {
  if (frame <= points[0].frame) return points[0];
  for (let i = 1; i < points.length; i++) {
    const from = points[i - 1];
    const to = points[i];
    if (frame < to.frame) {
      const start = Math.max(from.frame, to.frame - MAX_TRAVEL_FRAMES);
      const t = interpolate(frame, [start, to.frame], [0, 1], {
        extrapolateLeft: "clamp",
        extrapolateRight: "clamp",
        easing: ease,
      });
      return { x: from.x + (to.x - from.x) * t, y: from.y + (to.y - from.y) * t };
    }
  }
  return points[points.length - 1];
};

/**
 * Cursor simulado. Sin etiqueta de texto al lado a propósito (docs/reglas-de-video.md):
 * se ve el ratón, no un subtítulo que lo persigue.
 *
 * Se monta encima de la escena. Coordenadas en porcentaje del vídeo, frames
 * locales a la escena. Para medir un objetivo de clic: render_still.py en ese
 * frame y leer la posición en la imagen, nunca calcularla de cabeza.
 */
export const Cursor: React.FC<{ script?: CursorScript }> = ({ script }) => {
  const frame = useCurrentFrame();
  const { width, height } = useVideoConfig();
  if (!script || script.points.length === 0) return null;

  const pos = positionAt(script.points, frame);
  const x = (pos.x / 100) * width;
  const y = (pos.y / 100) * height;

  const activeClick = script.clickFrames.find((c) => frame >= c && frame < c + RIPPLE_FRAMES);
  let scale = 1;
  let rippleOpacity = 0;
  let rippleSize = 0;
  if (activeClick !== undefined) {
    const local = frame - activeClick;
    scale =
      local < PRESS_DOWN
        ? interpolate(local, [0, PRESS_DOWN], [1, 0.82])
        : interpolate(local, [PRESS_DOWN, PRESS_DOWN + PRESS_UP], [0.82, 1], { extrapolateRight: "clamp" });
    rippleOpacity = interpolate(local, [0, RIPPLE_FRAMES], [0.45, 0]);
    rippleSize = interpolate(local, [0, RIPPLE_FRAMES], [10, 46]);
  }

  return (
    <div style={{ position: "absolute", inset: 0, pointerEvents: "none", zIndex: 1000 }}>
      {rippleOpacity > 0 && (
        <div
          style={{
            position: "absolute",
            left: x - rippleSize / 2,
            top: y - rippleSize / 2,
            width: rippleSize,
            height: rippleSize,
            borderRadius: "50%",
            background: colors.cursorAccent,
            opacity: rippleOpacity,
          }}
        />
      )}
      <svg
        width={26}
        height={26}
        viewBox="0 0 24 24"
        style={{
          position: "absolute",
          left: x - 3,
          top: y - 2,
          transform: `scale(${scale})`,
          transformOrigin: "3px 2px",
          filter: "drop-shadow(0px 2px 3px rgba(0,0,0,0.35))",
        }}
      >
        <path
          d="M4 2.5 L4 19.5 L8.6 15.3 L11.6 22 L14.6 20.7 L11.7 14.1 L18 14.1 Z"
          fill="#111111"
          stroke="#FFFFFF"
          strokeWidth={1.6}
          strokeLinejoin="round"
        />
      </svg>
    </div>
  );
};
