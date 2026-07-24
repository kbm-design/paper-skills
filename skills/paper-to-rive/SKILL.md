---
name: paper-to-rive
description: Rebuild designs from Paper (paper.design) as interactive Rive assets — layouts, vectors, text, state machines with hover/press/pointer states — authored through the Rive MCP. Use when the user wants a Paper design made interactive in Rive, a stateful animated asset (mascot, loader, reactive component) built from their design, or asks to bring Paper work into Rive. Requires both the Paper MCP and the Rive MCP (Rive editor open on the target file).
---

# Paper → Rive

Rebuild a Paper design inside Rive and wire real interactivity (state machines, listeners, data binding). Rive's lane: **stateful, input-driven, data-bound assets an engineer ships as-is** (.riv + runtime). For plain UI hover/press, use `paper-interaction-preview` (CSS) instead — don't rebuild buttons in a canvas runtime.

## Capabilities & manual steps (set expectations up front)

- **Requires**: Paper MCP + Rive MCP, with the Rive editor open on the target file.
- **The Rive MCP cannot**: import assets (SVG/fonts/images — the user drags files into Rive's Assets panel), export the .riv (user: hamburger menu → export/download), or render screenshots (verification is by data + the user's eyes).
- Tell the user these manual steps exist before starting, not when hitting them.

## Workflow

1. **Read the design from Paper**: `get_jsx` (inline-styles) for exact values, `get_screenshot` for your own reference. Optionally `export` SVGs from Paper for the user to drag into Rive's Assets — imported vectors beat hand-redrawn ones.

2. **Artboard**: `open_file_editor` resize/rename. Background = the artboard's Fill → SolidColor child, color property key **37**, format `#aarrggbb`.

3. **Structure**
   - UI trees → `layout_editor createLayout` (flexbox-like; text nodes only exist inside layouts; `textStyle` = fontSize + fillColor only — **no font weights without a font asset** the user drags in).
   - Vectors → `path_editor createShapes` (shape x/y in parent space, path commands around shape-local 0,0; scale stroke widths by the source viewBox ratio).
   - After creating, `get_artboard_hierarchy` to map IDs — everything downstream needs them.

4. **Vector gotchas** (each verified the hard way)
   - **Paths default to `isClosed: true`** (key 32) — open strokes (icons, chevrons) render as filled closed shapes until you set it false.
   - Stroke: thickness key 47, cap key 48, join key 49 (enum: 1 = round).
   - Layouts **cannot take strokes/borders** (`addPaints` fails on layout IDs) — compensate with background shifts, or note the missing border to the user.

5. **Interactivity recipe** (ViewModel-driven; this exact sequence works)
   1. `viewmodel_editor createViewModels` — booleans per interaction (e.g. `primaryHover`, `primaryPress`) → `bindViewModelToArtboard`.
   2. Timelines: **reuse the default "Timeline 1"** (rename it) for the first state; `createLinearAnimations` (duration 1) for the rest. One single-frame timeline per state, keyframes at frame 0 (`modifyKeyFrames`): SolidColor color 37, node x 13, scale sx/sy 16/17.
   3. State machine: reuse the default; `createStates` on the default layer (its Entry already connects to the default timeline), `createStateMachineLayers` for additional independent components (one layer per component).
   4. `createTransitions` by state ID, then `createConditions` against the VM property IDs.
   5. **Verify conditions with `queryStateMachine`** — boolean `"true"` string values can silently store as `false`. Fix via the condition's rightComparator object, value key **647**.
   6. Transition blend duration: key **158**, milliseconds (150 is a good default), via `set_property_values`.
   7. `create_listeners` (enter/exit/down/up on the component layouts) → each action's `bindablePropertyId` object holds the value to set: key **634** (true for enter/down, false for exit/up — must be set explicitly).

6. **Verify by data, not pixels**: `queryStateMachine` end-to-end (states, transitions, conditions with resolved values, listeners), `query_property_values` for spot checks. Then have the user hit **Play** on the state machine in the editor and interact. There is no screenshot tool — the user's eyes are the visual check; expect one round of "that looks wrong" fixes (see step 4).

7. **Handoff**: user exports the .riv; embed with `@rive-app/react-canvas` (`useRive({src, stateMachines: '<name>', autoplay: true})`) — interactions are baked in, zero interaction code. Add Rive events fired on click if the app needs to react (navigation etc.).

## When NOT to use this

- Buttons/UI chrome → CSS (`paper-interaction-preview`). Canvas text isn't selectable, SEO-visible, or screen-reader accessible.
- Decorative/illustrative loops with no input or app-data needs → `paper-to-lottie` (open format, fully automatable pipeline).
- Choose Rive when the asset needs continuous input response, blended states, runtime data binding, or rigging.
