#!/usr/bin/env python3
"""Genera referencia/galeria.html: una página para ver el producto de un vistazo.

Pestañas:
  - Flujos: cada flujo de referencia/flujos.json como una tira de pantallas en orden (fase 4).
  - Todas las pantallas: todo lo descargado, agrupado por sección de Figma, con buscador.
  - Sistema visual: colores, tipografía, radios y espaciados de renderer/src/tokens/tokens.json (fase 5).

Uso:
  python3 tools/build_gallery.py [--open]

Se abre con doble clic (es un archivo local, no se publica en ningún sitio).
"""
import argparse
import html
import json
import webbrowser

from _common import INVENTARIO, REFERENCIA_DIR, RENDERER_DIR, emit, rel

FLUJOS = REFERENCIA_DIR / "flujos.json"
TOKENS = RENDERER_DIR / "src" / "tokens" / "tokens.json"
OUT = REFERENCIA_DIR / "galeria.html"


def img_src(local_path: str) -> str:
    # Las rutas del inventario son relativas a la raíz; la galería vive en referencia/.
    return local_path[len("referencia/"):] if local_path.startswith("referencia/") else "../" + local_path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--open", action="store_true")
    args = parser.parse_args()

    inv = json.loads(INVENTARIO.read_text(encoding="utf-8")) if INVENTARIO.exists() else {"sections": []}
    screens_by_id = {}
    sections = []
    for sec in inv["sections"]:
        items = []
        for sc in sec["screens"]:
            entry = {"id": sc["id"], "name": sc["name"], "status": sc["status"],
                     "src": img_src(sc["local_path"]) if sc.get("local_path") else None, "section": sec["name"]}
            screens_by_id[sc["id"]] = entry
            items.append(entry)
        sections.append({"name": sec["name"], "page": sec.get("page"), "screens": items})

    flows = []
    if FLUJOS.exists():
        for f in json.loads(FLUJOS.read_text(encoding="utf-8")).get("flujos", []):
            steps = []
            for step in f.get("pantallas", []):
                sid = step if isinstance(step, str) else step.get("id")
                note = "" if isinstance(step, str) else step.get("nota", "")
                sc = screens_by_id.get(sid, {"id": sid, "name": "(no está en el inventario)", "src": None})
                steps.append({**sc, "note": note})
            flows.append({"slug": f.get("slug"), "name": f.get("nombre"), "description": f.get("descripcion", ""),
                          "steps": steps})

    tokens = json.loads(TOKENS.read_text(encoding="utf-8")) if TOKENS.exists() else {}
    payload = json.dumps({"fileName": inv.get("file_name"), "flows": flows, "sections": sections, "tokens": tokens},
                         ensure_ascii=False).replace("</", "<\\/")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(TEMPLATE.replace("__DATA__", payload).replace("__TITLE__", html.escape(inv.get("file_name") or "Mi producto")), encoding="utf-8")

    if args.open:
        webbrowser.open(OUT.resolve().as_uri())
    emit({"ok": True, "gallery": rel(OUT), "flows": len(flows), "sections": len(sections),
          "screens": len(screens_by_id), "has_tokens": bool(tokens)})


TEMPLATE = r"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Galería · __TITLE__</title>
<style>
  :root { --bg:#f6f7f9; --card:#fff; --text:#101828; --muted:#667085; --line:#e4e7ec; --accent:#4f46e5; }
  @media (prefers-color-scheme: dark) { :root { --bg:#0f1115; --card:#181b21; --text:#eef0f3; --muted:#9aa3b2; --line:#2a2f38; --accent:#8b85ff; } }
  * { box-sizing: border-box; }
  body { margin:0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Inter, sans-serif; background:var(--bg); color:var(--text); }
  header { position:sticky; top:0; z-index:5; background:var(--bg); border-bottom:1px solid var(--line); padding:16px 24px 0; }
  h1 { font-size:20px; margin:0 0 12px; }
  nav { display:flex; gap:4px; flex-wrap:wrap; }
  nav button { border:0; background:none; color:var(--muted); font:inherit; font-weight:600; padding:10px 14px; border-bottom:2px solid transparent; cursor:pointer; }
  nav button.on { color:var(--accent); border-color:var(--accent); }
  main { padding:24px; max-width:1600px; margin:0 auto; }
  .empty { color:var(--muted); background:var(--card); border:1px dashed var(--line); border-radius:12px; padding:24px; }
  .flow { background:var(--card); border:1px solid var(--line); border-radius:14px; padding:18px; margin-bottom:20px; }
  .flow h2 { margin:0 0 4px; font-size:17px; } .flow p { margin:0 0 14px; color:var(--muted); font-size:14px; }
  .strip { display:flex; gap:14px; overflow-x:auto; padding-bottom:8px; }
  .step { flex:0 0 280px; } .step .n { font-size:12px; color:var(--accent); font-weight:700; }
  .grid { display:grid; grid-template-columns:repeat(auto-fill, minmax(240px, 1fr)); gap:14px; }
  .shot { background:var(--card); border:1px solid var(--line); border-radius:10px; overflow:hidden; cursor:zoom-in; }
  .shot img, .shot .ph { width:100%; aspect-ratio:16/9; object-fit:cover; object-position:top left; display:block; background:var(--line); }
  .shot .ph { display:flex; align-items:center; justify-content:center; color:var(--muted); font-size:12px; cursor:default; }
  .shot .cap { padding:8px 10px; font-size:12.5px; line-height:1.35; } .shot .cap small { color:var(--muted); display:block; }
  .sec h3 { font-size:15px; margin:28px 0 10px; } .sec h3 span { color:var(--muted); font-weight:400; }
  input[type=search] { width:100%; max-width:420px; padding:10px 12px; border-radius:8px; border:1px solid var(--line); background:var(--card); color:var(--text); font:inherit; margin-bottom:8px; }
  .swatches { display:grid; grid-template-columns:repeat(auto-fill, minmax(170px,1fr)); gap:12px; }
  .sw { background:var(--card); border:1px solid var(--line); border-radius:10px; overflow:hidden; font-size:12.5px; }
  .sw .c { height:64px; border-bottom:1px solid var(--line); } .sw div.t { padding:8px 10px; } .sw code { color:var(--muted); }
  .row { display:flex; align-items:baseline; gap:16px; padding:10px 0; border-bottom:1px solid var(--line); flex-wrap:wrap; }
  .row code { color:var(--muted); font-size:12px; min-width:220px; }
  .note { font-size:13px; color:var(--muted); margin:6px 0 18px; }
  #lb { position:fixed; inset:0; background:rgba(0,0,0,.85); display:none; align-items:center; justify-content:center; z-index:10; padding:24px; cursor:zoom-out; }
  #lb img { max-width:100%; max-height:100%; border-radius:8px; } #lb.on { display:flex; }
</style>
</head>
<body>
<header><h1>__TITLE__</h1><nav id="tabs"></nav></header>
<main id="view"></main>
<div id="lb"><img alt=""></div>
<script>
const D = __DATA__;
const esc = s => String(s ?? "").replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const shot = (s, label) => s.src
  ? `<div class="shot" data-src="${esc(s.src)}"><img loading="lazy" src="${esc(s.src)}" alt=""><div class="cap">${label || ""}${esc(s.name)}<small>${esc(s.id)}${s.note ? " · " + esc(s.note) : ""}</small></div></div>`
  : `<div class="shot"><div class="ph">${s.status === "error" ? "error al descargar" : "pendiente de descargar"}</div><div class="cap">${esc(s.name)}<small>${esc(s.id)}</small></div></div>`;

const views = {
  "Flujos": () => D.flows.length ? D.flows.map(f => `<section class="flow"><h2>${esc(f.name)}</h2><p>${esc(f.description)}</p>
      <div class="strip">${f.steps.map((s, i) => `<div class="step"><div class="n">Paso ${i + 1}</div>${shot(s)}</div>`).join("")}</div></section>`).join("")
    : `<div class="empty">Todavía no hay flujos definidos. Se crean en la fase 4 (referencia/flujos.json).</div>`,
  "Todas las pantallas": () => {
    if (!D.sections.length) return `<div class="empty">Todavía no hay inventario. Se crea en la fase 2.</div>`;
    const total = D.sections.reduce((n, s) => n + s.screens.length, 0);
    return `<input type="search" id="q" placeholder="Buscar entre ${total} pantallas…">` +
      D.sections.map(sec => `<div class="sec"><h3>${esc(sec.name)} <span>· ${sec.screens.length}${sec.page ? " · página " + esc(sec.page) : ""}</span></h3>
        <div class="grid">${sec.screens.map(s => shot(s)).join("")}</div></div>`).join("");
  },
  "Sistema visual": () => {
    const t = D.tokens || {};
    if (!t.colors) return `<div class="empty">No hay tokens todavía.</div>`;
    const placeholder = String(t._nota || "").startsWith("PLANTILLA");
    return (placeholder ? `<p class="note">Estos son los valores de ejemplo del kit. La fase 5 los sustituye por los de tu producto.</p>` : "") +
      `<h3>Colores</h3><div class="swatches">${Object.entries(t.colors).map(([k, v]) => `<div class="sw"><div class="c" style="background:${esc(v)}"></div><div class="t">${esc(k)}<br><code>${esc(v)}</code></div></div>`).join("")}</div>` +
      `<h3>Tipografía · ${esc(t.font?.family)}</h3>${Object.entries(t.type || {}).map(([k, v]) => `<div class="row"><code>${esc(k)} · ${v.fontSize}px / ${esc(v.lineHeight)} · ${v.fontWeight}</code><span style="font-family:'${esc(t.font?.family)}',sans-serif;font-size:${v.fontSize}px;font-weight:${v.fontWeight};line-height:${esc(v.lineHeight)}">El equipo revisa el proyecto</span></div>`).join("")}` +
      `<h3>Radios</h3><div class="swatches">${Object.entries(t.radius || {}).map(([k, v]) => `<div class="sw"><div class="t"><div style="width:100%;height:56px;border:2px solid var(--accent);border-radius:${Math.min(v, 28)}px"></div>${esc(k)} <code>${v}px</code></div></div>`).join("")}</div>` +
      `<h3>Espaciados</h3>${Object.entries(t.gap || {}).map(([k, v]) => `<div class="row"><code>${esc(k)} · ${v}px</code><span style="display:inline-block;height:14px;width:${v * 4}px;background:var(--accent);border-radius:3px"></span></div>`).join("")}`;
  },
};

const tabs = document.getElementById("tabs"), view = document.getElementById("view");
let current = localStorageGet() || (D.flows.length ? "Flujos" : "Todas las pantallas");
function localStorageGet() { try { return localStorage.getItem("galeria-tab"); } catch { return null; } }
function show(name) {
  current = views[name] ? name : "Todas las pantallas";
  try { localStorage.setItem("galeria-tab", current); } catch {}
  tabs.innerHTML = Object.keys(views).map(k => `<button class="${k === current ? "on" : ""}">${k}</button>`).join("");
  view.innerHTML = views[current]();
  const q = document.getElementById("q");
  if (q) q.addEventListener("input", () => {
    const v = q.value.toLowerCase();
    view.querySelectorAll(".sec").forEach(sec => {
      let any = false;
      sec.querySelectorAll(".shot").forEach(el => { const hit = el.textContent.toLowerCase().includes(v); el.style.display = hit ? "" : "none"; any ||= hit; });
      sec.style.display = any ? "" : "none";
    });
  });
}
tabs.addEventListener("click", e => { if (e.target.tagName === "BUTTON") show(e.target.textContent); });
const lb = document.getElementById("lb");
view.addEventListener("click", e => { const s = e.target.closest(".shot[data-src]"); if (s) { lb.querySelector("img").src = s.dataset.src; lb.classList.add("on"); } });
lb.addEventListener("click", () => lb.classList.remove("on"));
show(current);
</script>
</body>
</html>
"""

if __name__ == "__main__":
    main()
