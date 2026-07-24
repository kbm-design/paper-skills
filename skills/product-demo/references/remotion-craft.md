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
