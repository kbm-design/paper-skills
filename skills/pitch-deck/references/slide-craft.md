# Slide craft — template, layouts, cloning, export

## 1. The template comes first

Before slide 1 exists, decide the system once and write it down in the handoff. Everything below is applied identically to every slide — a deck reads amateur when these drift.

Derive values from the *product*, not defaults:

```
ground        the product's surface color (dark products keep their dark ground)
title         copy → 44–56px, semibold, tracking -0.02em
caption       caption → 20–24px, regular, ~60–70% opacity of the title color
frame scale   one scale for all frames (or one per layout), never per-slide fudging
margins       generous and equal; the frame is the hero, text is the label
slide number  optional, small, same corner on every slide
```

Read real values with `get_computed_styles` on the source frames and `get_font_family_info` before typographic styling. Prefer font families already in the file (`get_basic_info`). Use `px` for font size and line-height, `em` for letter-spacing.

**Build slide 1, screenshot it, get it right, then clone the pattern.** Slide 1 is the template; slides 2..n should be near-mechanical.

## 2. Layouts

The scene's `layout` field selects one. Keep the title/caption block on the *same baseline* across every slide regardless of layout.

- **`frame-center`** — title + caption stacked above (or below) a centered frame. The default; best for hero screens and wide frames.
- **`frame-left`** — frame on the left ~60%, title + caption right-aligned column on the right. Best when the caption needs room.
- **`frame-right`** — mirror of the above. Use to break rhythm on a long deck, not at random.

Title above caption, always, with a tight gap between them and a generous gap to the frame — group what belongs together.

## 3. Cloning frames (do this, don't re-author)

Use Paper's clone element inside `write_html` to place the *real* source node on the slide:

```html
<div layer-name="frame slot" style="display:flex; align-items:center; justify-content:center;">
  <x-paper-clone node-id="W-0" style="width: 640px;" />
</div>
```

This keeps the slide faithful to the design, survives design edits better than a hand-copy, and costs a fraction of the tokens. Never rebuild a product frame by hand in slide HTML.

For `title`-type scenes (no `src`), compose from tokens: the wordmark/headline and, if present, the subhead from `copy` (`"Headline|subhead"`).

## 4. Building

- One artboard per scene: `create_artboard` named `KBM/slide <n> — <title>`, sized to the board's `page` (default `1920×1080`).
- **Place slides in a deliberate left-to-right row as you build — do not trust auto-placement.** `create_artboard` drops each new artboard into "the best empty spot," which scatters slides across rows out of scene order. `export_combined_pdf` then orders pages by **canvas position** (top-to-bottom, then left-to-right), *not* by the node order you pass it — so scattered slides export as a mis-ordered deck. After creating each artboard, set its position with `update_styles` (`top`/`left` on an artboard move it on the canvas): pick one `top` for the whole row and step `left` by `page-width + ~200` per slide, in scene order. Then canvas order == scene order and the PDF is correct.
- Build incrementally — one visual group per `write_html` call (frame slot, then title, then caption). The user watches it assemble.
- Use flex, padding, and gap. No margin, no grid, no tables.
- After 3+ slides, screenshot and trace vertical/horizontal lanes: titles must share a baseline, frames must share a scale and center line.
- Content clipping the artboard → `update_styles` to `height: "fit-content"`. Never guess a new fixed height.

## 5. Review checkpoints (mandatory)

After every few slides, `get_screenshot` and evaluate:

- **Consistency** — same title size, caption color, frame scale, margins on every slide. This is the #1 deck failure.
- **Spacing** — deliberate grouping; generous around the frame.
- **Typography** — caption legible at presentation distance (never below 18px on a 1920 page); clear title/caption hierarchy.
- **Contrast** — caption readable at a glance, not a faint gray whisper.
- **Alignment** — title/caption baseline identical across slides.
- **Artboard fit** — nothing clipped.

Fix findings before moving on. Do not delete a slide and start over for a fixable issue.

## 6. Export

```
export_combined_pdf   → the deck, artboards in scene order (the primary deliverable)
export (png, 2x)      → per-slide images for embedding elsewhere (offer, don't assume)
```

Confirm the artboard order matches scene order before exporting — the PDF follows canvas position (top-to-bottom, then left-to-right), not the node order passed or the creation order. If you laid the slides in a single scene-ordered row (§4), this is already correct; if not, reposition them first. **Verify the result**: `Read` the exported PDF and check the pages are in scene order — the export tool reports success even when the order is wrong. Then `finish_working_on_nodes`.

## 7. Log

`.kbm/pitch-deck.md`: one entry per deck — board artboard name, storyboard.json path, slide artboard names, exported PDF path + date, pending edits. Read at start, write at end; hand-edits are instructions.
