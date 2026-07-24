# Remotion Craft — scaffold, scene recipes, verification, rendering

APIs verified against remotion.dev docs 2026-07. When anything here fails against the installed version, fetch the specific docs page (`remotion.dev/docs/...`) rather than guessing.

## Contents

1. [Scaffold](#1-scaffold)
2. [Compositions & the schema](#2-compositions--the-schema)
3. [Scene recipes](#3-scene-recipes)
4. [Transitions](#4-transitions)
5. [Assets & fonts](#5-assets--fonts)
6. [The verification loop](#6-the-verification-loop)
7. [Rendering & cutdowns](#7-rendering--cutdowns)
8. [Determinism & constraints](#8-determinism--constraints)

---

## 1. Scaffold

Create `video/` inside the user's repo (their tokens and exported assets live nearby):

```bash
cd video && npm init -y
npm i remotion @remotion/cli @remotion/transitions @remotion/zod-types zod
npm i -D @remotion/tailwind-v4 tailwindcss        # Tailwind v4 lane (Remotion ≥4.0.256)
# optional per storyboard: @remotion/rive @remotion/lottie @remotion/paths @remotion/motion-blur @remotion/noise @remotion/google-fonts/<Font>
```

`remotion.config.ts`:

```ts
import {Config} from '@remotion/cli/config';
import {enableTailwind} from '@remotion/tailwind-v4';
Config.overrideWebpackConfig((c) => enableTailwind(c));
```

`src/index.css` → `@import 'tailwindcss';`, imported in `src/Root.tsx`. If `package.json` has `"sideEffects": false`, change to `"sideEffects": ["*.css"]`. (Tailwind v3 lane: `@remotion/tailwind` + `tailwind.config.js` instead.)

**Map the Paper tokens into Tailwind/CSS variables first** — the reel must render with the product's real colors/type, not Tailwind defaults.

## 2. Compositions & the schema

One scene-player component, one `Composition` per aspect, shared zod schema, `defaultProps` = compiled storyboard.json:

```tsx
import {Composition} from 'remotion';
import {z} from 'zod';
import storyboard from '../storyboard.json';

export const reelSchema = z.object({
  reel: z.string(), fps: z.number(),
  scale: z.object({fast: z.number(), base: z.number(), slow: z.number(), ease: z.string()}),
  scenes: z.array(z.object({
    n: z.number(),
    type: z.enum(['frame','title','rive','svg','asset']),
    src: z.string().optional(), copy: z.string().optional(),
    seconds: z.number(),
    transitionIn: z.object({kind: z.string(), ms: z.number()}).nullable(),
    motion: z.string().optional(),
  })),
});

// In Root: durationInFrames = sum(scenes.seconds) × fps − transition overlaps
<Composition id="Reel16x9" component={Reel} schema={reelSchema} defaultProps={storyboard}
  width={1920} height={1080} fps={30} durationInFrames={...} />
<Composition id="Reel9x16" component={Reel} schema={reelSchema} defaultProps={storyboard}
  width={1080} height={1920} fps={30} durationInFrames={...} />
<Composition id="Reel1x1"  ... width={1080} height={1080} ... />
```

Input props can override at render time (`--props`) — input props merge over defaults. That's how one board serves many renders (per-variant copy swaps, etc.).

## 3. Scene recipes

All scene animation uses `useCurrentFrame()` + `interpolate()`/`spring()` on the storyboard's motion scale — never improvised timings. Convert ms → frames: `ms/1000 × fps`.

**frame scene (the workhorse).** Take the Paper frame's `get_jsx` (Tailwind) output, wrap in `<AbsoluteFill>`, scale to stage:

```tsx
const frame = useCurrentFrame();
const push = interpolate(frame, [0, sceneFrames], [1, 1.04]);         // slow push-in
const enter = spring({frame, fps, config: {damping: 200}});           // settle, no bounce
<AbsoluteFill className="bg-[--surface] items-center justify-center">
  <div style={{transform: `scale(${push})`, opacity: enter}}>
    {/* pasted Paper JSX, adjusted: remove interactive attrs, fix asset paths to staticFile() */}
  </div>
</AbsoluteFill>
```

Element-level motion inside a frame scene (stats counting up, rows staggering in) = per-element `interpolate` with staggered delays (`frame - i * staggerFrames`). Counters: `Math.round(interpolate(...))` — and use tabular-nums.

**title scene.** Copy + tokens. Type reveals via per-word/letter opacity+translateY stagger on the `base` duration. Restraint: one move per scene.

**rive scene.** `import {RemotionRiveCanvas} from '@remotion/rive'` → `<RemotionRiveCanvas src={staticFile('hero.riv')} artboard="..." animation="..." fit="contain"/>` — plays synced to the timeline; `onLoad` can set text runs per render.

**svg scene.** `@remotion/paths` (`getLength`, `evolvePath`) for draw-on; source = Paper `export` SVG.

**asset scene.** `<Img src={staticFile(...)}/>` or `<OffthreadVideo>`; slow scale/pan only.

## 4. Transitions

`@remotion/transitions` (≥4.0.59):

```tsx
import {TransitionSeries, linearTiming} from '@remotion/transitions';
import {fade} from '@remotion/transitions/fade';
import {slide} from '@remotion/transitions/slide';
import {wipe} from '@remotion/transitions/wipe';

<TransitionSeries>
  <TransitionSeries.Sequence durationInFrames={s1}>{scene1}</TransitionSeries.Sequence>
  <TransitionSeries.Transition presentation={slide({direction: 'from-right'})}
    timing={linearTiming({durationInFrames: msToFrames(board.ms)})}/>
  <TransitionSeries.Sequence durationInFrames={s2}>{scene2}</TransitionSeries.Sequence>
</TransitionSeries>
```

Map board `transitionIn.kind` → presentation: `cut` (no Transition element), `fade` → `fade()`, `slide-left/right/up/down` → `slide({direction})`, `wipe` → `wipe()`. Transitions *overlap* sequences — subtract overlap frames when computing total duration. Default transition duration: the scale's `base`.

### Morph transitions — when the product has its own reveal

`@remotion/transitions` presentations are generic by design; a reel cut entirely with `fade`/`slide` reads like a template. When the product has a signature reveal (a panel that opens from a bar, a card that expands to full screen, a tray that slides from an edge), **build the transition from that instead** — it's the single biggest difference between a demo that looks bought and one that looks like the product.

The pattern, which needs no `TransitionSeries` at all:

1. Use a plain `<Series>`. Each scene owns its own morph in and out — there are **no overlaps**, so total duration is the plain sum of scene durations.
2. Every scene renders the *same* morphing container: a box interpolating between the resting state (e.g. a collapsed capsule) and the open panel — width, height, and per-corner radius all lerped by one `0→1` progress value.
3. Progress is `expandT × (1 − collapseT)` — expand at the head of the scene, collapse at the tail.
4. Cross-fade two faces inside that container: the resting-state face out, the panel face in.
5. **Adjacent scenes must land on an identical container state.** Scene N collapses to exactly what scene N+1 expands from, so the hard cut between sequences is invisible and the whole reel reads as one continuous object.

```tsx
const p = expandT * (1 - collapseT);               // 0 = resting, 1 = open
const w = lerp(CAP.w * S, panel.w * S, p);
const h = lerp(CAP.h * S, panel.h * S, p);
const restingOpacity = interpolate(p, [0, 0.18], [1, 0], {extrapolateRight: 'clamp'});
const panelOpacity   = interpolate(p, [0.3, 0.75], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
```

**Tune the content fade against the geometry, not after it.** If the panel's contents only appear once the box has finished opening, you get several frames of an empty box — reads as a stall. Contents should be fading in while the box is still growing (note the `0.3–0.75` window above, not `0.55–0.9`). Verify this specific thing with a still taken *mid-morph*, not at the scene midpoint.

Anchor the container the way the real UI is anchored (an element that hangs from the top of the screen keeps `top: 0` and grows downward), and let one continuous camera push run across the *whole* composition rather than per-scene moves — per-scene pushes re-trigger on every cut and read as jumps.

## 5. Assets & fonts

- Export needed images/SVGs from Paper (`export`, 2x) into `video/public/`; reference via `staticFile()`. Never hotlink.
- Fonts: `@remotion/google-fonts/<Family>` (`loadFont()`) when Paper's `get_font_family_info` says Google; local files via `@remotion/fonts` otherwise. A substituted font is a flagged Candidate, never silent.
- `.riv` files from rive-bridge → `video/public/`.

## 6. The verification loop

The skill's superpower — use it, don't skip it:

```bash
npx remotion still Reel16x9 out/check-90.png --frame=90
```

Render a still at each scene's midpoint and each transition's midpoint → **Read the PNGs and look**: overflowing copy, broken asset paths, off-token colors, mis-scaled frames, transition artifacts. Fix, re-still, repeat until every checkpoint reads clean. Only then render video. Claims of correctness must cite looked-at stills.

Offer `npx remotion studio` for the user to scrub interactively before final render.

## 7. Rendering & cutdowns

```bash
npx remotion render Reel16x9 out/<reel>-16x9.mp4
npx remotion render Reel9x16 out/<reel>-9x16.mp4          # cutdown = different composition, same props
npx remotion render Reel16x9 out/<variant>.mp4 --props='{"scenes":[...]}'   # per-render overrides
```

Cutdown layout rule: keep critical content in a **center safe area** so one scene component serves all aspects; where that fails, branch on `useVideoConfig().width/height` inside the scene. Re-run the still loop per aspect — 9:16 breaks differently than 16:9.

## 8. Determinism & constraints

- No `Math.random()`/`Date.now()` in scenes (breaks deterministic rendering) — seed randomness or precompute in props.
- Everything the render needs must be local (`public/`) — no network fetches at render time.
- Render cost is real: a 15–30s reel takes minutes; stills take seconds. That's why the loop is stills-first.
- Tailwind lane must match the installed Remotion major (v4 lane ≥4.0.256).
- Respect `prefers-reduced-motion` where the reel embeds on the web (note in handoff); for MP4 output it's N/A.

## 9. Gotchas that cost real time

Each of these was hit on a live build. Check them before debugging from scratch.

**Scaffold**

- **`tsconfig.json` is required.** Remotion errors out with "Could not find a tsconfig.json file in your project" — `npm init` doesn't create one. Write it before the first `still`.
- **zod must be Remotion's exact version.** A plain `npm i zod` gets rejected ("install exact version X"). Run `npx remotion add zod` and let it pin.
- **`"sideEffects": false` in package.json kills the CSS.** Change it to `["*.css"]` or Tailwind silently doesn't load.

**Tailwind v4 vs v3 — the silent one**

- CSS variables in arbitrary values need the **`var()` wrapper** in v4: `bg-[var(--surface)]`, not v3's `bg-[--surface]`. The v3 form doesn't error — it produces **no style at all**, so a dark reel renders on a white stage and every token color falls back to browser defaults. If a still comes back white or unstyled, check this first.

**Paper assets**

- **`export` writes to `~/Downloads` using the node's display name** — spaces, em-dashes, slashes included. Those paths break `paper-asset://` references and `staticFile()`. Copy to safe filenames (`gw-thumb-agents.png`) before referencing them.
- **`<img>` in `write_html` needs explicit width *and* height.** `height: auto` collapses the element to zero — it renders as an empty box with no error. Compute the real aspect and set both.

**Animation**

- Content that fades in only *after* a morph completes reads as a stall — overlap it with the geometry (see §4).
- `spring()` with a high `damping` and no `stiffness` is very slow to settle; pass both (`{damping: 200, stiffness: 160}`) when a move needs to land inside a short scene.
- Removing an unused `spring()`/`interpolate()` is free, but removing the variable it fed without removing its use is a render-time crash — the still command surfaces it immediately, which is another reason to still early.

**Verification**

- Stills are cheap and renders are not: 11 stills took seconds, the 12s render took minutes. When in doubt, add stills.
- A still at a scene *midpoint* will not catch a broken transition. Take stills at morph/transition midpoints explicitly — most defects live there.
