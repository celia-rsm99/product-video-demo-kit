import { Img, staticFile } from "remotion";
import type { Company } from "../lib/schema";
import { colors, fontFamily, radius } from "../tokens";
import { colorFor } from "./Avatar";

/**
 * Logo de una empresa ficticia: su imagen si la tiene, o un monograma con la
 * inicial sobre un color derivado del nombre. Nunca el logo de una empresa real.
 */
export const LogoBadge: React.FC<{ company: Company; size?: number }> = ({ company, size = 32 }) => {
  const style = { width: size, height: size, borderRadius: radius.md, flex: `0 0 ${size}px`, overflow: "hidden" } as const;
  if (company.logoUrl) {
    return <Img src={staticFile(company.logoUrl)} style={{ ...style, objectFit: "cover" }} />;
  }
  return (
    <div
      style={{
        ...style,
        background: colorFor(company.name),
        color: colors.textOnAccent,
        fontFamily,
        fontWeight: 700,
        fontSize: size * 0.45,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      {company.name[0]?.toUpperCase()}
    </div>
  );
};
