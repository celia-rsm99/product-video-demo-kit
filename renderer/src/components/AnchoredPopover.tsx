import type { CSSProperties, ReactNode } from "react";
import { useCurrentFrame } from "remotion";
import { fadeIn, slideUp } from "./animation";
import { colors, radius, shadow } from "../tokens";

/**
 * Desplegable, menú o popover anclado a su botón con CSS. Nunca se coloca con
 * coordenadas de la escena medidas a mano: si el botón se mueve, el menú se
 * mueve con él (docs/reglas-de-video.md).
 *
 * Uso: <AnchoredPopover trigger={<Boton/>} openAt={40} closeAt={90}>opciones</AnchoredPopover>
 */
export const AnchoredPopover: React.FC<{
  trigger: ReactNode;
  children: ReactNode;
  openAt?: number;
  closeAt?: number;
  align?: "left" | "right";
  width?: number;
  style?: CSSProperties;
}> = ({ trigger, children, openAt, closeAt, align = "left", width = 220, style }) => {
  const frame = useCurrentFrame();
  const open = openAt !== undefined && frame >= openAt && (closeAt === undefined || frame < closeAt);
  return (
    <div style={{ position: "relative", display: "inline-block" }}>
      {trigger}
      {open && (
        <div
          style={{
            position: "absolute",
            top: "calc(100% + 6px)",
            [align]: 0,
            width,
            background: colors.surface,
            border: `1px solid ${colors.border}`,
            borderRadius: radius.md,
            boxShadow: shadow.modal,
            padding: 4,
            zIndex: 50,
            opacity: fadeIn(frame, openAt!, 5),
            transform: `translateY(${slideUp(frame, openAt!, 5, -4)}px)`,
            ...style,
          }}
        >
          {children}
        </div>
      )}
    </div>
  );
};
