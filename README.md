# Paper Skills

Seventeen skills for designing in [Paper](https://paper.design) with an agent.

I've been working in Paper for a while now. The MCP server is good. An agent can read your file, understand the structure, and write real nodes back to the canvas. But pointed at a design file without guidance, agents make the same handful of mistakes every time. They rebuild a component by hand in HTML instead of cloning the node you already made. They pull a color off a screenshot instead of asking for the computed value. They render a video and tell you it looks right without having looked at a single frame of it. They quietly swap your copy for lorem.

These skills are the guardrails against that, plus the pipelines I got tired of rebuilding by hand.

## Install

```
/plugin marketplace add kbm-design/paper-skills
/plugin install paper
```

Skills invoke as `paper:storyboard`, `paper:design-council`, and so on, or they trigger on their own when what you're doing matches. You need Paper Desktop running with a file open.

## The skills

Grouped by which way the work is moving.

**Into Paper**

- `canvas-views` — renders an external system onto the canvas as a designed view. A Linear sprint as a status board, a Notion roadmap as lanes, a repo as an architecture map. Read-only, so the source system stays the record and the canvas is just the lens.
- `paper-live-components` — mirrors real components from a codebase onto the canvas as token-bound islands, then pushes prop edits back to code.

**Working in Paper**

- `storyboard` — plans a sequence of scenes as cards on the canvas, waits for you to approve it, then compiles a typed `storyboard.json`.
- `design-council` — five reviewer personas audit a frame with measured evidence, pin their findings on the canvas, and hand back a fixed side-by-side duplicate.
- `art-direction` — the inverse of design-council: duplicates a frame into several genuinely different, internally-consistent design directions to react to.
- `reality-check` — floods copies of a frame with hostile real content (long strings, RTL, empty states, 47-item lists) and reports where the layout breaks.
- `site-to-system` — extracts a design system from any site, repo, or config and materializes it as real Paper tokens plus a sticker sheet wired to them.
- `token-warden` — audits a file for hardcoded values and near-duplicate tokens, proposes consolidations, and keeps design and code tokens in sync. Paper has no token UI, so these two are the token manager.
- `componentize` — finds repeated elements on the canvas and extracts them into a named variant set you clone from. (Paper clones are copies, not live instances — the skill is honest about that.)
- `layer-hygiene` — renames cryptic layers, removes true orphans, and flattens redundant wrappers. Names and structure only, never appearance.

**Out of Paper**

- `flows` — wires screens into a clickable prototype: a flow map on the canvas plus a standalone clickable HTML build of the real frames. The screen-to-screen prototyping Paper lacks.
- `product-demo` — turns an approved storyboard into a Remotion video that animates your actual frames, as JSX, using the tokens and copy already in the file.
- `pitch-deck` — turns the same kind of storyboard into slides. One artboard per scene, each a real frame with a caption saying what it does. Exports a PDF.
- `paper-interaction-preview` — takes selected components and builds a live HTML page where you can actually feel the hover and press states.
- `paper-to-lottie` — writes Lottie JSON directly from vector elements. No Lottie editor in the loop.
- `paper-to-rive` — rebuilds designs as Rive assets, including state machines with pointer states.
- `paper-shaders` — works with Paper's shader fills and effects.

## How storyboard fits

`storyboard` is the front half of both `product-demo` and `pitch-deck`. It compiles a small renderer-agnostic core for every scene, plus one profile block: `video` adds timing and transitions, `deck` adds captions and layout.

Which means one approved board can render twice. Same scenes, same copy, once as a launch video and once as the deck you talk over. Compile it with each profile.

The board on the canvas stays the source of truth. Edit a card and recompile; nothing patches the JSON by hand.

## What they have in common

Four rules run through all of them, and they're doing most of the work:

- The canvas is the source of truth. Anything compiled out of it gets regenerated when it changes.
- Nothing expensive runs before you approve something cheap. Editing a storyboard card takes seconds. A video render takes minutes.
- Look at the output. Screenshot it, render a still, actually read the image before saying it works.
- Copy ships exactly as written on the canvas, and colors come from your file rather than a framework default. Lorem anywhere is a blocker, not something to tidy up later.

## License

MIT
