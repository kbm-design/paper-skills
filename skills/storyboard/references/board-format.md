# Board format — core + profiles, and the compiled JSON

The board on the Paper canvas is authored by hand or drafted by the skill; on approval it compiles to `storyboard.json`. That file is the **interface**: `product-demo` and `pitch-deck` both read it and never touch the board directly. Keep the board the source of truth — recompile on any board change, never hand-patch the JSON.

## The compiled shape

```jsonc
{
  "project": "ghostwire-launch",   // slug
  "profile": "video",              // "video" | "deck" — selects the field set below
  "scenes": [ /* scene objects, in play order */ ],
  // one profile block, keyed by the profile name:
  "video": { "fps": 30, "scale": { "fast": 100, "base": 180, "slow": 300, "ease": "out" }, "aspects": ["16x9"] }
  // — or —
  "deck":  { "page": "1920x1080", "aspect": "16x9" }
}
```

## Core scene fields (every profile)

| field | type | meaning |
|---|---|---|
| `n` | number | order, 1-based |
| `type` | `"frame" \| "title"` | `frame` = render a Paper frame; `title` = typographic scene, no source frame |
| `src` | string? | Paper frame name/node id for `frame` scenes (e.g. `"Baseline/Agents tab"`); omit for `title` |
| `copy` | string? | on-screen text, **verbatim** (ships as-is). `title` scenes may use `"Headline\|subhead"` |
| `notes` | string? | freeform intent — not rendered; guidance for the renderer/author |

## `video` profile — adds (consumed by product-demo)

Per scene:

| field | type | meaning |
|---|---|---|
| `seconds` | number | scene duration; frames = `seconds × fps` at compile |
| `transitionIn` | `{kind, ms} \| null` | how this scene enters (`fade`, `slide-*`, `notch-morph`, `continuity`, `cut`); `null` on the opener |
| `motion` | string? | one-line motion intent (one idea per scene) |

Header block: `"video": { "fps", "scale": {fast, base, slow, ease}, "aspects": [] }`. Durations in seconds on the board convert to frames at compile.

```jsonc
{ "n": 3, "type": "frame", "src": "Baseline/Agents tab",
  "copy": "Every agent. One glance.", "notes": "at-a-glance value",
  "seconds": 2.5,
  "transitionIn": { "kind": "notch-morph", "ms": 270 },
  "motion": "rows stagger; usage bars fill; % count up" }
```

## `deck` profile — adds (consumed by pitch-deck)

Per scene:

| field | type | meaning |
|---|---|---|
| `caption` | string | the one-line explainer — "a title that says what's going on" |
| `layout` | `"frame-center" \| "frame-left" \| "frame-right"` | where the frame sits relative to the title + caption (default `frame-center`) |

Header block: `"deck": { "page": "1920x1080", "aspect": "16x9" }`.

```jsonc
{ "n": 3, "type": "frame", "src": "Baseline/Agents tab",
  "copy": "Every agent, one glance",
  "caption": "See every running agent and its status — without opening anything.",
  "layout": "frame-left" }
```

## Schema (zod-shaped, for the consumer to validate against)

```ts
const core = z.object({
  n: z.number(),
  type: z.enum(['frame', 'title']),
  src: z.string().optional(),
  copy: z.string().optional(),
  notes: z.string().optional(),
});

const videoScene = core.extend({
  seconds: z.number(),
  transitionIn: z.object({ kind: z.string(), ms: z.number() }).nullable(),
  motion: z.string().optional(),
});
const deckScene = core.extend({
  caption: z.string(),
  layout: z.enum(['frame-center', 'frame-left', 'frame-right']).default('frame-center'),
});

const storyboard = z.discriminatedUnion('profile', [
  z.object({ project: z.string(), profile: z.literal('video'),
    scenes: z.array(videoScene),
    video: z.object({ fps: z.number(),
      scale: z.object({ fast: z.number(), base: z.number(), slow: z.number(), ease: z.string() }),
      aspects: z.array(z.string()) }) }),
  z.object({ project: z.string(), profile: z.literal('deck'),
    scenes: z.array(deckScene),
    deck: z.object({ page: z.string(), aspect: z.string() }) }),
]);
```

## Compile rules

- Read the board back with `get_tree_summary` + text content; do not infer from a screenshot.
- Emit **core** fields for every scene, then the active profile's fields. Never emit both profiles' field sets.
- `copy` and `caption` ship verbatim — a card with placeholder text is a blocker, stop and flag.
- After a successful downstream render, the consumer stamps the board status chip; on compile, this skill stamps `compiled <date>`.
- One board = one profile. To serve both a video and a deck from the same scenes, keep the core the same and compile twice with different profile blocks (two JSON files).

## Log

`.kbm/storyboard.md`: one entry per board — artboard name, profile(s) compiled, JSON path(s), pending edits. Read at start, write at end; hand-edits are instructions.
