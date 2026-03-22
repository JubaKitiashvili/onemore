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

---

## 7. Apple Developer Website (developer.apple.com)

### 7.1 Sources

| # | File | Lines | Page |
|---|------|-------|------|
| 1 | developer-home.html | 1,183 | developer.apple.com main page |
| 2 | developer-design.html | 1,292 | developer.apple.com/design/ |
| 3 | developer-swift.html | 1,457 | developer.apple.com/swift/ |
| 4 | developer-xcode.html | 1,392 | developer.apple.com/xcode/ |
| 5 | developer-visionos.html | 1,477 | developer.apple.com/visionos/ |
| 6 | developer-ml.html | 1,425 | developer.apple.com/machine-learning/ |
| 7 | developer-wwdc25.html | 393 | developer.apple.com/wwdc25/ |

Total: 8,619 lines across 7 files. Significantly smaller than product pages (avg ~1,231 vs ~3,542 lines per page).

### 7.2 Animation Patterns (Developer)

The developer site uses a **fundamentally different animation approach** from apple.com product pages.

#### What Is Absent (vs. Product Pages)

| Pattern | Product Pages | Developer Pages |
|---------|--------------|-----------------|
| `data-anim-keyframe` | Hundreds of instances | **0** |
| `data-anim` attributes | Extensive | **0** |
| `opacity: 0` (scroll reveal) | 50-100+ per page | **0** |
| `transform:` (scroll-linked) | 100+ per page | **0** |
| `@keyframes` | Multiple per page | **0** |
| `IntersectionObserver` | Core engine | **0** |
| `data-component-list` | Dozens per page | **0** |
| Scroll-linked parallax | Extensive | **0** |

#### What Is Present

The developer site uses only **two animation mechanisms**:

1. **SVG `<animate>` elements** -- Used exclusively for micro-interactions in navigation:
   - Hamburger menu open/close (`globalnav-menutrigger-bread-top/bottom`): 0.24s, spline easing `0.42, 0, 1, 1; 0, 0, 0.58, 1`
   - Chevron expand/collapse (`data-chevron-animate="expand/collapse"`): 320ms, 3-keyframe spline with `keyTimes="0; 0.5; 1"`
   - Both use `begin="indefinite"` (triggered by JS), `fill="freeze"` (hold final state)

2. **CSS `transition`** -- Minimal, only 1-2 occurrences per page, used for hover/focus states on navigation elements. No scroll-linked transitions.

**Key insight**: Developer pages are **content-first, not experience-first**. There are zero scroll-triggered animations. Content appears immediately without any reveal effects.

### 7.3 Layout Patterns (Developer)

#### Navigation Architecture (Two-Tier)

Developer pages use a **dual navigation** system not found on product pages:

1. **Global Nav** (`#globalnav`) -- Shared across all developer.apple.com
   - 7 top-level items: Get Started, Platforms, Technologies, Community, Documentation, Downloads, Support
   - Each has a flyout submenu with `--r-globalnav-flyout-rate: 240ms` animation
   - Flyout uses CSS custom properties for layout: `--r-globalnav-flyout-item-total`, `--r-globalnav-flyout-group-number`, `--r-globalnav-flyout-height`
   - Contains inline search with Quick Links suggestions
   - Account icon with SVG avatar

2. **Local Nav** (`#localnav`) -- Per-section sticky sub-navigation
   - Sticky positioning via `css-sticky` class with `data-sticky` attribute
   - Uses `--r-localnav-menu-tray-natural-height: 55-90px` custom property
   - Contains section-specific tabs (Overview, What's New, Get Started, Resources)
   - Some have action buttons (e.g., Xcode "Download" with dropdown)
   - WWDC25 variant has a masthead SVG logo instead of text title
   - Viewport emitter: `data-viewport-emitter-state` JSON tracks viewport, orientation, retina

#### Grid System

12-column grid using `large-span-*`, `medium-span-*`, `small-span-*` classes:

| Class | Count | Usage |
|-------|-------|-------|
| `small-span-12` | 60 | Full width on mobile (universal) |
| `medium-span-6` | 42 | 2-column on tablet |
| `large-span-4` | 27 | 3-column on desktop |
| `large-span-12` | 22 | Full width on desktop |
| `large-span-6` | 21 | 2-column on desktop |
| `medium-span-12` | 20 | Full width on tablet |
| `large-span-5` | 6 | Asymmetric layouts |
| `large-span-7` | 3 | Asymmetric partner to span-5 |

Grid modifier: `grid-gutterless` (23 uses) removes gutters for edge-to-edge tile layouts.

Also uses an older `column large-* small-*` system alongside the span system:
- `large-centered` (17 uses) -- centers content
- `large-12`, `large-10`, `large-9`, `large-8` for content width constraints

#### Section Structure

```
<main class="main bg-light|bg-fill">
  <article _v="1.0">              <!-- versioned article wrapper (some pages) -->
    <section class="section section-hero [section-hero-img] [theme-dark]">
      <div class="section-content">
        <div class="row">
          <div class="column large-centered large-10 medium-12 text-center">
            <h1 class="typography-headline">...</h1>
            <p class="typography-intro">...</p>
          </div>
        </div>
      </div>
    </section>
    <section class="section [bg-alt|bg-fill|bg-light]">
      ...
    </section>
  </article>
</main>
```

Background alternation classes: `bg-light`, `bg-fill`, `bg-alt` -- simpler than product page system.

#### Homepage Layout (developer-home.html)

Uses a unique **promo-managed-unit** system:

```
<section class="homepage-section section-heroes">
  <ul class="homepage-section-positions">
    <li class="homepage-section-item hero-position homepage-section-light-copy">
      <div class="hero promo-managed-unit hero-large">
        <div class="unit-wrapper unit-wrapper-*">
          <a class="unit-link">
          <div class="unit-image-wrapper">
            <figure class="unit-image unit-image-feature-large">
          </div>
          <div class="unit-copy-wrapper">
            <h4 class="headline">
            <h5 class="subhead">
            <div class="cta-links">
              <a class="more nowrap">
```

Homepage sections: `section-heroes` (hero banner), `section-promos` (platform tiles), `section-pathways` (getting started).

### 7.4 Typography (Developer)

#### Typography Classes

| Class | Count | Purpose |
|-------|-------|---------|
| `typography-card-headline` | 51 | Card titles within tiles |
| `typography-intro` | 24 | Intro/lede paragraphs below headlines |
| `typography-headline-standalone` | 9 | Large standalone headlines (SF Symbol sizing) |
| `typography-eyebrow-reduced` | 7 | Small category labels above sections |
| `typography-headline` | 6 | Page-level h1 titles |
| `typography-manifesto` | 5 | Large statement text |
| `typography-eyebrow-super` | 1 | Extra-large eyebrow (Design page hero) |
| `typography-eyebrow-elevated` | 1 | Mid-size eyebrow |

#### Heading Hierarchy

- **`h1`**: Page title, always uses `typography-headline` class
- **`h2`**: Section titles, plain text (no typography class)
- **`h3`**: Card headlines with `typography-card-headline`, or section sub-headers with `typography-eyebrow-reduced`
- **`h4`**: Used in homepage promos with `headline` class, or card titles with `typography-card-headline`
- **`h5`**: Subheads in promo units with `subhead` class; also `vc-card__title` for video cards

#### Text Modifiers

- `lighter` (52 uses) -- Reduces text weight for secondary text
- `text-center` (41 uses) -- Centers text
- `text-left` (11 uses) -- Left-aligns text
- `nowrap` -- Prevents line breaks on specific phrases
- `more` (31 uses) -- "Learn more" arrow link style
- `link` -- Styled inline link

### 7.5 Component Catalog (Developer)

#### 1. Tile Component (Primary Building Block)

The tile is the atomic card component across all developer pages:

```html
<div class="tile tile-rounded tile-full [tile-shadow] [tile-light] [tile-link] hide-overflow [modal-opener]">
  <div class="tile-content [text-center]">
    <div class="tile-copy-section">
      <p class="tile-category lighter">Category Label</p>
      <h3 class="typography-card-headline">Title</h3>
    </div>
    <img class="card-icon" src="...256x256_2x.png" alt="">
  </div>
  <button class="tile-button-wrapper">
    <span class="tile-button">
      <svg class="tile-icon"><!-- plus icon --></svg>
    </span>
  </button>
</div>
```

| Tile modifier | Count | Purpose |
|---------------|-------|---------|
| `tile-rounded` | 83 | Rounded corners |
| `tile-full` | 66 | Full-height fill |
| `tile-category` | 45 | Category label styling |
| `tile-link` | 40 | Makes tile clickable link |
| `tile-copy-section` | 28 | Text content wrapper |
| `tile-icon` | 23 | Icon within tile |
| `tile-button` | 22 | Expand/modal trigger |
| `tile-shadow` | 6 | Drop shadow variant |
| `tile-light` | 6 | Light background variant |

#### 2. Scrolling Gallery (`sc-gallery`)

Horizontal scrolling card carousel used on visionOS, ML, Swift, and Design pages:

```html
<div class="sc-gallery-container" data-gallery-initialized="true">
  <div class="sc-gallery sc-gallery--align-start">
    <div class="sc-gallery__scroll-container">
      <div class="sc-gallery__item-container">
        <ul class="sc-gallery__card-set" role="list">
          <li class="sc-gallery__item" role="listitem">
            <div class="sc-gallery__card tile tile-rounded tile-full hide-overflow modal-opener"
                 data-aa="modal-*" data-modal="mc-*">
              <!-- tile content -->
            </div>
          </li>
        </ul>
      </div>
    </div>
  </div>
</div>
```

32 gallery items across 4 pages. Each card opens a modal via `data-modal="mc-N"`.

#### 3. Video Card (`vc-card`)

WWDC session video cards (found on wwdc25 page):

```html
<a href="/videos/play/wwdc2025/101/" class="vc-card tile tile-rounded grid-item large-span-4 medium-span-6 small-span-12"
   data-released="true" data-category="technology">
  <div class="vc-card__media">
    <div class="vc-card__image-container">
      <img class="vc-card__image" width="250" src="..." alt="...">
      <span class="vc-card__duration">1:32:36</span>
    </div>
  </div>
  <div class="vc-card__content">
    <div class="tile-content">
      <h5 class="vc-card__title">WWDC 2025 Keynote</h5>
    </div>
  </div>
</a>
```

6 video cards on the WWDC25 page. Uses `data-released` and `data-category` attributes for filtering.

#### 4. Modal System

Developer modals are simpler than product page modals:

```html
<div class="modal-overlay-container">
  <div class="modal-element-container">
    <div class="modal-element-overlay"></div>
    <div class="modal-element-content-container">
      <button class="modal-element-close-button">
        <span class="modal-element-close-icon">
      </button>
      <!-- modal content -->
    </div>
  </div>
</div>
```

- 25 `modal-opener` triggers across all pages
- Named modals: `modal-spatial-visionos-en`, `modal-safe-swift-en`, `modal-mlx-ml-en`, etc.
- Each framework/technology gets its own modal ID

#### 5. Thumbnail Video Component

Video preview with play button overlay (Xcode page):

```html
<a class="thumbnail thumbnail-rounded image-wrapper">
  <img class="thumbnail-image" data-session="wwdc25-219" src="..." width="100%">
  <span class="thumbnail-scrim thumbnail-scrim-bottom"></span>
  <span class="thumbnail-scrim thumbnail-scrim-top"></span>
  <span class="thumbnail-button" aria-label="play">
    <svg><!-- play triangle --></svg>
  </span>
</a>
```

Uses gradient scrims (`thumbnail-scrim-top`, `thumbnail-scrim-bottom`) for text readability over images.

#### 6. Device Hero Frame

Xcode page uses a device frame component:

```html
<figure class="device-hero device-macbook-pro-5th-gen-14-silver large-centered macos-hero">
  <picture class="device-screen">
    <img class="theme-dark-image" src="...dark_2x.png" width="100%">
    <img class="theme-light-image" src="...light_2x.png" width="100%">
  </picture>
</figure>
```

#### 7. Homepage Promo Managed Units

Platform tiles on developer homepage:

```html
<li class="homepage-section-item promo-position homepage-section-item-ios-15" data-promo-type="show-hide">
  <div class="promo promo-managed-unit">
    <div class="unit-wrapper">
      <a class="unit-link" href="...">
      <div class="unit-copy-wrapper">
        <h4 class="headline">iOS 26</h4>
      </div>
      <div class="unit-image-wrapper image-constraints-full">
        <picture>
          <source srcset="...webp" type="image/webp">
          <img class="unit-image unit-image-centered" src="...png">
        </picture>
      </div>
    </div>
  </div>
</li>
```

8 promo positions total. Uses `data-promo-type="show-hide"` for visibility toggling.

#### 8. SF Symbols (Inline SVG Icons)

Machine Learning page uses `<sf-symbol>` custom elements rendered as inline SVGs:

```html
<sf-symbol class="typography-headline-standalone sf-icon"
           name="microphone" weight="semibold" mode="hierarchical"
           loading="eager" aria-hidden="true"
           style="display: inline-flex;">
  <svg viewBox="..." style="width: 1.06em; overflow: visible;">
    <!-- SVG path data -->
  </svg>
</sf-symbol>
```

9 SF Symbol instances. Uses `--s-primary` CSS custom property for theming. `data-sa` attributes for animation state.

#### 9. Dark/Light Theme Image Switching

```html
<img class="theme-light-image" src="...light_2x.png">
<img class="theme-dark-image" src="...dark_2x.png">
```

12 light/dark image pairs. Controlled by `data-color-scheme="light"` on `<body>` and `theme-dark`/`theme-light` section classes. CSS toggles visibility based on active theme.

#### 10. Event Details Component

Homepage "Meet with Apple" section uses event detail containers:

```
event-details-a (10 uses) -- Primary event info
event-details-b (10 uses) -- Secondary event info
```

#### 11. Download Button with Dropdown

Xcode page features a multi-option download button:

```html
<div class="button-multi-container">
  <a class="localnav-button button button-compact button-pill button-multi icon icon-chevrondown">Download</a>
  <div class="button-multi-content button-multi-content-right button-multi-content-slide" role="menu">
    <a class="button-multi-option" role="menuitem">Xcode betas</a>
    <a class="button-multi-option" role="menuitem">Xcode</a>
  </div>
</div>
```

### 7.6 Key Differences from Product Pages

| Aspect | Product Pages (apple.com) | Developer Pages (developer.apple.com) |
|--------|--------------------------|--------------------------------------|
| **Animation engine** | Custom scroll-linked `data-anim-keyframe` with 100+ instances per page | None -- zero scroll animations |
| **Content reveal** | Progressive reveal as user scrolls (opacity 0 -> 1, transforms) | All content visible immediately on load |
| **Page weight** | 3,000-6,400 lines per page | 400-1,500 lines per page (3-4x lighter) |
| **JavaScript animation** | Heavy -- IntersectionObserver, scroll position tracking, RAF loops | Minimal -- only SVG `<animate>` for nav micro-interactions |
| **Navigation** | Simple global nav (apple.com bar) | Dual-tier: global nav + sticky local nav with section tabs |
| **Grid system** | `data-component-list` driven responsive layouts | Simple `large-span-*` / `column large-*` 12-column grid |
| **Typography system** | 160+ granular classes (`typography-feature-card-headline`, etc.) | 8 classes (headline, intro, card-headline, eyebrow variants, manifesto) |
| **Theme approach** | Dark = Pro product, section-level theme switching | Default light, selective `theme-dark` on individual tiles/heroes |
| **Video** | 61 video elements with scroll-synced playback | Simple thumbnail + play button, or `<video>` elements |
| **Card component** | Multiple types (feature-card, info-card, compare-card) | Single `tile` component with modifier classes |
| **Modal system** | Full content hierarchies with scroll groups and themes | Simple overlay with close button |
| **Image strategy** | `<picture>` with multiple breakpoints, WebP, 1x/2x | Simpler `<picture>` with WebP source + PNG fallback, 2x only |
| **Color system** | `--r-*` custom properties, extensive color token system | `--color-fill-blue`, `--s-primary` -- very few custom properties |

#### Shared Patterns

- Both use `globalnav` for the top-level Apple navigation bar (identical markup)
- Both serve 2x images for retina displays
- Both use `role` and `aria-*` attributes extensively for accessibility
- Both use `nowrap` spans to prevent awkward line breaks
- Both use WebP with PNG fallback via `<picture>` + `<source>`
- Both use `localnav` sticky navigation (product pages call it `chapternav` but same concept)

### 7.7 Developer Key Numbers

#### File Metrics

| Metric | Value |
|--------|-------|
| Total HTML lines (7 pages) | 8,619 |
| Average lines per page | 1,231 |
| Smallest page | developer-wwdc25.html (393 lines) |
| Largest page | developer-visionos.html (1,477 lines) |
| Ratio vs product pages | ~3x smaller on average |

#### Animation Counts

| Pattern | Total across 7 pages |
|---------|---------------------|
| `data-anim-keyframe` | 0 |
| `data-anim` attributes | 0 |
| `opacity: 0` | 0 |
| `transform:` | 0 |
| `@keyframes` | 0 |
| `transition` | 7 (1 per page, nav only) |
| `animation` | 1 (visionOS page) |
| SVG `<animate>` | ~28 (nav hamburger + chevrons) |

#### Component Counts

| Component | Instances |
|-----------|-----------|
| Tiles (`tile tile-rounded`) | 83 |
| Gallery cards (`sc-gallery__card`) | 32 |
| Modal openers | 25 |
| Tile copy sections | 28 |
| Card headlines (`typography-card-headline`) | 51 |
| Video cards (`vc-card`) | 6 |
| Theme image pairs (light/dark) | 12 |
| SF Symbol instances | 9 |
| Promo managed units | 9 |
| Thumbnail video previews | 9 |
| Event detail components | 20 |

#### Grid Breakpoint System

| Breakpoint prefix | Target | Most common span |
|-------------------|--------|-------------------|
| `large-span-*` | Desktop | 4 (3-col), 6 (2-col), 12 (full) |
| `medium-span-*` | Tablet | 6 (2-col), 12 (full) |
| `small-span-*` | Mobile | 12 (full-width, always) |

#### Spacing Utilities

| Class | Count | Purpose |
|-------|-------|---------|
| `margin-top-small` | 26 | Small top margin |
| `padding-top-small` | 19 | Small top padding |
| `margin-top` | 16 | Standard top margin |
| `padding-bottom-small` | 11 | Small bottom padding |
| `no-padding-top` | 8 | Remove top padding |
| `margin-bottom-xs` | 7 | Extra-small bottom margin |
| `margin-top-xs` | 5 | Extra-small top margin |

#### CSS Custom Properties (Navigation)

| Property | Value | Purpose |
|----------|-------|---------|
| `--r-globalnav-flyout-rate` | 240ms | Flyout animation speed |
| `--r-globalnav-flyout-height` | auto / 388px | Flyout container height |
| `--r-globalnav-text-zoom-scale` | 1 | Text scaling factor |
| `--r-localnav-menu-tray-natural-height` | 55-90px | Local nav tray height |
| `--r-localnav-text-zoom-factor` | 0.94 | WWDC25 text zoom |

---

## 8. Apple Services, Card, Shop, Accessibility & Environment Pages

### 8.1 Sources

| # | File | Size (KB) | Lines | Page Type |
|---|------|-----------|-------|-----------|
| 21 | services.html | 212 KB | 1,172 | Services / Subscriptions |
| 22 | apple-card.html | 254 KB | 1,270 | Financial Product |
| 23 | shop.html | 429 KB | 1,502 | E-Commerce / Store |
| 24 | accessibility.html | 305 KB | 1,691 | Values / Inclusive Design |
| 25 | environment.html | 715 KB | 3,476 | Values / Data Storytelling |

### 8.2 Animation Patterns

#### Per-Page Animation Usage

| File | `data-anim` | `opacity: 0` | `data-staggered` | `transform` | `transition` |
|------|------------|-------------|-----------------|------------|-------------|
| services.html | 7 | 0 | 0 | 12 | 7 |
| apple-card.html | 47 | 0 | 0 | 26 | 9 |
| shop.html | 0 | 0 | 0 | 14 | 30 |
| accessibility.html | 17 | 0 | 0 | 6 | 5 |
| environment.html | 9 | 22 | 0 | 21 | 6 |

#### Apple Card -- Heaviest Animation in This Batch

Apple Card uses the most `data-anim` attributes (47) of these five pages. It relies heavily on:

- **TriggerAnimation** (11 instances) -- class-based triggers that fire when elements scroll into view
- **data-anim-keyframes** with scroll-linked JSON -- same engine as product pages but used sparingly for hero parallax and interest wheel animations
- **data-anim-classname** with `fadein` class and `disabledWhen: "reduced-motion, text-zoom"` -- respects user preferences
- **Flip tiles** (14 open + 14 close buttons) -- card-flip interaction pattern unique to Apple Card, toggling front/back content
- **VideoViewportSource** (3 instances) -- viewport-triggered video playback
- **Parallax** component -- hero section depth effect
- **ScrollGradient** -- gradient reveal on scroll

#### Environment -- Lottie-Heavy Data Storytelling

- **17 LottieAnimation** components -- the highest Lottie count of any page analyzed
- Lottie icons represent lifecycle stages: design, make, product-use, recovery, shipping
- Additional Lottie for progress indicators: water, tree icons
- **22 `opacity: 0`** declarations -- elements hidden until scroll-reveal
- **Scroll groups** named by section: "Section - Hero", "Section - Plan", "Section - Progress", "Section - People", "Section - You"

#### Accessibility -- Moderate Animation with Inclusive Patterns

- **HeaderReveal** (3 instances) -- section headers that reveal on scroll
- **AnimationQueueItem + FeaturesTile + Modal** (2 instances) -- queued animation sequences
- **ScrollGallery** (3 instances, including DeafPresident variant) -- horizontal scroll galleries
- **Lottie** (2 instances) -- logo animation, accessibility icon
- **data-anim-load** attributes (8) -- load-triggered animations (not scroll-dependent)
- **OverviewHero + NavTheme + FocusManager** -- hero with theme-aware navigation

#### Services -- Gallery-Centric

- **DynamicGallery** (7 instances) -- dominant pattern, one per service section
- **InlineVideo** (4 instances) -- video content for TV+, Music, etc.
- No scroll-linked keyframe animations -- relies on gallery interaction instead

#### Shop -- Zero Custom Animation

- **No `data-anim`** attributes whatsoever -- the only non-developer page with zero
- **30 `transition`** declarations -- highest in this batch, all CSS transitions (hover states, card interactions)
- Relies entirely on CSS transitions rather than scroll-linked JavaScript animation
- Uses the `rf-` (retail framework) component system instead of the product page animation engine

### 8.3 Layout Patterns

#### Services -- Section-Per-Service Layout

Each Apple service gets its own full-width section:
- `section section-hero theme-dark` -- dark hero
- `section section-apple-music`
- `section section-apple-tv-plus remove-transition-delay`
- `section section-apple-fitness`
- `section section-apple-podcasts`
- `section section-apple-books`
- `section section-apple-news-plus`
- `section section-apple-one updated-apple-one-router`
- `section section-apple-one-banner theme-dark`

Pattern: Service sections use `section-content` containers (10 instances) with `DynamicGallery` components containing `dynamic-gallery-item-container` elements, some with `variable-width` and `manual-start` modifiers.

Theme alternation: 7 `theme-dark` sections, creating dark-light-dark rhythm.

#### Apple Card -- Tile Grid Layout

- `section section-hero` -- no theme class (neutral/white)
- `section section-tiles-grid` -- main content area with flip tiles
- `section section-simplicity` -- single feature section
- `section section-routers` / `section section-router` -- navigation sections
- Grid: `large-5`, `large-10`, `medium-5`, `small-12` -- asymmetric layouts (5/7 splits)
- No `theme-dark` or `theme-light` classes -- Apple Card uses a neutral white aesthetic throughout

#### Shop -- Retail Framework Layout (Unique System)

Shop uses an entirely different component system from all other Apple pages:

**`rf-` (Retail Framework) Components:**
| Component | Count | Purpose |
|-----------|-------|---------|
| `rf-cards-scroller-itemview` | 80 | Individual scrollable card items |
| `rf-recommcard-content` | 25 | Recommendation cards (33% width) |
| `rf-ccard-content` | 44 | Content cards (40% or 50% width) |
| `rf-productnav-card` | 11 | Product navigation cards |
| `rf-cards-scroller` | 9 | Horizontal card scrollers |
| `rf-ccard-img-full` | 38 | Full-bleed card images |

**`rs-` (Retail Store) Components:**
| Component | Count | Purpose |
|-----------|-------|---------|
| `rs-cardsshelf` | 9 | Card shelf containers |
| `rs-cardsshelf-mzone` | 4 | Marketing zone shelves |
| `rs-quicklinks` | 1 | Quick navigation links |
| `rs-quicklinks-item` | 5 | Individual quick link items |
| `rs-shop-neareststore` | 1 | Store locator component |
| `rs-sticky-chat` | 1 | Persistent chat support |

Card size variants: `rf-recommcard-33` (33% width), `rf-ccard-40` (40%), `rf-ccard-50` (50%).

#### Accessibility -- Responsive Content Sections

- `section-content-responsive` (7 instances) -- responsive content containers (unique to values pages)
- `section-header` (4 instances) with `section-header-headline` subcomponents
- Feature gallery sections with `features-gallery scroll-gallery with-paddlenav paddlenav-bottom-outside responsive`
- Stories gallery: `stories-gallery scroll-gallery with-paddlenav paddlenav-bottom-outside responsive`
- Resources gallery: `resources-gallery values-gallery scroll-gallery`
- Theme alternation: 15 `theme-dark` + 4 `theme-light` -- highest dark/light switching of any page

#### Environment -- Plan + Progress Data Layout

- `section-content-responsive` (12 instances) -- even more responsive containers than accessibility
- Unique sections: `section-plan`, `section-progress`, `section-progress-reports`, `section-products`, `section-people`, `section-you`
- **Plan items** with structured data: `plan-subhead` (10), `plan-item-description` (5 categories: design, make, product-use, recovery, shipping), `plan-item-progress`, `plan-item-approach`
- **Progress reports**: `progress-reports-item` (17 items), `progress-reports-title` (17)
- **Tile overlays**: 3 instances with `tile-overlay-toggle` for expand/collapse
- **Drawer components**: 2 expandable drawer sections
- **Product reports gallery** with archive gallery variant
- Custom theme: `theme-green` (1 instance) -- unique to environment page

### 8.4 Typography

#### Page-Specific Typography Classes

**Services** (7 unique classes):
- `typography-heading-headline` (7) / `typography-heading-subheadline` (8) -- standard heading hierarchy
- `typography-inline-video-caption` (9) -- video caption styling
- `typography-hero-headline`, `typography-hero-paragraph` -- hero text
- `typography-apple-one-banner` -- Apple One promotional text

**Apple Card** (20 unique classes -- most typography variety):
- `typography-tile-backface-content` (33) -- dominant class, flip-tile back content
- `typography-tile-backface-link` (4) -- back-of-tile links
- `typography-router-overview-headline/eyebrow/cta` (3 each) -- router navigation text
- `typography-tile-cash-headline/intro` -- Daily Cash display
- `typography-tile-physical-card` -- titanium card description
- `typography-tile-interest`, `typography-tile-fees`, `typography-tile-pay-over-time-headline` -- financial terms
- `typography-tile-exclusive-perks`, `typography-tile-partnerships`, `typography-tile-merchants` -- benefits
- `typography-grid-intro` (2) -- grid section introductions

**Shop** (3 classes only -- minimal typography system):
- `typography-body-tight` (13) -- compact body text
- `typography-body-reduced-tight` (13) -- even more compact body text
- `typography-caption` (1) -- captions

**Accessibility** (11 unique classes):
- `typography-eyebrow-elevated` (18) / `typography-features-eyebrow` (9) -- eyebrow text
- `typography-resources-copy` (18) -- resource section copy
- `typography-stories-headline` (7) -- story headlines
- `typography-section-header-cta` (8) -- section call-to-action links
- `typography-headline-reduced` (6) / `typography-headline-super` (1) -- heading scale
- `typography-secondary-section-headline` (3) -- sub-section headings
- `typography-intro` (6) / `typography-body` (6) -- body text

**Environment** (15 unique classes -- richest hierarchy):
- `typography-eyebrow-elevated` (15) -- shared with accessibility
- `typography-tout` (10) -- promotional callout text
- `typography-products-eyebrow/headline` (10/7) -- product section text
- `typography-plan-copy` (10) / `typography-plan-description` (5) -- plan data text
- `typography-headline-tight` (8) / `typography-headline-tight-alt` (4) / `typography-headline-elevated-tight` (5)
- `typography-products-overlay-copy` (3) -- tile overlay text
- `typography-modal-copy` (3) / `typography-modal-callout` (3) -- modal content
- `typography-label` (3) -- small label text

### 8.5 Unique Components

#### Service Tiles (services.html)
- **DynamicGallery** -- horizontal scroll gallery per service (Music, TV+, Fitness+, etc.)
- `dynamic-gallery-item-container` with `variable-width` and `manual-start` modifiers
- Each service section is a self-contained unit with heading + gallery + CTA
- Subscription pricing: 6 "subscription" mentions, 5 "free trial", 4 "/mo" pricing displays

#### Apple Card Visuals (apple-card.html)
- **Flip Tiles** -- 14 interactive cards that flip to reveal backface content (unique to Apple Card)
  - `flip-tile-button open-tile` / `close-tile` -- toggle controls
  - `typography-tile-backface-content backface-copy/headline` -- back content
- **Interest Wheel** -- scroll-animated circular visualization for interest/APR
- **Daily Cash Display** -- `tile-cash-headline`, `tile-cash-intro` typography
- **Physical Card** -- `tile-physical-card` typography for titanium card imagery
- **Financial Terms**: 45 "Daily Cash", 30 "interest", 13 "Goldman", 11 "titanium", 9 "APR" mentions
- **Router Overview** -- section navigation with eyebrow/headline/CTA pattern

#### Store Components (shop.html)
- **Card Scroller System** -- `rf-cards-scroller` with 80 individual `itemview` elements
- **Recommendation Cards** (`rf-recommcard`) -- 25 product recommendation tiles with:
  - Color image swatch (`rf-recommcard-content-colorimage`, 69 instances)
  - Price display (`rf-recommcard-content-price`)
  - Swatch container (`rf-recommcard-content-swatchescontainer`, 16 instances)
  - Violator badges (`rf-recommcard-content-violator`, 9 -- "New", "Save" labels)
- **Content Cards** (`rf-ccard`) -- 44 marketing/content cards with full-bleed images
- **Product Navigation** -- 11 product cards in a dedicated shelf
- **Quick Links** -- 5 secondary-neutral buttons for common actions
- **Nearest Store** -- store locator with content container
- **Sticky Chat** -- persistent support chat widget
- Commerce terms: 452 "store", 155 "trade-in", 54 "buy", 22 "financing", 12 "delivery", 5 "pickup"

#### Accessibility Demos (accessibility.html)
- **Feature Tiles with Modal** -- `AnimationQueueItem FeaturesTile Modal` for queued feature reveals
- **Overview Features Gallery** -- 4 features with light/dark image pairs:
  - Personal Voice, Magnifier, Live Listen, Assistive (each with `-dark` variant)
- **Hearing Aid Feature** -- standalone gallery image
- **Deaf President Gallery** -- specialized `ScrollGallery DeafPresident` variant
- **Music Haptics** -- tile with `gallery-item-music-haptics` class
- **Jordyn Zimmerman** -- named story tile in gallery
- **OverviewFeaturesGallery** -- curated feature showcase component
- **PrefersColorSchemeToggle** -- responds to user's OS color scheme preference
- **SetupLinks + SetupFootnotes** -- setup flow navigation
- Feature mentions: 50 "hearing", 48 "vision", 47 "magnifier", 46 "assistive", 4 "Live Captions", 4 "cognitive", 1 "Switch Control"

#### Environmental Charts & Data (environment.html)
- **Lottie Data Visualizations** -- 17 LottieAnimation components for animated data:
  - `lottie-with-picture` (15) -- Lottie overlaid on static images
  - `lottie-icon-*` variants: design, make, product-use, recovery, shipping
  - `lottie-boxes`, `lottie-arrow` -- diagram animations
  - `overview-icon-progress-water`, `overview-icon-progress-tree` -- progress icons
- **Plan Gallery** -- `PlanGallery FocusManager` with paddle navigation
- **Progress Gallery** -- `ScrollGallery ProgressGallery` variant
- **Product Reports Gallery** -- `ProductReportsGallery` with archive
- **Story Gallery** -- `StoryGallery` component
- **Tile Overlays** -- 3 expandable product tiles (iPhone, Watch, Recovery, PackagingShipping, Bands)
  - `ProductsTile` with product-specific variants: `ProductsTileWatch`, `ProductsTileIphone`, `ProductsTileRecovery`, `ProductsTilePackagingShipping`, `ProductsTileBands`
- **Drawers** -- 2 expandable content drawers with `drawer-toggle`
- **Tablist** -- tab navigation component
- Environmental terms: 62 "recycl*", 32 "renewable", 12 "supply chain", 12 "greenhouse", 4 "solar", 4 "clean energy", 2 "carbon footprint", 1 "carbon neutral", 1 "zero waste"

### 8.6 Key Insights

#### What These Pages Teach That Product and Developer Pages Do Not

**Services = Marketing + Pricing Hybrid**
- Uses `DynamicGallery` instead of scroll-linked animations -- content is browseable, not cinematic
- Each service is a self-contained section with its own gallery, creating a "catalog" feel
- Subscription pricing is presented inline, not in a separate purchase flow
- Moderate animation (7 `data-anim`) -- between developer (0) and product pages (20-44)
- `theme-dark` dominant (7 sections) -- premium feel without heavy animation

**Apple Card = Financial Product with Flip-Card Interaction**
- Highest animation count in this batch (47 `data-anim`) -- approaches product page levels
- **Flip tiles are unique** -- no other Apple page uses this card-flip interaction pattern
- Financial products require more detail density -- 33 backface content blocks to explain terms
- Uses scroll-linked keyframes but sparingly (5 keyframe sets vs. 30+ on product pages)
- No theme classes at all -- neutral white creates trust/clarity for financial content

**Shop = Entirely Separate Component System**
- The only page using `rf-` (Retail Framework) and `rs-` (Retail Store) component prefixes
- **Zero custom animation** -- relies on CSS `transition` only (30 instances)
- E-commerce requires functional, fast-loading UI -- no cinematic scroll effects
- Card-based browsing: horizontal scrollers (`rf-cards-scroller`) replace vertical scroll sections
- Typography is minimal (3 classes) -- content speaks through product images and prices
- Commerce UI patterns: sticky chat, nearest store, quick links, card shelf system

**Accessibility = Inclusive Design Showcase**
- Highest dark/light alternation (19 theme switches) -- demonstrates both modes extensively
- `PrefersColorSchemeToggle` -- responds to OS preference (unique component)
- Light/dark image pairs for every feature -- most thorough theme support of any page
- `data-anim-load` (8 instances) -- prefers load-triggered over scroll-triggered animation, reducing motion dependency
- Feature galleries use `paddlenav-bottom-outside responsive` -- accessible paddle navigation
- Named story tiles (Jordyn Zimmerman, Deaf President) -- human-centered content structure

**Environment = Data Storytelling Through Lottie**
- **17 Lottie animations** -- highest of any page -- used for data visualization, not decoration
- Lottie replaces traditional charts/graphs: each lifecycle stage (design, make, use, recover, ship) gets an animated icon
- `theme-green` -- the only page with a custom theme color beyond dark/light
- Progress reports with 17 structured items -- structured data display pattern
- Tile overlays with product-specific variants show environmental impact per product category
- Plan gallery with approach/progress/description structure -- educational content hierarchy
- At 715 KB, the largest file analyzed -- data-heavy content requires more markup

#### The Animation Spectrum Across Page Types

| Page Type | Representative | `data-anim` | Animation Style |
|-----------|---------------|-------------|-----------------|
| Developer | developer-*.html | 0 | None -- static content |
| Shop | shop.html | 0 | CSS transitions only |
| Services | services.html | 7 | Gallery-based interaction |
| Environment | environment.html | 9 | Lottie data viz |
| Accessibility | accessibility.html | 17 | Load-triggered + galleries |
| Apple Card | apple-card.html | 47 | Scroll-linked + flip tiles |
| Product (light) | iphone.html | 13 | Scroll-linked |
| Product (heavy) | macbook-pro.html | 41 | Full scroll + staggered + opacity |

---

## 9. Grand Summary -- All 25 Pages

### 9.1 Universal Patterns (Appear on ALL Pages)

Every Apple page analyzed shares these foundational patterns:

1. **Global Navigation** -- `r-globalnav` with flyout menus, `--r-globalnav-flyout-rate: 240ms`
2. **Local Navigation** -- `r-localnav` with page-specific sub-navigation
3. **Footer** -- consistent footer with legal, privacy, sitemap links
4. **SVG `<animate>`** elements -- hamburger menu and chevron animations in nav
5. **`transition`** CSS property -- at minimum for navigation hover states
6. **Responsive images** -- `srcset` with multiple resolutions
7. **`reduced-motion` awareness** -- `disabledWhen` checks or `prefers-reduced-motion` media queries
8. **Section-based structure** -- content organized in `<section>` elements with descriptive classes
9. **Semantic HTML** -- proper heading hierarchy, landmark roles
10. **Lazy loading** -- `loading="lazy"` or `data-anim-lazy-image` for below-fold content

### 9.2 Page Type Classification

| Type | Pages | Animation Level | Layout Approach | Typography Classes |
|------|-------|----------------|-----------------|-------------------|
| **Product** | 13 pages (iPhone, Mac, iPad, Watch, AirPods, Vision Pro, Apple Intelligence) | Heavy (13-128 `opacity:0`, 18-44 `data-anim`, 0-114 `data-staggered`) | Vertical scroll sections, `section-hero` + feature sections, `data-anim-keyframe` scroll engine | 40+ unique per page: `typography-site-*`, `typography-modal-*`, `typography-feature-card-*` |
| **Developer** | 7 pages (home, Swift, Xcode, Design, ML, visionOS, WWDC25) | Zero (0 `data-anim`, 0 `opacity:0`) | Tile grid (`tile tile-rounded`), card galleries (`sc-gallery`), 12-col grid | `typography-card-headline`, `typography-tile-copy`, `typography-eyebrow-reduced` |
| **Services** | 1 page (Services/Apple One) | Light (7 `data-anim`) | Section-per-service, `DynamicGallery` | `typography-heading-*`, `typography-inline-video-caption` |
| **Financial** | 1 page (Apple Card) | Moderate-Heavy (47 `data-anim`) | Flip-tile grid, router overview sections | `typography-tile-backface-*`, `typography-router-overview-*` |
| **E-Commerce** | 1 page (Shop) | None (0 `data-anim`, CSS transitions only) | `rf-`/`rs-` retail framework, card scrollers, product shelves | `typography-body-tight`, `typography-body-reduced-tight` |
| **Values** | 2 pages (Accessibility, Environment) | Moderate (9-17 `data-anim`) | `section-content-responsive`, scroll galleries, feature tiles | `typography-eyebrow-elevated`, `typography-features-*`, `typography-plan-*` |

### 9.3 The Apple Animation Spectrum

```
Zero Animation          Light              Moderate            Heavy
|                       |                  |                   |
Developer (0)     Services (7)     Accessibility (17)    Apple Card (47)
Shop (0)          Environment (9)  Apple Intelligence (2) MacBook Pro (41)
                                   iPhone (13)            MacBook Neo (44)
                                                          MacBook Air (44)
                                                          AirPods Pro (18)
                                                          iMac (28)
                                                          iPad Pro (26)
                                                          Watch Ultra (19)
                                                          Watch S11 (23)
                                                          Vision Pro (23)
                                                          iPad Air (21)
                                                          iPhone 16 Pro (13)
```

#### When to Use Which Level

- **Zero**: Reference/documentation content (developer), transactional pages (shop) -- users want information, not spectacle
- **Light (1-10)**: Service catalogs, data-heavy storytelling -- animation supports content without dominating
- **Moderate (11-25)**: Product pages with moderate feature sets, values/mission pages -- animation enhances but content leads
- **Heavy (25-50)**: Flagship product launches, financial products with complex features -- animation IS the storytelling medium

### 9.4 Master Numbers Tables

#### All Spacing Values (ps-spacing-* system, from product + values pages)

| Class | Count | Pixel Value |
|-------|-------|-------------|
| `ps-spacing-large-120` | 11 | 120px (desktop) |
| `ps-spacing-medium-96` | 10 | 96px (tablet) |
| `ps-spacing-small-72` | 10 | 72px (mobile) |
| `ps-spacing-small-8` | 8 | 8px (mobile tight) |
| `ps-spacing-large-10` | 8 | 10px (desktop tight) |
| `ps-spacing-medium-72` | 7 | 72px (tablet) |
| `ps-spacing-large-80` | 7 | 80px (desktop) |
| `ps-spacing-small-64` | 6 | 64px (mobile) |
| `ps-spacing-small-40` | 4 | 40px (mobile) |
| `ps-spacing-large-0` | 4 | 0px (desktop flush) |
| `ps-spacing-medium-92` | 2 | 92px (tablet) |
| `ps-spacing-large-112` | 2 | 112px (desktop) |
| `ps-spacing-medium-120` | 1 | 120px (tablet) |
| `ps-spacing-medium-100` | 1 | 100px (tablet) |
| `ps-spacing-large-96` | 1 | 96px (desktop) |
| `ps-spacing-large-48` | 1 | 48px (desktop) |
| `ps-spacing-large-32` | 1 | 32px (desktop) |
| `ps-spacing-medium-24` | 1 | 24px (tablet) |

Common spacing scale: 0, 8, 10, 24, 32, 40, 48, 64, 72, 80, 92, 96, 100, 112, 120

#### All Typography Classes (Top 40 across 25 pages)

| Class | Total Count | Found On |
|-------|-------------|----------|
| `typography-inner-container-modal-copy` | 224 | Product pages |
| `typography-utility-modal-block-body` | 187 | Product pages |
| `typography-caption-tile` | 183 | Product pages |
| `typography-modal-header-headline` | 113 | Product pages |
| `typography-site-body` | 98 | Product pages |
| `typography-modal-header-topic-label` | 95 | Product pages |
| `typography-feature-card-label` | 88 | Product pages |
| `typography-feature-card-headline` | 88 | Product pages |
| `typography-icon-card-body-copy` | 68 | Product pages |
| `typography-feature-card-body` | 60 | Product pages |
| `typography-section-header-headline` | 59 | Product pages |
| `typography-eyebrow-elevated` | 55 | Values + product pages |
| `typography-index-item-base` | 54 | Product pages |
| `typography-drawer-caption` | 51 | Product pages |
| `typography-card-headline` | 51 | Developer pages |
| `typography-icon-card-headline` | 50 | Product pages |
| `typography-callout-base` | 46 | Product pages |
| `typography-headline` | 44 | Product + developer pages |
| `typography-caption` | 42 | All page types |
| `typography-section-header-link` | 37 | Product pages |
| `typography-media-card-gallery-headline` | 35 | Product pages |
| `typography-all-access-pass-pv-item-*` | 35 | Product pages (Vision Pro) |
| `typography-intro` | 34 | Product + values pages |
| `typography-tile-backface-content` | 33 | Apple Card only |
| `typography-eyebrow-reduced` | 33 | Developer pages |
| `typography-product-tile-*` | 22-29 | Product pages |
| `typography-site-headline-reduced` | 28 | Product pages |
| `typography-body-tight` | 19 | Shop + environment |
| `typography-resources-copy` | 18 | Accessibility only |
| `typography-tout` | 10 | Environment only |
| `typography-plan-copy` | 10 | Environment only |

#### All Animation Component Types (Top 30 across 25 pages)

| Component (`data-component-list`) | Count | Page Types |
|-----------------------------------|-------|------------|
| `Card WillChange` | 138 | Product |
| `StaggeredFadeIn` | 135 | Product |
| `Modal` | 114 | Product + developer |
| `InlineMedia` | 38 | Product |
| `InlineMediaPlugins` | 36 | Product |
| `WordAnim` | 29 | Product |
| `IconCardModal` | 25 | Product |
| `InlineMediaDefault` | 19 | Product |
| `ScrollGallery` | 17 | Product + values + environment |
| `LottieAnimation` | 17 | Environment (all 17) |
| `AllAccessPassL2` | 14 | Product (Vision Pro) |
| `ScrollGallery WillChange` | 13 | Product |
| `CaptionTileGallery StaggeredFadeIn` | 12 | Product |
| `TriggerAnimation` | 11 | Apple Card (all 11) |
| `ProductViewerMediaDefault` | 10 | Product |
| `L2Modal` | 10 | Product |
| `CardGallery` | 9 | Product |
| `VideoGallery` | 8 | Product |
| `InlineVideo` | 8 | Product + services |
| `Index` | 8 | Product |
| `DynamicGallery` | 7 | Services (all 7) |
| `Portal` | 7 | Product |
| `TextIconControl` | 6 | Product |
| `SlideGallery` | 6 | Product |
| `MediaCardGallery` | 6 | Product |
| `GraphGalleryInitialize` | 5 | Product |
| `FadeGallery` | 5 | Product |
| `Welcome` | 5 | Product |
| `HeaderReveal` | 3 | Accessibility |
| `DrawerComponent` | 2 | Environment |

#### Theme Usage Across All 25 Pages

| Theme | Product Pages | Developer | Services | Apple Card | Shop | Accessibility | Environment |
|-------|--------------|-----------|----------|------------|------|---------------|-------------|
| `theme-dark` | Dominant | Present | 7 | 0 | 0 | 15 | 2 |
| `theme-light` | Present | Present | 0 | 0 | 0 | 4 | 0 |
| `theme-green` | 0 | 0 | 0 | 0 | 0 | 0 | 1 |

#### Navigation Timing Constants

| Property | Value | Source |
|----------|-------|--------|
| `--r-globalnav-flyout-rate` | 240ms | All pages |
| `--r-globalnav-flyout-height` | auto / 388px | All pages |
| `--r-localnav-menu-tray-natural-height` | 55-90px | Product + developer |
| `--r-localnav-text-zoom-factor` | 0.94 | WWDC25 |
