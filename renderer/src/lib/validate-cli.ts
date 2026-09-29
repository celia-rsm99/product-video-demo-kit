import { readFileSync } from "fs";
import { VideoScript } from "./schema";
import { registeredComponentNames } from "./registeredNames";

/**
 * Valida un guion JSON contra el esquema y comprueba reglas que el esquema no
 * puede expresar solo. Imprime un único objeto JSON (lo lee tools/validate_script.py).
 */
const path = process.argv[2];
if (!path) {
  console.log(JSON.stringify({ ok: false, error: "uso: validate-cli.ts <guion.json>" }));
  process.exit(1);
}

try {
  const raw = JSON.parse(readFileSync(path, "utf-8"));
  const script = VideoScript.parse(raw);
  const errors: string[] = [];
  const warnings: string[] = [];

  for (const scene of script.scenes) {
    if (!registeredComponentNames.includes(scene.component)) {
      errors.push(`escena "${scene.id}": el componente "${scene.component}" no está en componentRegistry.ts`);
    }
    for (const c of scene.captions) {
      if (c.toFrame > scene.durationInFrames) {
        errors.push(`escena "${scene.id}": un subtítulo termina en el frame ${c.toFrame}, después del final de la escena (${scene.durationInFrames})`);
      }
    }
    if (scene.cursor) {
      const last = scene.cursor.points[scene.cursor.points.length - 1];
      if (last.frame > scene.durationInFrames) {
        errors.push(`escena "${scene.id}": el cursor llega a su último punto después del final de la escena`);
      }
      for (let i = 1; i < scene.cursor.points.length; i++) {
        if (scene.cursor.points[i].frame <= scene.cursor.points[i - 1].frame) {
          errors.push(`escena "${scene.id}": los puntos del cursor tienen que ir en orden de frame creciente`);
        }
      }
    }
    const text = JSON.stringify(scene.props) + JSON.stringify(scene.captions);
    if (/[–—]/.test(text)) {
      warnings.push(`escena "${scene.id}": hay guiones largos o medios (— –) en el texto; ver docs/reglas-de-video.md`);
    }
  }

  // Continuidad del cursor entre escenas consecutivas (regla de cursor en docs/reglas-de-video.md).
  for (let i = 1; i < script.scenes.length; i++) {
    const prev = script.scenes[i - 1].cursor;
    const next = script.scenes[i].cursor;
    if (prev && next) {
      const a = prev.points[prev.points.length - 1];
      const b = next.points[0];
      if (Math.abs(a.x - b.x) > 0.5 || Math.abs(a.y - b.y) > 0.5) {
        warnings.push(
          `corte "${script.scenes[i - 1].id}" → "${script.scenes[i].id}": el cursor salta de (${a.x}, ${a.y}) a (${b.x}, ${b.y}); la escena nueva debería empezar donde acabó la anterior`,
        );
      }
    }
  }

  if (errors.length) {
    console.log(JSON.stringify({ ok: false, id: script.id, errors, warnings }));
    process.exit(1);
  }
  console.log(JSON.stringify({ ok: true, id: script.id, scenes: script.scenes.length, warnings }));
} catch (err) {
  console.log(JSON.stringify({ ok: false, error: err instanceof Error ? err.message : String(err) }));
  process.exit(1);
}
