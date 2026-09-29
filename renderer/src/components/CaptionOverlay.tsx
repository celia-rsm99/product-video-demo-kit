import { interpolate, useCurrentFrame } from "remotion";
import type { CaptionCue } from "../lib/schema";
import { fontFamily } from "../tokens";

/**
 * Subtítulos quemados en la parte baja del vídeo. Desactivados por defecto
 * (captionStyle.burnIn = false en el guion). Los frames de cada subtítulo son
 * locales a su escena.
 */
export const CaptionOverlay: React.FC<{
  cues: CaptionCue[];
  /** Para formatos verticales: margen inferior como fracción de la altura. */
  bottomFraction?: number;
}> = ({ cues, bottomFraction }) => {
  const frame = useCurrentFrame();
  const active = cues.find((c) => frame >= c.fromFrame && frame < c.toFrame);
  if (!active) return null;
  const opacity = interpolate(frame - active.fromFrame, [0, 6], [0, 1], { extrapolateRight: "clamp" });

  return (
    <div
      style={{
        position: "absolute",
        left: 0,
        right: 0,
        bottom: bottomFraction !== undefined ? `${bottomFraction * 100}%` : 28,
        display: "flex",
        justifyContent: "center",
        pointerEvents: "none",
        zIndex: 900,
      }}
    >
      <div
        style={{
          opacity,
          maxWidth: "70%",
          padding: "8px 16px",
          borderRadius: 8,
          background: "rgba(10, 15, 20, 0.82)",
          color: "#FFFFFF",
          fontFamily,
          fontSize: 18,
          fontWeight: 500,
          lineHeight: "24px",
          textAlign: "center",
        }}
      >
        {active.text}
      </div>
    </div>
  );
};
