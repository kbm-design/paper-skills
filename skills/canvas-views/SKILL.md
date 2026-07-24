---
name: canvas-views
description: Render designed, refreshable views of external systems onto a Paper (paper.design) canvas via the Paper MCP — a Linear sprint as a status board, a Notion database or roadmap as lanes, a repo as an architecture map, analytics as metric tiles, or .kbm logs as a board. Read-only in v0 - the source system stays the record; the canvas is the designed lens. Use this whenever the user wants to see their sprint/roadmap/tasks/docs/data "on the canvas" or "in Paper", asks for a board/dashboard/map of some system, says "render my Linear/Notion/repo", or asks to refresh an existing view. Requires Paper Desktop running with a file open, plus whatever source MCP the view needs (Linear, Notion, etc.) connected in the session.
---

# Canvas Views

Files and systems are the database, the agent is the backend, the canvas is the UI. This skill renders honest, designed views of systems the user already trusts — it never becomes a second copy of the truth, and it never fakes liveness.

Before starting, read `references/views.md` (manifest format, view types, layout recipes, freshness rules). If `paper-craft.md` is installed (design-council), its conventions apply on the Paper side.

## The three promises

1. **The source stays the record.** Views are read-only renderings. Nothing is written back (that's a future Markup integration); no state exists on canvas that doesn't exist in the source.
2. **Freshness is never lied about.** Every view carries a header: source, filter, rendered-at timestamp, item count, truncation. Static HTML doesn't update itself — the header says exactly when this snapshot was taken.
3. **Refresh replaces, never stacks.** One view = one artboard, replaced in place. Stale copies are deleted, not accumulated.

## Workflow

### 1. Preflight and manifest

Paper preflight: `get_basic_info`, confirm the file. Read `.kbm/views.md` if it exists — it defines every known view (source, query, type, layout). A "refresh" request maps to a manifest entry; a new view request will create one.

### 2. Define the view (new) or load it (refresh)

**New view:** agree the spec in one short exchange — source + filter ("Linear, current sprint, my team"), view type (status-board / roadmap-lanes / repo-map / table / metric-tiles / log-board — selection guide in `views.md`), and what each card shows. Default sensibly if the user's ask is clear; don't interrogate. Write the manifest entry before rendering — the manifest is what makes every future refresh deterministic.

**Refresh:** load the entry, re-run its exact source query, re-render its exact layout. Hand-edits to the manifest are instructions.

### 3. Fetch honestly

Pull the data via the source MCP or files. Hard rules: if the needed MCP isn't connected, name it and stop — **never render placeholder data into a view**; respect the manifest's `limit` and state truncation in the header; fetch once, render once.

### 4. Render

- Delete any existing `KBM/view — <name>` artboard (replace-in-place), then `create_artboard` at the same position and `write_html` the view per the recipe in `views.md`.
- Freshness header first, always.
- Use the file's tokens when present so the view looks like the user's product; otherwise the restrained neutral default.
- Inline styles only, `layer-name` everything, no rich text per node.

### 5. Verify and finish

Final `get_screenshot`; fix overflow or collisions. `finish_working_on_nodes`. Update the manifest's `last-rendered`. Report in chat, short:

```
Rendered "<name>" — <type>, <N> items from <source> (rendered <time>).
Refresh anytime with "refresh <name>". Manifest: .kbm/views.md
```

If the user asks for the view to stay current, offer the loop honestly: a scheduled local run ("refresh my views each morning") — the canvas cannot update itself, and Paper Desktop must be open when the loop fires.

## Failure modes to avoid

- **The fake dashboard.** Rendering placeholder/invented data, or omitting the freshness header. A view that lies about its data or its age poisons trust in every view.
- **The second source of truth.** Writing state to the canvas that isn't in the source, or treating canvas edits as data. The user's hand-edits are annotations — never overwrite them silently on refresh; mention what a refresh will clobber.
- **The stack of staleness.** A second copy of a view instead of replace-in-place.
- **The generic kanban.** Ignoring the file's tokens when they exist. The whole point is that it looks like *their* product.
- **The wall of everything.** Rendering 200 items because the source had 200. Cap, truncate visibly, and say so.
- **Re-improvised refreshes.** Re-deciding query or layout on refresh instead of reading the manifest — same data must produce the same view.
