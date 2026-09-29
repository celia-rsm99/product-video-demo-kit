import { loadFont } from "@remotion/google-fonts/Inter";
import tokens from "./tokens.json";

/**
 * Carga la fuente del producto antes de capturar cada frame, para que ningún
 * frame salga con una fuente de sustitución.
 *
 * Para cambiarla (fase 5): cambia "Inter" en la línea del import por la fuente
 * de tu producto tal como la nombra @remotion/google-fonts (p. ej. "DMSans",
 * "Roboto", "Poppins") y actualiza `font.family` en tokens.json. Si tu fuente
 * no está en Google Fonts, ver docs/solucion-de-problemas.md.
 */
const { fontFamily: loadedFamily } = loadFont("normal", {
  weights: tokens.font.weights as ("400" | "500" | "600" | "700")[],
  subsets: ["latin"],
});

export const fontFamily = loadedFamily;
