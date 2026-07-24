---
name: pitch-deck
description: Turn an approved storyboard into presentable slides on the Paper (paper.design) canvas — one slide artboard per scene showing a real product frame with a title and a one-line caption saying what's going on — then export a combined PDF (and per-slide images). Use whenever the user wants a pitch deck, product walkthrough deck, feature overview slides, investor/demo deck, or "the product explained screen by screen" from their designs. Consumes a `deck`-profile storyboard.json; if no approved board exists, invoke the `storyboard` skill first. Requires Paper Desktop open. No video, no Remotion — static slides you click through.
---

# Pitch Deck

Slides built from the user's *actual* designs: each scene is a real Paper frame, cloned onto a slide with a title and a one-line caption explaining what it does. The deck is assembled on the canvas and exported as a combined PDF.

This skill **consumes a storyboard**; it does not plan one. Planning lives in the `storyboard` skill. It shares that board format with `product-demo` — the same scenes can become a video or a deck, compiled with a different profile.

Read `references/slide-craft.md` before building (slide layouts, cloning frames, typography scale, export).

## The contract

**An approved board comes first.** No slides are built until a `deck`-profile `storyboard.json` exists, compiled from a board the user approved. **If there is no board, invoke the `storyboard` skill and let it run to approval — then come back.** Never invent scenes or captions inline; copy and captions ship verbatim from the board.

## What this skill consumes

A `deck`-profile board (see the `storyboard` skill's `references/board-format.md`): core scene fields (`n`, `type`, `src`, `copy`, `notes`) plus `caption` (the one-line explainer) and `layout` (`frame-center` / `frame-left` / `frame-right`), and a header block of `page` + `aspect`.

- `copy` → the slide **title** (short)
- `caption` → the slide **explainer** (one line, says what's going on)
- `src` → the Paper frame to show

## Workflow

### 1. Preflight
Confirm a compiled `deck`-profile `storyboard.json` (else → `storyboard` skill). Paper open with the source file (`get_basic_info`); locate every `src` frame and confirm it exists. Read `.kbm/pitch-deck.md` for prior decks.

### 2. Establish the slide system — once, before slide 1
Map the product's tokens/type off the source frames (`get_computed_styles`, `get_font_family_info`) into one slide template: ground color, title size/weight, caption size/color, frame scale, margins. Every slide reuses it. Build the first slide, screenshot it, get it right — then the rest follow it exactly. Per `slide-craft.md`.

### 3. Build slides
One artboard per scene, named `KBM/slide <n> — <title>`, at the board's `page` size. Compose per the scene's `layout`. **Clone the source frame** with `<x-paper-clone node-id="…">` rather than rewriting its HTML — it's cheaper and stays faithful to the design. Build incrementally (one visual group per `write_html` call) so the user watches it assemble.

### 4. Review
After every few slides: `get_screenshot` and evaluate spacing, type hierarchy, contrast, alignment, and frame scale consistency across slides. Trace the title/caption baseline across slides — they must sit in the same place on every one. Fix before continuing. Content clipping an artboard → switch it to `height: "fit-content"`, don't guess pixel heights.

### 5. Export & deliver
`export_combined_pdf` across the slide artboards in scene order → the deck. Offer per-slide PNGs (`export`, 2x) for embedding elsewhere. Deliver: PDF path, slide count, one line per slide. Stamp the board's status chip (`deck exported <date>` + path) and update `.kbm/pitch-deck.md`. Flag every approximation as a Candidate-style note. Call `finish_working_on_nodes` when done.

## Failure modes to avoid

- **Building without an approved board.** Slides nobody planned, captions nobody wrote.
- **Inventing captions.** `caption` ships verbatim; a missing one is a blocker — go back to the board, don't improvise marketing copy.
- **Slide drift.** Title 48px on slide 2 and 40px on slide 5, frames at different scales, captions on different baselines. One template, applied identically. This is the most common way a deck reads amateur.
- **Rebuilding frames by hand.** Clone the real nodes; don't re-author the design in slide HTML — it drifts from the source and costs tokens.
- **Screenshot-driven values.** Read sizes and colors with `get_computed_styles`, never off a screenshot.
- **Wall-of-text slides.** One title, one caption line. If a scene needs a paragraph, the board is wrong — send it back.
- **Animating anything.** This skill is static slides. Motion is `product-demo`.
