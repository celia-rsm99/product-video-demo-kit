import type React from "react";
import { ListadoProyectos } from "../flows/ejemplo/ListadoProyectos";
import { ModalNuevoProyecto } from "../flows/ejemplo/ModalNuevoProyecto";

/**
 * Traduce el nombre que aparece en un guion JSON (`scene.component`) al
 * componente de React que lo dibuja. Cada escena nueva se añade aquí y en
 * registeredNames.ts.
 *
 * Convención de nombre: "<flujo>/<NombreDeLaEscena>".
 */
// eslint-disable-next-line @typescript-eslint/no-explicit-any
export const componentRegistry: Record<string, React.FC<any>> = {
  "ejemplo/ListadoProyectos": ListadoProyectos,
  "ejemplo/ModalNuevoProyecto": ModalNuevoProyecto,
};
