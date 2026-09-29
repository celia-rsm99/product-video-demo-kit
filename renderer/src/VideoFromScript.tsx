import { AbsoluteFill, Series } from "remotion";
import type { Scene, VideoScript } from "./lib/schema";
import { componentRegistry } from "./lib/componentRegistry";
import { Cursor } from "./components/Cursor";
import { CaptionOverlay } from "./components/CaptionOverlay";
import { colors, fontFamily } from "./tokens";

/** Dibuja una escena del guion con su componente registrado, su cursor y sus subtítulos. */
export const SceneFromScript: React.FC<{ scene: Scene; data: VideoScript["data"]; burnIn: boolean }> = ({
  scene,
  data,
  burnIn,
}) => {
  const Component = componentRegistry[scene.component];
  return (
    <AbsoluteFill style={{ background: colors.canvas, fontFamily }}>
      {Component ? (
        <Component {...scene.props} data={data} cursor={scene.cursor} />
      ) : (
        <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", background: "#FEECEB" }}>
          <div style={{ fontSize: 28, color: "#B42318", fontFamily }}>
            Componente "{scene.component}" no registrado en componentRegistry.ts
          </div>
        </AbsoluteFill>
      )}
      <Cursor script={scene.cursor} />
      {burnIn && <CaptionOverlay cues={scene.captions} />}
    </AbsoluteFill>
  );
};

/**
 * Un vídeo completo: las escenas del guion una detrás de otra, con corte seco.
 * Sin fundidos entre escenas a propósito (docs/reglas-de-video.md): un corte
 * con el cursor en su sitio se lee como la misma pantalla que sigue.
 */
export const VideoFromScript: React.FC<{ script: VideoScript }> = ({ script }) => {
  return (
    <AbsoluteFill style={{ background: colors.canvas }}>
      <Series>
        {script.scenes.map((scene) => (
          <Series.Sequence key={scene.id} durationInFrames={scene.durationInFrames} name={scene.id}>
            <SceneFromScript scene={scene} data={script.data} burnIn={script.captionStyle.burnIn} />
          </Series.Sequence>
        ))}
      </Series>
    </AbsoluteFill>
  );
};
