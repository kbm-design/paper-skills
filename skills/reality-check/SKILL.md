---
name: reality-check
description: Stress-test a Paper (paper.design) design against real-world content — duplicate the frame and flood the copies with the longest plausible strings, other languages (German, Arabic RTL), empty states, huge lists, ugly user-generated content, and real data — then screenshot each and report where the layout breaks, optionally fixing the wrap/flex rules. Use whenever the user wants to test a design with real content, check edge cases, find where a layout breaks, pressure-test copy length / empty states / long lists / localization, or QA a design before handoff. Requires Paper Desktop open. A QA persona for layout: adversarial, evidence-based, and it never touches the original.
---

# Reality Check

Designs are drawn with the happy path — a name that fits, a list with three items, a title that's exactly the right length. Real content is hostile: the German translation is 40% longer, someone has no avatar, the list has 47 rows, the username is a wall of emoji with no spaces. This skill floods copies of a frame with that hostility and reports where it breaks.

Paper's own Notion guide pulls *pretty* real content into a frame. This is the opposite — adversarial. It's the QA persona for layout, and like every KBM review skill it works on copies and cites looked-at screenshots.

Read `references/paper-craft.md` (shared KBM conventions) and `references/stress-battery.md` (the standard battery of hostile content and what each catches) before running.

## The contract

- **Never the original.** Every stress case is a `duplicate_nodes` copy, placed in a labeled row beside the original. The original is untouched (`paper-craft.md` §3).
- **Hostile, not pretty.** The value is in extreme and ugly content — max-length, empty, RTL, emoji, 47 items. Realistic-but-benign content misses the breaks that ship.
- **A break is cited, not asserted.** Each finding names the case, the node, and what broke (overflow, meaning-losing truncation, collapsed wrap, misalignment), from a `get_screenshot` you actually looked at.
- **Real data only if you have it.** If a Notion/CMS MCP is connected, pull real records. Otherwise use adversarial synthetic strings and label them synthetic — never present invented data as the user's real content.

## Workflow

### 1. Preflight & scope
Preflight per `paper-craft.md`. Scope the frame/selection. `get_jsx` to see which elements carry content (text, counts, images, lists) — those are the stress surfaces.

### 2. Pick the battery
From `references/stress-battery.md`, select the cases that apply to *this* design: a card with a title → long / empty / RTL / emoji title; a list → 0 / 1 / 47 items; an avatar → missing image; a number → 7-digit value. Don't run cases that can't apply.

### 3. Duplicate & flood
`duplicate_nodes` the frame once per case; populate the copy with the stress content (`set_text_content`, and for lists/data `write_html` or `x-paper-clone` to multiply rows). Lay the copies in a labeled row, each captioned with its case (`KBM/reality — <frame>`).

### 4. Screenshot & diagnose
`get_screenshot` each copy and look. Diagnose breaks: text overflowing its container, truncation that removes meaning (not just an ellipsis), a wrap that collapses the layout, misalignment when content grows, an empty state that shows a broken shell instead of a designed zero-state. Report as findings on a `KBM/reality-findings — <frame>` board (annotation language, `paper-craft.md` §4), each keyed to the case and the node.

### 5. Optional: fix
On request, apply layout fixes (min-width, `flex-wrap`, truncation with a real max, a designed empty state) to a fixed copy — never the original — and attribute changes with change-pins. Re-screenshot the fixed copy under the same stress to prove it holds.

### 6. Verify, hygiene, log
Final screenshot of the row + findings board. `rename_nodes` under `KBM/`, `finish_working_on_nodes`. Log to `.kbm/reality-check.md`: cases run, breaks found, fixes applied, cases that held.

## Failure modes to avoid

- **Testing the original.** All stress lands on copies. The original stays pristine.
- **Pretty content.** Benign realistic strings miss the breaks. Use the extremes — that's the point.
- **Uncited breaks.** "This probably overflows" without a screenshot. Look, then claim.
- **Invisible fixes.** Fixes on the original, or unattributed. Fixes go on labeled copies with change-pins, re-tested under stress.
- **Faked real data.** Presenting synthetic strings as the user's real CMS content. Label synthetic as synthetic; only real MCP data is real.
- **Battery overkill.** Running RTL on a number field or 47-items on a single-value card. Pick cases that can actually apply to each element.
