import type { CSSProperties } from "react";

/**
 * Recorta con "…" un texto de longitud variable en una sola línea. Poner en el
 * nodo de texto; su celda o contenedor flex necesita además `minWidth: 0`
 * (sin eso, un valor largo ensancha la columna y desalinea la fila).
 */
export const truncate: CSSProperties = {
  flex: 1,
  minWidth: 0,
  overflow: "hidden",
  textOverflow: "ellipsis",
  whiteSpace: "nowrap",
};
