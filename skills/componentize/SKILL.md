---
name: componentize
description: Find repeated elements already on a Paper (paper.design) canvas and extract them into a named, organized component — the canonical version plus its variants (a button in default/hover/disabled, a card in its states) laid out as a labeled variant set you clone new instances from. Use whenever the user wants to componentize a design, turn repeated elements into a component, build a variant set, extract a button/card/row into something reusable, or clean up copy-pasted duplicates. Requires Paper Desktop open. Honest constraint: Paper clones are copies, not live Figma-style instances — this organizes the source of truth and the reuse path, it does not auto-propagate edits.
---

# Componentize

Figma's object model is components → variants → instances, and editing a master updates every instance. **Paper has no component primitive** — its reuse mechanism is `<x-paper-clone>`, which produces a *copy*, not a linked instance. So this skill does the honest, useful version of the Figma workflow: it finds elements that recur on the canvas, extracts a single **canonical component with its variants** into a named, organized set, and gives you one place to clone new instances from. What it does **not** do is make old copies update when you edit the master — Paper can't, and the skill never pretends otherwise.

That's still most of the value: a scattered pile of copy-pasted buttons becomes one labeled Button set with its states, named consistently, that you and other skills (`site-to-system`, `design-council`) can point at.

Read `references/paper-craft.md` (shared KBM conventions) and `references/detection.md` (finding repetition, choosing the canonical, laying out the variant set) before building.

## The contract

- **Repetition is evidence, not assumption.** Identify recurring elements by comparing structure and computed styles (`get_jsx`, `get_computed_styles`), not by eyeballing a screenshot. "These five are the same button" must be shown, not guessed.
- **Propose the component before extracting.** Present the detected group, the proposed canonical, and the variant axes ("Button: default / hover / disabled × sm / md") for approval. The user may split or merge before anything is built.
- **Be explicit about the clone limitation.** When you deliver, say it plainly: the variant set is the source to clone *from*; existing copies are not linked and won't update. Replacing in-place duplicates with clones (optional, on request) makes future edits a re-clone, not an automatic propagation.
- **Never mutate the originals silently.** The variant set is built on a components artboard. Only replace in-place duplicates with clones if the user asks, and mark what changed (`paper-craft.md` §4).

## Workflow

### 1. Preflight & scope
Preflight per `paper-craft.md`. Scope: a selected frame, an artboard, or the page. `get_tree_summary` for shape, `get_jsx` for structure.

### 2. Detect repetition
Find groups of nodes with matching structure and near-matching styles (`references/detection.md`): buttons, cards, list rows, badges, inputs. Cluster them; within a cluster, the differences across copies are the **variant axes** (state, size, emphasis). Ignore genuine one-offs.

### 3. Propose
For each cluster, present: what it is, how many instances, the proposed canonical (the cleanest / most-complete copy), the variant axes and their values, and a proposed name (`Button`, `Card/issue`). Stop for approval. Placeholder or inconsistent content across copies is worth surfacing — it's often why they drifted.

### 4. Build the variant set
On a components artboard `KBM/components — <scope>`, build the canonical and each variant as a clean, token-referencing version (reuse `var(--…)` tokens if the file has them — pairs with `site-to-system`). Lay variants in a labeled matrix (axis headers, one cell per combination), fixed-width label slots so the grid aligns (`paper-craft.md` vertical-lane rule). Name every layer under the component name. This set is the source of truth to clone from.

### 5. Optional: adopt in place
If the user wants existing duplicates replaced with clones of the canonical: `write_html` `<x-paper-clone node-id="…">` at each site (or `duplicate_nodes` the canonical and `move_nodes` into place), mark each with one change-pin, and state clearly that these are copies — editing the master later means re-cloning, not auto-update.

### 6. Verify, hygiene, log
Screenshot the variant set: every cell renders, the grid aligns, variants actually differ along their axis. `rename_nodes` under `KBM/`, `finish_working_on_nodes`. Log to `.kbm/componentize.md`: components extracted, variant axes, instance counts, whether adoption was applied.

## Failure modes to avoid

- **Pretending clones are instances.** The cardinal honesty failure. Paper copies don't propagate; say so every time.
- **Eyeballed repetition.** "These look the same" without comparing structure/styles. Two similar-looking rows can be built differently; cluster on evidence.
- **Componentizing one-offs.** Not every element wants to be a component. A thing that appears once is not a component; forcing it is noise (the token-warden over-tokenizing mistake in another form).
- **Missing a variant axis.** Extracting "Button" but dropping the disabled state that existed in the copies. The variants *are* the differences across instances — capture them.
- **Silent in-place edits.** Replacing the user's duplicates without asking, or without change-pins. Adoption is opt-in and attributed.
- **A misaligned matrix.** Variant cells that don't line up read as amateur. Fixed label slots, screenshot-verify the grid.
