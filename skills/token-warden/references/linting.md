# Linting — drift rules, consolidation, CSS-var sync

## 1. The finding classes

Every visual value on a node is exactly one of these when measured against the token set (`get_tokens`):

| class | test | action |
|---|---|---|
| **Tokenized** | already `var(--token)` | skip |
| **Exact raw** | literal == some token's value, but not referenced | retokenize: point at that token |
| **Near-miss** | within threshold of a token, not equal | propose snapping; flag as drift |
| **Orphan** | no token within threshold | cluster; propose one token per cluster, or leave as one-off |

## 2. Thresholds (the "near" in near-miss)

- **Color** — CIE ΔE (perceptual distance). ΔE < 2 is "same to the eye, drifted in the value" → near-miss. ΔE 2–5 → borderline, propose but flag lower-confidence. ΔE > 5 → treat as distinct (orphan). Convert to Lab from the actual computed color; never judge from a screenshot.
- **Spacing** — off by ≤ 2px from a `spacing` token → near-miss. Also flag values that aren't on the scale at all (a `13px` gap in a 4/8 system) even if far from any token — off-grid is its own drift.
- **Radius** — off by ≤ 2px → near-miss.
- **fontSize / lineHeight / letterSpacing / fontWeight** — exact match or it's off-scale; type has few enough steps that "near" mostly means "should have been this step."

State the threshold used in the report so the user can calibrate it. A memory-file entry that changes a threshold is an instruction for next run.

## 3. Clustering — the core move

The value of this skill is turning *many* raw values into *few* tokens. Before proposing, cluster:

1. Collect all Exact-raw + Near-miss + Orphan values of a type.
2. Group by proximity (colors by ΔE, sizes by value). A group of near-equal values is **one** proposal.
3. Pick the group's canonical: an existing token if one is in range (snap to it), else the most-used value in the cluster (mint one token, snap the rest).
4. Report the group as a single finding with the node count: "4 grays (#8A8A8A ×22, #8A8A8B ×9, #898989 ×4, #8B8B8B ×2) → `--color-text-muted`, 37 nodes."

Never surface 37 individual findings where there is one consolidation. Confetti kills the report the same way it kills annotations (`paper-craft.md` §4).

## 4. Applying

On approval, in this order:

1. **Snap to existing token** — `update_styles` (batched) sets the affected nodes to `var(--token)`. No new token needed.
2. **Mint then snap** — for an approved orphan cluster: `create_tokens` the canonical (correct type + ordering per `site-to-system`'s `extraction.md`), then `update_styles` the cluster to reference it.
3. **Retire a redundant token** — if the audit found two tokens that are one: `set_tokens` to alias the loser to the winner (`value: "var(--winner)"`) so nothing breaks, then, once nothing references the loser directly, `set_tokens` `delete`. Never delete a token still referenced by value.

One change-pin per consolidation (not per node), keyed to the changelog card, count in the entry. Change-pins are the neutral chip family from `paper-craft.md` §4, never the severity colors.

## 5. Design ↔ code sync

When a codebase is in scope, the sync is a **reviewable patch, not an apply**:

- `get_tokens` `format: "css"` → a `:root { --token: value; … }` block. `format: "tailwind"` → a `@theme { … }` block for Tailwind v4 repos.
- Diff that against the repo's current variables. Report both directions:
  - **File → code**: tokens in Paper the repo lacks (or values that differ) → emit the CSS/Tailwind patch for the user to apply in the repo.
  - **Code → file**: variables in the repo Paper lacks → propose `create_tokens` to bring them in (Candidates until approved).
- Never write to the repo directly beyond producing the patch text. The user applies it as a normal PR — small, reviewable, theirs to merge.

## 6. The report card

Findings board `KBM/token-audit — <file>`, plain/mono styling per `paper-craft.md` §4 (never the audited product's fonts/colors). Order: consolidations with the biggest node counts first, then near-misses, then orphan proposals, then an "also noted" card for the long tail. Each card:

```
[Warning]  4 grays → --color-text-muted            37 nodes
  #8A8A8A ×22 · #8A8A8B ×9 · #898989 ×4 · #8B8B8B ×2
  ΔE all < 1.5 from --color-text-muted (#8A8A8A)
  → snap all to var(--color-text-muted)
```

Severity: exact-raw and near-miss = Warning (amber); orphan-cluster proposal = Suggestion (blue); a token that resolves to a broken/duplicate value = Blocker (red). Cap pins at ~12; the rest live on the board without pins.

## 7. Memory

`.kbm/token-warden.md`, keyed by finding id (type + canonical token). Statuses: `open`, `applied`, `accepted` (user wants the raw value kept — never re-raise), `dismissed`. Read at start; a status the user edited by hand is the instruction for this run. Record the thresholds used so successive runs are comparable.
