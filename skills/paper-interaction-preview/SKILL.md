---
name: paper-interaction-preview
description: Take components the user has selected in Paper (paper.design) and turn them into live, interactive HTML previews with hover/press/focus motion applied — accumulating onto one running preview page per design system. Use when the user wants to feel interactions on Paper components, add motion to a Paper design, preview hover/press states in the browser, or build up an interaction reference page from their Paper component system. Companion to generate-design-html (static token board); this one covers behavior. Requires the Paper MCP.
---

# Paper Interaction Preview

Turn selected Paper components into live specimens on a single self-contained HTML page, with the interaction layer (hover / press / focus / transitions) applied. The page accumulates: each request appends specimens; the user refreshes the browser to see them.

## Capabilities

- **Requires**: Paper MCP (the design source).
- **Uses if present**: any browser automation (Chrome extension MCP, agent-browser, playwright CLI, cmux-browser, …) for verification and capture; ffmpeg for GIF conversion.
- **No hard tool dependency beyond Paper**: the final fallback for showing/verifying is always `open <url>` + the user's eyes, and the primary share artifact is the HTML file itself.

Siblings: `generate-design-html` (static token board), `paper-to-lottie` (animated assets as open Lottie JSON), `paper-to-rive` (stateful/data-bound assets in Rive). UI chrome belongs here in CSS — don't route it to a canvas runtime.

## Workflow

1. **Get the component(s)**
   - `get_selection` on the Paper file. If nothing useful is selected, ask the user to select the component(s) or name the node.
   - `get_jsx` (inline-styles) + `get_screenshot` for each component. The JSX is the source of truth for values; the screenshot is for your own visual check.

2. **Create or append the preview page**
   - One page per system: `<system>-interactions.html`, started from `assets/preview-shell.html`.
   - First run: ask where it lives (project dir vs scratchpad), copy the shell, set the page title and canvas background to the product's (read from the Paper frame — don't default to dark).
   - Later runs: append a new specimen section before `<!-- /specimens -->`. Never regenerate existing specimens unless asked.

3. **Translate JSX → specimen**
   - Clean HTML with a CSS class per component (styles in the page `<style>`, not inline) so states are expressible.
   - Real text, real SVGs from the JSX. Interactive elements are real `<button>`/`<a>`/`<input>` tags.

4. **Apply motion**
   - Read `references/motion-presets.md`. On the first specimen for a system, offer either a direct pick — **Crisp** (fast, utilitarian — default for tools) / **Soft** (calm, friendly) / **Springy** (playful, branded), with a recommendation — or **tryout mode**: the same specimen rendered three times in one row, one column per preset (mechanics in the presets file), so the user feels all three before choosing. Default to offering tryout when the user hasn't expressed a preference.
   - After the pick, **lock the preset**: promote the winner's tokens to `:root`, remove the losing scopes, note it in the page header ("Motion: Crisp"). Later specimens reuse the locked preset without re-asking.
   - If the user specifies a custom feel, honor it over the preset — but keep the shared rules (palette-derived colors, no `ease-in`, transform/color-only, press feedback, reduced-motion).

5. **Emit the handoff** (on preset lock, and refresh it when components are added)
   - Write `motion-tokens.css` next to the preview file: the locked preset's `:root` token block, then one commented state-rule block per component type present on the page, using the resolved values from the specimens.
   - This file is what the codebase imports/copies — keep it valid standalone CSS, no placeholder text.

6. **Specimen anatomy** (pattern is in the shell as a comment)
   - Label (component name as in Paper) + the live specimen(s) + a one-line spec caption: `hover: bg #4FD1C5→#6EDCD1, arrow +3px · press: #3EBFB3, scale .97 · 150ms ease-out`.
   - Variants of one component (primary/secondary) share a row.

7. **Show it**
   - Local browser available: serve the directory (`python3 -m http.server <port>`, background) and `open http://localhost:<port>/<file>`. If already serving, just tell the user to refresh.
   - No display (claude.ai / sandbox): publish as an Artifact instead.

8. **Share** (only when asked)
   - Default: the HTML file itself — self-contained, small, live, and its CSS is the spec. Artifact publish when a URL beats a file.
   - GIF backup, for surfaces where HTML can't run (Slack, issue comments, docs) — use **whatever browser automation the session has** (Chrome extension recorder, agent-browser, playwright video, …). The capability needed is: drive the mouse through hover/press with natural pauses while recording video, then convert. If no automation is available, the user's own screen recorder over the live page works fine.
     1. Choreography (any driver): idle 600ms → move onto component → 600ms → button down → 350ms → up → 500ms, per component; end with the cursor off-component.
     2. Example with agent-browser: `get box @ref` for coordinates, `record start x.webm`, `mouse move/down/up` + `wait` per above, `record stop`.
     3. Convert: `ffmpeg -y -i in.webm -vf "fps=25,scale=800:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=128[p];[s1][p]paletteuse=dither=bayer" -loop 0 out.gif` (~80KB for a 5s clip).
   - Caveat: headless recordings show no cursor — states appear to change on their own. Acceptable for spec review; note it when sharing, or inject a cursor dot via JS if legibility matters.

## Hard constraints

- One standalone HTML file. Inline `<style>`, no frameworks, no build step, no `localStorage`.
- The interaction CSS **is** the deliverable spec — an engineer should be able to copy a specimen's CSS block as-is. Keep each specimen's rules grouped and commented with its name.
- Don't overdo it: no routers, no state-forcing chips, no token views. That's `generate-design-html`'s territory.
- Match the product's theme and fonts (`system-ui` fallback); never restyle the component beyond adding states.
