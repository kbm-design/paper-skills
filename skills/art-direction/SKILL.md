---
name: art-direction
description: Generate several genuinely different design directions from one Paper (paper.design) frame — duplicate it and let a distinct "art director" persona restyle each into a coherent, named direction (restraint/Geist, editorial, brutalist, semantic-role color/Material, etc.), each one internally consistent, so you get a row of real options to react to instead of noodling one file for hours. Use whenever the user wants design directions, explorations, variations, alternatives, "show me some options", a style exploration, or to break out of one look. Requires Paper Desktop open. The inverse of design-council: it generates instead of critiques, and each direction is a whole system, not style-transfer noise.
---

# Art Direction

The inverse of `design-council`. Council points several critics at one frame; this points several *art directors* at one frame — each duplicates it and restyles the copy into a coherent, named direction. Ten minutes later you have a row of legitimately different explorations to react to, instead of having forked the file and noodled one look for two hours.

The differentiator versus generic AI restyling: **each direction is a system, not a filter.** A direction makes internally-consistent decisions about color roles, type scale, spacing rhythm, and shape language, grounded in a named reference (Geist's subtraction, Material's semantic-role color, editorial print, brutalist). A row of five directions is five points of view, each of which could be built — not five noise passes over the same layout.

Read `references/paper-craft.md` (shared KBM conventions) and `references/directions.md` (the art-director directions, what system each applies, how to keep them distinct) before generating.

## The contract

- **Never the original.** Each direction is a `duplicate_nodes` copy in a labeled row; the original is untouched (`paper-craft.md` §3).
- **A direction is a system.** Restyling is coherent across color, type, space, and shape, grounded in a named reference — not a random new accent color. If you can't name the system a direction applies, it isn't one.
- **Genuinely different, not variations.** Three directions that look alike wasted the run. Pull from real opposites — restraint vs maximalism, geometric vs editorial, mono vs expressive.
- **Restraint on count.** 3–5 strong directions beat a dozen near-duplicates. Propose the set; don't spray.

## Workflow

### 1. Preflight & brief
Preflight per `paper-craft.md`. Scope the frame to explore. Read its current system (tokens if any, computed styles) so the directions are departures *from something*, not from nothing. Pick N (default 3–4) and propose the directions — each a named art-director persona with the system it applies (`references/directions.md`). Confirm before generating; the user may swap a direction.

### 2. Duplicate the set
`duplicate_nodes` the frame N times, laid in a labeled row (`KBM/directions — <frame>`). Each copy gets a direction card above it: the name, the one-line thesis, and the reference system it's grounded in.

### 3. Apply each direction
Restyle each copy as a *whole system* — `update_styles` for color roles / type / spacing / radius, `set_text_content` only if copy tone is part of the direction, `write_html` for any added treatment. Work token-aware if the file has tokens (a direction can re-map semantic roles rather than hardcode). One coherent system per copy; resist mixing two directions in one.

### 4. Label & review
Each direction reads with its name and a one-line rationale ("Restraint — one accent, everything else grayscale, spacing does the work"). `get_screenshot` the row; check the directions are actually distinct and each is internally consistent (no half-applied system — a brutalist direction with soft shadows is a tell).

### 5. Verify, hygiene, log
Fix any half-applied direction, misaligned card, or overflow. `rename_nodes` under `KBM/`, `finish_working_on_nodes`. The row is the deliverable — the user picks one, or grafts the best of several. Log to `.kbm/art-direction.md`: frame, directions generated, which the user favored (informs the next run's range).

## Failure modes to avoid

- **Noise, not systems.** A new accent color slapped on is not a direction. Every direction is a coherent set of decisions from a named reference.
- **Same-y set.** Directions that differ by a hue. Reach for opposites — the value is in the spread.
- **Half-applied systems.** A direction that restyles the buttons but leaves the type untouched. Apply the whole system or it reads as a mistake, not a choice.
- **Mutating the original.** All directions on copies; the source stays clean.
- **Too many.** Twelve directions is a menu nobody can react to. 3–5 with real spread.
- **Ungrounded vibes.** "Make it pop" is not a direction. Name the system (Geist / Material / editorial / brutalist) so the choices are principled and the user knows what they're picking.
