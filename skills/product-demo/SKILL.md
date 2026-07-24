---
name: product-demo
description: Turn an approved storyboard into a rendered product video with Remotion — animates the user's actual Paper (paper.design) frames as real Tailwind JSX with their tokens and copy, verifies visually with rendered stills, and outputs MP4s with cutdowns (16:9 / 9:16 / 1:1) as prop changes. Use whenever the user wants a product video, launch video, demo reel, feature walkthrough clip, changelog video, App Store preview, or social video from their designs, says "make a video of this" or "animate these frames" — even if they don't name Remotion. Consumes a `video`-profile storyboard.json; if no approved board exists, invoke the `storyboard` skill first. Requires Paper Desktop open (for the source frames) and Node.
---

# Product Demo

Paper is pre-production; Remotion is the renderer; you are the producer. The deliverable is a rendered MP4 built from the user's *actual designs* — their frames as Tailwind JSX, their tokens, their copy.

This skill **consumes a storyboard**; it does not plan one. Planning lives in the `storyboard` skill.

Read `references/remotion-craft.md` before working (scaffold, scene recipes, transitions, the verification loop — APIs verified against current docs; re-fetch specific remotion.dev pages when the installed version disagrees).

## The two contracts

1. **An approved board comes first.** No composition is built and nothing renders until a `video`-profile `storyboard.json` exists, compiled from a board the user approved. **If there is no board, invoke the `storyboard` skill and let it run to approval — then come back.** Never draft scenes inline here; the board is the editing interface, and edits to it are re-compiled, never hand-patched into the JSON.
2. **Stills before video.** Never claim a scene works without having rendered and *looked at* stills of it (`remotion still` at scene and transition midpoints). Video renders cost minutes; stills cost seconds; blindness costs trust.

## What this skill consumes

A `video`-profile board (see the `storyboard` skill's `references/board-format.md`): core scene fields (`n`, `type`, `src`, `copy`, `notes`) plus `seconds`, `transitionIn`, `motion`, and a header block of `fps` + motion `scale` + `aspects`. Validate it against the schema before building.

## Workflow

### 1. Preflight
Confirm a compiled `video`-profile `storyboard.json` (else → `storyboard` skill). Paper open with the source file; Node available; read `.kbm/product-demo.md` for prior demos.

### 2. Build
Scaffold the Remotion project per `remotion-craft.md` (Tailwind lane matching the installed major, **tokens mapped first** — the reel must look like *their* product, not stock Tailwind). Export needed assets from Paper into `public/`. Build the scene player: one component, per-type scene recipes (frame scenes from `get_jsx`, title scenes from tokens), all timing on the board's motion scale. One `Composition` per target aspect sharing the schema and props.

**Transitions carry the product's identity.** Prefer a transition system derived from the product's own interaction language over generic fade/slide — e.g. a surface that expands out of and collapses back into its resting state, so adjacent scenes share an identical frame and cuts read as one continuous object. Generic crossfades are the fallback, not the default. Whatever the system, it must be *consistent* across the whole piece and declared on the board.

### 3. Verify with stills
The loop from `remotion-craft.md` §6: still at every scene midpoint + transition midpoint → Read each PNG → fix overflow, broken paths, off-token color, mis-scale → re-still. Repeat until clean, per aspect. Offer `remotion studio` for the user to scrub before the full render.

### 4. Render & deliver
Render 16:9 first; cutdowns on request (or if the board lists them) as additional compositions — re-run the still loop per aspect, center-safe-area rule for shared layouts. Deliver: output paths, duration, a one-line per-scene summary. Stamp the board's status chip (`rendered <date>` + path) and update `.kbm/product-demo.md`. Flag every approximation (substituted font, adjusted layout, dropped interaction) as a Candidate-style note.

## Failure modes to avoid

- **Rendering without an approved board.** Skipping the storyboard produces a video nobody planned.
- **Patching the JSON against the board.** The board is truth; if they diverge, recompile via the `storyboard` skill.
- **Blind confidence.** "The video should look right" without stills looked at. Cite checkpoints.
- **Generic transition vocabulary.** Stock fade/slide on every cut is what makes a demo feel like a template. Derive the motion from the product.
- **Motion improv.** Timings not on the board's scale; five motion ideas in one scene. One move per scene, scale values only.
- **Dead frames.** A product frame that just sits there. Give it the life it has in the real app — counters counting, rows arriving, a button actually pressed.
- **Lorem in the render.** Copy ships verbatim from the board; placeholder anywhere is a blocker.
- **Default-Tailwind aesthetics.** Map the product's tokens before writing a single scene.
- **The everything-reel.** 12 scenes, 90 seconds, every feature. Demos are 3–7 scenes; propose cutting, don't comply silently.
