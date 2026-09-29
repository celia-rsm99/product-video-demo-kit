import { Img, staticFile } from "remotion";
import type { Person } from "../lib/schema";
import { colors, fontFamily } from "../tokens";

const PALETTE = ["#F97066", "#F79009", "#12B76A", "#2E90FA", "#7A5AF8", "#EE46BC", "#15B79E", "#6172F3"];

/** Color estable a partir de un texto: la misma persona siempre sale del mismo color. */
export const colorFor = (seed: string) => {
  let h = 0;
  for (let i = 0; i < seed.length; i++) h = (h * 31 + seed.charCodeAt(i)) >>> 0;
  return PALETTE[h % PALETTE.length];
};

/**
 * Foto de una persona ficticia, o sus iniciales sobre un color si no hay foto.
 * Las fotos van en renderer/public/ (ver docs/datos-ficticios.md).
 */
export const Avatar: React.FC<{ person: Person; size?: number }> = ({ person, size = 32 }) => {
  const style = {
    width: size,
    height: size,
    borderRadius: "50%",
    flex: `0 0 ${size}px`,
    overflow: "hidden",
  } as const;
  if (person.avatarUrl) {
    return <Img src={staticFile(person.avatarUrl)} style={{ ...style, objectFit: "cover" }} />;
  }
  const initials = `${person.firstName[0] ?? ""}${person.lastName[0] ?? ""}`.toUpperCase();
  return (
    <div
      style={{
        ...style,
        background: colorFor(person.id),
        color: colors.textOnAccent,
        fontFamily,
        fontWeight: 600,
        fontSize: size * 0.38,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      {initials}
    </div>
  );
};
