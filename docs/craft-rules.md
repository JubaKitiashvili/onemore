# Craft & Physics Rules — "Feels Like Apple"

The difference between "looks like Apple" and "feels like Apple." These rules cover the invisible details that create the Jony Ive-level experience.

---

## 1. Spring Physics

Apple uses spring-based animations for virtually everything. Ease curves feel robotic. Springs feel alive.

### Spring Parameters

```
mass      — weight of the object (higher = more inertia)
stiffness — spring tightness (higher = snappier)
damping   — resistance (higher = less oscillation)
velocity  — initial speed (inherited from gesture)

The relationship:
- High stiffness + high damping = snappy (buttons, toggles)
- Low stiffness + low damping = gentle (sheets, modals)
- High stiffness + low damping = bouncy (playful, games)
- velocity from gesture = continuity (feels connected to your finger)
```

### Apple's Built-in Spring Presets (SwiftUI)

```swift
// The three presets Apple provides:
.smooth    // duration: 0.5, bounce: 0.0  — no bounce, settling
.snappy    // duration: 0.5, bounce: 0.15 — small bounce, responsive
.bouncy    // duration: 0.5, bounce: 0.3  — playful bounce

// Custom tuning:
.smooth(duration: 0.35, extraBounce: 0.0)    // faster settle
.snappy(duration: 0.4, extraBounce: 0.05)    // subtle snap
.bouncy(duration: 0.6, extraBounce: -0.1)    // tempered bounce

// Raw physics:
.interpolatingSpring(mass: 1, stiffness: 200, damping: 20, initialVelocity: 0)
```

### Web Equivalents

```javascript
// Framer Motion springs
const appleSmooth = { type: "spring", stiffness: 300, damping: 30, mass: 1 };
const appleSnappy = { type: "spring", stiffness: 400, damping: 25, mass: 0.8 };
const appleBouncy = { type: "spring", stiffness: 350, damping: 18, mass: 1 };
const appleGentle = { type: "spring", stiffness: 120, damping: 14, mass: 1 };

// react-spring configs
const smooth  = { tension: 300, friction: 30, mass: 1 };
const snappy  = { tension: 400, friction: 25, mass: 0.8 };
const bouncy  = { tension: 350, friction: 18, mass: 1 };

// react-spring decay (for momentum)
const momentum = { decay: true, velocity: gestureVelocity };

// GSAP spring approximation
gsap.to(el, {
  x: 100,
  duration: 0.5,
  ease: "elastic.out(1, 0.5)" // amplitude, period
});
```

### CSS Spring Approximation

```css
/* Apple's standard easing (not spring, but close) */
--ease-default: cubic-bezier(0.25, 0.1, 0.25, 1.0);

/* More spring-like curves */
--ease-spring-out: cubic-bezier(0.175, 0.885, 0.32, 1.275);  /* slight overshoot */
--ease-spring-snappy: cubic-bezier(0.2, 0.0, 0.0, 1.0);      /* fast start, smooth end */
--ease-spring-gentle: cubic-bezier(0.4, 0.0, 0.2, 1.0);       /* material-like */
```

### Rules

- **ALWAYS** use spring animations for interactive elements (buttons, cards, modals)
- **ALWAYS** pass gesture velocity to spring's `initialVelocity` — this is what makes it feel connected
- **NEVER** use `linear` easing for UI animations (only for progress bars or scroll-linked)
- **PREFER** `smooth` for navigation transitions, sheets, modals
- **PREFER** `snappy` for buttons, toggles, interactive controls
- **PREFER** `bouncy` only for playful/delightful moments (not primary UI)
- **USE** ease curves only when springs aren't available (CSS transitions)
- **MATCH** spring parameters to the physical metaphor:
  - Heavy objects: higher mass, lower stiffness
  - Light objects: lower mass, higher stiffness
  - Precise controls: high damping
  - Playful elements: low damping

---

## 2. Rubber Banding

The elastic resistance when you try to scroll/drag beyond bounds. This single effect defines iOS's feel.

### The Physics

```
displacement = offset × (1 / (1 + |offset| × resistance))

Where:
  offset     = distance past the boundary
  resistance = 0.55 (Apple's standard factor)
  result     = logarithmic decay — starts responsive, quickly diminishes
```

### Implementation

```javascript
// Core rubber band function
function rubberBand(offset, dimension, constant = 0.55) {
  const absOffset = Math.abs(offset);
  const sign = offset < 0 ? -1 : 1;
  // Rubber band formula: x * d / (d + x * c)
  return sign * (absOffset * dimension) / (dimension + absOffset * constant);
}

// Usage in drag handler
function onDrag(event) {
  const offset = event.y - dragStart;
  if (offset < minBound || offset > maxBound) {
    const overflow = offset < minBound
      ? offset - minBound
      : offset - maxBound;
    const bounded = rubberBand(overflow, containerHeight);
    return (offset < minBound ? minBound : maxBound) + bounded;
  }
  return offset;
}

// Release: spring back to boundary
function onRelease() {
  spring.start({
    y: nearestBound,
    config: { tension: 300, friction: 30 } // smooth return
  });
}
```

### CSS Scroll Overscroll

```css
/* Native rubber banding */
.scrollable {
  overscroll-behavior: contain;  /* prevent page bounce, keep element bounce */
  -webkit-overflow-scrolling: touch;  /* iOS momentum + rubber band */
}

/* Disable rubber banding */
.no-bounce {
  overscroll-behavior: none;
}
```

### Rules

- **ALWAYS** rubber band when dragging past boundaries — never hard-stop
- **ALWAYS** spring back on release — never snap
- **USE** constant 0.55 as Apple's standard resistance factor
- **USE** logarithmic curve — first 10px feels normal, next 10px feels heavier
- **COMBINE** with spring on release: tension 300, friction 30
- **APPLY** to: pull-to-refresh, bottom sheet overdrag, carousel edges, scroll bounds

---

## 3. Gesture Velocity & Momentum

In Apple's design, velocity is data — it determines where animations land, how long they take, and how far they go.

### Velocity-Driven Animations

```javascript
// Swipe to dismiss: velocity determines if dismiss or return
function onSwipeEnd(velocity, offset, threshold = 0.5) {
  const screenHeight = window.innerHeight;
  const shouldDismiss =
    Math.abs(offset) > screenHeight * threshold ||  // far enough
    Math.abs(velocity) > 500;                        // fast enough

  if (shouldDismiss) {
    // Velocity determines animation duration
    const distance = screenHeight - Math.abs(offset);
    const duration = Math.min(
      Math.max(distance / Math.abs(velocity), 0.15),  // min 150ms
      0.4                                                // max 400ms
    );
    animateTo(offset > 0 ? screenHeight : -screenHeight, duration);
  } else {
    // Spring back
    springTo(0, { initialVelocity: velocity });
  }
}
```

### Momentum Scrolling (Deceleration)

```javascript
// Apple's deceleration curve: exponential decay
function momentumScroll(velocity, decelerationRate = 0.998) {
  // Apple uses ~0.998 for normal, ~0.999 for fast
  const displacement = velocity * decelerationRate / (1 - decelerationRate);
  const duration = Math.log(1 / Math.abs(velocity)) / Math.log(decelerationRate);

  return { displacement, duration: Math.min(duration, 3000) };
}

// Framer Motion velocity usage
<motion.div
  drag="y"
  onDragEnd={(e, info) => {
    const velocity = info.velocity.y;
    // velocity > 0 = dragging down, < 0 = dragging up
    if (Math.abs(velocity) > 500) {
      dismiss();
    }
  }}
  dragConstraints={{ top: 0, bottom: 0 }}
  dragElastic={0.2}  // rubber banding factor
/>
```

### Velocity Thresholds (Apple conventions)

```
Slow gesture:    < 200 px/s   → return to original, no action
Medium gesture:  200-800 px/s → context-dependent (may trigger action)
Fast gesture:    > 800 px/s   → always trigger action (dismiss, switch, etc.)

Flick:           > 1200 px/s  → instant action, minimal animation
```

### Rules

- **ALWAYS** use gesture velocity as spring initialVelocity — this creates continuity
- **ALWAYS** have a velocity threshold (500px/s) AND a distance threshold (50%) — either can trigger
- **NEVER** hard-cut from gesture to animation — the velocity must transfer
- **NEVER** use fixed animation duration after gesture — derive from velocity
- **PREFER** shorter animations for high velocity, longer for low velocity
- **USE** deceleration rate 0.998 for standard scroll momentum
- **USE** `dragElastic={0.2}` in Framer Motion for rubber band on drag bounds

---

## 4. Optical Corrections

Mathematics lies. Human perception is the truth. Apple adjusts everything for how it looks, not how it measures.

### Vertical Center Correction

```css
/* Math says centered. Eyes say it's too low. */
.visually-centered {
  /* Shift up ~4% of container height */
  transform: translateY(-4%);
}

/* Icon in circle — shift right and down slightly to compensate optical weight */
.play-icon-in-circle {
  /* Play triangle appears left-heavy, shift right ~8% */
  transform: translateX(8%);
}
```

### Text Alignment Corrections

```css
/* Text with large first letter appears indented — negative margin compensates */
.headline-text {
  margin-left: -0.04em; /* pull left for optical alignment */
}

/* All-caps text needs more letter-spacing */
.label-caps {
  text-transform: uppercase;
  letter-spacing: 0.08em; /* Apple uses 0.06-0.12em for caps */
  font-weight: 600;
}

/* Numbers often need tabular figures for alignment */
.stats-number {
  font-variant-numeric: tabular-nums;
}
```

### Icon Optical Weight

```
Rule: Different shapes at the same pixel size look different sizes.

Circle at 24px looks smaller than square at 24px.
Triangle at 24px looks smaller than circle at 24px.

Compensation:
  Square:   24px (baseline)
  Circle:   26px (~8% larger)
  Triangle: 27px (~12% larger)

Apple's SF Symbols handles this automatically. On web, adjust manually.
```

### Border Radius Optical Sizing

```css
/* Smaller elements need proportionally larger corner radius to look consistent */
.chip       { border-radius: 8px; }   /* 32px height → 25% of height */
.button     { border-radius: 10px; }  /* 44px height → 23% of height */
.card       { border-radius: 14px; }  /* 200px height → 7% of height */
.modal      { border-radius: 20px; }  /* 400px height → 5% of height */
.fullscreen { border-radius: 0; }     /* no radius at edges of screen */

/* Apple's rule: radius decreases as % of height for larger elements */
```

### Padding Optical Balance

```css
/* Buttons: horizontal padding > vertical (text is wider than tall) */
.button {
  padding: 10px 20px; /* 1:2 ratio — looks evenly padded */
  /* padding: 15px 15px → looks taller than wide to the eye */
}

/* Cards: bottom padding slightly larger (gravity effect) */
.card {
  padding: 24px 24px 28px 24px; /* extra 4px bottom */
}

/* Icons next to text: icon needs less horizontal spacing than text suggests */
.icon-text {
  gap: 6px; /* not 8px — icon "carries" its own optical space */
}
```

### Rules

- **ALWAYS** adjust vertical centering up by ~4% for visual balance
- **ALWAYS** use wider letter-spacing for uppercase text (0.06-0.12em)
- **ALWAYS** use `font-variant-numeric: tabular-nums` for number columns
- **NEVER** trust mathematical centering — verify visually
- **PREFER** asymmetric padding: more horizontal on buttons, more bottom on cards
- **SCALE** corner radius relative to element size (smaller elements → proportionally larger radius)
- **COMPENSATE** icon sizes: triangles > circles > squares at same visual weight
- **INDENT** play buttons right ~8% to optically center in circles

---

## 5. Material Depth System

Apple's interfaces are layered like physical materials. Each layer has distinct properties.

### Layer Hierarchy

```
Layer 0: Base (background)
  → No blur, no shadow
  → Solid color: --bg-primary (#fbfbfd / #1d1d1f)

Layer 1: Grouped content (cards, cells)
  → Slight elevation
  → Shadow: 0 1px 3px rgba(0,0,0,0.06)
  → Background: --bg-secondary (#f5f5f7 / #2c2c2e)

Layer 2: Elevated (popovers, menus)
  → Medium elevation
  → Shadow: 0 4px 12px rgba(0,0,0,0.08)
  → Can use material blur

Layer 3: Modal (sheets, dialogs)
  → High elevation
  → Shadow: 0 8px 28px rgba(0,0,0,0.12)
  → Background dims underneath (scrim)
  → Material: regular blur

Layer 4: Overlay (alerts, toasts)
  → Highest elevation
  → Shadow: 0 12px 40px rgba(0,0,0,0.16)
  → Material: thick blur
```

### Material Blur Levels

```css
/* Ultra Thin — most translucent */
.material-ultra-thin {
  background: rgba(255, 255, 255, 0.25);
  backdrop-filter: blur(10px) saturate(180%);
}

/* Thin — slightly more opaque */
.material-thin {
  background: rgba(255, 255, 255, 0.4);
  backdrop-filter: blur(16px) saturate(180%);
}

/* Regular — standard material (most common) */
.material-regular {
  background: rgba(255, 255, 255, 0.55);
  backdrop-filter: blur(20px) saturate(180%);
}

/* Thick — most opaque */
.material-thick {
  background: rgba(255, 255, 255, 0.72);
  backdrop-filter: blur(30px) saturate(180%);
}

/* Chrome — navigation bars, tab bars */
.material-chrome {
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(40px) saturate(200%);
}

/* Dark mode variants */
@media (prefers-color-scheme: dark) {
  .material-ultra-thin { background: rgba(30, 30, 30, 0.4); }
  .material-thin       { background: rgba(30, 30, 30, 0.55); }
  .material-regular    { background: rgba(30, 30, 30, 0.65); }
  .material-thick      { background: rgba(30, 30, 30, 0.8); }
  .material-chrome     { background: rgba(30, 30, 30, 0.85); }
}
```

### Scrim (Background Dim)

```css
/* Modal scrim */
.scrim {
  background: rgba(0, 0, 0, 0.4);     /* light mode */
  /* background: rgba(0, 0, 0, 0.6); */  /* dark mode — more opaque */
  transition: opacity 0.3s ease;
}
```

### Concentric Radius Rule

```css
/*
  Inner radius = Outer radius - Gap

  This creates "nested" feeling, like physical materials
*/
.outer-container {
  border-radius: 20px;
  padding: 8px;
}
.inner-card {
  border-radius: 12px; /* 20 - 8 = 12 */
}

.modal {
  border-radius: 28px;
  padding: 16px;
}
.modal-content {
  border-radius: 12px; /* 28 - 16 = 12 */
}
```

### Rules

- **ALWAYS** increase blur with layer depth (10px → 16px → 20px → 30px → 40px)
- **ALWAYS** increase shadow spread with depth
- **ALWAYS** use `saturate(180%)` with `backdrop-filter: blur()` — prevents washed-out look
- **ALWAYS** apply concentric radius: inner = outer - padding
- **ALWAYS** include `-webkit-backdrop-filter` for Safari
- **PREFER** semi-transparent backgrounds over solid colors for elevated layers
- **USE** scrim behind modals: rgba(0,0,0,0.4) light / rgba(0,0,0,0.6) dark
- **STACK** shadows — don't just use one: combine ambient (spread) + direct (offset)
- **MATCH** blur opacity to content importance: more important = more opaque material

---

## 6. P3 Wide Gamut Color

Apple devices use Display P3 — 25% more colors than sRGB. If you only design in sRGB, you're leaving vibrancy on the table.

### Using P3 on Web

```css
/* P3 colors — more vivid than sRGB equivalents */
:root {
  --blue-p3: color(display-p3 0 0.478 1);              /* brighter than #007AFF */
  --red-p3: color(display-p3 1 0.231 0.188);             /* more vivid than #FF3B30 */
  --green-p3: color(display-p3 0.204 0.78 0.349);        /* richer than #34C759 */
  --orange-p3: color(display-p3 1 0.584 0);               /* more saturated #FF9500 */
  --purple-p3: color(display-p3 0.686 0.322 0.871);       /* deeper than #AF52DE */
}

/* Fallback pattern */
.vibrant-button {
  background: #007AFF;                          /* sRGB fallback */
  background: color(display-p3 0 0.478 1);     /* P3 when supported */
}

/* Feature detection */
@media (color-gamut: p3) {
  :root {
    --accent: color(display-p3 0 0.478 1);
  }
}

/* P3 gradients — noticeably more vibrant */
.hero-gradient {
  background: linear-gradient(
    135deg,
    color(display-p3 0.4 0.2 0.9),
    color(display-p3 0.1 0.6 1)
  );
}
```

### oklch + P3

```css
/* oklch can represent P3 colors naturally */
:root {
  /* These oklch values extend into P3 gamut */
  --vivid-blue: oklch(0.65 0.30 265);   /* C > 0.25 = likely P3 */
  --vivid-red: oklch(0.60 0.30 25);
  --vivid-green: oklch(0.70 0.28 155);

  /* sRGB-safe: keep chroma ≤ 0.25 */
  --safe-blue: oklch(0.65 0.20 265);
}
```

### Rules

- **ALWAYS** provide sRGB fallback before P3 color declaration
- **ALWAYS** test on both sRGB and P3 displays
- **PREFER** `color(display-p3 ...)` for known Apple-device targets
- **PREFER** oklch with high chroma (>0.25) for automatic P3 extension
- **USE** `@media (color-gamut: p3)` for P3-specific styles
- **KNOW** P3 gamut: reds, greens, oranges gain the most vibrancy; blues gain less
- **AVOID** P3 for text colors — legibility matters more than vibrancy
- **USE** P3 for: hero gradients, accent buttons, brand colors, illustrations

---

## 7. Micro-Interactions

The tiny moments that create delight. Each must feel physically motivated.

### Button Press

```css
/* Apple-style button press — scale + slight darken */
.button {
  transition: transform 0.15s cubic-bezier(0.2, 0, 0, 1),
              filter 0.15s cubic-bezier(0.2, 0, 0, 1);
  transform-origin: center;
}
.button:active {
  transform: scale(0.97);
  filter: brightness(0.95);
}
/* Spring back handled by browser transition */
```

```javascript
// Framer Motion — spring-based press
<motion.button
  whileTap={{ scale: 0.97 }}
  transition={{ type: "spring", stiffness: 400, damping: 25 }}
/>
```

### Toggle Switch

```css
/* The knob slides AND the track color morphs */
.toggle-track {
  width: 51px; height: 31px;
  border-radius: 16px;
  background: #e9e9ea;
  transition: background 0.25s cubic-bezier(0.25, 0.1, 0.25, 1);
}
.toggle-track.active {
  background: #34c759;
}

.toggle-knob {
  width: 27px; height: 27px;
  border-radius: 14px;
  background: white;
  box-shadow: 0 3px 8px rgba(0, 0, 0, 0.15),
              0 1px 1px rgba(0, 0, 0, 0.06);
  transition: transform 0.25s cubic-bezier(0.25, 0.1, 0.25, 1);
}
.toggle-track.active .toggle-knob {
  transform: translateX(20px);
}

/* Press state: knob stretches slightly */
.toggle-knob:active {
  width: 32px; /* horizontal stretch */
}
```

### Pull-to-Refresh

```
Phase 1: Pull (0-60px)
  → Spinner appears, scales from 0 to 1
  → Resistance increases (rubber band)
  → Haptic: light impact at 60px threshold

Phase 2: Threshold reached (>60px)
  → Spinner starts rotating
  → Haptic: medium impact
  → Release triggers refresh

Phase 3: Loading
  → Content pushes down 60px
  → Spinner animates
  → Spring back on complete
```

### Checkbox / Radio

```css
/* Checkmark draws in with stroke-dasharray animation */
.checkbox-mark {
  stroke-dasharray: 20;
  stroke-dashoffset: 20;
  transition: stroke-dashoffset 0.2s cubic-bezier(0.25, 0.1, 0.25, 1) 0.05s;
}
.checkbox.checked .checkbox-mark {
  stroke-dashoffset: 0;
}

/* Background color fills simultaneously */
.checkbox-bg {
  transition: background 0.15s, border-color 0.15s;
}
.checkbox.checked .checkbox-bg {
  background: var(--accent);
  border-color: var(--accent);
}
```

### Long Press

```
0ms:     Touch down → scale(0.97), brightness(0.95)
100ms:   Still holding → no change
500ms:   Long press threshold → haptic feedback, context menu
Release: Spring back scale(1.0)

The key: scale down happens IMMEDIATELY, context menu appears AFTER delay.
```

### Rules

- **ALWAYS** give immediate visual feedback on touch/click — 0ms delay
- **ALWAYS** use `scale(0.97)` for press (not 0.95 — too aggressive for Apple style)
- **ALWAYS** spring back on release, never snap
- **PREFER** physical metaphor: press = compress, release = expand, swipe = momentum
- **USE** `brightness(0.95)` with scale for press depth
- **USE** stroke-dasharray for checkbox/checkmark draw animation
- **PAIR** with haptics on mobile: light impact for small interactions, medium for confirmations
- **TIME** long press at 500ms — Apple's standard threshold

---

## 8. Proportional Systems

Jony Ive didn't pick numbers randomly. Apple uses mathematical relationships for visual harmony.

### Modular Scale for Typography

```css
/* Based on Major Third (1.25) — Apple's approximate scale */
:root {
  --scale-ratio: 1.25;
  --text-xs:  0.64rem;   /* 10.24px */
  --text-sm:  0.8rem;    /* 12.8px */
  --text-base: 1rem;     /* 16px */
  --text-lg:  1.25rem;   /* 20px */
  --text-xl:  1.563rem;  /* 25px */
  --text-2xl: 1.953rem;  /* 31.25px */
  --text-3xl: 2.441rem;  /* 39.06px */
  --text-4xl: 3.052rem;  /* 48.83px */
  --text-5xl: 3.815rem;  /* 61.04px */
}
```

### Spacing Based on Typography

```css
/* Spacing derives from the type scale — creates visual connection */
:root {
  --space-xs:  0.25rem;  /* 4px  — hairline */
  --space-sm:  0.5rem;   /* 8px  — tight */
  --space-md:  1rem;     /* 16px — body text size = base spacing */
  --space-lg:  1.5rem;   /* 24px — 1.5× base */
  --space-xl:  2.5rem;   /* 40px — ~golden ratio × base */
  --space-2xl: 4rem;     /* 64px — 4× base */
  --space-3xl: 6.5rem;   /* 104px — ~golden ratio × 2xl */
}
```

### Golden Ratio Applications

```
φ = 1.618

Where Apple uses it (approximately):
  - Hero text : body text size ≈ 1.618
  - Content width : sidebar width ≈ 1.618
  - Image aspect ratios: approach 1.618:1
  - Section spacing : content padding ≈ 1.618
  - Card width : card height for landscape cards

Not a strict rule — Apple uses it as a starting point, then adjusts optically.
```

### Aspect Ratios Apple Uses

```css
/* Common Apple aspect ratios */
--ratio-hero: 16 / 9;       /* hero images, videos */
--ratio-product: 4 / 3;     /* product shots */
--ratio-card: 3 / 2;        /* content cards */
--ratio-thumbnail: 1 / 1;   /* app icons, thumbnails */
--ratio-banner: 21 / 9;     /* cinematic, edge-to-edge */

.hero-image {
  aspect-ratio: 16 / 9;
  object-fit: cover;
}
```

### Rules

- **PREFER** modular scale (1.25× or 1.2×) for type sizes — creates natural hierarchy
- **DERIVE** spacing from type scale — creates invisible visual connection
- **USE** golden ratio (~1.618) as starting point, then adjust optically
- **USE** consistent aspect ratios across a page — don't mix randomly
- **KNOW** these are guides, not laws — optical correctness always overrides math

---

## 9. Icon Construction

### Apple's Icon Grid

SVG template: `data/apple-icon-grid.svg` — use as guide layer when designing app icons.

```
Canvas:             1024×1024pt
Squircle mask:      iOS superellipse, ~224pt corner radius
Grid:               8×8 cells (128pt each)

Keyline shapes:
  - Large circle:   r=440pt — primary shape boundary
  - Medium circle:  r=352pt — secondary content boundary
  - Small circle:   r=176pt — inner detail area
  - Square:         720×720pt centered — square icon baseline
  - Landscape rect: 768×592pt — horizontal icons
  - Portrait rect:  592×768pt — vertical icons

All icons use these keyline shapes as starting points.
Diagonal guides cross at center (512, 512) for optical alignment.
```

### SF Symbols Design Principles

```
1. Optical sizing:   Symbols adjust weight at different sizes
2. Weight matching:   Symbol weight matches adjacent text weight
3. Scale variants:    small (footnote), medium (body), large (title)
4. Baseline alignment: symbols sit on text baseline, not center

Web implementation:
  - Use SVG icons at 1em size to match text
  - Set stroke-width relative to font-weight
  - Align with vertical-align: -0.125em (optical baseline)
```

### Web Icon Rules

```css
/* Icon sizing relative to text */
.icon {
  width: 1em;
  height: 1em;
  vertical-align: -0.125em; /* optical baseline alignment */
  fill: currentColor;       /* inherits text color */
}

/* Stroke weight should match font weight */
.icon-light   { stroke-width: 1.2; }  /* with font-weight: 300 */
.icon-regular { stroke-width: 1.5; }  /* with font-weight: 400 */
.icon-medium  { stroke-width: 1.8; }  /* with font-weight: 500 */
.icon-bold    { stroke-width: 2.2; }  /* with font-weight: 700 */
```

### Rules

- **ALWAYS** size icons relative to text (1em) — not fixed pixel sizes
- **ALWAYS** use `fill: currentColor` so icons inherit text color
- **ALWAYS** match icon stroke weight to adjacent font weight
- **PREFER** `vertical-align: -0.125em` for baseline alignment with text
- **USE** Apple's 4 keyline shapes as starting points for custom icons
- **MAINTAIN** consistent optical weight across all icons in a set

---

## 10. Progressive Disclosure

Apple reveals complexity gradually. The first view is always simple.

### Information Architecture Pattern

```
Level 1: Glanceable (hero, summary)
  → One sentence, one action
  → No scrolling required for core message

Level 2: Scannable (features, sections)
  → Short paragraphs, visual anchors
  → Cards, grids, icons
  → Each section self-contained

Level 3: Detailed (specs, comparisons)
  → Full specs, tables, footnotes
  → Often behind "Learn more" or accordion
  → User opted in to see this

Level 4: Expert (developer docs, API)
  → Technical depth
  → Code examples, parameters
  → Only shown on demand
```

### UI Patterns

```css
/* Accordion — hidden by default */
.disclosure details {
  border-bottom: 1px solid var(--separator);
}
.disclosure summary {
  padding: 16px 0;
  cursor: pointer;
  list-style: none;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.disclosure summary::after {
  content: "+";
  font-size: 1.5rem;
  color: var(--secondary-label);
  transition: transform 0.3s var(--ease-default);
}
.disclosure details[open] summary::after {
  transform: rotate(45deg);
}
.disclosure .content {
  padding-bottom: 16px;
  color: var(--secondary-label);
}

/* "Learn more" link */
.learn-more {
  color: var(--accent);
  text-decoration: none;
  cursor: pointer;
}
.learn-more::after {
  content: " ›";
}
```

### Rules

- **ALWAYS** lead with the simplest possible view — one message, one action
- **ALWAYS** let users opt into complexity (expand, "Learn more", drill-down)
- **NEVER** show everything at once — it's not transparency, it's noise
- **NEVER** hide primary actions — only hide secondary/tertiary information
- **PREFER** progressive reveal over tabs for sequential information
- **PREFER** inline expansion over navigation for small amounts of detail
- **USE** "Learn more ›" pattern for linking to detailed content
- **TIME** reveal animations at 300-400ms with ease-out

---

## 11. Sensory Pairing

Apple synchronizes haptic, audio, and visual feedback. They should feel like one event.

### Haptic Types (iOS)

```swift
// Impact feedback — physical collision feel
UIImpactFeedbackGenerator(style: .light)    // tap a button
UIImpactFeedbackGenerator(style: .medium)   // toggle switch
UIImpactFeedbackGenerator(style: .heavy)    // significant action
UIImpactFeedbackGenerator(style: .soft)     // gentle interaction
UIImpactFeedbackGenerator(style: .rigid)    // hard surface feel

// Selection feedback — moving through options
UISelectionFeedbackGenerator()              // picker, slider tick

// Notification feedback — outcome
UINotificationFeedbackGenerator(.success)   // task completed
UINotificationFeedbackGenerator(.warning)   // careful
UINotificationFeedbackGenerator(.error)     // something failed
```

### Web Vibration (limited)

```javascript
// Web Vibration API (Android only, no iOS)
navigator.vibrate(10);   // short buzz — button press
navigator.vibrate(25);   // medium — toggle
navigator.vibrate([10, 50, 10]); // pattern — error

// Feature detection
if ('vibrate' in navigator) {
  navigator.vibrate(10);
}
```

### Pairing Matrix

```
Action              Visual                Haptic          Sound
─────────           ──────                ──────          ─────
Button press        scale(0.97)           light impact    —
Toggle on           slide + color         medium impact   click
Toggle off          slide + decolor       light impact    —
Pull-to-refresh     spinner + threshold   light at pull   —
Delete swipe        red reveal            medium impact   —
Success             checkmark draw        success notif   chime
Error               shake animation       error notif     bonk
Selection change    highlight + spring    selection       tick
Long press          scale + context menu  heavy impact    —
Drag threshold      snap to guide         rigid impact    snap
```

### Rules

- **ALWAYS** synchronize: haptic fires at the same frame as visual change
- **NEVER** use haptics without visual feedback — they must reinforce each other
- **NEVER** overuse haptics — they should mark moments, not narrate everything
- **PREFER** subtle haptics (light, soft) for frequent interactions
- **RESERVE** heavy haptics for significant moments (confirm, delete, complete)
- **USE** selection feedback for continuous controls (sliders, pickers)
- **USE** notification feedback for outcomes (success, warning, error)
- **PAIR** error haptic with shake animation (3-4 oscillations, 300ms)
- **ON WEB** compensate for no haptics with stronger visual feedback

---

## 12. Reduced Motion — The Complete Picture

Apple's `prefers-reduced-motion` is more nuanced than "disable all animations."

### What to Do (Not Just Disable)

```
Instead of...              Do this...
─────────────              ─────────
Slide in from right    →   Crossfade (opacity only)
Zoom in/out            →   Crossfade
Parallax scrolling     →   Static (no movement)
Bouncy spring          →   Smooth ease (no overshoot)
Auto-playing video     →   Poster frame (pause)
Spinning loader        →   Pulsing opacity
Shake animation        →   Border color flash
Scroll-linked motion   →   Instant state (no scrub)

The principle: reduce MOTION, not FEEDBACK.
Still communicate state changes — just without spatial movement.
```

### Implementation

```css
@media (prefers-reduced-motion: reduce) {
  /* Replace spatial animations with opacity */
  .reveal {
    animation: none;
    opacity: 1; /* just show it */
  }

  /* Shorten transitions instead of removing */
  * {
    transition-duration: 0.1s !important;
  }

  /* Replace bouncy springs with smooth */
  .interactive {
    transition-timing-function: ease !important;
  }

  /* Stop auto-playing animations */
  .ambient-animation {
    animation-play-state: paused !important;
  }

  /* Disable parallax */
  .parallax {
    transform: none !important;
  }
}
```

```javascript
// JavaScript — swap spring for smooth
const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

const transitionConfig = reducedMotion.matches
  ? { duration: 0.15, ease: "easeOut" }                    // smooth, fast
  : { type: "spring", stiffness: 300, damping: 25 };       // springy

// GSAP
if (reducedMotion.matches) {
  gsap.globalTimeline.timeScale(10); // effectively instant
  ScrollTrigger.config({ limitCallbacks: true });
}

// Three.js
if (reducedMotion.matches) {
  // Show static scene, don't animate
  renderer.setAnimationLoop(null);
  renderer.render(scene, camera); // single frame
}
```

### Rules

- **ALWAYS** respect `prefers-reduced-motion` — this is accessibility, not optional
- **NEVER** just disable everything — replace spatial motion with opacity transitions
- **PREFER** crossfades over slides/zooms for reduced motion
- **KEEP** state feedback — color changes, opacity, borders still communicate
- **SHORTEN** transition durations to 100-150ms (not zero)
- **PAUSE** ambient/decorative animations
- **REMOVE** parallax, scroll-linked motion, bouncy springs entirely
- **TEST** with reduced motion ON — the experience must still be complete

---

## Quick Reference: The Feel Checklist

Before shipping any interaction:

```
□ Does it use spring physics (not linear/ease)?
□ Does gesture velocity transfer to animation?
□ Does it rubber-band at boundaries?
□ Is it optically centered (not mathematically)?
□ Do corners follow concentric radius rule?
□ Is spacing on the 8pt grid?
□ Does reduced motion provide equivalent feedback?
□ Are touch targets ≥ 44×44pt?
□ Is the hierarchy clear at a glance?
□ Does the material depth feel consistent?
□ Are haptic/visual/audio synchronized?
□ Does it feel inevitable — like the only possible solution?
```
