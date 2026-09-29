import type { ReactNode } from "react";

export type FocusRect = { x: number; y: number; width: number; height: number };

/**
 * Cámara virtual para sacar formatos vertical (9:16) o cuadrado (1:1) sin
 * rehacer la interfaz: la escena se dibuja una vez a su tamaño nativo
 * (1440×800) y este marco recorta y escala la zona `focusRect` para llenar el
 * formato de salida, como `background-size: cover`.
 */
export const CameraFrame: React.FC<{
  width: number;
  height: number;
  nativeWidth: number;
  nativeHeight: number;
  focusRect: FocusRect;
  children: ReactNode;
}> = ({ width, height, nativeWidth, nativeHeight, focusRect, children }) => {
  const scale = Math.max(width / focusRect.width, height / focusRect.height);
  const tx = width / 2 - (focusRect.x + focusRect.width / 2) * scale;
  const ty = height / 2 - (focusRect.y + focusRect.height / 2) * scale;
  return (
    <div style={{ width, height, overflow: "hidden", position: "relative" }}>
      <div
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          width: nativeWidth,
          height: nativeHeight,
          transform: `translate(${tx}px, ${ty}px) scale(${scale})`,
          transformOrigin: "0 0",
        }}
      >
        {children}
      </div>
    </div>
  );
};
