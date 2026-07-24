---
name: paper-to-lottie
description: Turn vector elements from Paper (paper.design) into animated Lottie assets by generating Lottie JSON directly — no Lottie editor, no manual import/export. Use when the user wants a Paper icon/illustration animated as a Lottie or dotLottie file, a looping motion asset from their Paper design, or asks to convert Paper vectors to Lottie. The .json produced is the shippable deliverable (lottie-web or any dotLottie player). Requires the Paper MCP.
---

# Paper → Lottie

Export a vector from Paper, hand-author the Lottie JSON around it, verify in a local player. The pipeline is fully automated because both ends are open formats: Paper exports real SVG via MCP, and Lottie is documented JSON an agent can write and patch as text.

## Capabilities

- **Requires**: Paper MCP.
- **Uses if present**: any browser automation (Chrome extension MCP, agent-browser, playwright CLI, …) for blind verification and GIF capture; ffmpeg for GIF conversion.
- **No Lottie account, editor, or MCP needed** for playback assets. Fallback verification is always `open <url>` + the user's eyes.
- **Optional**: LottieFiles Creator MCP (`@lottiefiles/creator-mcp` + a creator.lottiefiles.com tab with MCP enabled) — upgrades SVG conversion and verification; see "Optional: Creator MCP path" below.

Siblings: `paper-interaction-preview` (UI chrome → CSS, the default for buttons/hovers), `paper-to-rive` (stateful, data-bound runtime assets). Lottie's lane: illustrative/decorative motion, looping icons, brand-themed animation.

## Scope — read before promising

- **Proven**: vector shapes (paths, strokes, fills, groups), transform keyframe animation, looping playback.
- **Not covered (yet)**: dotLottie interactivity/state machines (needs their newer players — separate experiment), text layers (Lottie font handling is weak; avoid text-heavy comps — that's CSS territory anyway), gradients/masks/complex SVG features **by hand-mapping** (needs a real SVG→Lottie converter — if the Creator MCP is connected, its SVG import *is* that converter; otherwise tell the user rather than approximating badly).

## Workflow

1. **Get the vector out of Paper**
   - Find the node (`get_selection`, `get_children`, or `find_nodes`). Confirm it's actually vector (`SVG` component or shape nodes) — image-fill nodes export as embedded rasters and won't map to Lottie shapes.
   - `export` with `{"<nodeId>": [{"format": "svg", "scale": "1x"}]}` → returns a local file path. Read the file; its paths/strokes/viewBox are the source of truth.

2. **Author the Lottie JSON** (write the file directly; no editor)
   - Canvas: `w`/`h` from the viewBox, `fr: 60`, `op` = loop length in frames.
   - Map SVG → shape layers. Per-path: `sh` item with `v` (vertices), `i`/`o` (in/out tangents, `[0,0]` for straight lines), `"c": false` for open paths (`Z` in the SVG path = `true`).
   - Strokes → `st` item: color `c.k` as 0–1 RGBA array, width `w`, `lc`/`lj` = 2 for round caps/joins. Fills → `fl`. Rounded rects → `rc` with `p`(center)/`s`/`r`.
   - **Every group's `it` array must end with a `tr` transform item** — silent no-render otherwise.
   - Animate on the layer transform (`ks`): position/scale/rotation keyframes `{"a":1,"k":[{t,s,o,i,to,ti}, …]}`; set the layer anchor `a` to the intended pivot; position keyframes want `to`/`ti` spatial tangents (zeros are fine).
   - Ease with `o`/`i` beziers (e.g. `o:{x:.33,y:0}, i:{x:.2,y:1}` for a settle).

3. **Verify blind**
   - Local page: `<script src="https://cdnjs.cloudflare.com/ajax/libs/bodymovin/5.12.2/lottie.min.js">` + `lottie.loadAnimation({container, renderer:'svg', loop:true, autoplay:true, path:'x.json'})`. Serve the directory (`python3 -m http.server`, background).
   - With browser automation: open the page, check console errors, screenshot; record a short video → GIF to confirm motion. Without: `open` the URL and ask the user to look.
   - A blank render with no errors almost always means a missing group `tr`, a closed path that should be open, or colors given as 0–255 instead of 0–1.

4. **Deliver**
   - The `.json` is the shippable asset (lottie-web, dotLottie players, mobile runtimes). Zip with assets as `.dotlottie` only if the consumer wants that container.
   - Iteration = patching JSON fields (colors, timings, vertices) — no re-export, no editor round-trip.
   - GIF for chat/docs: record the player page with any available recorder, then `ffmpeg -vf "fps=30,split[s0][s1];[s0]palettegen=max_colors=64[p];[s1][p]paletteuse" -loop 0 out.gif`.

## Optional: Creator MCP path

When the LottieFiles Creator MCP is connected (`@lottiefiles/creator-mcp` in the client + creator.lottiefiles.com open with **Settings → MCP Settings → Enable MCP**), it upgrades two stages of the pipeline. It does **not** replace the deliverable step — see the export caveat.

**Worth switching to when:**
- The Paper SVG has gradients, masks, or path features hand-mapping can't do — Creator's `scene.import({ type: 'SVG', content })` does real conversion.
- The user wants to watch motion live or hand-tweak keyframes after — the animation plays in their open tab; no localhost player loop needed.
- Complex choreography — the typed API (`Animatable.addKeyframes`, `CUBIC_BEZIER` easing) beats hand-writing keyframe JSON and sidesteps the `tr`/anchor/color-scale gotchas below.

**Workflow:** ping the bridge with a trivial `run_script` (`console.log`) → read ALL pages of `get_api_doc` + `get_rules` (mandatory once per session) → import the Paper SVG → restore any gradient alpha (see below) → position via `getMatrix()` calibration → animate layers via the API → verify live in the tab (user's eyes — key reads lie, see gotchas).

**Export caveat (verified 2026-07-22):** the script API has **no programmatic Lottie export**. `scene.toJSON()` returns only an `{id, type}` bridge stub; the `ExportFormat = 'LOTTIE_JSON'` type is declared but no reachable method uses it. The shippable `.json` requires a manual export from the Creator UI. If the deliverable must be produced hands-free, hand-author the JSON (main path) — or use Creator for conversion/preview and have the user export once at the end.

**Gradient alpha — the one thing that needs a special recipe (tested 2026-07-22).** Creator supports per-stop opacity (UI proves it renders correctly), but almost every programmatic path to it is broken:
- SVG import: `stop-opacity` flattened to opaque. `stops.staticValue = ...`: silently ignored. `createFill` stop opacities: ignored. Lottie-JSON import with alpha stops: fill survives but renders **invisible**.
- ✅ THE WORKING PATH: write the stops as a single keyframe — `fill.stops.addKeyframes([{ frame: 0, value: [{color, offset, opacity}, …] }])`. One keyframe at frame 0 behaves as a static value. Fallback: the user drags the stop's opacity slider in the Creator UI.
- Read-back of stop opacity **always reports 1** on every path (staticValue AND keyframes), including immediately after a visually-confirmed-correct write. Never trust reads for alpha — verify with the user's eyes.

**Paper-side export gotchas:**
- Exporting a Paper **Frame/artboard** as SVG yields a `<foreignObject>` HTML blob (with embedded fonts, MBs) — zero top-level vector content. Export the individual **SVG component nodes** instead; those come out as clean true-vector files.
- CSS gradients (on divs or artboard backgrounds) **rasterize** on export. Author gradient elements as inline `<svg>` with `<linearGradient>`/`<radialGradient>` defs — those export as real vector gradients and convert cleanly (colors + offsets exact).

**Creator-side gotchas:**
- The browser bridge dies **silently after tab inactivity** (recurred ~every 10–15 min of the tab being backgrounded) — errors say "No Creator tab is connected" while the client still lists the server as Connected. Fix: re-press Enable MCP in the Creator tab. Ping before every work batch.
- No top-level `await` in `run_script` (SyntaxError). Wrap in an async IIFE — but the tool returns before the IIFE settles and **console output after the first await is lost**. Fire the async script, then verify with a second synchronous script.
- `scene.import()` completion order is nondeterministic — importing in stack order does NOT produce that stacking. Reorder afterward with `bringToFront()`/`moveBefore()`.
- Imported SVGs land at arbitrary offsets. Calibrate with `layer.getMatrix()`: `(e, f)` = rendered top-left of the SVG box in scene coords; adjust `position` by (desired − actual).
- Per-element `style="opacity: …"` on SVG shapes is dropped by import — restore via group `opacity.staticValue` (that setter works; scale 0–100).
- Layer stacking behaved **opposite** to what `get_rules` documents: new layers arrived on top. Always verify `scene.layers` (index 0 = topmost) and correct.
- `createFill` can transiently fail with `Cannot read properties of null (reading 'scene_obb')` under rapid successive calls — wrap in a small retry loop.
- Colors are **0–255** in the Creator API (raw Lottie JSON is 0–1 floats — don't carry one convention into the other).
- Layer scale pivots at the layer origin: to squash/stretch around a contact point, offset the shape inside the layer so the origin sits on the pivot.

## Gotchas (each cost a debug cycle once)

- Colors are **0–1 floats**, not 0–255.
- Groups without a trailing `tr` item render nothing, silently.
- `"c": true` on a path that should be an open stroke turns it into a filled/closed shape.
- Layer `a` (anchor) defaults to `[0,0]` — set it to the visual center or rotation/scale pivots wrong.
- lottie-web won't load `path:` JSON over `file://` — always serve over localhost.
