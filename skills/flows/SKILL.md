---
name: flows
description: Wire Paper (paper.design) screens into a clickable prototype — connect frames into a user flow (tap this element on screen A goes to screen B), draw the flow map on the canvas with labeled connection arrows and hotspots, and compile a self-contained clickable HTML prototype of the real frames that opens in a browser. Use whenever the user wants to prototype, make screens clickable, wire up a flow, connect screens, test a user journey, or "see it working" — the screen-to-screen prototyping Figma has that Paper lacks. Requires Paper Desktop open. Because Paper frames are real HTML, the prototype is genuinely clickable, not a mockup.
---

# Flows

Paper has no prototyping engine — no connections, no play mode, no clickable preview. But Paper frames *are* real HTML (`get_jsx` returns it), so the gap is fillable. This skill produces two things from a set of screens and the transitions between them:

1. **A flow map on the canvas** — the screens laid out in order with labeled connection arrows (`Login —Sign in→ Dashboard`) and hotspot markers on the tap targets. Editable and shareable; this is the *plan*.
2. **A clickable HTML prototype** — the real frames compiled into one standalone page where tapping a hotspot navigates to the next screen. This is the *deliverable* you open in a browser and click through.

The canvas map is the source of truth; the prototype is compiled from it (like `storyboard` → render). Edit the map, recompile.

Read `references/paper-craft.md` (shared KBM conventions) and `references/prototype-build.md` (drawing the flow map, compiling the clickable HTML) before building.

## The contract

- **Navigation comes from the user, or is proposed and confirmed — never invented.** "From Login, Sign In goes to Dashboard" is theirs to state. If they don't, propose a flow from the screens' apparent structure and confirm before wiring anything. A tap the user didn't ask for is a bug.
- **A hotspot means navigation.** Only draw a hotspot on an element that actually goes somewhere. Decorative targets get no marker.
- **The real frames, not rebuilds.** Screens come from `get_jsx` / `x-paper-clone`. The prototype shows the user's actual design.
- **No dead ends.** Every screen needs a way out (a back target, or it's a declared terminal). Flag unreachable screens.

## Workflow

### 1. Preflight & the flow
Preflight per `paper-craft.md`. Identify the screens (selection or named frames) and the transitions. Ask for the flow if it isn't given; propose one from the screens and confirm. Write the flow down as a list of `{from, trigger, to}` edges — this is what both outputs compile from.

### 2. Flow map on the canvas
Lay the screens in flow order (or keep their positions). Draw the edges as labeled connection arrows (absolute-positioned SVG with arrowheads, `write_html`) and place hotspot markers on each tap target. One locked group, `KBM/flow — <name>`, deletable in one gesture. Per `references/prototype-build.md`.

### 3. Compile the clickable prototype
For each screen, take its `get_jsx`. Assemble one self-contained HTML file: screens as full-viewport sections, one visible at a time; each hotspot wired (`data-goto`) to switch screens with a CSS transition; a tiny vanilla router. No build step, no frameworks, no `localStorage`; inline assets as data URIs or reference exported files. Per `references/prototype-build.md`.

### 4. Verify
Screenshot the flow map; open the HTML and click every path. Confirm each hotspot navigates, transitions play, and no screen is an accidental dead end. Fix before declaring done — a prototype with one broken tap is worse than none.

### 5. Deliver, hygiene, log
Deliver: the HTML path, the flow map, one line per transition. `rename_nodes` under `KBM/`, `finish_working_on_nodes`. Log to `.kbm/flows.md`: screens, edges, prototype path, open questions.

## Failure modes to avoid

- **Invented navigation.** Wiring taps the user never described. Propose and confirm; don't guess a journey.
- **Dead ends.** A screen with no way out. Every screen is reachable and escapable, or flagged.
- **Hotspots on nothing.** A marker on an element that doesn't navigate. Markers mean navigation, always.
- **Rebuilt frames.** Hand-authoring a screen instead of using `get_jsx`. The prototype must be the real design.
- **A heavy prototype.** Frameworks, a build step, npm. One HTML file, inline everything, vanilla JS. It has to open by double-clicking.
- **Map and prototype drifting apart.** The canvas map is the plan; recompile the HTML when it changes. A map edit that never reaches the prototype is the storyboard-JSON failure in another form.
