import { Composition, Folder } from "remotion";
import { scripts } from "./scripts";
import { SceneFromScript, VideoFromScript } from "./VideoFromScript";
import { totalDuration } from "./lib/schema";
import { componentRegistry } from "./lib/componentRegistry";
import { registeredComponentNames } from "./lib/registeredNames";

const registryKeys = Object.keys(componentRegistry).sort().join(",");
if (registryKeys !== [...registeredComponentNames].sort().join(",")) {
  throw new Error(
    "componentRegistry.ts y registeredNames.ts no tienen los mismos nombres de escena. Añade la escena nueva en los dos.",
  );
}

/**
 * Registra en Remotion, por cada guion de src/scripts.ts:
 *  - "<id-del-guion>": el vídeo completo.
 *  - "<id-del-guion>--<id-de-escena>": cada escena suelta, con los frames
 *    empezando en 0. Es la que se usa para comprobar una escena con
 *    tools/render_still.py sin tener que calcular en qué frame del vídeo cae.
 */
export const RemotionRoot: React.FC = () => {
  return (
    <>
      {scripts.map((script) => (
        <Folder key={script.id} name={script.id}>
          <Composition
            id={script.id}
            component={VideoFromScript}
            durationInFrames={totalDuration(script)}
            fps={script.fps}
            width={script.width}
            height={script.height}
            defaultProps={{ script }}
          />
          {script.scenes.map((scene) => (
            <Composition
              key={scene.id}
              id={`${script.id}--${scene.id}`}
              component={SceneFromScript}
              durationInFrames={scene.durationInFrames}
              fps={script.fps}
              width={script.width}
              height={script.height}
              defaultProps={{ scene, data: script.data, burnIn: script.captionStyle.burnIn }}
            />
          ))}
        </Folder>
      ))}
    </>
  );
};
