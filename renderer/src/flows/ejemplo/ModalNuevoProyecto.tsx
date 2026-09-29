import { AbsoluteFill, Freeze, useCurrentFrame } from "remotion";
import type { SceneProps } from "../../lib/schema";
import { colors, gap, radius, shadow, type } from "../../tokens";
import { ListadoProyectos } from "./ListadoProyectos";
import { Avatar } from "../../components/Avatar";
import { AnchoredPopover } from "../../components/AnchoredPopover";
import { pressScale, typewriter, typewriterEnd } from "../../components/animation";

type Props = SceneProps<{
  nombre: string;
  typingStartFrame: number;
  openSelectAt: number;
  selectAt: number;
  responsableId: string;
  createPressAt: number;
}>;

const Label: React.FC<{ children: string }> = ({ children }) => (
  <div style={{ ...type.bodyStrong, color: colors.textPrimary, marginBottom: gap.xs }}>{children}</div>
);

const fieldStyle = (focused: boolean): React.CSSProperties => ({
  height: 44,
  borderRadius: radius.md,
  border: `1px solid ${focused ? colors.accent : colors.border}`,
  boxShadow: focused ? `0 0 0 3px ${colors.accentSoft}` : "none",
  padding: `0 ${gap.md}px`,
  display: "flex",
  alignItems: "center",
  gap: gap.sm,
  ...type.body,
  color: colors.textPrimary,
  background: colors.surface,
  boxSizing: "border-box",
});

/**
 * Escena de ejemplo: modal "Nuevo proyecto". Detrás, la pantalla real
 * congelada y atenuada (no un color plano). El modal tiene su tamaño final
 * desde el frame 0. El nombre se ve escribirse, el desplegable se abre bajo
 * su campo y el cursor elige la opción, y el botón no se pulsa hasta que el
 * texto termina de escribirse (docs/reglas-de-video.md).
 */
export const ModalNuevoProyecto: React.FC<Props> = ({
  data,
  nombre,
  typingStartFrame,
  openSelectAt,
  selectAt,
  responsableId,
  createPressAt,
}) => {
  const frame = useCurrentFrame();
  const typed = typewriter(nombre, frame, typingStartFrame);
  const typingDone = frame >= typewriterEnd(nombre, typingStartFrame);
  const chosen = frame >= selectAt ? data.people.find((p) => p.id === responsableId) : undefined;
  const options = data.people.slice(0, 4);
  const canCreate = typed.length > 0 && chosen !== undefined;

  return (
    <AbsoluteFill>
      <Freeze frame={0}>
        <ListadoProyectos data={data} />
      </Freeze>
      <AbsoluteFill style={{ background: colors.overlay, alignItems: "center", justifyContent: "center" }}>
        <div
          style={{
            width: 520,
            background: colors.surface,
            borderRadius: radius.panel,
            boxShadow: shadow.modal,
            padding: gap.xl,
            boxSizing: "border-box",
          }}
        >
          <div style={{ ...type.title, color: colors.textPrimary, marginBottom: gap.xs }}>Nuevo proyecto</div>
          <div style={{ ...type.body, color: colors.textSecondary, marginBottom: gap.xl }}>
            Dale un nombre y asigna a una persona responsable.
          </div>

          <Label>Nombre del proyecto</Label>
          <div style={{ ...fieldStyle(frame >= typingStartFrame && !typingDone), marginBottom: gap.lg }}>
            {typed ? (
              <span>{typed}</span>
            ) : (
              <span style={{ color: colors.textSecondary }}>Ej. Rediseño de la web</span>
            )}
            {frame >= typingStartFrame && !typingDone && (
              <span style={{ width: 1.5, height: 18, background: colors.textPrimary, marginLeft: -6 }} />
            )}
          </div>

          <Label>Responsable</Label>
          <div style={{ display: "block", marginBottom: gap.xl }}>
            <AnchoredPopover
              openAt={openSelectAt}
              closeAt={selectAt}
              width={472}
              trigger={
                <div style={{ ...fieldStyle(frame >= openSelectAt && frame < selectAt), width: 472 }}>
                  {chosen ? (
                    <>
                      <Avatar person={chosen} size={24} />
                      <span>
                        {chosen.firstName} {chosen.lastName}
                      </span>
                    </>
                  ) : (
                    <span style={{ color: colors.textSecondary }}>Elige a alguien del equipo</span>
                  )}
                  <span style={{ flex: 1 }} />
                  <span style={{ color: colors.textSecondary }}>▾</span>
                </div>
              }
            >
              {options.map((p) => (
                <div
                  key={p.id}
                  style={{
                    display: "flex",
                    alignItems: "center",
                    gap: gap.sm,
                    padding: `${gap.sm}px ${gap.md}px`,
                    borderRadius: radius.sm,
                    background: p.id === responsableId && frame >= selectAt - 12 ? colors.accentSoft : "transparent",
                    ...type.body,
                    color: colors.textPrimary,
                    height: 40,
                    boxSizing: "border-box",
                  }}
                >
                  <Avatar person={p} size={24} />
                  <span>
                    {p.firstName} {p.lastName}
                  </span>
                  <span style={{ flex: 1 }} />
                  <span style={{ ...type.caption, color: colors.textSecondary }}>{p.role}</span>
                </div>
              ))}
            </AnchoredPopover>
          </div>

          <div style={{ display: "flex", justifyContent: "flex-end", gap: gap.sm }}>
            <div
              style={{
                ...type.bodyStrong,
                height: 40,
                padding: `0 ${gap.lg}px`,
                borderRadius: radius.md,
                border: `1px solid ${colors.border}`,
                color: colors.textPrimary,
                display: "flex",
                alignItems: "center",
              }}
            >
              Cancelar
            </div>
            <div
              style={{
                ...type.bodyStrong,
                height: 40,
                padding: `0 ${gap.lg}px`,
                borderRadius: radius.md,
                background: colors.accent,
                opacity: canCreate ? 1 : 0.45,
                color: colors.textOnAccent,
                display: "flex",
                alignItems: "center",
                transform: `scale(${pressScale(frame, createPressAt)})`,
              }}
            >
              Crear proyecto
            </div>
          </div>
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
