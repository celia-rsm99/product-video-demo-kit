import { interpolate, useCurrentFrame } from "remotion";
import type { SceneProps } from "../../lib/schema";
import { colors, gap, radius, shadow, type } from "../../tokens";
import { AppShell } from "./AppShell";
import { Avatar } from "../../components/Avatar";
import { LogoBadge } from "../../components/LogoBadge";
import { truncate } from "../../components/text";
import { pressScale } from "../../components/animation";

export type Proyecto = {
  id: string;
  nombre: string;
  responsableId: string;
  empresaId: string;
  estado: "En curso" | "En riesgo" | "Completado";
  entrega: string;
};

type Props = SceneProps<{
  /** Frame en el que se pulsa "Nuevo proyecto" (el cursor hace clic ahí). */
  pressNewAt?: number;
  /** Proyecto recién creado: aparece arriba del todo, resaltado. */
  proyectoNuevo?: Proyecto;
  /** Frame a partir del cual el resaltado del proyecto nuevo se desvanece. */
  resaltadoHasta?: number;
}>;

const ESTADO: Record<Proyecto["estado"], { bg: string; fg: string }> = {
  "En curso": { bg: colors.accentSoft, fg: colors.accent },
  "En riesgo": { bg: colors.warningSoft, fg: colors.warning },
  Completado: { bg: colors.successSoft, fg: colors.success },
};

const COLS = "2.2fr 1.6fr 1.4fr 1fr 0.9fr";

/**
 * Escena de ejemplo: listado de proyectos. Todo el contenido viene de
 * `data` (guion JSON), nada escrito dentro del componente. La tabla tiene
 * filas suficientes para llenar la pantalla (docs/reglas-de-video.md).
 */
export const ListadoProyectos: React.FC<Props> = ({ data, pressNewAt, proyectoNuevo, resaltadoHasta = 60 }) => {
  const frame = useCurrentFrame();
  const base = (data.extra.proyectos ?? []) as Proyecto[];
  const rows = proyectoNuevo ? [proyectoNuevo, ...base] : base;
  const person = (id: string) => data.people.find((p) => p.id === id) ?? data.user;
  const company = (id: string) => data.companies.find((c) => c.id === id) ?? { id, name: "?" };
  const highlight = interpolate(frame, [resaltadoHasta - 20, resaltadoHasta], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AppShell user={data.user} active="Proyectos">
      <div style={{ display: "flex", alignItems: "center", marginBottom: gap.lg }}>
        <div style={{ flex: 1 }}>
          <div style={{ ...type.title, color: colors.textPrimary }}>Proyectos</div>
          <div style={{ ...type.body, color: colors.textSecondary }}>{rows.length} proyectos activos</div>
        </div>
        <div
          style={{
            ...type.bodyStrong,
            background: colors.accent,
            color: colors.textOnAccent,
            borderRadius: radius.md,
            height: 40,
            padding: `0 ${gap.lg}px`,
            display: "flex",
            alignItems: "center",
            transform: `scale(${pressScale(frame, pressNewAt)})`,
          }}
        >
          + Nuevo proyecto
        </div>
      </div>
      <div
        style={{
          flex: 1,
          minHeight: 0,
          background: colors.surface,
          border: `1px solid ${colors.border}`,
          borderRadius: radius.lg,
          boxShadow: shadow.card,
          overflow: "hidden",
        }}
      >
        <div
          style={{
            display: "grid",
            gridTemplateColumns: COLS,
            ...type.caption,
            fontWeight: 600,
            color: colors.textSecondary,
            background: colors.surfaceMuted,
            borderBottom: `1px solid ${colors.border}`,
            height: 44,
            alignItems: "center",
            padding: `0 ${gap.lg}px`,
          }}
        >
          <span>Proyecto</span>
          <span>Responsable</span>
          <span>Cliente</span>
          <span>Estado</span>
          <span>Entrega</span>
        </div>
        {rows.map((p, i) => {
          const owner = person(p.responsableId);
          const client = company(p.empresaId);
          const isNew = proyectoNuevo !== undefined && i === 0;
          return (
            <div
              key={p.id}
              style={{
                display: "grid",
                gridTemplateColumns: COLS,
                alignItems: "center",
                height: 56,
                padding: `0 ${gap.lg}px`,
                borderBottom: `1px solid ${colors.border}`,
                background: isNew ? `rgba(79, 70, 229, ${0.08 * highlight})` : "transparent",
                ...type.body,
                color: colors.textPrimary,
              }}
            >
              <span style={{ ...type.bodyStrong, ...truncate, paddingRight: gap.md }}>{p.nombre}</span>
              <div style={{ display: "flex", alignItems: "center", gap: gap.sm, minWidth: 0 }}>
                <Avatar person={owner} size={28} />
                <span style={truncate}>
                  {owner.firstName} {owner.lastName}
                </span>
              </div>
              <div style={{ display: "flex", alignItems: "center", gap: gap.sm, minWidth: 0 }}>
                <LogoBadge company={client} size={24} />
                <span style={truncate}>{client.name}</span>
              </div>
              <div>
                <span
                  style={{
                    ...type.caption,
                    fontWeight: 600,
                    background: ESTADO[p.estado].bg,
                    color: ESTADO[p.estado].fg,
                    borderRadius: radius.circular,
                    padding: "3px 10px",
                  }}
                >
                  {p.estado}
                </span>
              </div>
              <span style={{ color: colors.textSecondary }}>{p.entrega}</span>
            </div>
          );
        })}
      </div>
    </AppShell>
  );
};
