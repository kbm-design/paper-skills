# Motion Presets

Three prepackaged motion personalities. Offer the user the pick in one line — "Crisp (fast, utilitarian) / Soft (calm, friendly) / Springy (playful, branded)?" — defaulting to **Crisp** for tools/dashboards, **Soft** for content/marketing surfaces, **Springy** only when the brand is expressive. Apply one preset per preview page; mixing presets on one system is the inconsistency this file exists to prevent.

Distilled from the vault's `emil-design-eng` + `motion-choreography` skills (durations, easings, craft rules) — read those for the *why*; this file is the frozen *what*.

## Tryout mode

Let the user *feel* the choice instead of reading it. On the first specimen for a system:

1. Render the same specimen three times in one `.specimen-row`, each copy wrapped in a scope div: `<div class="preset-crisp">…</div>`, `.preset-soft`, `.preset-springy`. Put a small dim tag under each copy (`Crisp · 150ms` / `Soft · 220ms` / `Springy · 250ms`).
2. Declare each preset's tokens **scoped, not on `:root`**: `.preset-crisp { --m-fast: 120ms; --m-base: 150ms; --m-ease: …; }` etc. Write the component's state rules once, referencing only the vars plus per-scope overrides for behavior differences (e.g. `.preset-soft .btn:hover { transform: translateY(-1px); }`).
3. The user hovers/presses all three and picks.
4. **Lock**: promote the winner's token values to `:root`, delete the losing scope divs and their CSS, unwrap the winner, add "Motion: {Preset}" to the page header note, and emit `motion-tokens.css` (see SKILL.md step 5).

Never leave a page in tryout state after the pick — tryout is a decision device, not a layout.

## Shared rules (all presets)

- Derive hover/press colors from the component's own palette (shift lightness ~8–12%); never introduce new hues.
- **Never `ease-in` for UI.** Transforms/entrances use the preset's ease-out; plain color changes may use `ease`.
- Transitions, not keyframes — interruptible and retargetable.
- Animate only `transform`, `opacity`, `color`/`background-color`/`border-color`, `box-shadow`. Never layout properties.
- Press feedback is non-negotiable: every clickable gets an `:active` scale.
- Focus states: visible ring in the accent color, fast (~120ms), same in every preset.
- `prefers-reduced-motion`: transforms off, color changes may remain (the shell already wires this).

## 1. Crisp — fast, utilitarian (default for tools)

The Linear/Geist feel. Color does the work; nothing moves on hover. Feels instant.

```css
:root {
  --m-fast: 120ms;
  --m-base: 150ms;
  --m-ease: cubic-bezier(0.23, 1, 0.32, 1); /* punchy ease-out */
}
```

| Component | Hover | Press | Duration |
|---|---|---|---|
| Button | bg one step lighter/darker | bg one more step + `scale(0.97)` | fast / fast |
| Card / row | border + bg lift one step | `scale(0.99)` | base |
| Input | border to mid-accent | — (focus ring instead) | fast |
| Link / chip | color shift only | opacity 0.8 | fast |
| Icon-in-button | none | none | — |

## 2. Soft — calm, friendly (content & marketing surfaces)

Gentle lift and settle. Slightly slower; movement is small and vertical.

```css
:root {
  --m-fast: 150ms;
  --m-base: 220ms;
  --m-ease: cubic-bezier(0.32, 0.72, 0, 1); /* iOS-like settle */
}
```

| Component | Hover | Press | Duration |
|---|---|---|---|
| Button | bg step + `translateY(-1px)` + soft shadow | shadow off, `translateY(0)` + `scale(0.98)` | base / fast |
| Card / row | `translateY(-2px)` + shadow grow | `scale(0.99)`, shadow reduced | base |
| Input | border + subtle bg tint | — | fast |
| Link / chip | color + underline fade-in | opacity 0.85 | base |
| Icon-in-button | nudge 2px on hover | — | base |

## 3. Springy — playful, branded (expressive products)

Overshoot on transforms; color still plain. Use sparingly — this personality is loud.

```css
:root {
  --m-fast: 150ms;
  --m-base: 250ms;
  --m-ease: cubic-bezier(0.34, 1.56, 0.64, 1); /* overshoot */
  --m-ease-color: ease;                        /* color never overshoots */
}
```

| Component | Hover | Press | Duration |
|---|---|---|---|
| Button | bg step + `scale(1.03)` | `scale(0.96)` snap | base / fast |
| Card / row | `scale(1.01)` + shadow | `scale(0.98)` | base |
| Input | border + ring pulse-in | — | base |
| Link / chip | color + `translateY(-1px)` hop | `scale(0.95)` | fast |
| Icon-in-button | nudge 3px with overshoot | — | base |

## Spec caption format

Whatever the preset, the specimen caption states resolved values, not preset names:
`hover: bg #4FD1C5→#6EDCD1, arrow +3px · press: #3EBFB3, scale .97 · 150ms cubic-bezier(0.23,1,0.32,1)`
The preset name goes once in the page header note (e.g. "Motion: Crisp").
