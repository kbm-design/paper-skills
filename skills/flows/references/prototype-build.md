# Prototype build — the flow map and the clickable HTML

Two outputs from one flow definition: a `{from, trigger, to}` edge list. The map is authored on the canvas; the prototype is compiled. Keep them in sync — the map is truth.

## 1. The flow definition

Before drawing anything, settle the edges as a plain list:

```
[
  { from: "Login",     trigger: "Sign in",        to: "Dashboard" },
  { from: "Dashboard", trigger: "Settings icon",  to: "Settings" },
  { from: "Settings",  trigger: "Back",           to: "Dashboard" },
  { from: "Dashboard", trigger: "New issue",      to: "Compose" }
]
```

Each `trigger` names a real element on the `from` screen (the tap target). Each `to` is a screen. A screen with no outgoing edge is a terminal — fine if intended, a dead end if not. Every screen should appear as some edge's `to` (reachable) unless it's the entry.

## 2. The flow map on the canvas

Purpose: the plan, editable and shareable, that the prototype compiles from.

- **Layout.** Place the screens left-to-right (or in a grid) in rough flow order. Prefer keeping the user's existing frame positions if they already read as a flow; otherwise duplicate the frames into a `KBM/flow — <name>` layout area so the original screens are untouched.
- **Connection arrows.** One per edge, `write_html` absolute-positioned SVG: a line from the `from` screen's hotspot to the `to` screen's edge, with an arrowhead (`<marker>`) and the `trigger` as a small label chip at the line's midpoint. Route them so they don't cross screens; curve (quadratic path) when a straight line would overlap content.
- **Hotspots.** A KBM-styled marker on each tap target — a translucent rounded rect over the element's bounds (accent outline, ~12% fill) with the trigger label. Distinct from `design-council`'s finding pins (different color, no number) so a flow is never confused with a review.
- **Group + lock.** Everything the skill draws goes in one locked group `KBM/flow — <name>`, deletable in one gesture. Never draw arrows directly onto the user's frames.

## 3. The clickable HTML prototype

Purpose: the thing you open and click. One self-contained file.

**Screens.** For each screen frame, `get_jsx` (Tailwind format). Wrap each as a full-viewport `<section data-screen="Login">`, absolutely stacked, only the active one visible:

```html
<section data-screen="Login" class="screen">…get_jsx output…</section>
<section data-screen="Dashboard" class="screen" hidden>…</section>
```

**Hotspots → navigation.** For each edge, find the trigger element in the `from` screen's JSX and give it `data-goto="Dashboard"` (and `cursor:pointer`). If the element is hard to target precisely, overlay a transparent positioned `<a data-goto>` at its bounds rather than mangling the frame markup.

**The router — vanilla, tiny, no deps:**

```html
<script>
  const screens = [...document.querySelectorAll('[data-screen]')];
  const show = (name) => screens.forEach(s => s.toggleAttribute('hidden', s.dataset.screen !== name));
  document.addEventListener('click', (e) => {
    const t = e.target.closest('[data-goto]');
    if (t) { e.preventDefault(); show(t.dataset.goto); }
  });
  show(screens[0].dataset.screen); // entry screen
</script>
```

**Transitions.** A CSS class on `.screen` — opacity + small translate, `transition: .18s ease`. Keep it to one move; this is navigation feedback, not choreography. For richer per-screen motion (hover/press within a screen), that's `paper-interaction-preview`'s job — compose, don't reinvent.

**Constraints (same discipline as the other export skills):**
- One HTML file. Inline all CSS and the one `<script>`. No frameworks, no build, no CDN.
- **No `localStorage`/`sessionStorage`** — fails in sandboxes.
- Assets: inline images as data URIs (`get_fill_image`) or reference files exported alongside; never hotlink.
- It must run by double-clicking the file. If it needs a server, it's wrong.

## 4. Verify

- Screenshot the flow map: arrows land on the right screens, labels legible, hotspots sit on their targets, nothing crosses a screen.
- Open the HTML and walk **every** edge. Each hotspot navigates; the entry screen shows first; transitions play; back-edges work. A terminal screen is intended, not a mistake.
- Cross-check reachability against the edge list: any screen that's never a `to` (and isn't the entry) is unreachable — flag it.

## 5. Log

`.kbm/flows.md`: one entry per flow — name, screen list, the edge list, prototype file path, date, open questions (unwired targets, proposed-but-unconfirmed edges). Read at start; a user edit to the edge list is the instruction to recompile.
