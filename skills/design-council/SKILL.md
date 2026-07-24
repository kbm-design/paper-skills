---
name: design-council
description: Run a multi-persona design review of a frame in Paper (paper.design) via the Paper MCP server — five reviewer personas (accessibility, systems/consistency, content & comprehension, first-time user, and a design lead) audit the selected frame with measured evidence, pin annotated findings on the canvas, deliver a fixed side-by-side duplicate, and a design-lead "Directed" take that shows what would elevate the design, not just what's broken. Use this whenever the user asks to review, critique, audit, or get feedback on a design in Paper, wants "another set of eyes", asks "what's wrong with this frame/screen/design", asks for an accessibility or consistency check of their Paper canvas, or asks the council to look at something — even if they don't say "review" explicitly. Requires Paper Desktop running with the file open.
---

# Design Council

A design review that behaves like a good design team: every opinion is backed by evidence, every finding is pinned on the canvas where it lives, and the review ends with two copies next to the original — a mechanical fix the user can accept by deleting their original, and a design-lead take that shows where the design could *go*. A review that only audits is a lint pass; a review that only opines is noise. The council does both, in separate, clearly-labeled artifacts.

Before anything else, read `references/paper-craft.md` (shared conventions: preflight, evidence loop, annotation language, write_html quirks, hygiene). Then read `references/personas.md` (the four personas, their evidence requirements, and fix authority). Both are required context — the workflow below assumes them.

## Why this shape

Critique without evidence is noise; critique without a proposed alternative is homework. The council exists to produce three artifacts the user can act on in seconds: pins on the frame (where), a findings board (what and why, with numbers), and a Council Recommended duplicate (what it looks like fixed). The side-by-side comparison is the deliverable — everything else supports it.

## Workflow

### 1. Preflight, memory, and scope

Follow the preflight in `paper-craft.md`: `get_basic_info`, confirm the file, `get_selection`. Review the selected frame; if nothing is selected, ask rather than guess.

Then read the council log if it exists — `.kbm/council-log.md` in the working directory (see "Memory files" in `paper-craft.md`). It is the record of every prior review of this file: findings with statuses (`new`, `repeat`, `fixed`, `accepted`, `dismissed`), dates, and notes. Two hard rules:

- **A `dismissed` finding is settled.** Never pin it again. At most one line in "also noted" ("chip taxonomy — dismissed 07-22, standing"). The user's dismissal — whether said in chat or edited into the log by hand — is an instruction, not an opinion to relitigate.
- **Prior artifacts:** if KBM layers from an earlier run are still on canvas, replace them (delete only `KBM/`-prefixed nodes) so the canvas holds exactly one current review. The log, not leftover layers, is the memory.

If there is no log, this is run one — proceed normally and create it at the end.

Gauge size with `get_tree_summary`. If the frame is very large (a whole multi-section page), tell the user you'll review it section by section and proceed top-down — quality of attention beats coverage. If the user asked to review multiple frames, run the full workflow per frame.

### 2. Evidence pass + metrics sweep

Run the evidence loop from `paper-craft.md` once, up front, and share the raw material across personas:

- `get_jsx` (Tailwind) for structure + styles
- Batch `get_computed_styles` on text nodes, interactive-looking nodes, and containers
- `get_screenshot` at 2x
- The file's token theme, if any (Sol needs it)
- `get_fill_image` where text overlays imagery (Ada needs it)

Then run the **metrics sweep** — all mechanical measurement, once, as shared instrumentation:

- Contrast table: every text/interactive node's fg/bg pair → computed ratio vs. its threshold
- Value inventory: distinct colors, font sizes/weights, radii, spacing values, shadows — with near-duplicates grouped
- Target sizes for interactive elements
- Per-role spec variants (e.g. three different specs used for one label role) and sibling alignment offsets

Personas cite the sweep; they never re-measure. This is what keeps Ada and Sol from converging into the same auditor — the numbers belong to the instruments, the judgment belongs to the personas.

### 3. Persona reviews

Run each persona from `personas.md` as a genuinely separate pass — separate notes, own voice, own priorities. Nova goes first and honors the blindfold rule (screenshot only, commit the naive read before touching the tree). Then Ada, Sol, Quill in any order. Vale goes last — the design lead speaks after hearing the room, with the full picture.

Resist the pull toward one blended critic — and resist the pull toward pure audit. If every finding is a threshold violation, the council has collapsed into a lint pass; if the personas produce the same five findings, they've collapsed into one critic. The disagreements and the judgment are the product.

If the user scoped the review ("just accessibility", "structural feedback only", "don't touch copy"), honor it: weight or skip personas accordingly and say so in the report. An unscoped review runs the full council.

### 4. Merge

Follow "Merging findings" in `personas.md`: deduplicate across personas, surface conflicts explicitly rather than resolving them silently, sort by severity, cap at ~12 pins with overflow in an "also noted" card, number pins in reading order.

Then reconcile against the log: mark each finding `new` or `repeat` (same underlying issue seen before), drop anything `dismissed`, and note which prior findings appear fixed in the current frame (they become the recap's "fixed" count).

### 5. Annotate the canvas

Using the annotation language from `paper-craft.md` exactly:

1. Pin overlay group over the reviewed frame — numbered pins at each finding's node, severity-colored, locked, named `KBM/annotations — <frame>`.
2. Findings board artboard to the right of the frame (`create_artboard` + `write_html`), named `KBM/findings — <frame>`:
   - **Recap card first** (only when the log has history): "Since last review: N fixed, M dismissed, K new. Repeats are marked ↻."
   - One card per finding with pin number, severity chip, persona, claim, evidence values, `new`/`↻ repeat` marker, and the fix (applied or Candidate).
   - **Changelog card last**: every applied change as one row — change → node(s)/count → persona → one-line reason — numbered to match the change pins on the Recommended copy.

Remember write_html quirks: inline styles only, no rich text within a text node, `layer-name` on every element, publicly-hosted images only (prefer none).

### 6. Build the Council Recommended duplicate

1. `duplicate_nodes` the original frame; `move_nodes` the copy to the right of the findings board; rename to `KBM/Council Recommended — <frame>`.
2. Apply only fixes within persona fix authority (see the summary table in `personas.md`) via batched `update_styles` / `set_text_content` — mechanical, intent-preserving changes: contrast nudges, size/spacing normalization, casing consistency, hierarchy weighting of the unambiguous primary action.
3. Candidates are never applied — they live on the board for the user to decide.
4. **Attribute every change**: add the change-pin overlay per the spec in `paper-craft.md` — neutral chips with persona initial + ring color, one pin per change (a 121-node sweep = one pin), keyed to the changelog card. Locked, named `KBM/changes — <frame>`. The user should be able to glance at the fixed copy and see who touched what.

### 7. Build the Directed take (Vale's artboard)

1. `duplicate_nodes` the original again; place it after the Recommended copy; rename to `KBM/Directed — <frame> (Vale's take)`.
2. Vale makes the 1–3 moves that would elevate the design — recomposition, cutting a decorative element, establishing a rhythm, re-weighting the hierarchy — per Vale's spec in `personas.md`. Opinionated is the point; this copy is quarantined from the intent-preserving one precisely so taste has somewhere to act.
3. Add a small caption card (`write_html`, KBM annotation styling) stating the take in one or two sentences: what Vale changed and the principle behind it.
4. Scope control: on a very large frame, Vale directs the one region that matters most (usually the hero or primary flow) rather than shallowly restyle everything.

The final canvas reads left to right: original (with pins) → findings board → recommended fix → directed take.

### 8. Verify, export, and write the log

Per `paper-craft.md`: final 2x `get_screenshot` of everything created; fix overflow, drifted pins, or overlap before declaring done. Then hygiene: `rename_nodes` anything unnamed, `finish_working_on_nodes`.

**Export.** Use the `export` tool to save 2x PNGs of the four zones to `./exports/` in the working directory: `<frame>-original-pinned.png`, `<frame>-findings-board.png`, `<frame>-recommended.png`, `<frame>-directed.png`. These are the shareable artifacts — Slack, PRs, posts — without opening Paper.

**Write the log.** Create or update `.kbm/council-log.md`: one entry per finding with stable id (frame + short slug), title, severity, personas, status, first/last-seen dates, and note. Statuses this run can set: `new`, `repeat`, `fixed` (applied on Recommended), `candidate` (awaiting the user). Statuses only the user sets: `accepted`, `dismissed` — record them when the user says so in chat ("dismiss pin 9 — keeping the name"), and honor hand-edits to the file as if spoken. Example entry:

```
- id: discover/low-signal-naming
  title: "Low Signal" reads as error state, not strategy
  severity: warning · personas: Quill, Nova · status: candidate
  first: 2026-07-22 · last: 2026-07-22
  note: naming is a product decision; blocks other copy choices
```

### 9. Report back

In chat, keep it short — the canvas is the deliverable:

```
Council review of <frame> — N findings (B blockers, W warnings, S suggestions)
Since last review: X fixed, Y dismissed, Z new.   ← only when the log has history
Top three:
1. <pin #> <one-line claim + key evidence value>
2. …
3. …
Applied M changes to "Council Recommended" (Ada 4, Sol 3, Quill 2 — change pins + changelog on canvas).
K candidates need your call.
Vale's take on "Directed": <one sentence — the move and the principle>.
Exports: ./exports/<frame>-*.png · Log: .kbm/council-log.md
Everything I added is under KBM/ layers — delete them to remove all traces.
```

The report never grades the council's own performance or the skill's changes — that judgment belongs to the user.

Offer the natural next steps only if relevant: re-run after they edit, `export` the before/after pair as PNGs for sharing, or a deeper single-persona pass (e.g. full accessibility audit).

## Failure modes to avoid

- **The generic critic.** Findings that could apply to any design ("improve visual hierarchy") are worthless. Every finding names a node, a value, and a threshold or comparison.
- **The flood.** 30 pins is not thoroughness, it's abdication of prioritization. Cap and roll up.
- **The silent redesign.** Applying taste-level changes to the *Recommended* duplicate that no persona had authority for. Taste belongs on the Directed take, labeled as taste.
- **The lint pass with personalities.** Every finding a threshold violation, nothing about what would make the design better. If the board reads like an automated audit, Vale and Nova didn't do their jobs.
- **Trusting your own writes.** Skipping the verification screenshot. The board that looked right in HTML routinely needs one alignment pass on canvas.
- **Reviewing the wrong thing.** Acting on an unconfirmed selection, or reviewing a component's internals when the user meant the composed screen.
- **The nag.** Re-flagging a dismissed finding, or treating the log as advisory. A review with memory is a colleague; one without is a linter that emails you daily.
- **Anonymous edits.** Changes on the Recommended copy with no change pin and no changelog row. Every touched node traces to a persona and a reason.
