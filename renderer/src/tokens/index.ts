import tokens from "./tokens.json";

/**
 * Único punto de entrada a los tokens. Los componentes importan de aquí,
 * nunca escriben un color, tamaño o radio a mano.
 */
export const colors = tokens.colors;
export const type = tokens.type;
export const radius = tokens.radius;
export const gap = tokens.gap;
export const shadow = tokens.shadow;
export const video = tokens.video;
export { fontFamily } from "./fonts";
