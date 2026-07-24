---
name: token-warden
description: Governance for Paper (paper.design) design tokens — audits a file for hardcoded values that should reference tokens, proposes consolidations ("these three grays are one token"), applies them on approval, and can emit a matching CSS-variables patch so the design file and a codebase stay in sync. Because Paper tokens are MCP-only (no UI exists), this is the missing token manager plus an opinionated linter in the "no unsafe raw values" tradition. Use whenever the user wants to tidy or govern their Paper tokens, find hardcoded values, consolidate near-duplicate colors/spacing, check design/code token drift, or run a token audit. Requires Paper Desktop open. Reports on the canvas; never mutates the user's frames without approval.
---

# Token Warden

Tokens are the file's contract with itself. In Paper they can only be created or edited through the MCP — **there is no token UI** — so a file's tokens drift silently: a designer types `#8A8A8A` because reaching for the token is friction, and three sessions later there are four grays that were meant to be one. This skill is the manager that keeps that from happening, with a linter grounded in the discipline that treats an un-tokenized raw value as a defect (Atlassian's "no unsafe raw values", Primer/Spectrum density rules).

It **reports and proposes; it applies only on approval.** Nothing about the user's design changes until they say so.

Read `references/paper-craft.md` (shared KBM conventions) and `references/linting.md` (the drift rules, the consolidation heuristics, the CSS-var sync) before auditing.

## What it does, in one line

Walk the file's computed styles, compare every value against the token set, and surface three things: **hardcoded values that should be a token**, **near-duplicate tokens that should be one**, and **design↔code drift** — as an annotated report on the canvas, applied only where the user agrees.

## The contract

- **Evidence, not eyeballing.** Every finding cites the node, the raw value, and the token it should reference or consolidate into — read from `get_computed_styles` and `get_tokens`, never a screenshot (`paper-craft.md` §2).
- **Propose, then apply.** Consolidations and retokenizations land on an annotated report first. Apply with `set_tokens` / `update_styles` only on approval, and only ever mark up copies or the tokens themselves — never rewrite the user's frame silently (`paper-craft.md` §3).
- **A near-miss is a finding.** A value that is *close to* a token but not it (`#8A8A8B` vs the `--color-text-muted` `#8A8A8A`) is the most valuable catch — it's the drift the token system exists to prevent.

## Workflow

### 1. Preflight & read the system
Preflight per `paper-craft.md`. Then `get_tokens` (json) for the full token set, and `get_tokens` with `format: "css"` if a codebase sync is in scope. This is the ruler everything is measured against. If the file has *no* tokens, stop and point the user at `site-to-system` — there's nothing to govern yet.

### 2. Walk & measure
`get_tree_summary` for shape, then batched `get_computed_styles` across the nodes that carry visual values (fills, text colors, spacing, radii, type). Build the audit set: for each value, the nearest token and the distance to it.

### 3. Classify findings
Per `references/linting.md`, each value is one of:
- **Tokenized** — already references a token. Fine, skip.
- **Exact raw** — a literal value that equals a token's value but doesn't reference it. Retokenize (point it at the token).
- **Near-miss** — close to a token but not equal (color ΔE within threshold, spacing off by ≤2px, radius off by ≤2px). Propose snapping to the token, flag the drift.
- **Orphan** — a raw value with no nearby token. Either a genuine one-off (leave, note it) or a missing token (propose creating one). Cluster orphans — three near-equal grays are *one* proposed token, not three.

### 4. Report on the canvas
A `KBM/token-audit — <file>` findings board (annotation language from `paper-craft.md` §4): one card per finding — the node(s), the raw value, the proposed token, the count affected, and severity (exact-raw = Warning, near-miss = Warning, orphan cluster = Suggestion). Consolidation proposals lead ("4 grays → 1 `--color-text-muted`, 37 nodes"). Cap the pins; roll minor items into an "also noted" card.

### 5. Apply on approval
For what the user approves:
- **Retokenize / snap**: `update_styles` on the affected nodes to reference `var(--token)` (batched). Mark changed nodes with change-pins (`paper-craft.md` §4), one pin per consolidation with the count in its changelog entry.
- **New token**: `create_tokens` for an approved orphan cluster, then point the nodes at it.
- **Rename / retire**: `set_tokens` `newName` or `delete` for tokens the audit found redundant (alias the loser to the winner first if anything still references it).

### 6. Optional: code sync
If a codebase is in scope, emit a CSS-variables patch (`:root { … }`) from `get_tokens` `format: "css"` (or `tailwind`) so the repo's variables match the file — a small reviewable diff, not an apply. Per `references/linting.md`.

### 7. Verify, hygiene, log
Final 2x `get_screenshot` of the report and any changed copies. `rename_nodes` under `KBM/`, `finish_working_on_nodes`. Log to `.kbm/token-warden.md`: findings by class, what was applied, what's still proposed. Statuses the user edits are instructions on the next run (a finding marked `accepted` is not re-raised).

## Failure modes to avoid

- **Silent retokenizing.** Pointing a user's node at a token without approval — even when "obviously right" — breaks the propose-then-apply contract. Report first.
- **Splitting what should merge.** Proposing three grays as three tokens instead of catching that they're one. The consolidation *is* the value; clustering is the core move (`references/linting.md`).
- **Tokenizing genuine one-offs.** Not every raw value wants a token. A single decorative gradient stop is an orphan to leave, not a token to mint. Over-tokenizing is its own kind of drift.
- **Eyeballed color distance.** "These look the same" — compute ΔE from the actual values. Two hexes that read alike on a screenshot can be a real, intended difference.
- **Aliasing loops.** When renaming/retiring, never point a token at one that points back. Resolve to the canonical token.
- **Auditing a file with no tokens.** There's nothing to govern — that's `site-to-system`'s job first. Don't invent a system here; hand off.
