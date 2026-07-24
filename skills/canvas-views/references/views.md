# Views — manifest format, view types, and rendering recipes

Companion to canvas-views. The thesis in one line: **files/systems are the database, the agent is the backend, the canvas is the UI.** A view is a designed, honest, refreshable *rendering* of a system the user already trusts — never a second copy of the truth.

## Contents

1. [The view manifest](#1-the-view-manifest)
2. [View types & layout recipes](#2-view-types--layout-recipes)
3. [Freshness header](#3-freshness-header)
4. [Rendering conventions](#4-rendering-conventions)
5. [Data sources](#5-data-sources)

---

## 1. The view manifest

`.kbm/views.md` in the working directory. One entry per view. The manifest is what makes refreshes deterministic — re-render from the manifest, never re-improvise the query or layout. Hand-edits to the manifest are instructions (same contract as council-log).

```
- name: skill-roadmap
  source: notion · page "Paper-Design" · the two prioritization tables
  type: status-board
  columns: [Shipped, Next up, Candidates, Backlog]
  card: title + one-line hook + effort chip
  artboard: KBM/view — skill-roadmap
  limit: 30 (overflow noted)
  created: 2026-07-22 · last-rendered: 2026-07-22
```

Fields: `name`, `source` (system + query/filter, specific enough to re-run), `type`, layout params (columns/lanes/grouping), `card` (what each item shows), `artboard`, `limit`, dates. Add freely — the manifest serves the re-render, not a schema.

## 2. View types & layout recipes

All rendered with `write_html`, inline styles only, one artboard per view.

**status-board** — items in columns by state (sprint boards, roadmaps-by-stage, pipeline). Columns as flex row of equal-width lanes; column header = state name + count chip; cards stacked with 8px gap: title (13–14px/600), one meta line (12px, secondary), optional chips. Cap ~8 cards per column visually; overflow becomes "+ N more" at column foot.

**roadmap-lanes** — horizontal lanes per track/initiative, items placed left→right by time bucket (weeks/months across the top). Use when sequence matters more than status.

**repo-map** — architecture diagram from a codebase: boxes per module/service (name + one-line role + key files count), arrows as simple positioned lines or, cleaner, a layered top-down flow (entry → core → data). Derive from reading the repo, not from guessing; label edges only where the relationship is certain.

**log-board** — render `.kbm/` state (council-log findings by status, rive-bridge inventory). The self-referential view; statuses as columns.

**table** — dense list with columns (title, owner, status, date). Use when items > ~15 and scanning beats spatial grouping. Right-align numbers, tabular feel.

**metric-tiles** — small grid of stat cards (value large, label small, delta chip). For analytics/API pulls. Follow restraint: one accent color for deltas, neutral everything else.

Choosing: status when state matters, lanes when time matters, table when volume matters, tiles when numbers matter, map when structure matters.

## 3. Freshness header

Every view carries a header strip — this is non-negotiable, it's what separates a view from a fake dashboard:

```
<view title>          <source> · <filter> · rendered <date time> · <N> items<, M truncated>
```

Example: `Skill Roadmap — Notion · Paper-Design page · rendered 2026-07-22 09:40 · 18 items`. The canvas must never imply liveness it doesn't have. If data was truncated or a source call partially failed, say so in the header line, on the canvas, not just in chat.

## 4. Rendering conventions

- Artboard named `KBM/view — <name>`. **Refresh = replace-in-place**: delete the existing artboard of that exact name, then render fresh at the same position. Never stack stale copies; never leave two versions of one view.
- **Use the file's tokens when present** — the view should look like the user's product, not a generic kanban. No tokens → neutral, restrained default (near-black/white, one accent, 8px radius, system-ui/mono for numbers).
- Inline styles only; no rich text within a text node; `layer-name` on every element; no external images unless publicly hosted (prefer none). All the write_html rules from paper-craft apply if that reference is installed.
- Deterministic layout: same data → same layout. Order items by the manifest's stated sort, not vibes.
- Verify with a final `get_screenshot`; fix overflow before declaring done. `rename_nodes` strays, `finish_working_on_nodes`.
- **The canvas is never the record.** Never write state into a view that doesn't exist in the source. If the user edits a card by hand, that's their annotation — don't sync it anywhere, and don't overwrite it silently on refresh without mentioning it.

## 5. Data sources

- **Linear / Notion / GitHub etc.** — via the MCPs connected in the session. If a needed MCP isn't connected, say exactly which one and stop; don't fabricate placeholder data into a view, ever. A view with fake data is worse than no view.
- **Repo** — read files directly (this is the strongest source: diffable, versioned, agent-native).
- **`.kbm/` files** — the skill family's own state.
- **APIs** — fetch via the shell when the user provides an endpoint; snapshot semantics, noted in the header.
- Respect `limit` from the manifest; state truncation. Big queries: fetch once, render once — don't hammer sources per-card.
