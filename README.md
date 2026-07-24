# Paper Skills

Ten skills for [Paper](https://paper.design), the design canvas — built on the Paper MCP server.

Paper is good at being a canvas. These skills are about everything around it: getting real data and real code *onto* the canvas, doing structured work *on* it, and turning finished designs *into* the things you actually ship — videos, decks, Lottie files, Rive assets, live interactive pages.

They compose. The canvas stays the source of truth; the skills read from it and write back to it.

## Install

```
/plugin marketplace add <your-org>/paper-skills
/plugin install paper
```

Skills then invoke as `paper:storyboard`, `paper:design-council`, and so on — or they trigger on their own when what you're doing matches.

**Requires:** Paper Desktop running with a file open, and the Paper MCP server connected. Individual skills note any extra requirements (Node for `product-demo`, a connected Linear/Notion MCP for `canvas-views`).

## The skills

Organized by direction of travel.

### → Into Paper

| skill | what it does |
|---|---|
| **canvas-views** | Renders external systems onto the canvas as designed views — a Linear sprint as a status board, a Notion roadmap as lanes, a repo as an architecture map. Read-only: the source system stays the record, the canvas is the lens. |
| **paper-live-components** | Mirrors real components from a codebase onto the canvas as token-bound islands. Extracts your theme into Paper tokens, renders faithful variant matrices, and pushes prop edits back to code. "Paper Dev Mode." |

### ↻ Within Paper

| skill | what it does |
|---|---|
| **storyboard** | Plans a sequence of scenes as cards on the canvas, gets your approval, and compiles a typed `storyboard.json`. Renderer-agnostic — it's the shared front end for `product-demo` and `pitch-deck`. |
| **design-council** | Five reviewer personas (accessibility, systems, content, first-time user, design lead) audit a frame with measured evidence, pin annotated findings on the canvas, and deliver a fixed side-by-side duplicate. |

### → Out of Paper

| skill | what it does |
|---|---|
| **product-demo** | Compiles an approved storyboard into a Remotion composition that animates your *actual* frames — real JSX, real tokens, real copy — verifies with rendered stills, and outputs MP4 with cutdowns. |
| **pitch-deck** | Turns an approved storyboard into slides: one artboard per scene, each a real frame with a title and a caption saying what's going on. Exports a combined PDF. |
| **paper-interaction-preview** | Takes selected components and builds a live interactive HTML page with hover/press/focus motion applied — an accumulating interaction reference for your design system. |
| **paper-to-lottie** | Turns vector elements into animated Lottie assets by generating Lottie JSON directly. No Lottie editor in the loop. |
| **paper-to-rive** | Rebuilds designs as interactive Rive assets — layouts, vectors, text, state machines with hover/press/pointer states. |
| **paper-shaders** | Works with Paper's shader fills and effects. |

## How they compose

```
                    ┌─────────────┐
                    │ storyboard  │  plan scenes on canvas → storyboard.json
                    └──────┬──────┘
                    ┌──────┴───────┐
                    ▼              ▼
            ┌──────────────┐  ┌────────────┐
            │ product-demo │  │ pitch-deck │   video          slides
            └──────────────┘  └────────────┘
```

`storyboard` compiles a small renderer-agnostic core (`n`, `type`, `src`, `copy`, `notes`) plus one **profile** block — `video` adds timing/transitions/motion, `deck` adds captions and layout. Same board, two outputs: compile it twice.

`paper-live-components` and `paper-interaction-preview` pair up — one mirrors components in from code, the other makes them feel real in the browser.

## Conventions

Every skill here follows the same house rules, which is most of why they work:

- **The canvas is the source of truth.** Compiled artifacts (JSON, JSX, slides) are generated *from* it and regenerated when it changes — never hand-patched to match.
- **Stop for approval before expensive work.** Anything that takes minutes to produce gets a cheap plan you can edit first.
- **Verify visually, and actually look.** Screenshot or render a still and read it before claiming something works.
- **Copy ships verbatim.** Placeholder text is a blocker, not a detail to fix later.
- **Use the product's own tokens.** Read real values off the design; never fall back to framework defaults.

## License

MIT
