/**
 * Lista de nombres de componentes de escena. Tiene que coincidir con las claves
 * de componentRegistry.ts (Root.tsx avisa si no). Está aparte para que el
 * validador de guiones pueda leerla sin cargar React ni Remotion.
 */
export const registeredComponentNames: string[] = [
  "ejemplo/ListadoProyectos",
  "ejemplo/ModalNuevoProyecto",
];
