# Extraction — sources, the Paper token taxonomy, ordering, the sticker sheet

## 1. Sources, ranked by fidelity

| source | how to read it | fidelity |
|---|---|---|
| CSS custom properties / SCSS vars | read the file directly | **Canonical** — these *are* the system |
| Tailwind `theme` / config | read `tailwind.config.*` or the `@theme` block | **Canonical** — declared scales map 1:1 to token types |
| Live site computed styles | browser inspection on real elements | Canonical for values you read; Candidate for anything you generalize |
| Rendered stylesheet (fetched CSS) | parse declarations, cluster repeated values | mixed — repeated values Canonical, one-offs Avoid |
| Screenshot / design note | measure carefully; most values are inferred | mostly **Candidate** — flag it |

Prefer the highest-fidelity source available. A repo's config beats a screenshot every time; if you have both, read the config and use the screenshot only to understand structure.

## 2. The Paper token taxonomy

Paper's `create_tokens` accepts exactly these `type`s. Map every extracted value to one:

| type | value form | notes |
|---|---|---|
| `color` | `"#2563EB"`, `"oklch(...)"`, or `var(--other)` | both semantic roles and a palette ramp |
| `fontFamily` | `"Inter"` | the loaded families (check `get_font_family_info`) |
| `fontSize` | `"16px"` | one per step of the type scale |
| `fontWeight` | `400` (number) | the weights actually used |
| `lineHeight` | `"24px"` or `1.5` | px preferred for determinism |
| `letterSpacing` | `"-0.01em"` or number | em preferred |
| `spacing` | `"8px"` | the spacing scale (4/8-based usually) |
| `radius` | `"8px"` | corner radii in use |
| `container` | `"1280px"` | max content widths |
| `breakpoint` | `"768px"` | responsive breakpoints |

Aliases: a value of `var(--palette-blue-600)` points one token at another. This is how semantic tokens stay re-themeable.

## 3. Color structure — semantic over palette

Two layers, and the order matters both for correctness and for Paper's create order:

**Palette ramp** (the raw scale): `--palette-neutral-50 … --palette-neutral-900`, `--palette-blue-500`, etc. Literal hex/oklch values.

**Semantic roles** (what the UI actually references), each aliasing a palette token:
- `--color-surface`, `--color-surface-raised`, `--color-surface-sunken`
- `--color-text`, `--color-text-muted`, `--color-text-subtle`
- `--color-primary`, `--color-primary-hover`, `--color-on-primary`
- `--color-border`, `--color-border-strong`
- `--color-accent`, and states `--color-success` / `--color-warning` / `--color-danger` / `--color-info`

```
--color-primary: var(--palette-blue-600)   ✓ re-themeable
--color-primary: #2563EB                    ✗ flat, can't re-theme
```

**Create order Paper wants:** semantic colors before palette colors; within each, neutrals first, then primary, secondary, accent. (Paper's `create_tokens` doc states this explicitly.) For every non-color type, smallest value first.

## 4. Classification discipline

Per `paper-craft.md` §7, tag every value:
- **Canonical** — read directly from the source. Becomes a token.
- **Candidate** — inferred (a consolidation, a missing scale step, a gray three near-misses reach for). Goes on the proposals board; created only on approval.
- **Avoid** — a one-off the source happens to contain that shouldn't become a token (a stray `#3B3B3C` used once). Not created, not proposed — noted as "left out" if worth mentioning.

The reference systems (Primer, Material, Atlassian, Spectrum) treat an un-tokenized or un-sourced value as a *defect*. Extract the system, not the accident.

## 5. The sticker sheet

One artboard, `KBM/system — <source>`, dark or light ground to match the source. Build incrementally (`write_html`, one group per call), every value referencing `var(--…)` so the sheet is itself proof the tokens work.

Sections, top to bottom:

1. **Header** — source name, token counts, date.
2. **Semantic colors** — a row of swatches, each: the color (as `var(--color-…)`), the token name, the resolved value, and the palette token it aliases.
3. **Palette ramp** — the raw scale as chips, grouped by hue, labeled with step.
4. **Type ramp** — every `fontSize` as a live line of sample text at its real weight/line-height, labeled with the token.
5. **Spacing** — bars at each `spacing` value, labeled.
6. **Radius** — squares at each `radius`, labeled.
7. **Components** — button (default/hover/disabled), input (rest/focus), card, badge — each built purely from tokens, so restyling a token visibly moves them.

Fixed-width label slots so the columns line up across rows (`paper-craft.md` vertical-lane rule). After ~3 component rows, screenshot and trace the lanes.

## 6. Verification

Final 2x `get_screenshot`. Check: every swatch resolves (no transparent/black failures = a bad `var()` name), type samples aren't clipped, the components visibly use the tokens (change one token with `set_tokens`, re-screenshot, confirm the component moved — the fastest proof the wiring is real). Then hygiene + log.
