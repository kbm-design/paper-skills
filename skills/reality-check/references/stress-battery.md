# Stress battery — the hostile content, and what each case catches

Apply only the cases that fit an element. A single-value stat doesn't get the 47-item case; a number field doesn't get RTL. Pick by what the element carries.

## Constrain the copy to the production width — first, always

**A stress copy must render at the same width it has in production, or the test lies.** A row that lives in a 320px panel, copied into a roomy 720px board, will *not* truncate a long name — it has space it never has in the real app, so the truncation cases silently pass. Before flooding content, read the source frame's real width (`get_node_info` / `get_computed_styles`) and give the copy exactly that — no more. The most common false-negative in this skill is a break that "didn't happen" only because the copy had room the real layout doesn't. If a container's width comes from its parent, reproduce that constraint on the copy.

## Colour and other data-coupled properties

`set_text_content` changes text but not the styling logic behind it. A PnL that is green for gains and red for losses will stay whatever colour the original was when you swap in a negative value — so a negative-value stress must also *check the colour*, not just overflow: should red-for-loss have fired? Flag any property that should be driven by the value but isn't visibly bound to it (sign→colour, status→badge, count→state). This is a real finding even though the static frame can't run the logic — it shows the binding was never designed.

## Text fields

| case | content | catches |
|---|---|---|
| **Max length** | the longest plausible real string (a full sentence where a word is expected) | overflow, truncation that loses meaning, push-out of siblings |
| **Empty** | `""` / missing | broken shell where a designed empty/zero state should be; collapsed height |
| **Single char** | `"A"` | over-wide min-width, awkward centering |
| **No spaces** | a 40-char unbroken token (a URL, a hash) | overflow that `word-break` should catch but doesn't |
| **RTL** | an Arabic or Hebrew string | direction not handled, mirrored layout wrong, punctuation flipped |
| **Long language** | the German/Finnish translation (~40% longer) | fixed-width labels that fit English only |
| **Emoji / UGC** | emoji run, mixed scripts, zero-width junk | line-height jumps, baseline misalignment, render gaps |

## Counts & lists

| case | content | catches |
|---|---|---|
| **Zero** | empty list | missing empty-state design; a bare container |
| **One** | single item | layout that only looks right with several |
| **Many** | 47 items | no scroll/overflow handling, page blow-out, a footer that floats into the list |
| **Long labels in rows** | max-length text in every row | row height inconsistency, column misalignment across rows |

## Numbers & data

| case | content | catches |
|---|---|---|
| **Big number** | 7+ digits, or 1,234,567.89 | width overflow, no thousands handling, overlap with an adjacent label |
| **Negative / zero** | -100%, 0 | sign handling, a progress bar that breaks at 0 or >100 |
| **Long date/time** | a full localized timestamp | truncation, wrap |

## Media

| case | content | catches |
|---|---|---|
| **Missing image** | no fill | broken/empty image box instead of a fallback |
| **Wrong aspect** | a very tall or very wide image | distortion, crop that hides the subject, container blow-out |

## Real data (only if a data MCP is connected)

If Notion / a CMS / another data MCP is available, pull actual records and populate the frame with them — real content breaks in ways synthetic strings don't (inconsistent field presence, unexpected nulls, real-world lengths). If no data source is connected, use the synthetic cases above and **label them synthetic** — never present invented records as the user's real data.

## Fixture knobs (optional, Fixture-Kit fold-in)

For a design a stakeholder will pressure-test themselves, optionally emit a small standalone HTML fixture with knobs — sliders/toggles that regenerate the frame at N items, string length X, empty-on/off — so they can crank the chaos live. Same self-contained-HTML discipline as the `flows` prototype (one file, inline, vanilla JS, no `localStorage`). This is an add-on, not the default deliverable.

## Diagnosis vocabulary

Report each break precisely, not "looks off":
- **Overflow** — content exceeds its container's bounds.
- **Meaning-losing truncation** — the cut removes information the user needs (not a benign ellipsis on a repeatable label).
- **Collapse** — a wrap or flex rule that makes the layout fall apart, not reflow.
- **Misalignment** — columns/rows that stop lining up once content varies.
- **Missing state** — no designed handling for empty / error / loading where real data requires one.
