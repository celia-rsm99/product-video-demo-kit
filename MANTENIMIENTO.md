# Mantenimiento del kit

Notas para quien mantiene este repositorio. Si solo quieres usar el kit, lee el [README](README.md).

## De dónde sale

El método se desarrolló en un proyecto privado que hace vídeos demo de un producto real. Este kit es ese método **reescrito desde cero** para que sirva con cualquier producto. No contiene nada de aquel proyecto: ni pantallas, ni escenas, ni datos, ni marcas.

Las mejoras siguen llegando desde allí, pero **solo como aprendizajes genéricos, reescritos**, nunca como archivos copiados:

- una corrección de vídeo que valga para cualquier producto → regla nueva en `docs/reglas-de-video.md` (numerada y añadida al checklist);
- un truco de proceso (Remotion, ffmpeg, límites de Figma) → la fase correspondiente o `docs/solucion-de-problemas.md`;
- un ayudante de animación genérico → `renderer/src/components/`, con los tokens del kit, usado en el flujo de ejemplo si encaja.

## Piezas y dónde tocar

| Para cambiar… | Toca… |
|---|---|
| El proceso que sigue Claude | `fases/` (una por fase) y `CLAUDE.md` |
| Las reglas de calidad | `docs/reglas-de-video.md` |
| Lo que ve una persona al llegar | `README.md` (y `docs/img/demo-ejemplo.gif`) |
| Los comandos `/empezar`, `/feedback`… | `.claude/commands/` |
| Los permisos por defecto | `.claude/settings.json` |
| El esquema del guion | `renderer/src/lib/schema.ts` y el validador `validate-cli.ts` |
| Piezas reutilizables (cursor, animaciones…) | `renderer/src/components/` |
| El vídeo de ejemplo | `renderer/src/flows/ejemplo/` y `renderer/scripts/ejemplo/demo-ejemplo.json` |
| Herramientas | `tools/` (todas imprimen un único JSON con `ok`) |

Cada escena nueva se registra en **dos** sitios: `renderer/src/lib/componentRegistry.ts` y `registeredNames.ts` (`Root.tsx` falla si no coinciden).

## Comprobaciones antes de publicar un cambio

```bash
cd renderer && npx tsc --noEmit && cd ..
python3 tools/validate_script.py renderer/scripts/ejemplo/demo-ejemplo.json
python3 tools/list_compositions.py
python3 tools/render_video.py --composition demo-ejemplo --output .tmp/renders/ejemplo/demo-ejemplo.mp4
python3 tools/probe_video.py .tmp/renders/ejemplo/demo-ejemplo.mp4   # ≈12 s, 1440×800, sin audio
python3 tools/build_gallery.py
```

Si el cambio toca el ejemplo, vuelve a medir los clics con `tools/render_still.py` en cada frame de clic (regla 18) y regenera el GIF del README.

Antes del push, repasa el diff completo: el repo es público y lo que se sube puede quedar copiado aunque se borre después. Busca nombres de personas, empresas o productos reales, rutas de tu ordenador, claves y capturas que no sean del ejemplo ficticio.

## Pendiente y gotchas conocidos

- **Sin probar todavía:** la descarga con token contra un archivo real de Figma (`figma_inventory.py --dry-run` gasta 1 llamada y lo confirma) y la instalación en Windows.
- El ffmpeg que trae Remotion no incluye los filtros `fps`, `setpts` ni `select`: se usa `-r N` y `-itsscale` (ya aplicado en `speed_variant.py` y en las fases).
- `remotion.config.ts` lleva `Config.setMuted(true)`: los vídeos salen sin pista de audio.
- Licencia: el kit es MIT, pero Remotion exige licencia de empresa a organizaciones de más de 3 personas (lo avisa el README).
