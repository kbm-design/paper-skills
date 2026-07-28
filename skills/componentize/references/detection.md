# Detection — finding repetition, choosing the canonical, the variant set

## 1. What counts as repetition

A component candidate is a group of nodes that share **structure** and mostly share **styles**, differing along a small number of axes. Detect on evidence, not appearance:

- **Structure** — same child shape from `get_jsx` (a frame with an icon slot + label + optional trailing element is one structure). Two things that render alike but have different trees are *not* the same component.
- **Styles** — `get_computed_styles` across the candidates. Matching radius, padding, type, and token references; the colors/labels/states are what vary.

Typical finds: buttons, icon buttons, list/table rows, cards, badges/tags, inputs, avatars, nav items. A cluster needs at least ~2–3 real occurrences to be worth extracting — below that it's a one-off.

## 2. The variant axes

Within a cluster, the *differences* across copies are the variant axes. Name them:

- **State** — default / hover / pressed / disabled / selected / error.
- **Size** — sm / md / lg (from padding + type differences).
- **Emphasis** — primary / secondary / ghost / danger.
- **Content kind** — for cards/rows: text / image / link / color (like a Shelf card's kinds).

Most components have one or two real axes. If you find five, you're probably looking at two components, not one — split them.

## 3. Choosing the canonical

The canonical is the version every variant derives from. Pick:
1. The most **complete** copy (has all the parts, nothing missing).
2. The most **token-referencing** copy if the file has tokens (hardcoded ones are drift — prefer the clean one, or clean it as you extract).
3. The **default state** at the **medium size** as the base cell.

If no single copy is clean, build the canonical from the best parts and flag it as a constructed base (Candidate per `paper-craft.md` §7), not lifted verbatim.

## 4. The variant set (sticker sheet)

On `KBM/components — <scope>`, lay the component as a labeled matrix:

- **Axis headers** — states across the top, sizes down the side (or whatever the two axes are). Small muted labels.
- **Cells** — one per combination, each a real, token-referencing build. Empty combinations (no `disabled × lg`) are left blank, not faked.
- **Alignment** — fixed-width label slots and consistent cell sizes so columns line up (`paper-craft.md` vertical-lane rule). After building the grid, screenshot and trace the lanes.
- **Naming** — every layer under the component name: `Button/default·md`, `Button/hover·md`. This is what makes it clonable and legible.
- **One component per section** — if the scope has a Button and a Card, two matrices, clearly headed.

## 5. Clone semantics — the honest part

`<x-paper-clone node-id="…">` (in `write_html`) and `duplicate_nodes` both produce **independent copies**. There is no link back to the canonical; editing the canonical later does not change prior clones. Consequences to state to the user, every time:

- The variant set is a **source to clone from**, not a master that drives instances.
- "Updating the component" = edit the canonical, then re-clone where needed (or re-run this skill's adoption step).
- This is a Paper limitation, not a skill choice. If Paper adds a real component primitive, this skill upgrades to use it; until then, copies are copies.

Design around it: keep the canonical set as the one place to look, name consistently so clones are findable, and lean on tokens (`var(--…)`) so a *token* edit — which Paper *does* propagate — moves every clone that references it. Token-level change is the closest thing to instance-update Paper offers; prefer components built from tokens for exactly this reason.

## 6. Adoption (optional)

If replacing in-place duplicates with clones: for each site, either `write_html` an `<x-paper-clone>` of the canonical or `duplicate_nodes` + `move_nodes`. One change-pin per site (or per section if many), keyed to a changelog card. Always paired with the plain statement that these are unlinked copies.

## 7. Log

`.kbm/componentize.md`: one entry per component — name, structure signature, variant axes + values, instance count found, canonical source (lifted vs constructed), whether adoption ran. Read at start; entries let successive runs recognize an already-extracted component instead of re-proposing it.
