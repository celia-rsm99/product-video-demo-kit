import type { ReactNode } from "react";
import { colors, gap, radius, type } from "../../tokens";
import { Avatar } from "../../components/Avatar";
import { truncate } from "../../components/text";
import type { Person } from "../../lib/schema";

const NAV = ["Inicio", "Proyectos", "Equipo", "Informes", "Ajustes"];

/**
 * Marco de la app de ejemplo: barra lateral + zona de contenido. En tu
 * producto, este componente se sustituye por el chrome real (fase 6). Aunque
 * esté siempre en pantalla y nunca sea el foco, lleva la misma fidelidad que
 * el resto: foto del usuario, nombres coherentes con el tema del vídeo.
 */
export const AppShell: React.FC<{ user: Person; active: string; children: ReactNode }> = ({
  user,
  active,
  children,
}) => {
  return (
    <div style={{ display: "flex", width: "100%", height: "100%", background: colors.canvas }}>
      <div
        style={{
          width: 232,
          flex: "0 0 232px",
          background: colors.sidebarBg,
          borderRight: `1px solid ${colors.border}`,
          display: "flex",
          flexDirection: "column",
          padding: gap.lg,
          boxSizing: "border-box",
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: gap.sm, padding: `${gap.xs}px ${gap.sm}px`, marginBottom: gap.xl }}>
          <div style={{ width: 28, height: 28, borderRadius: radius.md, background: colors.accent }} />
          <div style={{ ...type.heading, color: colors.textPrimary }}>Proyecta</div>
        </div>
        {NAV.map((item) => {
          const isActive = item === active;
          return (
            <div
              key={item}
              style={{
                ...(isActive ? type.bodyStrong : type.body),
                color: isActive ? colors.accent : colors.textSecondary,
                background: isActive ? colors.sidebarItemActiveBg : "transparent",
                borderRadius: radius.md,
                padding: `${gap.sm}px ${gap.md}px`,
                marginBottom: 2,
              }}
            >
              {item}
            </div>
          );
        })}
        <div style={{ flex: 1 }} />
        <div style={{ display: "flex", alignItems: "center", gap: gap.sm, padding: gap.sm, minWidth: 0 }}>
          <Avatar person={user} size={32} />
          <div style={{ minWidth: 0, flex: 1, display: "flex", flexDirection: "column" }}>
            <span style={{ ...type.bodyStrong, color: colors.textPrimary, ...truncate }}>
              {user.firstName} {user.lastName}
            </span>
            <span style={{ ...type.caption, color: colors.textSecondary, ...truncate }}>{user.company}</span>
          </div>
        </div>
      </div>
      <div style={{ flex: 1, minWidth: 0, padding: gap.xl, boxSizing: "border-box", display: "flex", flexDirection: "column" }}>
        {children}
      </div>
    </div>
  );
};
