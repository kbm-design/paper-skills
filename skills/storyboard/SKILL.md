---
name: storyboard
description: Plan a sequence of product scenes on the Paper (paper.design) canvas as the source of truth, then compile the approved board into a typed storyboard.json that renderers consume. This is the pre-production base for product videos (see product-demo) and pitch decks (see pitch-deck) — a board of scene cards (number · type · source frame · verbatim copy · notes) laid out left-to-right in play order, with a draft→approve contract before anything downstream is built. Use whenever the user wants to storyboard, plan a reel/demo/deck, sequence product screens with captions, or asks to "storyboard this" — even if they haven't decided how it renders yet. Requires Paper Desktop open. Renderer-agnostic: it stops at an approved board + compiled JSON.
---

# Storyboard

The board on the Paper canvas is the source of truth. You plan a sequence of scenes as cards, the user approves it, and you compile it to a typed `storyboard.json` that a renderer reads. This skill owns **planning and the interface** — it never renders. `product-demo` (Remotion video) and `pitch-deck` (Paper slides) are consumers of the JSON this produces.

## The contract

**Storyboard first, always.** Nothing downstream is built until the board exists on the canvas and the user has approved it. If asked to "just make the video/deck," draft the board from their brief + selected frames, mark it `draft`, and stop for edits. The board is truth; the JSON is compiled *from* it, never the reverse. A user edit to the board that never reaches the JSON is the worst failure — always recompile from the board.

## The board on canvas

One artboard, `KBM/storyboard — <name>`, built with `write_html` (inline styles). Structure:

**Header strip:** name · profile (`video` / `deck`) · status chip (`draft` / `approved` / `compiled <date>`) · profile-specific meta (video: fps · duration · aspects · motion scale; deck: page size · aspect).

**Scene cards, left-to-right in play order.** Every card carries the **core** fields; the active profile adds its own (see `references/board-format.md`):

```
┌──────────────────────────────┐
│ #3 · frame                   │  ← number · type
│ [thumbnail of source frame]  │  ← screenshot crop of the Paper frame (or icon for title scenes)
│ "Every agent. One glance."   │  ← on-screen copy (verbatim — this ships)
│ notes: at-a-glance value     │  ← freeform intent
│ src: Baseline/Agents tab     │  ← Paper frame name/node id
│  · · · profile fields · · ·  │  ← video: seconds/transition/motion  |  deck: caption/layout
└──────────────────────────────┘
```

3–7 scenes for a launch/demo; a deck can run longer. Placeholder copy on any card is a **blocker** — flag it, never let lorem survive to compile.

## Profiles

The board has a small renderer-agnostic **core** plus one **profile** that adds fields for the target medium. Pick the profile up front (ask if unstated):

- **`video`** → consumed by `product-demo`. Adds `seconds`, `transitionIn`, `motion`, and a header `fps` + `scale`.
- **`deck`** → consumed by `pitch-deck`. Adds `caption` (the one-line explainer) and `layout`.

Full field lists, the zod-shaped schema, and worked examples of each profile live in `references/board-format.md`. Read it before compiling.

## Workflow

1. **Preflight.** Paper open with the source file (`get_basic_info`). Identify source frames (selection or named) and the brief: what's being shown, the target medium (→ profile), tone. Read any prior board from `.kbm/storyboard.md`.
2. **Draft or read the board.** Either the user hand-builds it, or you draft cards from the brief + frames — draft cards, status `draft`. Build incrementally with `write_html` (one card per call), export frame thumbnails into the cards. **Stop for approval.**
3. **Compile on approval.** Read the board back (`get_tree_summary` + text), compile `storyboard.json` (core + the active profile block), validate against the schema in `references/board-format.md`. Stamp the status chip `compiled <date>`. Hand off: tell the user the JSON path and which renderer consumes it.

## Failure modes

- **Compiling without approval.** The stop is the product, not ceremony.
- **Patching the JSON against the board.** Board is truth; if they diverge, recompile.
- **Lorem in the compile.** Copy ships verbatim; placeholder anywhere is a blocker.
- **Mixed profiles.** One board, one profile. If the user wants both a video and a deck from the same scenes, compile the board twice — once per profile — don't cram both field sets onto the cards.
- **Guessing the render.** This skill stops at the JSON. Don't scaffold Remotion or export slides here — that's the consumer's job.
