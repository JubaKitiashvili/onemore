# Apple.com Design Patterns -- Deep Analysis

Extracted from 13 Apple product page HTML source files. Every animation, layout, typography, and interaction pattern cataloged.

## Sources

| # | File | Lines | Product Type |
|---|------|-------|--------------|
| 1 | airpods-pro.html | 3,371 | Wearable / Audio |
| 2 | apple-intelligence.html | 1,771 | Software / AI |
| 3 | apple-vision-pro.html | 2,467 | Spatial / Premium |
| 4 | apple-watch-series-11.html | 3,453 | Wearable / Watch |
| 5 | apple-watch-ultra-3.html | 3,583 | Wearable / Watch Pro |
| 6 | imac.html | 3,326 | Desktop |
| 7 | ipad-air.html | 3,542 | Tablet |
| 8 | ipad-pro.html | 4,013 | Tablet Pro |
| 9 | iphone-16-pro.html | 4,441 | Phone Pro |
| 10 | iphone.html | 4,441 | Phone |
| 11 | macbook-air.html | 3,585 | Laptop |
| 12 | macbook-neo.html | 3,748 | Laptop (new gen) |
| 13 | macbook-pro.html | 6,453 | Laptop Pro |

---

## 1. Animation System

### 1.1 Scroll-Linked Animation Engine (`data-anim-keyframe`)

Apple uses a custom scroll-linked animation engine controlled entirely through `data-anim-keyframe` JSON attributes on HTML elements. The engine maps scroll position to CSS property changes.

#### Keyframe JSON Format

```json
{
  "start": "t - 70vh",           // Scroll position where animation begins
  "end": "a0b + 100vh",          // Scroll position where animation ends
  "opacity": [0, 1],             // Property: [startValue, endValue]
  "y": ["0", "max(-10h, -10vh)"],// Y translation range
  "cssClass": "animate",         // Class to toggle instead of interpolating
  "toggle": false,               // Whether class toggles on/off
  "anchors": [".section-performance"], // Reference elements for positioning
  "breakpointMask": ["xlarge", "large", "medium", "small", "xsmall"],
  "disabledWhen": ["no-enhanced", "reduced-motion"],
  "easeFunction": "easeInOutQuad"
}
```

#### Position Expression Syntax

The engine uses a custom expression language for `start` and `end`:

| Token | Meaning |
|-------|---------|
| `t` | Top of current element |
| `b` | Bottom of current element |
| `h` | Height of current element |
| `a0t` | Top of anchor[0] |
| `a0b` | Bottom of anchor[0] |
| `a0h` | Height of anchor[0] |
| `a1t`, `a1b` | Top/bottom of anchor[1] |
| `Xvh` | Viewport height percentage |
| `css(--var-name)` | Read CSS custom property |
| `css(--var, a0)` | Read CSS var from anchor[0]'s context |
| `min(a, b)` | Minimum of two values |
| `max(a, b)` | Maximum of two values |
| `lerp(pos, rangeStart, rangeEnd)` | Linear interpolation within range |

#### Start Trigger Expressions (by frequency)

| Expression | Count | Description |
|------------|-------|-------------|
| `a0t - 200vh` | 55 | 2 viewports before anchor top (earliest trigger) |
| `a0t - 100vh` | 49 | 1 viewport before anchor top |
| `t - 200vh` | 16 | 2 viewports before element top |
| `min(a0t + 1px, a1t - 95vh)` | 9 | Complex: earliest of two conditions |
| `t - 70vh` | 7 | 70% viewport before element |
| `a0t - 75vh` | 6 | 75% viewport before anchor |
| `a0t - 150vh` | 5 | 1.5 viewports before anchor |
| `t - 220vh` | 3 | 2.2 viewports before element |
| `t - 90vh` | used in macbook-pro | 90% viewport before element |
| `a0t - 80vh` | 1 | 80% viewport before anchor |

#### End Trigger Expressions (by frequency)

| Expression | Count | Description |
|------------|-------|-------------|
| `a0b + 100vh` | 101 | 1 viewport past anchor bottom (dominant) |
| `b + 100vh` | 9 | 1 viewport past element bottom |
| `a1b` | 9 | At anchor[1] bottom |
| `a0b` | 7 | At anchor bottom |
| `a0t + 50vh` | 6 | Half viewport past anchor top |
| `b + 200vh` | 4 | 2 viewports past element bottom |
| `b + 500vh` | 2 | 5 viewports past element bottom (very long) |
| `a0b + 150vh` | 1 | 1.5 viewports past anchor bottom |

#### CSS Class Triggers (non-interpolated)

Instead of interpolating values, some keyframes toggle CSS classes:

| cssClass | Count | Purpose |
|----------|-------|---------|
| `animate` | 7 | Generic animation trigger (used on 7 pages) |
| `active` | 7 | Active state (macbook-neo chapters) |
| `slide` | 6 | Slide-in animation (ipad-pro touts) |
| `will-change` | 4 | Enable GPU acceleration on-demand |
| `show` | 1 | Visibility toggle (macbook-pro hardware zoom) |

#### Multi-Step Keyframes

Elements can have sequential keyframes using numbered attributes:

| Attribute | Count |
|-----------|-------|
| `data-anim-keyframe` | (primary) |
| `data-anim-keyframe-1` | 5 |
| `data-anim-keyframe-2` | 6 |
| `data-anim-keyframe-3` | 6 |
| `data-anim-keyframe-4` | 4 |

Used on macbook-pro for scrim opacity fading in/out with hardware zoom.

#### Animated Properties

| Property | Values | Count |
|----------|--------|-------|
| `opacity` | [0, 1] | 10 |
| `opacity` | [1, 0] | 4 |
| `opacity` | [0, css(--hz-css-scrim-opacity)] | 1 |
| `y` | CSS var driven intro/bridge/outro | 12 |
| `--gt-position-x` | [100, 0, "%"] | 1 (gradient text) |

#### Easing Functions

Only one easing function found across all pages:

- `easeInOutQuad` -- used in Apple Vision Pro parallax

Most animations rely on the default (likely linear interpolation between scroll positions).

#### disabledWhen Conditions (Progressive Enhancement)

| Condition | Count | Purpose |
|-----------|-------|---------|
| `no-performance-enhanced` | 25 | Disable on low-power devices |
| `no-inline-media` | 22 | Disable when video not supported |
| `no-inline-media` + `reduced-motion` | 18 | Both checks |
| `no-hero-enhance-xp` | 11 | Disable hero enhancements |
| `inline-media` | 9 | Fallback: show when video IS disabled |
| `reduced-motion` | 8 | Respect prefers-reduced-motion |
| `no-enhanced` | 6 | General capability check |
| `enhanced` | 4 | Inverse: show only without enhancement |

#### breakpointMask Values

| Breakpoints | Count | Purpose |
|-------------|-------|---------|
| `xlarge, large, medium, small, xsmall` | 16 | All breakpoints (universal) |
| `xlarge, large` | 9 | Desktop only |
| `small, xsmall` | 2 | Mobile only |
| `medium, small, xsmall` | 2 | Tablet and below |
| `medium` | 1 | Tablet only |

### 1.2 Scroll Animation Groups (`data-anim-scroll-group`)

97 unique scroll group names found across all pages. Groups organize related animations.

#### Universal Groups (appear on most product pages)

- `Hero` / `Hero - Global` -- Hero section animations
- `Design` / `Design - Global` -- Product design sections
- `Performance` -- Chip/speed sections
- `Display` -- Screen sections
- `Camera` / `Cameras` -- Camera sections
- `Battery` -- Battery life sections
- `Chip` -- Processor sections
- `Apple Intelligence` / `Intelligence` -- AI features
- `Index` -- Section index navigation
- `Product Viewer` -- Interactive product explorer
- `Environment` / `Values` -- Sustainability sections
- `Incentive` / `Consider` -- Purchase CTAs
- `Welcome` -- Hero/welcome section

#### Product-Specific Groups

- Vision Pro: `Experiences - Subsection - *`, `Foundation - Global`, `visionOS - Global`
- AirPods: `Audio Performance`, `Noise Control`, `Personalized Listening`, `Hearing Health`
- Watch: `Fitness`, `Health`, `Safety`, `Running`, `Adventure`, `Motivation`
- MacBook Neo: `Section - *` (performance chapters)
- iMac: `Imac Iphone`, `Connections`, `Macos`, `Magic Keyboard`
- iPad: `Ipados`, `Apple Pencil Pro`

### 1.3 StaggeredFadeIn Pattern

**579 total `data-staggered-item` elements** across 8 pages.

| Page | Staggered Items |
|------|----------------|
| apple-watch-ultra-3.html | 114 |
| apple-watch-series-11.html | 89 |
| macbook-pro.html | 78 |
| macbook-neo.html | 72 |
| airpods-pro.html | 68 |
| iphone-16-pro.html | 59 |
| iphone.html | 59 |
| imac.html | 40 |

**How it works:**
- Parent element has `data-component-list="StaggeredFadeIn"`
- Child elements have `data-staggered-item=""` attribute
- Initial state: `opacity: 0; transform: matrix(1, 0, 0, 1, 0, 30)` (invisible, 30px below)
- Final state: `opacity: 1; transform: matrix(1, 0, 0, 1, 0, 0)` (visible, original position)
- Items animate in sequence with staggered delays

**Transform states found:**

| Transform | Count | Usage |
|-----------|-------|-------|
| `matrix(1,0,0,1,0,0)` | 164 | Identity / final state |
| `matrix(1,0,0,1,0,30)` | 110 | 30px translateY (stagger start) |
| `translate(0px, 0px)` | 84 | Identity alternate |
| `translate3d(0px,0px,0px) scale(1)` | 19 | 3D identity |
| `translate3d(0px,180px,0px) scale(1)` | 5 | 180px offset (large stagger) |
| `translate3d(-15px,0px,0px) scale(1.3)` | 5 | Shift left + scale up |
| `translate3d(0px,0px,0px) scale(0.5)` | 3 | Scale from 50% |
| `translate3d(0px,-18px,0px) scale(0)` | 3 | Scale from 0 with offset |
| `scale(1.15)` | 1 | Slight scale down to 1 |

**Opacity values found:**

| Value | Count |
|-------|-------|
| `opacity: 0` | 339 (hidden, initial state) |
| `opacity: 1` | 117 (visible, final state) |
| `opacity: 0.001` | 2 (near-invisible, for layout) |
| `opacity: 0.999` | 1 (near-visible, avoids repaint) |

### 1.4 Video Scrubbing (Scroll-Linked Video)

`VideoScrub` component found on 2 pages:
- **airpods-pro.html** (1 instance)
- **macbook-neo.html** (3 instances)

Related DOM classes: `video-scrub-container`, `video-scrub`, `video-scrub-offset-x-progress`

Video playback position is mapped to scroll position, creating the "scrubbing" effect where scrolling controls video timeline.

### 1.5 Video Elements (`data-video-id`)

61 unique video IDs across all pages. Common patterns:

| Category | Example IDs |
|----------|-------------|
| Welcome/Hero | `welcome-hero`, `welcome-video`, `welcome-hero-airpods` |
| Product Viewer | `product-viewer-landing-video`, `product-viewer-display`, `product-viewer-camera` |
| Feature Sections | `display-video`, `chip-video`, `design-video`, `cameras-video` |
| Product Stories | `product-story-video-noise-control`, `product-story-video-fitness-hero` |
| AI/Intelligence | `apple-intelligence-glow`, `ai-apps-ai-features`, `image-playground` |

### 1.6 Gradient Text Animation

**Occurrences:** 43 elements use `gradient-text` class.

**Variants:**
- `gradient-text` -- base gradient
- `gradient-text-blue` -- 13 occurrences (blue-tinted gradient)
- `gradient-text text headline` -- combined with typography classes
- `gradient-text image` -- image-based gradient (performance stats)
- `gradient-text persistent` -- persistent gradient (does not animate out)

**Timing (`--gt-duration` CSS variable):**

| Duration | Count |
|----------|-------|
| `1s` | 8 |
| `1.5s` | 5 |
| `0s` | 1 (instant, no animation) |

**Position animation:** `--gt-position-x: [100, 0, "%"]` -- gradient sweeps from right (100%) to left (0%).

### 1.7 WordAnim Pattern

`WordAnim` component found on **macbook-air.html** (29 instances). Animates individual words within a sentence, likely with staggered opacity/transform reveals.

### 1.8 GPU Acceleration

`will-change: transform` found 8 times (inline styles). Additionally, `WillChange` appears as a component modifier:
- `Card WillChange` (138 instances)
- `ScrollGallery WillChange` (13)
- `VideoGallery WillChange` (3)
- `HighlightsGallery WillChange` (2)
- `ProductGallery WillChange` (2)
- `MediaBlockGallery WillChange` (1)

Pattern: `WillChange` is a composable behavior added to any component that needs GPU acceleration.

### 1.9 lerp() Interpolation System (macbook-neo chapters)

Advanced chapter animations use `lerp()` for normalized positioning within a scroll range:

```
lerp(position, rangeStart, rangeEnd)
```

- `position`: 0.0 to 1.0 normalized position, or CSS variable
- `rangeStart`: scroll position of animation range start
- `rangeEnd`: scroll position of animation range end

**Chapter animation lifecycle (4 phases per chapter):**
1. **intro** -- fade in + translate Y up (opacity 0->1)
2. **bridge** -- hold position, translate Y continues
3. **outro** -- fade out + translate Y (opacity 1->0)
4. **gradient-trigger** -- toggle `active` class for gradient text

Each chapter uses CSS variables like `--ct-chapter1-intro-start`, `--ct-chapter1-bridge-end`, etc.

### 1.10 Preload Strategy

| Strategy | Count |
|----------|-------|
| `keyframe, prior-section` | 8 |

Assets are preloaded when the prior section enters the viewport, driven by keyframe scroll position.

---

## 2. Layout System

### 2.1 Section Types

#### Universal Sections (appear across most pages)

| Section Class | Count | Purpose |
|---------------|-------|---------|
| `section-welcome` | 43 | Hero/landing |
| `section-highlights` | 41 | Key feature highlights |
| `section-performance` | 59 | Chip/speed |
| `section-design` | 22 | Industrial design |
| `section-display` | 29 | Screen/display |
| `section-chip` | 23 | Processor details |
| `section-hero` | 19 | Alternative hero |
| `section-index` | 14 | Section navigation |
| `section-product-stories` | 22 | Feature deep dives |
| `section-contrast` | 24 | High-contrast section |
| `section-apple-intelligence` | 17 | AI features |
| `section-continuity` | 17 | Cross-device features |
| `section-cameras` | 15 | Camera system |
| `section-incentive` | 13 | Purchase CTA |
| `section-storeservices` | 13 | Store services |
| `section-responsibility` | 13 | Values/environment |
| `section-privacy` | 13 | Privacy features |

#### Structural Classes

| Class | Count | Purpose |
|-------|-------|---------|
| `section-header` | 142 | Section header container |
| `section-content` | 94 | Section body content |
| `section-wrapper` | 27 | Section outer wrapper |
| `section-intro` | 34 | Section introduction text |
| `section-copy-block` | 27 | Text content block |
| `section-header-headline` | 156 | Headline within header |
| `section-header-cta-list` | 48 | CTA button list |
| `section-header-link` | 46 | Header links |
| `section-header-eyebrow` | 25 | Eyebrow text |

### 2.2 Spacing System (`ps-spacing-*`)

Three-tier responsive spacing: `large` (desktop), `medium` (tablet), `small` (mobile).

#### All Spacing Values Found

| Class | Count | Likely Pixel Value |
|-------|-------|--------------------|
| `ps-spacing-large-120` | 11 | 120px top padding |
| `ps-spacing-large-80` | 7 | 80px |
| `ps-spacing-large-112` | 2 | 112px |
| `ps-spacing-large-96` | 1 | 96px |
| `ps-spacing-large-48` | 1 | 48px |
| `ps-spacing-large-32` | 1 | 32px |
| `ps-spacing-large-24` | 1 | 24px |
| `ps-spacing-large-16` | 1 | 16px |
| `ps-spacing-large-10` | 8 | 10px |
| `ps-spacing-large-0` | 4 | 0px |
| `ps-spacing-medium-120` | 1 | 120px |
| `ps-spacing-medium-100` | 1 | 100px |
| `ps-spacing-medium-96` | 10 | 96px |
| `ps-spacing-medium-92` | 2 | 92px |
| `ps-spacing-medium-72` | 7 | 72px |
| `ps-spacing-medium-24` | 1 | 24px |
| `ps-spacing-small-72` | 10 | 72px |
| `ps-spacing-small-64` | 6 | 64px |
| `ps-spacing-small-60` | 1 | 60px |
| `ps-spacing-small-40` | 4 | 40px |
| `ps-spacing-small-32` | 1 | 32px |
| `ps-spacing-small-8` | 8 | 8px |

**Common spacing combinations (desktop/tablet/mobile):**
- 120 / 96 / 72 -- Large section gaps (most common)
- 80 / 72 / 64 -- Medium section gaps
- 10 / 24 / 8 -- Small internal spacing

### 2.3 Grid System (`ric-*`)

12-column responsive grid with three breakpoints: `large`, `medium`, `small`.

#### Large (Desktop) Columns

| Class | Count | Usage |
|-------|-------|-------|
| `ric-large-12` | 36 | Full width |
| `ric-large-8` | 14 | 2/3 width |
| `ric-large-6` | 15 | Half width |
| `ric-large-5` | 9 | ~42% width |
| `ric-large-4` | 12 | 1/3 width |
| `ric-large-3` | 9 | 1/4 width |
| `ric-large-7` | 8 | ~58% width |
| `ric-large-10` | 7 | ~83% width |
| `ric-large-9` | 1 | 3/4 width |
| `ric-large-2` | 1 | 1/6 width |

#### Medium (Tablet) Columns

| Class | Count |
|-------|-------|
| `ric-medium-10` | 9 |
| `ric-medium-8` | 6 |
| `ric-medium-12` | 6 |
| `ric-medium-4` | 8 |
| `ric-medium-7` | 3 |
| `ric-medium-6` | 3 |
| `ric-medium-5` | 3 |

#### Small (Mobile) Columns

| Class | Count |
|-------|-------|
| `ric-small-12` | 65 | Nearly always full width on mobile |
| `ric-small-10` | 6 |
| `ric-small-8` | 2 |
| `ric-small-11` | 1 |

**Key pattern:** Mobile is almost always full-width (`ric-small-12`). Content narrows responsively via `ric-large-10` -> `ric-medium-10` -> `ric-small-12`.

### 2.4 Dark/Light Theme Alternation

| Class | Total Count |
|-------|-------------|
| `theme-light` | 121 |
| `theme-dark` | 87 |
| `theme-changer` | 36 (dynamic switching) |
| `theme-toggle` | 2 |

**Per-Page Theme Distribution:**

| Page | Light | Dark | Dominant |
|------|-------|------|----------|
| airpods-pro | 10 | 0 | All light |
| apple-intelligence | 0 | 2 | All dark |
| apple-vision-pro | 3 | 1 | Mostly light |
| apple-watch-series-11 | 12 | 5 | Mixed, light dominant |
| apple-watch-ultra-3 | 15 | 18 | Mixed, dark dominant |
| imac | 0 | 0 | Neutral (no theme classes) |
| ipad-air | 5 | 1 | Light dominant |
| ipad-pro | 0 | 11 | All dark (Pro = dark) |
| iphone-16-pro | 22 | 12 | Mixed |
| iphone | 22 | 12 | Mixed |
| macbook-air | 0 | 2 | Dark |
| macbook-neo | 14 | 2 | Light dominant |
| macbook-pro | 17 | 22 | Mixed, dark dominant |

**Pattern:** "Pro" products tend toward dark themes. Consumer products lean light. Sections alternate to create visual rhythm.

### 2.5 Section Padding Overrides

| Class | Count |
|-------|-------|
| `background-alt` | 135 (alternating background colors) |
| `no-pad-top` | 40 (removes top padding) |
| `no-pad-bottom` | 30 (removes bottom padding) |

---

## 3. Typography System

### 3.1 Typography Classes (All 160+ unique classes)

#### Tier 1: High-Impact Headlines (used sparingly)

| Class | Count | Purpose |
|-------|-------|---------|
| `typography-headline-super` | 15 | Largest headline |
| `typography-headline` | 38 | Primary headline |
| `typography-headline-standalone` | 7 | Full-width standalone |
| `typography-headline-elevated` | 1 | Elevated variant |
| `typography-headline-reduced` | 6 | Smaller headline |
| `typography-hero-headline` | 3 | Hero-specific headline |
| `typography-site-headline` | 15 | Site-level headline |
| `typography-site-headline-elevated` | 18 | Larger site headline |
| `typography-site-headline-reduced` | 28 | Smaller site headline |
| `typography-site-headline-secondary` | 4 | Secondary headline |

#### Tier 2: Section Headers

| Class | Count | Purpose |
|-------|-------|---------|
| `typography-section-header-headline` | 59 | Section header text |
| `typography-section-headline` | 25 | Section title |
| `typography-section-headline-reduced` | 7 | Smaller section title |
| `typography-section-intro` | 20 | Section intro paragraph |
| `typography-section-intro-headline` | 11 | Intro headline |
| `typography-section-intro-copy` | 15 | Intro body text |
| `typography-section-intro-eyebrow` | 7 | Intro eyebrow |
| `typography-section-intro-elevated` | 5 | Elevated intro |
| `typography-section-body` | 16 | Section body text |
| `typography-section-label` | 9 | Section labels |
| `typography-section-eyebrow` | 8 | Section eyebrow |
| `typography-section-subheadline` | 2 | Sub-headline |
| `typography-section-stats` | 3 | Stats display |

#### Tier 3: Eyebrows and Labels

| Class | Count | Purpose |
|-------|-------|---------|
| `typography-eyebrow` | 15 | Standard eyebrow |
| `typography-eyebrow-elevated` | 21 | Larger eyebrow |
| `typography-eyebrow-reduced` | 26 | Smaller eyebrow |
| `typography-eyebrow-super` | 10 | Largest eyebrow |

#### Tier 4: Body Text

| Class | Count | Purpose |
|-------|-------|---------|
| `typography-site-body` | 98 | Standard body |
| `typography-site-body-reduced` | 25 | Smaller body |
| `typography-body` | 5 | Base body |
| `typography-body-reduced` | 9 | Reduced body |
| `typography-body-tight` | 1 | Tight line-height |
| `typography-body-reduced-tight` | 1 | Both reduced + tight |

#### Tier 5: Component-Specific Typography

| Class | Count | Context |
|-------|-------|---------|
| `typography-feature-card-headline` | 88 | Feature card titles |
| `typography-feature-card-label` | 88 | Feature card labels |
| `typography-feature-card-body` | 60 | Feature card body |
| `typography-icon-card-headline` | 50 | Icon card titles |
| `typography-icon-card-body-copy` | 68 | Icon card body |
| `typography-caption-tile` | 183 | Tile captions (most used) |
| `typography-drawer-caption` | 51 | Drawer/accordion captions |
| `typography-media-card-gallery-headline` | 35 | Media card headlines |
| `typography-product-tile-headline` | 22 | Product tile titles |
| `typography-product-tile-subheading` | 29 | Product tile subtitles |
| `typography-product-tile-positioning` | 22 | Product tile positioning text |
| `typography-product-tile-ctas` | 22 | Product tile CTAs |
| `typography-product-stories-headline` | 18 | Product story titles |
| `typography-product-stories-copy` | 15 | Product story body |
| `typography-chapternav-label` | 18 | Chapter navigation labels |
| `typography-index-item-base` | 54 | Index navigation items |
| `typography-index-item-elevated` | 21 | Elevated index items |
| `typography-index-headline` | 8 | Index section headline |

#### Tier 6: Modal Typography

| Class | Count | Context |
|-------|-------|---------|
| `typography-inner-container-modal-copy` | 224 | Modal body (MOST used class) |
| `typography-utility-modal-block-body` | 187 | Modal block body |
| `typography-modal-header-headline` | 113 | Modal headers |
| `typography-modal-header-topic-label` | 95 | Modal topic labels |
| `typography-site-modal-body` | 26 | Site modal body |
| `typography-site-modal-headline` | 22 | Site modal headline |
| `typography-site-modal-link` | 24 | Site modal links |
| `typography-site-modal-topic-label` | 16 | Site modal topics |
| `typography-site-modal-inline-headline` | 10 | Inline headline in modal |
| `typography-utility-modal-block-inline-headline` | 30 | Inline headline in utility modal |
| `typography-icon-card-modal-content-inline-headline` | 29 | Icon card modal headline |

#### Tier 7: Gallery and Caption Typography

| Class | Count |
|-------|-------|
| `typography-gallery-card-caption` | 20 |
| `typography-gallery-caption` | 19 |
| `typography-gallery-description-copy` | 7 |
| `typography-gallery-headline` | 3 |
| `typography-fade-gallery-captions` | 28 |
| `typography-fade-gallery-captions-elevated` | 8 |
| `typography-fade-gallery-sosumi` | 15 |
| `typography-caption` | 36 |
| `typography-display-caption` | 3 |

#### Tier 8: Special Purpose

| Class | Count | Context |
|-------|-------|---------|
| `typography-callout-base` | 46 | Callout text |
| `typography-callout-elevated` | 3 | Larger callout |
| `typography-callout-copy` | 3 | Callout body |
| `typography-ps-callout` | 14 | Product story callout |
| `typography-ps-body` | 17 | Product story body |
| `typography-ps-headline-standalone` | 8 | Product story standalone headline |
| `typography-tout-copy` | 12 | Tout copy |
| `typography-tout-reduced` | 8 | Reduced tout |
| `typography-tout-subheading` | 5 | Tout subheading |
| `typography-site-stat-caption` | 13 | Stat captions |
| `typography-graph-label` | 9 | Performance graph labels |
| `typography-graph-stat` | 3 | Performance graph stats |
| `typography-banner-card-headline` | 9 | Banner card titles |
| `typography-banner-card-copy` | 9 | Banner card body |
| `typography-video-attribution` | 9 | Video attributions |
| `typography-compare-product-name` | 2 | Compare table names |
| `typography-compare-product-eyebrow` | 2 | Compare table eyebrows |
| `typography-compare-cta` | 2 | Compare table CTAs |
| `typography-compare-headline` | 1 | Compare table headline |
| `typography-site-play-pause-button` | 7 | Play/pause button text |
| `typography-all-access-pass-pv-item-title` | 35 | AAP item titles |
| `typography-all-access-pass-pv-item-label` | 35 | AAP item labels |
| `typography-all-access-pass-pv-item-body` | 35 | AAP item body |

### 3.2 Headline Hierarchy Pattern

Typical section structure:
```
eyebrow (typography-eyebrow-*)         -- "New" / category label
headline (typography-section-headline)  -- Main section title
intro (typography-section-intro-copy)   -- 1-2 sentence description
CTA link (typography-section-header-link) -- "Learn more >"
```

---

## 4. Component Catalog

### 4.1 Core Components by Frequency

| Component | Count | Pages |
|-----------|-------|-------|
| `Card WillChange` | 138 | All except apple-intelligence, vision-pro |
| `StaggeredFadeIn` | 135 | 8 pages |
| `Modal` | 114 | All major product pages |
| `InlineMedia` | 37 | apple-intelligence, vision-pro, macbook-air |
| `InlineMediaPlugins` | 36 | imac, ipad-air, ipad-pro |
| `WordAnim` | 29 | macbook-air only |
| `IconCardModal` | 25 | ipad-air, ipad-pro, macbook-air |
| `InlineMediaDefault` | 19 | airpods, watches, macbooks |
| `AllAccessPassL2` | 14 | imac, ipad-air, ipad-pro |
| `ScrollGallery` | 13 | Multiple pages |
| `ScrollGallery WillChange` | 13 | Multiple pages |
| `CaptionTileGallery StaggeredFadeIn` | 12 | watches, macbooks |
| `ProductViewerMediaDefault` | 10 | watches, macbooks |
| `L2Modal` | 10 | ipad-air, ipad-pro |
| `CardGallery` | 9 | vision-pro, iphones |
| `VideoGallery` | 8 | iphones |
| `Index` | 8 | Navigation indexes |
| `Portal` | 7 | vision-pro (spatial content) |
| `TextIconControl` | 6 | watches, macbooks |
| `SlideGallery` | 6 | iPads |
| `MediaCardGallery` | 6 | watches, macbooks, airpods |
| `MediaCardGalleryControl` | 5 | Same pages as MediaCardGallery |
| `ProductViewerCore ProductViewer ProductViewerSmall` | 5 | watches, macbooks, airpods |
| `GraphGalleryInitialize` | 5 | macbook-pro |
| `FadeGallery` | 5 | airpods, macbooks |
| `Welcome` | 5 | watches, macbooks, airpods |
| `VideoScrub` | 4 | airpods, macbook-neo |
| `ScrollGallery FocusManager` | 4 | macbook-air |
| `ProductViewerColorNavGallery` | 4 | watches, macbooks |
| `CaptionTileGallery` | 4 | airpods, macbook-pro |
| `BackgroundBlur` | 3 | watch-series-11 |
| `ParallaxImage` | 3 | airpods |
| `PerformanceGallery` | 3 | macbook-air |
| `ArLink` | 3 | imac, iPads |
| `UpgradersGallery` | 3 | imac, macbooks |
| `HardwarePinAnimation` | 2 | macbook-air |
| `ImageAccordion` | 2 | iphones |
| `ChapterNav ChapterNavAnimation ChapterNavGallery` | 2 | iphones |
| `TextOverMedia` | 2 | macbooks |
| `ModelsToggleGallery` | 2 | macbook-pro |
| `ProductTileGallery` | 2 | iphones |
| `TabnavGallery FocusManager` | 2 | macbook-air |

### 4.2 MediaCardGallery

Horizontal scrolling card galleries with auto-advancing behavior.

**Found on:** airpods-pro, apple-watch-series-11, apple-watch-ultra-3, imac, macbook-neo, macbook-pro

**Structure:**
- `MediaCardGallery` -- main container
- `MediaCardGalleryControl` -- navigation controls (paddlenav)
- Cards with `data-gallery-index="0"` through `"8"`
- Supported by `data-gallery-paddlenav=""` (49 instances)

**Gallery IDs found:**
- `apps-gallery`, `camera-gallery`, `design-gallery`
- `continuity-gallery`, `continuity-fade-gallery`
- `entertainment-gallery`, `connection-gallery`
- `productivity-gallery`, `photos-videos-gallery`
- `visionos-gallery`, `technology-gallery`, `values-gallery`
- `magical`

### 4.3 ProductViewer (Interactive Product Explorer)

**Found on:** airpods-pro, apple-watch-series-11, apple-watch-ultra-3, macbook-neo, macbook-pro

**Components:**
- `ProductViewerCore ProductViewer ProductViewerSmall` -- core viewer
- `ProductViewerColorNavGallery` -- color selection gallery
- `ProductViewerMediaDefault` -- media fallback

**Color navigation values:**
- `default__starlight`, `default__space-gray`, `default__space-black`
- `default__silver`, `default__purple`, `default__blue`
- `default__all-colors`

**Deep links:** `data-deep-link="product-viewer"` (3 instances)

### 4.4 All-Access Pass (AAP) -- Sticky Navigation

A sticky overlay that shows contextual info as user scrolls through long sections.

**Structure:**
- Level 1 (`data-aap-level="1"`, 34 instances) -- primary sticky bar
- Level 2 (`data-aap-level="2"`, 12 instances) -- detail overlay/modal

**AAP Types:**
| Type | Count | Purpose |
|------|-------|---------|
| `base` | 12 | Standard AAP |
| `l2-close` | 12 | L2 close button |
| `base-link` | 3 | AAP with link |
| `highlights` | 2 | Highlights variant |
| `base-button` | 2 | AAP with button |
| `3d-viewer` | 2 | AR/3D viewer AAP |
| `product-viewer` | 1 | Product viewer AAP |
| `media-card-gallery` | 1 | Gallery AAP |

**AAP Names:** `all-access-pass` (10), `media-card-gallery` (3), `highlights-gallery` (3)

### 4.5 Chapters (Scroll-Through Performance Stories)

**Found on:** iphone-16-pro, iphone, macbook-neo

`ChapterNav ChapterNavAnimation ChapterNavGallery` -- chapter-based scroll storytelling

macbook-neo uses 4 chapters with:
- Per-chapter CSS variables (`--ct-chapter1-intro-start`, etc.)
- lerp-based scroll positioning
- Gradient text activation per chapter
- Focus management per chapter (`focus-enabled-when: "performance-enhanced"`)

### 4.6 InlineMedia (Video/Image Components)

**60 PlayPause controls** across all pages.

**Media Plugin System:**

| Plugin | Purpose |
|--------|---------|
| `AnimLoad` | Load on scroll animation trigger |
| `AnimPlay` | Play on scroll trigger |
| `AnimPlayReset` | Play and reset on scroll |
| `AnimPlayOnce` | Play once only |
| `ViewportSourceOnce` | Switch source once in viewport |
| `ViewportSourceBaseRes` | Base resolution viewport source |
| `ViewportSource` | Dynamic viewport-based source |
| `ObjectFitFix` | Cross-browser object-fit fix |
| `PlayPauseButton` | Show play/pause UI |
| `PlayPauseButtonDisable` | Disable play/pause UI |
| `PlayProgress` | Show progress indicator |
| `UnloadVideo` | Unload when out of viewport |
| `LoadTimeout` | Timeout fallback for loading |
| `ReplayOnlyAX` | Replay accessible only |
| `WebmReadyEvent` | WebM format ready handler |
| `DisableOnBreakpointChange` | Reset on resize |

**Most common plugin combinations:**
1. `ObjectFitFix, AnimLoad, ViewportSourceBaseRes, PlayPauseButtonDisable, PlayProgress` (20)
2. `AnimLoad, AnimPlayReset, ViewportSourceOnce, ObjectFitFix, UnloadVideo` (9)
3. `PlayPauseButton, AnimLoad, ViewportSourceOnce, ObjectFitFix, UnloadVideo` (8)

**Play keyframe triggers:**
- `{ "start": "t - 100vh", "end": "b" }` -- 23 instances (start 1 viewport before, end at bottom)
- Load keyframe: `{ "start": "t - 150vh", "end": "b + 100vh" }` -- preload 1.5 viewports ahead

### 4.7 Modal System

**113 modal containers** across all pages.

**Structure:**
- `data-modal-container` -- outer container
- `data-modal-overlay` -- background overlay
- `data-modal-content-wrapper` -- content wrapper
- `data-modal-close-button` -- close button
- `data-modal-close-icon` -- close icon
- `data-modal-dialog-labelledby-target` -- accessibility label

**Modal themes:**
- `data-modal-theme="dark"` (8)
- `data-modal-theme="light"` (4)

**Modal blur:** `data-modal-scrim-blur="true"` (12) -- backdrop blur effect

**939 `data-modal-close` elements** -- multiple close targets per modal (close on overlay click, button, etc.)

### 4.8 Compare Tables

`data-compare-gallery=""` found 3 times (iphone-16-pro, iphone, one other). Side-by-side product comparison with product names, eyebrows, and CTAs.

### 4.9 ImageAccordion

Found on iphone-16-pro and iphone. Expandable image panels with titles and descriptions.

Classes: `typography-image-accordion-title-text` (6), `typography-image-accordion-paragraph-text` (6)

### 4.10 Unique Per-Product Components

| Component | Page | Purpose |
|-----------|------|---------|
| `Portal` (7) | apple-vision-pro | Spatial content portals |
| `Sensors` | apple-vision-pro | Sensor visualization |
| `GLGradient` | apple-vision-pro | WebGL gradient background |
| `BatteryAnimation` | apple-watch-series-11 | Battery life animation |
| `BatteryAnim` | macbook-pro | Battery animation variant |
| `BackgroundBlur` (3) | apple-watch-series-11 | Blur effect |
| `AppsParallax` | imac | Parallax app icons |
| `BentoGallery` | imac | Bento grid gallery |
| `ChipSlide` | ipad-air | Chip comparison slide |
| `FanOut` | ipad-air | Fan-out card reveal |
| `FloatUp` | ipad-air | Float-up animation |
| `ChipHero` | macbook-pro | Chip hero animation |
| `ChipFamily` | macbook-pro | Chip family comparison |
| `HardwareZoom` | macbook-pro | Hardware detail zoom |
| `HardwareSlide` | macbook-pro | Hardware slide reveal |
| `HardwarePinAnimation` (2) | macbook-air | Hardware pin callouts |
| `DisplayLayers VideoScroll` | apple-vision-pro | Display layer visualization |
| `PrivacyLock` | apple-intelligence | Privacy lock animation |
| `GraphBars` | ipad-pro | Performance graph bars |
| `ColorGallery` | macbook-air | Color picker gallery |
| `MoreAppsAnimation` | apple-watch-ultra-3 | App grid animation |
| `DesignMediaConfigured` | macbook-neo | Design media handler |
| `Continuity` | macbook-neo | Continuity feature handler |

---

## 5. Interaction Patterns

### 5.1 Focus Management (`data-focus-expression`)

Apple uses scroll-position-based focus management for accessibility. Elements receive focus when they reach a specific scroll position.

**Most common focus expressions:**

| Expression | Count | Behavior |
|------------|-------|----------|
| `a0t - (50vh - 50a0h)` (tabindex 0) | 56 | Focus when gallery centered |
| `a0t - 100vh + a0h + var(...)` | 35 | Focus in media card gallery |
| `max(a0t - (50vh - 50a0h), a0b - 100vh + h)` (tab 0) | 24 | Focus with bottom constraint |
| `a0t - (50vh - 50a0h)` (tabindex -1) | 22 | Focusable but not in tab order |
| `t - 50vh` (tabindex 0) | 18 | Focus when element at 50vh |
| `a0t - ((100vh - 100a0h) / 2)` | 13 | Center in viewport |
| `a0t` (scroll-gallery) | 12 | Focus at gallery top |
| `t - 50vh` with focus-delay | 10 | Delayed focus at 50vh |
| `a0t - 25vh` | 7+6 | Focus at 25vh from anchor |

**`focus-delay: true`** -- delays focus transfer to avoid jarring jumps during fast scrolling.

### 5.2 Deep Linking

| Deep Link Target | Count |
|-----------------|-------|
| `product-viewer` | 3 |
| `get-to-know` | 2 |
| `upgraders-gallery` | 1 |

### 5.3 LocalNav Triggers

The local navigation bar appears/hides based on scroll position:
- `data-localnav-trigger-distance="0"` (4) -- trigger immediately
- `data-localnav-trigger-distance="80px"` (1) -- 80px offset
- `data-localnav-trigger-anchor=".marquee-ctas-link"` (2) -- trigger at CTA
- `data-localnav-trigger-anchor=".detail-inner-group"` (2) -- trigger at detail section

### 5.4 Theme Changers

`theme-changer` (36 instances) -- elements that dynamically switch the theme-light/theme-dark class based on scroll position or state.

---

## 6. Cross-Page Consistency

### Patterns that appear on ALL major product pages (10+)

1. **StaggeredFadeIn or Card WillChange** -- every page has scroll-triggered reveal animations
2. **Modal system** -- every product page has modals with consistent structure
3. **Section header pattern** -- eyebrow + headline + intro copy + CTA
4. **Scroll animation groups** -- every page organizes animations into named groups
5. **Theme alternation** -- sections alternate between light/dark backgrounds
6. **background-alt** -- alternating section backgrounds for visual rhythm
7. **ps-spacing system** -- consistent vertical spacing between sections
8. **typography-* classes** -- unified typography system across all pages
9. **Index navigation** -- section-by-section navigation index
10. **InlineMedia or InlineMediaDefault** -- video components on every page

### Patterns unique to specific product types

| Pattern | Product Types |
|---------|--------------|
| `ProductViewer` + `ColorNavGallery` | Watches, MacBooks, AirPods (physical products with color options) |
| `ChapterNav` | iPhones (scroll-through story chapters) |
| `AllAccessPass` | iPads, iMac (sticky contextual navigation) |
| `VideoScrub` | AirPods, MacBook Neo (scroll-linked video scrubbing) |
| `Portal` + `GLGradient` | Vision Pro (spatial/3D content) |
| `WordAnim` | MacBook Air (word-by-word text animation) |
| `HardwareZoom` + `HardwareSlide` | MacBook Pro (hardware detail exploration) |
| `GraphBars` + `GraphGallery` | MacBook Pro, iPad Pro (performance comparisons) |
| `BentoGallery` | iMac (bento grid layout) |
| `ImageAccordion` | iPhones (expandable image panels) |

### Consumer vs Pro Product Patterns

| Aspect | Consumer (iPhone, Air, Watch) | Pro (iPhone Pro, iPad Pro, MacBook Pro) |
|--------|-------------------------------|----------------------------------------|
| Theme | Light dominant | Dark dominant |
| Animations | Simpler (StaggeredFadeIn) | Complex (multi-step keyframes, chapters) |
| Components | MediaCardGallery, FadeGallery | GraphGallery, HardwareZoom, ChapterNav |
| Performance section | Simple stats | Interactive graphs, chapter-based storytelling |

---

## 7. Key Numbers

### 7.1 All Spacing Values

| Breakpoint | Values Used (px) |
|------------|------------------|
| Large (desktop) | 0, 10, 16, 24, 32, 48, 80, 96, 112, 120 |
| Medium (tablet) | 24, 72, 92, 96, 100, 120 |
| Small (mobile) | 8, 32, 40, 60, 64, 72 |

### 7.2 Animation Timing

| Property | Value | Notes |
|----------|-------|-------|
| Gradient text duration | 1s (dominant), 1.5s, 0s | CSS `--gt-duration` |
| StaggeredFadeIn translateY | 30px | `matrix(1,0,0,1,0,30)` to `matrix(1,0,0,1,0,0)` |
| Opacity transition | 0.5s | Only 1 explicit CSS transition found |
| Easing | `easeInOutQuad` | Only named easing found |
| Most scroll ranges | 100vh - 200vh | Start-to-end distance |

### 7.3 Transform Values

| Transform | Purpose |
|-----------|---------|
| `translateY(30px)` | StaggeredFadeIn offset |
| `translateY(180px)` | Large stagger offset |
| `translate(-15px, 0) scale(1.3)` | Gallery item approach |
| `scale(0.5)` | Scale-up entrance |
| `scale(0)` | Scale from nothing |
| `scale(1.15)` | Slight scale-down entrance |

### 7.4 Opacity Values

| Value | Count | Usage |
|-------|-------|-------|
| 0 | 339 | Initial hidden state |
| 1 | 117 | Final visible state |
| 0.001 | 2 | Near-invisible (maintains layout) |
| 0.999 | 1 | Near-visible (avoids repaint edge case) |

### 7.5 Grid Column Patterns (Common Layouts)

| Layout | Large | Medium | Small |
|--------|-------|--------|-------|
| Full width | 12 | 12 | 12 |
| Centered content | 10 | 10 | 12 |
| Two-column | 6+6 | 6+6 | 12+12 |
| Content + sidebar | 8+4 | 8+4 | 12+12 |
| Three-column | 4+4+4 | 4+4+4 | 12+12+12 |
| Asymmetric | 7+5 | 7+5 | 12+12 |

### 7.6 Component Count Summary

| Component Category | Total Instances |
|-------------------|-----------------|
| Cards (Card WillChange) | 138 |
| Staggered animations | 135 + 579 items |
| Modals | 114 containers, 939 close targets |
| InlineMedia (all variants) | 92 |
| Gallery types (all) | ~80 |
| ProductViewer instances | ~19 |
| Video elements | 61 |
| Gradient text elements | 43 |
| AllAccessPass elements | 34 L1 + 12 L2 |
| Focus expressions | 200+ |

### 7.7 Breakpoint Names

| Name | Likely Viewport |
|------|----------------|
| `xsmall` | < 375px (small phone) |
| `small` | 375-767px (phone) |
| `medium` | 768-1023px (tablet) |
| `large` | 1024-1439px (desktop) |
| `xlarge` | 1440px+ (large desktop) |

---

## 8. Implementation Notes for OneMore

### Key Takeaways

1. **Scroll is the primary interaction paradigm.** Almost every animation is scroll-driven, not time-driven. The `data-anim-keyframe` system maps scroll position to property values through a declarative JSON format.

2. **Progressive enhancement is mandatory.** Every animation has `disabledWhen` conditions. Reduced motion, device capability, and inline media support are all checked before enabling animations.

3. **Components are composable.** `WillChange`, `StaggeredFadeIn`, `FocusManager` are mixed into other components via space-separated `data-component-list` values.

4. **The 30px translate + opacity fade is THE universal reveal pattern.** 339 elements start at `opacity: 0` with `translateY(30px)` and animate to `opacity: 1` at `translateY(0)`.

5. **Sections alternate backgrounds.** 135 uses of `background-alt` create visual rhythm. Combined with `theme-light`/`theme-dark`, this creates the signature Apple scrolling experience.

6. **Typography is extremely granular.** 160+ typography classes ensure every text element has a purpose-specific style. No generic "text-large" -- instead, `typography-feature-card-headline` knows exactly what size/weight/spacing it needs.

7. **Video is treated as first-class content.** 61 video elements with a sophisticated plugin system handle loading, playing, pausing, scrubbing, and unloading based on viewport position.

8. **Modal content is extensive.** Modals are not simple overlays -- they contain full content hierarchies with their own scroll groups, themes, and typography systems.

9. **Spacing follows a clear system.** Desktop: 80-120px between sections. Tablet: 72-96px. Mobile: 40-72px. Internal spacing uses 8-16px.

10. **Dark themes signal "Pro."** Consumer products default to light themes; Pro products default to dark themes. This is a consistent brand signal across all product lines.
