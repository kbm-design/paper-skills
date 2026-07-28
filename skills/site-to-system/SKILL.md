---
name: site-to-system
description: Turn any website, repo, CSS/Tailwind config, or screenshot into an editable design system inside Paper (paper.design) — extract the palette, type scale, spacing, radii, and components, materialize them as real Paper design tokens (created via the Paper MCP, the only way tokens can be made today), and lay down a component sticker sheet wired to those tokens so everything you design afterward snaps to the system. Use whenever the user wants to build a design system in Paper, extract tokens from a site or codebase, bootstrap a system from their marketing site, study a reference as a live editable system, or "turn this into tokens." Requires Paper Desktop open. Canonical values become tokens; inferred ones wait on a proposals board for approval.
---

# Site to System

Paper's own `code-to-design` reads *your* repo to build one requested page. This does the opposite job: it ingests *any* source — a third-party site, a codebase, a CSS/Tailwind config, a screenshot — and produces the reusable **system** itself. Real Paper tokens wired into the file, plus a sticker sheet of editable components, so every later design snaps to them.

The point is the tokens. **Paper design tokens can only be created or edited through the MCP — there is no UI for them.** So this skill is not documenting a system; it is *the* way that system gets into the file.

Read `references/paper-craft.md` (shared KBM conventions: preflight, evidence loop, Canonical/Candidate/Avoid, `write_html` quirks, `KBM/` hygiene, `.kbm/` memory) and `references/extraction.md` (source ingestion, the token taxonomy Paper supports, ordering rules, the sticker-sheet layout) before building.

## The contract

- **Canonical becomes a token; Candidate waits for approval.** A value read directly from the source (a CSS variable, a repeated computed color, a declared Tailwind scale) is Canonical and is created as a token. A value *inferred* — a gray you think three near-misses are reaching for, a spacing step the site skips — is a Candidate: it goes on a `KBM/proposals` board for the user to approve, never silently created. Present inference as inference (per `paper-craft.md` §7).
- **Read the values, don't eyeball them.** Colors, sizes, and type come from computed styles / the config / the stylesheet — not from a screenshot. A screenshot tells you *what exists to extract*; it never sets a token's value.
- **Reuse before creating.** Call `get_tokens` first. If the file already has tokens, extend the system; don't duplicate. Alias with `var(--other-token)` rather than repeating a value.

## Workflow

### 1. Preflight & source
Preflight per `paper-craft.md` (`get_basic_info`, confirm file). Then identify the source and gather it with the right tool:
- **Live site** → browser inspection / computed styles / a screenshot for structure. (If the `generate-design-html` skill is available, its extraction heuristics apply — this skill is the Paper-destination remix of it.)
- **Repo / config** → read the CSS custom properties, the Tailwind `theme`, the SCSS variables directly. This is the richest, most Canonical source.
- **Screenshot / design note** → lowest fidelity; most values will be Candidates, flag accordingly.

Call `get_tokens` to see what already exists.

### 2. Extract & classify
Pull the design language into the Paper token taxonomy (`references/extraction.md`): `color`, `fontFamily`, `fontSize`, `fontWeight`, `lineHeight`, `letterSpacing`, `spacing`, `radius`, `container`, `breakpoint`. Classify every value **Canonical / Candidate / Avoid**. Group colors into semantic roles (surface, text, primary, accent, borders, states) *and* a palette ramp — semantic tokens alias palette tokens.

### 3. Create the tokens
`create_tokens` for the Canonical set. **Create the palette (literal values) first, then the semantic layer (aliases)** — an alias needs its target to exist, so dependency order wins over Paper's stated "semantic first" display preference (see `extraction.md` §3). Use `var(--…)` aliases so semantic tokens point at palette tokens (change the palette once, the whole system moves). Put Candidates on the proposals board instead — do not create them.

### 4. Build the sticker sheet
One artboard, `KBM/system — <source name>`, built incrementally with `write_html` (one group per call, inline styles, referencing the new tokens via `var(--…)`): color swatches (semantic + palette, with the token name and value on each), the type ramp (every `fontSize` as a live sample), the spacing scale, radii, and a components row (button/input/card/badge in their real states) built from the tokens. Per `references/extraction.md`.

### 5. Proposals board
If any Candidates exist, a second artboard `KBM/proposals — <source name>`: each proposed token as a swatch/sample with *why* it's inferred and what it would consolidate ("three near-#8A8A8A grays → one `--color-text-muted`"). The user approves by telling you, or edits the board; approved Candidates then get `create_tokens`.

### 6. Verify, hygiene, log
Final 2x `get_screenshot` of the sticker sheet — fix overflow, off-token swatches, mis-scaled samples. `rename_nodes` under `KBM/`, `finish_working_on_nodes`. Log to `.kbm/site-to-system.md`: source, tokens created (count by type), open proposals. Tell the user the token count and that the file now snaps to them.

## Failure modes to avoid

- **Inventing canon.** A guessed value created as a token silently is the cardinal sin — the whole file inherits it. Guessed values are Candidates on the proposals board, full stop.
- **Screenshot-derived values.** Read computed styles / the config. A hex off a JPEG is already wrong by a few points.
- **Flat color tokens.** Semantic tokens that hardcode hex instead of aliasing a palette ramp means the system can't be re-themed. `--color-primary: var(--palette-blue-600)`, not `--color-primary: #2563EB`.
- **Duplicate tokens.** `get_tokens` first; extend, don't re-create. Alias existing ones.
- **The everything-dump.** A 60-swatch sheet from a site with six real colors. Extract the *system*, not every one-off value the CSS happens to contain — one-offs are noise, and the discipline (Primer/Material/Atlassian) treats an un-tokenized one-off as a defect, not a token.
- **Skipping the sticker sheet.** Tokens with no visible board are invisible — the user can't see what they got. The sheet is how the system becomes real on the canvas.
