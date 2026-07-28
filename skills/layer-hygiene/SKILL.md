---
name: layer-hygiene
description: Tidy a Paper (paper.design) file's layer tree — rename cryptic layers ("Frame 47", "Rectangle") to semantic names based on what they actually are, flag and remove true orphans (empty frames, zero-size nodes, hidden junk), and flatten redundant single-child wrappers. Use whenever the user wants to clean up layers, rename layers, organize the layer tree, fix messy naming, or tidy a file before handoff. Requires Paper Desktop open. This is the one skill that edits the user's own nodes in place — but only their names and structure, never their visual design — and always proposes before applying.
---

# Layer Hygiene

The unglamorous, universal chore: a file full of `Frame 47`, `Rectangle`, `Group 12`, empty leftover frames, and wrappers that wrap a single child. This skill reads the tree, proposes a tidy, and — on approval — applies it. It is the "second set of hands" for the boring part nobody wants to do by hand.

**This skill is the deliberate exception to `paper-craft.md` §3 ("never mutate the original").** Renaming and regrouping a user's own layers *is* the job, and it's safe precisely because it touches only **names and structure, never visual properties** — the design looks pixel-identical before and after. That safety is the whole license; the moment a change would alter how anything *looks*, it's out of scope.

Read `references/paper-craft.md` (shared KBM conventions) and `references/naming.md` (what a good name is, what's an orphan, what's safe to flatten) before touching anything.

## The contract

- **Names and structure only, never appearance.** Rename layers, regroup, flatten redundant wrappers, delete true orphans. Never change a fill, size, position, font, or spacing. A screenshot before and after must be identical.
- **Propose, then apply.** Present the rename map and the structural changes as a plan the user approves (or edits) before anything runs. Batch the application.
- **Deletion is conservative.** Only nodes that are provably inert — zero-size, empty frames with no children, fully-hidden leftovers — are proposed for deletion, and only on explicit approval. When unsure, leave it and note it. Never delete something that renders.
- **Evidence-based names.** A layer's name comes from what it *is* — its content (`get_jsx` / text), its role (a row of nav items → `Nav`), its position in the tree — not a guess from a thumbnail.

## Workflow

### 1. Preflight & scope
Preflight per `paper-craft.md`. Scope: a frame, an artboard, or the page. `get_tree_summary` for the shape and the bad names; `get_jsx` where content is needed to name well.

### 2. Build the tidy plan (don't apply yet)
Per `references/naming.md`, assemble three lists:
- **Renames** — `Frame 47 → Header`, `Rectangle → Avatar`, each with the evidence (what the node contains/does).
- **Flattens** — single-child wrappers that add nesting without layout purpose, safe to unwrap.
- **Orphans** — zero-size nodes, empty frames, hidden leftovers proposed for deletion, each with why it's inert.

### 3. Present for approval
Show the plan as a compact report — counts and the notable changes ("38 renames, 3 wrappers flattened, 5 empty frames to delete"). For a large tree, list the structural changes and orphan deletions in full (those are the ones with consequences) and summarize the renames by pattern. The user approves, or edits the plan (a name they'd rather use is an instruction).

### 4. Apply
On approval, batched:
- `rename_nodes` for the rename map (one call, many nodes).
- Flatten wrappers with `move_nodes` (reparent the child up, then remove the empty wrapper) — never by deleting-and-recreating, which loses node identity.
- `delete_nodes` only the approved orphans.
After applying, **screenshot and compare to before** — pixel-identical confirms you changed only names/structure. If anything moved, you flattened something load-bearing; undo it.

### 5. Hygiene & log
This skill's *output* is a clean tree, so there's little of its own to clean — but still `finish_working_on_nodes`. Log to `.kbm/layer-hygiene.md`: what was renamed/flattened/deleted, by scope, and any nodes left alone with a note (so a rerun doesn't re-propose them).

## Failure modes to avoid

- **Changing appearance.** The one unforgivable error. If the before/after screenshots differ, you touched something visual — revert it. Names and structure only.
- **Flattening a load-bearing wrapper.** A single-child frame that provides padding, a background, or a clip is *not* redundant. "Single child" is necessary but not sufficient — check it adds no layout before unwrapping.
- **Deleting something that renders.** Aggressive orphan removal that nukes a faint or off-canvas element the user wanted. Conservative: inert-and-provable only, on approval.
- **Applying without approval.** Renaming a user's whole tree unprompted, even "obviously better" names. Propose first; naming is opinionated and theirs to veto.
- **Guessed names.** `Frame 47 → Container` is not a tidy — it's a different vague name. A good name says what the thing *is*, read from its content.
- **Losing node identity.** Delete-and-recreate to "reorganize" breaks every reference (other skills' logs, clone sources). Use `move_nodes`/`rename_nodes`, which preserve ids.
