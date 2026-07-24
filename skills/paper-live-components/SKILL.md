---
name: paper-live-components
description: >
  Mirror real components from a codebase onto the Paper.design canvas as
  token-bound "islands" — a code→canvas design system mirror. Extracts the
  codebase theme into Paper design tokens, renders components as faithful
  variant matrices bound to those tokens, edits props conversationally, and
  pushes changes back to code. Use when the user wants to pull components into
  Paper, build a design system in Paper from code, sync Paper designs with a
  repo, or asks for "Paper Dev Mode". Requires the Paper MCP. For interactive
  hover/press/motion previews, pair with the paper-interaction-preview skill.
version: 0.2.0
author: KBM Design Tools
tags: [paper, design, react, mcp, components, design-system, tokens, dev-mode]
---

# Paper Live Components (Paper Dev Mode) — v0.2

Bridge real code components and the Paper.design canvas. The canvas becomes a
**faithful mirror of the codebase's design system**: tokens first, then
components rendered as native Paper nodes bound to those tokens, with
round-trip sync back to code.

## What changed in v0.2 (read this first)

v0.1 assumed `write_html` injects live HTML/JS. **Empirically tested 2026-07-22
— it does not.** Verified facts about the Paper runtime:

- ❌ `<script>` tags DO NOT execute — they parse into literal Text nodes on the
  canvas. Never include scripts. No React mounting, no `window.*` globals, no
  on-canvas JS props panels.
- ❌ `class` attributes are silently dropped. Tailwind/CSS classes render as
  unstyled text. **Everything must be inline styles.**
- ✅ Static rendering is pixel-faithful and produces real, editable nodes in
  the layer tree.
- ✅ Design tokens are live-bound: `style="background-color: var(--color-accent)"`
  resolves against file tokens, and `set_tokens` retheming updates every bound
  node instantly. This is the interactivity story — no JS needed.
- ✅ Prop changes via `update_styles` + `set_text_content` are surgical and
  instant. **Claude is the props panel** — the user asks in chat, you mutate
  nodes directly.
- ✅ `get_tokens({format: "tailwind"})` exports file tokens as a Tailwind v4
  `@theme` block — native token push-back.
- ✅ `get_jsx` / `get_computed_styles` give exact values for component push-back.

## Prerequisites

- Paper Desktop running with the target file open (Paper MCP tools reachable).
  If Paper tools are unavailable, say so and stop — there is no fallback surface.
- Load Paper's guide once per session before other Paper tools:
  `get_guide({topic: "paper-mcp-instructions"})`, then `get_basic_info`.
- A codebase connected in the session to pull components/theme from.

## Workflow

### Phase 1 — Tokens first (the foundation)

Before pulling any component:

1. Check existing file tokens (`get_basic_info` / `get_tokens`). Reuse them
   when they cover the codebase's values.
2. Extract the codebase theme — Tailwind config, `globals.css` CSS variables,
   theme files — and create missing tokens with `create_tokens`. Follow
   Paper's ordering rules (semantic before palette, neutrals → primary →
   accent; sizes smallest-first). Use the Tailwind v4 namespaces:
   `--color-*`, `--text-*`, `--font-weight-*`, `--radius-*`, `--spacing-*`.
3. Record the mapping (code value ↔ token name) — you need it for push-back.

### Phase 2 — Pull components as islands

For each requested component:

1. Read the source (`.tsx`/`.jsx`). Extract exported props, variants, sizes,
   and default values (interfaces, cva configs, PropTypes, JSDoc).
2. **Translate all styling to inline styles** (see cheatsheet below). Bind
   every value that has a token to `var(--token-name)` — never hardcode a hex
   that a token covers. Values with no matching token: render them, but flag
   them to the user as potential token gaps ("Token Warden" finding).
3. Render as a **variant matrix** on its own artboard: header with the
   component name + source path + fidelity label, then one row per variant
   with a fixed-width (flexShrink: 0) label lane and one instance per size.
4. Build incrementally — one row per `write_html` call. Screenshot and review
   when done (Paper's mandatory checkpoints).
5. Name layers: artboard `Island / Button`, rows `Row / destructive`.
6. Label fidelity honestly in the header, e.g.
   `STATIC ISLAND · variants × sizes · fidelity: visual only (no hover/focus)`.

### Phase 3 — Prop edits (conversational)

When the user asks to change props ("make it destructive/lg", "text → Ship it"):

- Mutate the existing nodes with `update_styles` + `set_text_content`. Do not
  delete + rewrite.
- New instances/compositions: `duplicate_nodes` from the matrix, then adjust.
- Never mutate a user's original hand-made frames — duplicate first unless
  they explicitly say to edit in place.
- Retheming: change token values with `set_tokens`; all bound islands update.
  The user can also do this themselves in Paper's token panel — tell them so.

### Phase 4 — Push back to code

Two modes, always show a summary/diff and get confirmation before writing:

- **Update usage** (preferred): read the composed design with `get_jsx` +
  `get_computed_styles`, map `var(--token)` values back to the codebase's
  Tailwind classes / CSS vars via the Phase 1 mapping, and update how the
  component is used in a page.
- **Update component**: write changes into the component file itself. Use with
  caution; always show the diff first.
- **Theme push-back**: `get_tokens({format: "tailwind"})` returns a `@theme`
  block to diff against the codebase's Tailwind config.
- Never use screenshots as the source for code values — only exact values from
  `get_jsx` / `get_computed_styles` / `get_fill_image`.

## Tailwind → inline-style cheatsheet

Common translations (Tailwind default scale):

| Tailwind | Inline style |
|---|---|
| `flex items-center justify-center` | `display: flex; align-items: center; justify-content: center` |
| `rounded-md` / `rounded-lg` / `rounded-full` | `border-radius: 6px / 8px / 999px` |
| `h-8` / `h-10` / `h-12` | `height: 32px / 40px / 48px` |
| `px-3` / `px-4` / `px-6` | `padding: 0 12px / 0 16px / 0 24px` |
| `text-sm` / `text-base` | `font-size: 14px / 16px` |
| `font-medium` / `font-semibold` / `font-bold` | `font-weight: 500 / 600 / 700` |
| `bg-neutral-900` / `bg-neutral-100` | `background-color: #171717 / #F5F5F5` |
| `bg-red-600` | `background-color: #DC2626` |
| `border border-neutral-300` | `border: 1px solid #D4D4D4` |
| `disabled:opacity-50` | `opacity: 0.5` (render as a "disabled" row) |
| `gap-2` / `gap-4` | `gap: 8px / 16px` |

If the project overrides the Tailwind scale, resolve against its config, not
this table. Prefer `var(--token)` over any literal when a token exists.

Paper HTML rules (hard constraints): inline styles only; no `margin`,
`display: grid`, `display: inline`, or HTML tables — use flex + padding + gap;
no emojis as icons (use SVG); `layer-name` attribute for layer tree names.

## Scope and honest limitations

This skill delivers **structure, variants, composition, and code sync** — not
behavior. Hover/press/focus states render only as separate static rows if the
source defines them. For interactions the user can actually feel, hand off to
the **paper-interaction-preview** skill (browser-based live previews) — canvas
holds structure, browser holds behavior.

State-driven rendering (open/closed, loading) → render each state as its own
labeled instance.

## Error handling

- Component too complex to translate faithfully (heavy context, portals,
  runtime-computed styles) → render the closest static version, label the
  gaps explicitly, and tell the user what was approximated.
- `write_html` failure → simplify markup and retry once; then report.
- Never overwrite source files without explicit confirmation.
- Always `finish_working_on_nodes` when done.

## Upgrade path

When Paper ships native "use your code components": detect the capability,
prefer the official API, keep this island technique as the fallback.

## Example invocations

- "Pull Button from src/components as an island with all variants"
- "Extract our Tailwind theme into Paper tokens"
- "Change the Button island to variant=destructive size=lg"
- "Retheme: make the accent purple"
- "Push this composition back to the pricing page"
- "Which values in Card.tsx aren't covered by our tokens?"
