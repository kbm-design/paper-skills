---
name: paper-shaders
description: Use Paper Shaders for zero-dependency canvas shader effects in React or vanilla JS — gradients, noise, glass, metal, halftone, water, and more. Use when adding visual texture, animated backgrounds, or shader-based effects to websites. Docs at shaders.paper.design
---

# Paper Shaders

Zero-dependency HTML canvas shaders from Paper. Lightweight, performant, animated (or static), highly customizable. Use as backgrounds, masked with shapes/text, or as standalone visual elements.

## Install

```bash
# React
npm i @paper-design/shaders-react

# Vanilla JS
npm i @paper-design/shaders
```

Pin your dependency — breaking changes ship under 0.0.x versioning.

Docs and interactive examples: https://shaders.paper.design/

## React Usage

```jsx
import { MeshGradient, DotOrbit } from '@paper-design/shaders-react';

<MeshGradient
  colors={['#5100ff', '#00ff80', '#ffcc00', '#ea00ff']}
  distortion={1}
  swirl={0.8}
  speed={0.2}
  style={{ width: '100%', height: '100vh' }}
/>
```

All components are `'use client'` and accept standard React style/className props. Each shader has a `*Presets` export with curated starting points.

## Available Shaders (28)

### Gradients & Color
| Component | Description |
|-----------|-------------|
| `MeshGradient` | Animated multi-color mesh gradient |
| `StaticMeshGradient` | Non-animated mesh gradient |
| `StaticRadialGradient` | Non-animated radial gradient |
| `GrainGradient` | Gradient with grain texture |
| `ColorPanels` | Animated color panel transitions |

### Noise & Organic
| Component | Description |
|-----------|-------------|
| `NeuroNoise` | Brain-like organic noise pattern |
| `SimplexNoise` | Classic simplex noise |
| `PerlinNoise` | Classic perlin noise |
| `Metaballs` | Blobby metaball shapes |
| `GemSmoke` | Gem-like smoke wisps |

### Motion & Flow
| Component | Description |
|-----------|-------------|
| `SmokeRing` | Circular smoke effect |
| `Waves` | Wave animation |
| `Water` | Water surface simulation |
| `Swirl` | Swirling vortex |
| `Spiral` | Spiral pattern |
| `Warp` | Warped distortion (multiple patterns) |
| `GodRays` | Volumetric light rays |
| `LiquidMetal` | Chrome/metal fluid effect |

### Dots & Patterns
| Component | Description |
|-----------|-------------|
| `DotOrbit` | Orbiting dot pattern |
| `DotGrid` | Grid of dots |
| `HalftoneDots` | Halftone dot pattern |
| `HalftoneCmyk` | CMYK halftone print effect |
| `Dithering` | Dithering pattern |
| `ImageDithering` | Apply dithering to images |

### Texture & Effects
| Component | Description |
|-----------|-------------|
| `PaperTexture` | Paper/canvas texture |
| `FlutedGlass` | Ribbed glass distortion |
| `Heatmap` | Thermal heatmap effect |
| `PulsingBorder` | Animated glowing border |

## Common Props

All shader components accept:
- `style` — React CSSProperties (set width/height here)
- `className` — CSS class
- `speed` — Animation speed (0 = frozen)
- `colors` — Array of hex color strings
- `colorBack` — Background color

## Presets

Each shader exports presets for quick starts:
```jsx
import { MeshGradient, meshGradientPresets } from '@paper-design/shaders-react';

<MeshGradient {...meshGradientPresets.default} style={{ width: '100%', height: 400 }} />
```

## Vanilla JS Usage

```js
import { meshGradientMeta, ShaderMount } from '@paper-design/shaders';

const canvas = document.createElement('canvas');
const mount = new ShaderMount(canvas, meshGradientMeta.shader);
mount.setParams({ colors: ['#5100ff', '#00ff80'], speed: 0.2 });
```

## Best Practices

- Set explicit width/height via `style` prop — shaders need dimensions
- Use `speed: 0` for static textures (better performance)
- Layer shaders behind content with `position: absolute` + `z-index: -1`
- Use presets as starting points, then customize
- Shaders are GPU-accelerated but still cost paint — avoid stacking many on one page
- Check https://shaders.paper.design/ for interactive examples of all params
