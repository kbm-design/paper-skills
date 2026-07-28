# Naming — what a good name is, what's an orphan, what's safe to flatten

## 1. What a good layer name is

A name says what the thing **is**, so someone scanning the tree understands the design without opening each node. Derive it, in order of preference:

1. **Its content** — a Text node's text ("Sign in" → the button is `Sign in button` or `Button/sign-in`); an image fill → `Avatar`, `Hero image`.
2. **Its role** — a horizontal row of nav items → `Nav`; a repeated card → `Card`; the top bar → `Header`; the wrapping frame of a screen → the screen's name.
3. **Its structure** — a column of rows → `List`; a grid → `Grid`.

Good vs bad:

| bad | good | why |
|---|---|---|
| `Frame 47` | `Header` | says what it is |
| `Rectangle` | `Avatar` | named by content |
| `Group 12` | `Toolbar actions` | named by role |
| `Frame 47 → Container` | `Session card` | "Container" is just another vague name |

Match the file's existing convention if it has one (`Button/primary` vs `PrimaryButton` — follow what's already there). Don't impose `KBM/` on the user's own layers — that prefix is for nodes *this* or other KBM skills created, not for renamed user content.

## 2. Orphans — what's safe to delete

Only nodes that are **provably inert** — they render nothing and hold nothing:

- **Zero-size** — width or height 0 (a collapsed leftover).
- **Empty frames** — a frame/group with no children and no visible fill/border.
- **Fully hidden leftovers** — `hidden`/opacity-0 nodes that are clearly abandoned (no name, no content), *not* an intentionally-hidden variant the user toggles.

When unsure, **leave it and note it.** A faint element, an off-canvas-but-referenced node, an intentionally-hidden state — none of these are orphans. Deleting something that renders (however faintly) is the worst outcome of this skill; conservatism is correct. Every deletion is approved explicitly.

## 3. Flattening — when a wrapper is truly redundant

A single-child wrapper is a candidate for flattening **only if it adds no layout**. "Has one child" is necessary but not sufficient. A wrapper is *load-bearing* (leave it) if it provides any of:

- padding or margin around the child,
- a background fill, border, or shadow,
- a clip/overflow boundary or border-radius mask,
- a flex/positioning context the child depends on,
- a size different from the child's.

A wrapper is *redundant* (safe to flatten) only when it's a bare pass-through: same size as its child, no fill/border/padding, no clip. Flatten by `move_nodes` (reparent the child to the wrapper's parent at the wrapper's position), then delete the now-empty wrapper — never delete-and-recreate.

## 4. Preserve node identity

Renaming, reparenting, and flattening must keep node ids stable:
- `rename_nodes` changes the label only — id preserved.
- `move_nodes` reparents — id preserved.
- **Never** delete a node and recreate an equivalent to "reorganize" — it mints a new id and breaks every reference (this and other skills' `.kbm/` logs keyed by node, clone sources, the user's own selections).

## 5. The before/after proof

The skill's safety claim is "the design is unchanged." Prove it: `get_screenshot` of the scope before applying and after. They must be pixel-identical. Any visible difference means a rename/flatten touched something load-bearing — revert that change. This check is not optional; it is what separates a safe tidy from silent damage.

## 6. Log

`.kbm/layer-hygiene.md`, by scope: renames applied (or by pattern for large sets), wrappers flattened, orphans deleted, and — importantly — nodes deliberately **left alone** with the reason (so a rerun doesn't re-propose deleting the intentionally-hidden variant it already spared). A user note in the log is an instruction for next run.
