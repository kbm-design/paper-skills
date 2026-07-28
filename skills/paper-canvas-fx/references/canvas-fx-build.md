# Canvas-fx build — the proven recipe

This is the pipeline validated on the Polydex "Recently Spotlighted" card + Canvas UI **Liquid**. Follow it; the gotchas are load-bearing.

## 1. Frame → plain HTML

```
get_jsx(nodeId, format="inline-styles")   →   assets/jsx2html.py   →   content.html
```

`jsx2html.py` handles what Paper emits: `style={{…}}` objects → `style='…'` (paren/quote-aware split, camelCase→kebab with `-webkit-`/`-moz-`/`-ms-` prefixes), SVG camelCase attrs (`strokeWidth`→`stroke-width`, `fontSize`→`font-size`), and expands self-closing `<div/>`/`<span/>` (HTML has no self-closing non-void tags — leave them and later siblings nest wrongly). Use `style='…'` (single quotes) so inner `font-family: "Geist Mono"` double-quotes don't break the attribute.

## 2. Inline every cross-origin asset (do NOT skip)

Cross-origin images (`app.paper.design/file-assets/…`, any external `url(…)`) **taint the html-in-canvas texture and silently disappear**. Fetch each and swap for a `data:` URI:

```python
import urllib.request, base64, re
html = open('content.html').read()
for u in dict.fromkeys(re.findall(r'url\((https?://[^)]+)\)', html)):
    data = urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent':'Mozilla/5.0'})).read()
    mime = 'image/webp' if u.endswith('.webp') else 'image/png'
    html = html.replace(u, f'data:{mime};base64,{base64.b64encode(data).decode()}')
open('content.html','w').write(html)
```

Verify zero `url(https://…)` remain. (SVG paths and gradients are fine — only raster URLs taint.)

## 3. Pull + compile the Canvas UI component (vanilla flavor)

Components live in a shadcn registry, one entry per framework. The **vanilla** entry is what a standalone page wants:

```bash
curl -s https://canvasui.dev/r/liquid-vanilla.json -o liquid-vanilla.json
# extract files[].content (path e.g. components/canvasui/LiquidVanilla.ts) to a .ts file, then:
npx --yes esbuild LiquidVanilla.ts --format=esm --bundle --outfile=liquid.js
```

Liquid's vanilla API (verified):
- `supportsHtmlInCanvas(): boolean` — checks for the `drawElementImage` canvas method.
- `createLiquid({ source, content, output }, options): { splat(x,y,dx,dy), setOptions, resize, destroy }`.
- Elements: `source` = `<canvas layoutsubtree="true">` hosting the DOM, `content` = the div inside it, `output` = an overlay `<canvas>`.
- Options (defaults): `force 1.1, radius 0.3, curl 1.9, intensity 2, distortion 0.4, blend 5, densityDissipation 0.96, color [0.145,0.239,0.867] (0–1 RGB), rainbow false, simResolution 128, dyeResolution 512`.

## 4. The preview page

```html
<div class="stage" id="stage" style="position:relative; width:440px; height:296px;">
  <canvas id="source" layoutsubtree="true" style="width:100%;height:100%;">
    <div id="content" style="position:relative;width:100%;height:100%;"><!-- content.html --></div>
  </canvas>
  <canvas id="output" aria-hidden style="position:absolute;inset:0;pointer-events:none;"></canvas>
</div>
<div id="status"></div>

<script type="module">
  import { createLiquid, supportsHtmlInCanvas } from './liquid.js';
  const stage=…, source=…, content=…, output=…, status=…;

  function fallback(msg){ stage.insertBefore(content, source); source.remove(); output.remove();
    content.style.position='static'; status.innerHTML=msg; }

  function start(){
    if(!supportsHtmlInCanvas()){ fallback('Enable chrome://flags/#canvas-draw-element in Chrome to see the effect.'); return; }
    let inst;
    try { inst = createLiquid({source,content,output},
      { rainbow:false, color:[0.13,0.77,0.33], distortion:0.5, force:1.4, radius:0.32, intensity:2.2, curl:2.0 }); }
    catch(e){ fallback('Effect failed: '+e.message); return; }
    // pointer splats
    let px,py; stage.addEventListener('pointermove',e=>{ const r=output.getBoundingClientRect();
      const x=(e.clientX-r.left)/r.width, y=1-(e.clientY-r.top)/r.height;
      if(px!==undefined) inst.splat(x,y,(x-px)*10,(y-py)*10); px=x;py=y; });
    // idle auto-motion so it's alive with no input
    let t=0; (function loop(){ t+=0.016; const x=0.5+0.36*Math.cos(t*0.7), y=0.5+0.30*Math.sin(t*1.1);
      inst.splat(x,y,Math.cos(t*0.7)*0.9,Math.sin(t*1.1)*0.9); requestAnimationFrame(loop); })();
    status.textContent='Liquid active — move your cursor over the card.';
  }
  window.addEventListener('load', start);   // wait for images so they're in the first texture
</script>
```

Key points:
- **Match the effect `color` to the design's accent** (normalize the hex to 0–1). It's what makes it read as *the product's* effect, not a generic demo.
- **Idle auto-motion** (the `loop`) so the demo moves without a cursor — essential for a GIF/screenshot.
- **`window.load`, not `DOMContentLoaded`** — wait for images so they're in the first painted texture.
- **The fallback** relocates `#content` out of the `<canvas>` so it shows as plain HTML when the flag's off (content inside a `<canvas>` is otherwise invisible).

## 5. Serve, view, deliver

```bash
python3 -m http.server 8787    # module imports + experimental API need http, not file://
```

Open `http://localhost:8787/index.html` in **Chrome** with `chrome://flags/#canvas-draw-element` enabled. Look at it: effect running, content crisp, no vanished assets. A still undersells motion — offer a GIF capture. In other browsers / without the flag it degrades to the plain card, no errors.

## 6. Constraints to state plainly

- html-in-canvas is a Chrome **origin-trial / flag** feature. Full effect = Chrome-with-flag today; production needs an origin-trial token. Demo-grade, not shippable UI.
- Canvas UI is early — Liquid is the first component; the effect set grows over time (same registry pattern: `<name>-vanilla.json`).
