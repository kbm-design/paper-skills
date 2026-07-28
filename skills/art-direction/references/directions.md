# Directions — the art-director systems, and keeping them distinct

A direction is a named reference system applied coherently across four axes: **color** (roles + palette), **type** (family, scale, weight contrast), **space** (rhythm, density), **shape** (radius, borders, elevation). A restyle that only moves one axis is a tweak, not a direction.

## The starter set of directions

Pick 3–5 with real spread. Each names a system so the choices are principled and the user knows what they're picking.

| direction | reference | color | type | space | shape |
|---|---|---|---|---|---|
| **Restraint** | Geist / Vercel | one accent, everything else grayscale | one family, tight scale, weight for hierarchy | generous; space does the work | minimal radius, hairline borders, no shadow |
| **Semantic** | Material 3 | role-based (primary/secondary/tertiary/surface tones) | clear type roles, larger steps | systematic 4/8 rhythm | tokened radius, tonal elevation |
| **Editorial** | print / magazine | ink + one bold spot color on paper ground | serif display + sans body, big scale contrast | asymmetric, columnar, roomy | square-ish, rules over boxes |
| **Brutalist** | web-brutalism | high contrast, few colors, raw | one strong grotesk, heavy weights | dense, grid-exposed | no radius, thick borders, hard shadows (offset, not soft) |
| **Expressive** | consumer / playful | a duo or trio of accents from one scene | display face with character, playful scale | varied, tilted or offset elements | rounded, soft shadow, sticker-like |
| **Density** | Primer / pro tools | muted, functional, low chroma | small, tight, tabular where numeric | compact; information-dense | small radius, subtle dividers |

These are starting points, not a fixed menu — interpret and extend, but always keep a direction *internally consistent*. The tells of a broken direction: a brutalist copy with soft shadows, a restraint copy spending three accents, an editorial copy in a geometric sans.

## Choosing the set for a given frame

Read the frame's current direction first, then pick departures that map the real space:
- Include at least one direction *toward* more restraint and one *toward* more expression than the current design — that's the axis most explorations actually want.
- If the product has a category convention (a dev tool leans Restraint/Density; a consumer app leans Expressive), include the convention *and* a deliberate break from it, so the row shows both the safe and the surprising.
- Don't include two directions that would resolve to nearly the same surface (Restraint and Density can collapse together on a simple frame — pick one).

## Applying a direction as a system

For each copy, move all four axes together:
1. **Color** — re-map the roles first (what's the surface, the primary, the accent in this system), then apply. If the file has tokens, prefer re-pointing semantic tokens on the copy over hardcoding — the whole copy moves coherently.
2. **Type** — set the family and the scale/weight relationships the system calls for (`get_font_family_info` before committing to a family; substitute and flag if unavailable, per `paper-craft.md`).
3. **Space** — adjust padding/gap to the system's density; this is the axis most often forgotten and most responsible for a direction reading as real.
4. **Shape** — radius, border weight, elevation to match.

Screenshot and check: could someone name the system from the result without the label? If not, it's under-applied.

## Relationship to design-council

This skill reuses Council's persona discipline in reverse — a Council persona *audits against* a system; an art-director persona *applies* one. Where Council cites named systems as the standard a design falls short of, Art Direction uses the same named systems as the target a direction builds toward. If a generated direction is later reviewed, Council will grade it against the very reference it claims — which is the honest test of whether the direction was really a system or just a vibe.

## Log

`.kbm/art-direction.md`: one entry per run — frame, the directions generated (name + reference), and which the user favored or grafted from. Over runs this records the user's taste range, so the set proposed next time leans into directions they've reacted well to without collapsing to only those.
