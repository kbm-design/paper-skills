# Paper Craft — shared conventions for KBM skills on the Paper canvas

These conventions are shared by every KBM skill that works on a Paper file (Design Council, Site-to-System, Token Warden, Reality Check, Art Direction Sprints…). They exist so that every skill behaves like the same careful collaborator: evidence before opinion, copies before edits, tidy layers after.

## Contents

1. [Preflight](#1-preflight)
2. [The evidence loop](#2-the-evidence-loop)
3. [Never mutate the original](#3-never-mutate-the-original)
4. [The annotation language](#4-the-annotation-language)
5. [Verify your own work](#5-verify-your-own-work)
6. [Hygiene](#6-hygiene)
7. [Canonical / Candidate / Avoid](#7-canonical--candidate--avoid)
8. [Tool playbook](#8-tool-playbook)
9. [write_html quirks](#9-write_html-quirks)
10. [Memory files](#10-memory-files)

---

## 1. Preflight

The Paper MCP server only runs while Paper Desktop is open with a file loaded, at `http://127.0.0.1:29979/mcp`. Before doing anything:

- Call `get_basic_info`. If the connection fails, stop and tell the user to open Paper Desktop with their file, then retry. Do not fall back to guessing about the design.
- Confirm you are in the file the user means (file name and page name are in `get_basic_info`).
- Call `get_selection`. If the user said "this frame" or "my selection" and nothing is selected, ask them to select it rather than picking an artboard yourself — acting on the wrong frame wastes their trust and your tokens.

## 2. The evidence loop

Opinions about a design are only worth having when they cite the actual values. Before forming any judgment, gather in this order (cheapest first):

1. `get_tree_summary` — the shape of the design; how big the job is.
2. `get_jsx` (Tailwind format) — the single richest read: structure and styles in one call. Prefer this over walking nodes one at a time.
3. `get_computed_styles` — batch, on the specific nodes a finding will cite. This is where contrast ratios, real font sizes, and true spacing come from.
4. `get_screenshot` — how it actually looks. Request 2x when you'll examine detail.
5. `get_fill_image` / `get_font_family_info` — when a finding concerns imagery or proposes a type change.

A finding that says "the caption text is #8A8A8A on #F4F4F4 — contrast 2.1:1, below the 4.5:1 AA threshold" earns action. A finding that says "the text looks low-contrast" earns nothing. Compute contrast ratios from the actual computed colors; do not eyeball them from a screenshot.

## 3. Never mutate the original

The user's frame is their work. All edits land on copies:

- `duplicate_nodes` the frame first; apply fixes to the duplicate.
- The duplicate is placed beside the original (use `move_nodes`), never on top of it.
- The only thing ever added near the original is the annotation overlay (below), and it must be a single group that can be deleted in one gesture.
- Never `delete_nodes` on anything the user made. Deleting is only allowed on nodes a KBM skill created (identifiable by the `KBM/` layer-name prefix).

Why this matters beyond politeness: side-by-side originals and fixes are the artifact. The comparison *is* the deliverable.

## 4. The annotation language

All KBM skills annotate the canvas the same way, so the output is recognizable at a glance (and in screenshots people share). Annotations are written with `write_html`, inline styles only.

**Structure.** Two pieces:

1. **Pin overlay** — one absolutely-positioned group placed over the reviewed frame, containing numbered pins. Locked (`data-paper-locked`) and named `KBM/annotations — <frame name>`. Pins are small circles (20px, white number, 600 weight, 11px) positioned at the top-left corner of the node they reference, offset -10px so they sit on the corner rather than covering content.
2. **Findings board** — a separate artboard placed to the right of the frame, named `KBM/findings — <frame name>`, listing each pin number with its finding: claim, evidence (the measured values), severity, persona, and proposed fix.

**Severity palette.** Deliberately alien to any product palette so annotations never read as part of the design:

| Severity | Color | Meaning |
|----------|-------|---------|
| Blocker | `#E5484D` (red) | Breaks usability, accessibility failure, or data loss of meaning |
| Warning | `#FFB224` (amber) | Hurts quality; fix before shipping |
| Suggestion | `#3B9EFF` (blue) | Would improve; reasonable people may disagree |

**Board styling.** Neutral, mono-ish, opinionatedly plain: white background, `#111` text, system-ui/mono stack, 12–13px, 8px radius cards, one card per finding. The board never uses the audited product's fonts or colors — the reviewer must not be confused with the reviewed.

**Cap the pins.** More than ~12 pins on one frame stops being a review and becomes noise. Prioritize by severity; roll remaining minor items into a single "also noted" card on the findings board.

**Change pins (attribution).** When a skill applies changes to a duplicate, it marks *what it changed and who changed it* with a second pin family on the changed copy — visually distinct from problem pins so before/after can never be confused:

- Problem pins (on the original): severity-colored circles with numbers.
- Change pins (on the fixed copy): neutral dark chips (`#1C1C22` bg, white initial, 11px/600) with a 2px ring in the persona's color. Persona ring colors — deliberately distinct from the severity palette: Ada `#8E4EC6` (violet), Sol `#12A594` (teal), Quill `#D6409F` (pink), Nova `#46A758` (green), Vale `#B0B4BA` (silver).
- **One pin per change, not per node.** A sweep that touches 121 nodes gets one pin on a representative node or the affected section, with the count in its changelog entry. Confetti kills the artifact.
- Every change pin keys to an entry on the changelog card (below). Locked group, named `KBM/changes — <frame name>`.

## 5. Verify your own work

After writing anything to the canvas, take a final `get_screenshot` of everything you created (overlay, board, fixed duplicate) and actually look at it:

- Text overflowing its card? Pins drifted off their targets? Duplicate overlapping the original?
- Fix with `update_styles` / `move_nodes` before declaring done.

The screenshot check is not optional ceremony — `write_html` layout on the canvas does not always match what you pictured, and shipping a misaligned findings board undermines a skill whose whole message is craft.

## 6. Hygiene

How a skill leaves the file is part of its output:

- `rename_nodes` everything you created to human-readable names under the `KBM/` prefix. No `div`, no `Frame 47`.
- Call `finish_working_on_nodes` when done so the working indicator clears.
- Batch tool calls (`get_computed_styles`, `update_styles`, `set_text_content` all accept batches). One call with 20 nodes beats 20 calls.
- Tell the user exactly what you added and that deleting the `KBM/` groups removes every trace.

## 7. Canonical / Candidate / Avoid

When a skill infers values (tokens from a screenshot, intent from a layout), it labels them honestly:

- **Canonical** — read directly from the file or codebase; safe to act on.
- **Candidate** — inferred; present for approval, never silently apply.
- **Avoid** — conflicts with the product or would make future work worse.

Never present an inferred value as canon. The systems this discipline comes from (Primer, Material, Atlassian, Spectrum) treat an un-tokenized or un-sourced value as a defect; so do we.

## 8. Tool playbook

| Role | Tools | Rules of use |
|------|-------|--------------|
| Orient | `get_basic_info`, `get_selection`, `get_guide` | Always first. Confirm file + selection before acting. |
| Evidence | `get_tree_summary`, `get_node_info`, `get_children`, `get_jsx`, `get_computed_styles`, `get_screenshot`, `get_fill_image`, `get_font_family_info` | `get_jsx` is the cheapest deep read. Batch computed-styles calls. Check font availability before recommending a font. |
| Act | `duplicate_nodes`, `create_artboard`, `write_html`, `update_styles`, `set_text_content`, `move_nodes`, `rename_nodes`, `delete_nodes` | Duplicate before editing. Batch updates. `delete_nodes` only on `KBM/`-prefixed nodes. |
| Hygiene | `rename_nodes`, `finish_working_on_nodes` | Non-negotiable finish. |
| Ship | `export` | PNG/SVG/MP4; use 2x for anything shared publicly. |

## 9. write_html quirks

`write_html` parses HTML into canvas layers with these translation rules — write accordingly:

- **Inline styles only.** Class names and `<style>` blocks are dropped entirely. Every style must be a `style=""` attribute.
- **No rich text.** A bolded word inside a sentence is not possible; block elements with only inline children flatten to a single Text node. Structure copy so each distinct style is its own element.
- `layer-name="…"` sets the layer's label — use it on every element you'd otherwise have to `rename_nodes` afterward.
- `data-paper-locked` locks the layer; `hidden` hides it.
- `<x-paper-clone node-id="…">` clones an existing node in the file — use this to reference the user's own elements instead of recreating them.
- Images must be publicly-reachable URLs; use them sparingly in annotations (prefer pure HTML/CSS shapes).
- Everything gets `box-sizing: border-box`; inputs become frames with text children.

## 9b. Ordering nodes (move_nodes quirk)

`move_nodes` is unreliable for placing a child at a specific position in a **flex parent**: `before`, `after`, and `parentId`+`index` have all been observed to push the moved node to the **end** instead (e.g. `index: 2` and `before: X` both resolving to the last slot). Do not trust a single positional move to reorder.

**Reliable pattern:** to set a specific child order, issue ONE `move_nodes` batch that moves *every* child in the desired final order using just `{nodeId, parentId}` (no `before`/`after`/`index`). Each move appends to the end, so the batch order becomes the final order.

Corollary: `duplicate_nodes({parentId})` does **not** append at the end the way `write_html` insert-children does — so building an interleaved layout (label, item, label, item…) by alternating `duplicate_nodes` and `write_html` will scramble. Create everything first, then reorder with the append-in-order batch above.

## 10. Memory files

KBM skills that run repeatedly on the same file keep their memory in plain, human-editable files in the working directory, under `.kbm/` — not hidden inside the Paper file. Why: a visible file is diffable, greppable, editable by the user (changing a status by hand is a first-class way to give the skill instructions), readable by scheduled runs, and survives canvas cleanups.

Conventions:

- One file per skill per design file, named clearly: `.kbm/council-log.md`, `.kbm/reality-check.md`, etc. Key entries by frame name.
- Entries carry a stable id (frame + short slug), a status, first/last-seen dates, and a one-line note. Statuses are the skill's contract with the user — a memory the user edits is an instruction, and the skill obeys it without argument.
- Read the file at the start of every run; write it at the end. Never let canvas archaeology (reading leftover KBM layers) substitute for the log — layers get deleted, the log is the record.
