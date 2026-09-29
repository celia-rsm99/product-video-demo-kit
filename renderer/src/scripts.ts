import { VideoScript } from "./lib/schema";
import demoEjemplo from "../scripts/ejemplo/demo-ejemplo.json";

/**
 * Guiones que aparecen como vídeos en Remotion Studio. Cada guion nuevo
 * (renderer/scripts/<flujo>/<nombre>.json) se importa y se añade a esta lista.
 * Si un guion no cumple el esquema, Studio muestra el error al abrir.
 */
export const scripts: VideoScript[] = [VideoScript.parse(demoEjemplo)];
