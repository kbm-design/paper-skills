---
name: paper-canvas-fx
description: Apply Canvas UI (canvasui.dev) WebGL effects — Liquid fluid simulation, shaders — over a real Paper (paper.design) frame, and open a live self-contained preview in the browser. Pulls the frame via get_jsx, converts it to plain HTML, inlines its assets, and renders it under the effect via the html-in-canvas API so the content stays crisp and real — no screenshots, no flattening. Use when the user wants to add a WebGL / shader / fluid effect to a Paper design, preview a mockup with Canvas UI, make a splashy effect demo or GIF of a frame, or "melt / ripple / distort this design." Requires Paper Desktop open and Chrome with the `canvas-draw-element` flag for the full effect (degrades to plain HTML otherwise). A preview/demo skill for dazzle, not production output.
---

# Paper × Canvas UI effects

[Canvas UI](https://canvasui.dev) is a library of WebGL effects (fluid sims, shaders) that render *over real HTML* using the experimental html-in-canvas API — your DOM becomes a texture the shader samples and distorts, without screenshots or DOM-to-image hacks. And Paper's `get_jsx` hands you real HTML of any design element. So a Paper frame drops straight in as the effect's texture and **stays crisp** — you're rippling the actual design, not a flattened image. That marriage is the whole skill.

This is a **preview / demo skill**, and honest about it: the effect is Chrome-flag-gated and experimental. It's for dazzle — launch GIFs, "look what your mockup can do" posts, an announcement hero — not for shipping to end users.

Read `references/paper-craft.md` (shared KBM conventions) and `references/canvas-fx-build.md` (the exact build: JSX→HTML, asset inlining, pulling + compiling the Canvas UI component, the preview structure, serving) before building. The proven JSX→HTML converter ships at `assets/jsx2html.py`.

## The contract

- **The real frame, not a rebuild.** Content comes from `get_jsx` (inline-styles format), converted to HTML — never hand-authored. The point is *their actual design* under the effect.
- **Inline every asset.** Cross-origin images (Paper file-assets, external URLs) **taint the canvas and silently vanish** when the effect paints the DOM to a texture. Fetch each asset and swap it for a `data:` URI before rendering. This is the #1 gotcha — a card whose avatars disappeared is almost always this.
- **Serve over http, never `file://`.** The preview uses ES module imports and an experimental API; both need a real origin. Run a local server and open `http://localhost:…`.
- **Graceful fallback, never a blank page.** Without the flag, the content must still show as plain HTML (move it out of the `<canvas>`). Detect support and degrade.
- **Be honest about the flag.** Tell the user to enable `chrome://flags/#canvas-draw-element` in Chrome for the full effect, and that it's a demo-grade capability.

## Workflow

### 1. Preflight & pick
Preflight per `paper-craft.md`. Pick the source frame (selection or named) and the effect (Liquid is Canvas UI's first component and the default; others as the library grows). Note the design's accent colour — you'll match the effect tint to it (`#22C55E` → `[0.13, 0.77, 0.33]`).

### 2. Pull the frame → HTML
`get_jsx` (format `inline-styles`) on the frame → run it through `assets/jsx2html.py` (converts style objects, vendor prefixes, SVG camelCase attrs, expands self-closing divs). Then **inline every cross-origin asset** as a `data:` URI (fetch → base64 → replace the `url(...)`).

### 3. Pull & compile the Canvas UI component
Fetch the **vanilla** flavor from the shadcn registry: `https://canvasui.dev/r/<effect>-vanilla.json` → the `files[].content` is the TS source. Compile it to an ESM JS module with esbuild (`npx esbuild <file>.ts --format=esm --bundle`). (See `canvas-fx-build.md` for the API — `createLiquid({source, content, output}, options)` + `supportsHtmlInCanvas()`.)

### 4. Assemble the preview
One self-contained page with the effect's canvas structure (`<canvas id="source" layoutsubtree>` wrapping the frame HTML in `#content`, plus an `#output` overlay), a module script that: feature-detects → inits the effect (accent-matched colour) → drives idle auto-motion + pointer splats → falls back to plain HTML if unsupported. Template in `canvas-fx-build.md`.

### 5. Serve & view
Start a local server (`python3 -m http.server`), open the URL in Chrome, and tell the user to enable the flag if the effect isn't running. **Verify by looking** — the effect must render and the content must stay crisp; check assets survived (no vanished images).

### 6. Deliver
Give the URL + folder path, name the effect and the flag requirement, and offer a GIF capture (the effect is motion — a still undersells it). Log to `.kbm/paper-canvas-fx.md`: frame, effect, options used.

## Failure modes to avoid

- **`file://`.** Module imports and the experimental API both break. Always serve over http.
- **Un-inlined cross-origin assets.** They taint the canvas and disappear. Inline everything as `data:` URIs before rendering — the single most common broken demo.
- **No fallback.** Content nested in `<canvas>` shows nothing when the flag's off. Always provide the move-out-and-show-plain path.
- **Claiming it works unseen.** The effect only runs in Chrome-with-flag — look at it there before declaring success (a still doesn't prove motion).
- **Treating it as production.** It's flag-gated and experimental — a demo/marketing capability, not shippable UI. Say so.
- **Rebuilding the frame by hand.** Defeats the whole point; the magic is the *real* design staying crisp under the effect. Use `get_jsx`.
