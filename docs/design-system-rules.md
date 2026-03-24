# Design System & Platform Rules

Comprehensive rules for Apple HIG design, frameworks, modern CSS, and accessibility. Follow these when building UI.

---

## 1. Apple HIG Typography

### System Font Stack

```css
/* Web equivalent of SF Pro */
font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text",
  "Helvetica Neue", Helvetica, Arial, sans-serif;

/* Monospace (SF Mono equivalent) */
font-family: "SF Mono", SFMono-Regular, ui-monospace, Menlo, Monaco, Consolas, monospace;

/* Serif (New York equivalent) */
font-family: "New York", "Iowan Old Style", "Apple Garamond", Baskerville,
  "Times New Roman", serif;
```

### Apple Text Styles (iOS)

| Style | Size | Weight | Leading | Tracking |
|-------|------|--------|---------|----------|
| Large Title | 34pt | Regular | 41pt | 0.37 |
| Title 1 | 28pt | Regular | 34pt | 0.36 |
| Title 2 | 22pt | Regular | 28pt | 0.35 |
| Title 3 | 20pt | Regular | 25pt | 0.38 |
| Headline | 17pt | Semibold | 22pt | -0.41 |
| Body | 17pt | Regular | 22pt | -0.41 |
| Callout | 16pt | Regular | 21pt | -0.32 |
| Subheadline | 15pt | Regular | 20pt | -0.24 |
| Footnote | 13pt | Regular | 18pt | -0.08 |
| Caption 1 | 12pt | Regular | 16pt | 0 |
| Caption 2 | 11pt | Regular | 13pt | 0.07 |

### Web Mapping (rem-based)

```css
:root {
  --text-large-title: 2.125rem;    /* 34px */
  --text-title-1: 1.75rem;         /* 28px */
  --text-title-2: 1.375rem;        /* 22px */
  --text-title-3: 1.25rem;         /* 20px */
  --text-headline: 1.0625rem;      /* 17px, semibold */
  --text-body: 1.0625rem;          /* 17px */
  --text-callout: 1rem;            /* 16px */
  --text-subheadline: 0.9375rem;   /* 15px */
  --text-footnote: 0.8125rem;      /* 13px */
  --text-caption-1: 0.75rem;       /* 12px */
  --text-caption-2: 0.6875rem;     /* 11px */
}
```

### Rules

- **ALWAYS** use `-apple-system, BlinkMacSystemFont` as first font-family values on web
- **NEVER** use SF Pro directly on web (licensing — Apple devices only)
- **PREFER** semibold (600) over bold (700) for emphasis — Apple convention
- **PREFER** negative letter-spacing for body text sizes (tighter tracking)
- **PREFER** positive letter-spacing for small text (caption, footnote — aids readability)
- **USE** font-weight 400 (regular) for body, 600 (semibold) for headlines, 700 (bold) sparingly
- **MINIMUM** font size: 11pt (Caption 2) — never go smaller
- **LINE HEIGHT** ratio: ~1.3× for large text, ~1.4× for body, ~1.2× for small text
- **HIERARCHY** through weight and size, not color alone — supports accessibility

---

## 2. Apple HIG Layout & Spacing

### Spacing Scale (4pt/8pt grid)

```css
:root {
  /* Apple uses a 4pt base with 8pt as the primary unit */
  --space-1: 0.25rem;   /* 4px — minimum spacing */
  --space-2: 0.5rem;    /* 8px — tight spacing */
  --space-3: 0.75rem;   /* 12px */
  --space-4: 1rem;      /* 16px — standard padding */
  --space-5: 1.25rem;   /* 20px */
  --space-6: 1.5rem;    /* 24px — section padding */
  --space-8: 2rem;      /* 32px */
  --space-10: 2.5rem;   /* 40px */
  --space-12: 3rem;     /* 48px — large section gaps */
  --space-16: 4rem;     /* 64px */
  --space-20: 5rem;     /* 80px — section spacing */
  --space-24: 6rem;     /* 96px */
}
```

### Content Width Constraints

```css
:root {
  --content-max: 980px;      /* Apple's standard content width */
  --content-wide: 1120px;    /* Extended for product pages */
  --content-narrow: 692px;   /* Text-heavy content */
  --content-hero: 1440px;    /* Full-width hero sections */
}

.content {
  max-width: var(--content-max);
  margin-inline: auto;
  padding-inline: var(--space-6);
}
```

### Safe Areas (Mobile)

```css
/* iOS safe areas */
.container {
  padding-top: env(safe-area-inset-top);
  padding-bottom: env(safe-area-inset-bottom);
  padding-left: env(safe-area-inset-left);
  padding-right: env(safe-area-inset-right);
}
```

### Apple Corner Radius Scale

```css
:root {
  --radius-sm: 6px;     /* Small elements (chips, badges) */
  --radius-md: 10px;    /* Buttons, inputs */
  --radius-lg: 14px;    /* Cards */
  --radius-xl: 20px;    /* Large cards, modals */
  --radius-2xl: 28px;   /* Hero elements */
  --radius-full: 9999px; /* Pills */
}

/* Concentric radius rule: inner radius = outer radius - padding */
.outer { border-radius: 20px; padding: 8px; }
.inner { border-radius: 12px; } /* 20 - 8 = 12 */
```

### Rules

- **ALWAYS** use 8pt grid increments for spacing (4pt for fine adjustments)
- **ALWAYS** apply concentric corner radii (inner = outer - padding)
- **ALWAYS** respect safe areas on iOS — use `env(safe-area-inset-*)`
- **PREFER** `margin-inline: auto` with `max-width` for content centering
- **PREFER** 980px max-width for standard content (Apple's convention)
- **USE** logical properties (`inline`, `block`) instead of physical (`left`, `right`)
- **MINIMUM** touch target: 44×44pt (Apple HIG requirement)
- **MINIMUM** spacing between interactive elements: 8pt
- **SECTION SPACING** on landing pages: 80-120px between major sections

---

## 3. Apple HIG Color System

### Semantic System Colors

```css
:root {
  /* Primary text/backgrounds */
  --color-label: #1d1d1f;
  --color-secondary-label: #86868b;
  --color-tertiary-label: #b0b0b3;
  --color-background: #fbfbfd;
  --color-secondary-bg: #f5f5f7;
  --color-tertiary-bg: #e8e8ed;

  /* System colors (light mode) */
  --color-blue: #007AFF;
  --color-green: #34C759;
  --color-indigo: #5856D6;
  --color-orange: #FF9500;
  --color-pink: #FF2D55;
  --color-purple: #AF52DE;
  --color-red: #FF3B30;
  --color-teal: #5AC8FA;
  --color-yellow: #FFCC00;

  /* Separators & fills */
  --color-separator: rgba(60, 60, 67, 0.29);
  --color-fill: rgba(120, 120, 128, 0.2);
}

/* Dark mode */
@media (prefers-color-scheme: dark) {
  :root {
    --color-label: #f5f5f7;
    --color-secondary-label: #a1a1a6;
    --color-tertiary-label: #6e6e73;
    --color-background: #1d1d1f;
    --color-secondary-bg: #2c2c2e;
    --color-tertiary-bg: #3a3a3c;

    --color-blue: #0A84FF;
    --color-green: #30D158;
    --color-red: #FF453A;
    --color-separator: rgba(84, 84, 88, 0.65);
  }
}
```

### Materials & Vibrancy (CSS approximation)

```css
/* Ultra-thin material */
.material-ultra-thin {
  background: rgba(255, 255, 255, 0.3);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
}

/* Thick material */
.material-thick {
  background: rgba(255, 255, 255, 0.72);
  backdrop-filter: blur(30px) saturate(180%);
  -webkit-backdrop-filter: blur(30px) saturate(180%);
}

/* Regular material (most common) */
.material-regular {
  background: rgba(255, 255, 255, 0.5);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
}
```

### Category-Specific Accent Colors

```css
/* Don't always use #007AFF — match the product category */
--accent-productivity: #007AFF;   /* Blue — default, tools */
--accent-creativity: #AF52DE;      /* Purple — creative apps */
--accent-health: #34C759;          /* Green — health, fitness */
--accent-entertainment: #FF2D55;   /* Pink — media, music */
--accent-finance: #30D158;         /* Green — money, banking */
--accent-social: #5856D6;          /* Indigo — communication */
--accent-education: #FF9500;       /* Orange — learning */
--accent-developer: #5AC8FA;       /* Teal — dev tools */
```

### Rules

- **ALWAYS** use semantic color names, not raw hex values
- **ALWAYS** provide dark mode variants for all custom colors
- **ALWAYS** ensure 4.5:1 contrast ratio minimum (7:1 preferred for body text)
- **NEVER** use pure black (#000) for text — use #1d1d1f (Apple convention)
- **NEVER** use pure white (#fff) for backgrounds — use #fbfbfd
- **PREFER** rgba separators over solid borders (semi-transparent adapts to backgrounds)
- **PREFER** `backdrop-filter: blur()` for glass effects — always include `-webkit-` prefix
- **USE** category-specific accent colors, not always default blue
- **USE** semantic colors: label, secondary-label, separator, fill, background
- **SOFTEN** white images in dark mode (slightly reduce brightness/opacity)

---

## 4. SwiftUI Patterns

### Layout Fundamentals

```swift
// Standard stack layout with spacing
VStack(alignment: .leading, spacing: 16) {
    Text("Title")
        .font(.title)
        .fontWeight(.semibold)
    Text("Subtitle")
        .font(.body)
        .foregroundStyle(.secondary)
}
.padding()

// Grid layout
LazyVGrid(columns: [
    GridItem(.flexible()),
    GridItem(.flexible()),
    GridItem(.flexible())
], spacing: 16) {
    ForEach(items) { item in
        CardView(item: item)
    }
}

// Navigation
NavigationStack {
    List(items) { item in
        NavigationLink(item.title, value: item)
    }
    .navigationTitle("Items")
    .navigationDestination(for: Item.self) { item in
        DetailView(item: item)
    }
}
```

### State Management

```swift
// Modern @Observable (iOS 17+)
@Observable
class ViewModel {
    var items: [Item] = []
    var isLoading = false

    func loadItems() async {
        isLoading = true
        items = await api.fetchItems()
        isLoading = false
    }
}

struct ContentView: View {
    @State private var viewModel = ViewModel()

    var body: some View {
        List(viewModel.items) { item in
            Text(item.title)
        }
        .task { await viewModel.loadItems() }
    }
}
```

### Rules

- **PREFER** `@Observable` over `@ObservableObject` (iOS 17+)
- **PREFER** `NavigationStack` over deprecated `NavigationView`
- **PREFER** `.task` over `.onAppear` for async work (automatic cancellation)
- **PREFER** `LazyVGrid`/`LazyHGrid` over custom layouts for grids
- **ALWAYS** use `.foregroundStyle(.secondary)` not `.foregroundColor(.gray)`
- **ALWAYS** use system text styles (`.font(.body)`) not hard-coded sizes
- **USE** `@State` for view-local state, `@Binding` for parent-child
- **USE** `@Environment` for system values (colorScheme, dismiss, etc.)
- **AVOID** `AnyView` — use `@ViewBuilder` or concrete types for type erasure
- **AVOID** heavy computation in `body` — move to view model

---

## 5. Tailwind CSS v4

### Theme Configuration (v4 — CSS-native)

```css
@import "tailwindcss";

@theme {
  /* Custom colors in oklch */
  --color-brand: oklch(0.65 0.25 265);
  --color-brand-light: oklch(0.85 0.10 265);
  --color-brand-dark: oklch(0.45 0.20 265);

  /* Custom fonts */
  --font-display: "SF Pro Display", -apple-system, sans-serif;
  --font-body: "SF Pro Text", -apple-system, sans-serif;
  --font-mono: "SF Mono", ui-monospace, monospace;

  /* Custom easing */
  --ease-apple: cubic-bezier(0.25, 0.1, 0.25, 1);
  --ease-spring: cubic-bezier(0.175, 0.885, 0.32, 1.275);

  /* Custom spacing */
  --spacing-section: 5rem;
  --spacing-content: 1.5rem;

  /* Custom breakpoints */
  --breakpoint-xs: 30rem;
}
```

### Key v4 Changes

```css
/* v4 uses CSS-native features */

/* Container queries (built-in, no plugin) */
<div class="@container">
  <div class="@lg:grid-cols-3 @md:grid-cols-2 grid-cols-1">

/* CSS nesting (built-in) */
.card {
  & .title { font-weight: 600; }
  &:hover { background: var(--color-brand-light); }
}

/* Dark mode */
@custom-variant dark (&:is(.dark *));  /* class-based */
/* OR automatic with prefers-color-scheme */

/* oklch colors everywhere */
--color-primary: oklch(0.65 0.25 265);
```

### Rules

- **ALWAYS** use `@theme` directive for custom tokens (v4), not `tailwind.config.js`
- **ALWAYS** use oklch for custom colors in v4 (Tailwind v4 default)
- **PREFER** `@container` queries over media queries for component-level responsiveness
- **PREFER** CSS nesting for component-scoped styles
- **USE** `@custom-variant` for custom dark mode or platform targeting
- **USE** `@apply` sparingly — prefer utility classes in markup
- **AVOID** `tailwind.config.js` in v4 — use CSS `@theme` instead
- **KNOW** v4 breakpoints: sm=40rem, md=48rem, lg=64rem, xl=80rem, 2xl=96rem

---

## 6. shadcn/ui

### Theming System

```css
/* shadcn/ui uses oklch CSS variables */
:root {
  --background: oklch(1 0 0);
  --foreground: oklch(0.145 0 0);
  --primary: oklch(0.205 0 0);
  --primary-foreground: oklch(0.985 0 0);
  --secondary: oklch(0.97 0 0);
  --muted: oklch(0.97 0 0);
  --muted-foreground: oklch(0.556 0 0);
  --accent: oklch(0.97 0 0);
  --destructive: oklch(0.577 0.245 27.325);
  --border: oklch(0.922 0 0);
  --ring: oklch(0.708 0 0);
  --radius: 0.625rem;
}

.dark {
  --background: oklch(0.145 0 0);
  --foreground: oklch(0.985 0 0);
  --primary: oklch(0.922 0 0);
  --primary-foreground: oklch(0.205 0 0);
  --border: oklch(1 0 0 / 10%);
}
```

### Component Usage

```tsx
// Button variants
<Button variant="default">Primary</Button>
<Button variant="secondary">Secondary</Button>
<Button variant="outline">Outline</Button>
<Button variant="ghost">Ghost</Button>
<Button variant="destructive">Delete</Button>

// Dialog
<Dialog>
  <DialogTrigger asChild>
    <Button>Open</Button>
  </DialogTrigger>
  <DialogContent>
    <DialogHeader>
      <DialogTitle>Title</DialogTitle>
      <DialogDescription>Description</DialogDescription>
    </DialogHeader>
    {/* content */}
    <DialogFooter>
      <Button>Save</Button>
    </DialogFooter>
  </DialogContent>
</Dialog>

// Form with validation
<Form {...form}>
  <FormField
    control={form.control}
    name="email"
    render={({ field }) => (
      <FormItem>
        <FormLabel>Email</FormLabel>
        <FormControl>
          <Input placeholder="email@example.com" {...field} />
        </FormControl>
        <FormMessage />
      </FormItem>
    )}
  />
</Form>
```

### Rules

- **ALWAYS** use oklch color space for theme variables (shadcn default)
- **ALWAYS** use semantic token names (--primary, --muted, --accent, not raw colors)
- **ALWAYS** provide both light and dark theme values
- **PREFER** `asChild` prop to compose with your own components
- **PREFER** the "new-york" style variant (closer to Apple HIG aesthetic)
- **USE** `cn()` utility for conditional class merging
- **USE** CSS variables for theming, not Tailwind config
- **INSTALL** components individually (`npx shadcn@latest add button`) — not monolithic
- **CUSTOMIZE** via the source files in `components/ui/` — they're yours to modify
- **DON'T** wrap shadcn components in unnecessary abstraction layers

---

## 7. NativeWind (v5)

### Setup

```css
/* global.css */
@import "tailwindcss/theme.css" layer(theme);
@import "tailwindcss/preflight.css" layer(base);
@import "tailwindcss/utilities.css";
@import "nativewind/theme";
```

```javascript
// metro.config.js
const { getDefaultConfig } = require("expo/metro-config");
const { withNativewind } = require("nativewind/metro");
module.exports = withNativewind(getDefaultConfig(__dirname));
```

### Usage

```tsx
import { View, Text, Pressable } from "react-native";

function Card({ title, onPress }) {
  return (
    <Pressable
      className="bg-white dark:bg-gray-900 rounded-xl p-4 shadow-sm
                 active:scale-[0.98] transition-transform"
      onPress={onPress}
    >
      <Text className="text-lg font-semibold text-gray-900 dark:text-white">
        {title}
      </Text>
    </Pressable>
  );
}
```

### Platform Variants

```tsx
// Built-in platform variants
<View className="ios:bg-blue-500 android:bg-green-500 web:bg-purple-500" />

// Custom platform theming
<Text className="native:font-semibold web:font-medium" />
```

### Rules

- **ALWAYS** import `nativewind/theme` in global CSS
- **ALWAYS** use `className` prop (NativeWind patches RN components)
- **PREFER** `Pressable` over `TouchableOpacity` (NativeWind v5 compatible)
- **PREFER** `dark:` variant for dark mode (auto-detects system preference)
- **USE** `ios:`, `android:`, `web:`, `native:` variants for platform-specific styles
- **USE** `active:scale-[0.98]` for press feedback (Apple HIG convention)
- **AVOID** inline `style` prop when using NativeWind — use `className`
- **AVOID** `gap` on older React Native versions — use padding/margin
- **KNOW** not all Tailwind utilities work in RN (no `::before`, `::after`, limited `grid`)

---

## 8. Modern CSS Features

### Container Queries

```css
/* Define a container */
.card-container {
  container-type: inline-size;
  container-name: card;
}

/* Respond to container size, not viewport */
@container card (min-width: 400px) {
  .card-body { display: grid; grid-template-columns: 1fr 1fr; }
}

@container card (min-width: 600px) {
  .card-body { grid-template-columns: 1fr 1fr 1fr; }
}

/* Tailwind v4 syntax */
<div class="@container">
  <div class="@md:flex @md:gap-4">...</div>
</div>
```

### CSS Nesting

```css
/* Native CSS nesting — no preprocessor needed */
.card {
  background: var(--surface);
  border-radius: var(--radius-lg);

  & .title {
    font-weight: 600;
    color: var(--color-label);
  }

  & .body {
    color: var(--color-secondary-label);
  }

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
  }

  &:has(.image) {
    padding-top: 0;
  }

  @media (prefers-color-scheme: dark) {
    background: var(--surface-dark);
  }
}
```

### :has() Selector

```css
/* Style parent based on child state */
.form-group:has(input:focus) {
  border-color: var(--color-blue);
}

.card:has(img) {
  padding: 0;
}

.nav:has(.dropdown.open) {
  backdrop-filter: blur(20px);
}

/* Select previous sibling */
h2:has(+ p) {
  margin-bottom: 0.5rem;
}
```

### Subgrid

```css
/* Parent grid */
.grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: auto 1fr auto;
  gap: 1.5rem;
}

/* Child inherits parent tracks — perfect alignment across cards */
.card {
  display: grid;
  grid-row: span 3;
  grid-template-rows: subgrid;
  /* Header, body, footer all align across cards */
}
```

### Rules

- **PREFER** container queries over media queries for component responsiveness
- **PREFER** CSS nesting over BEM or preprocessor nesting
- **USE** `:has()` for parent-aware styling (supported in all modern browsers)
- **USE** `subgrid` for aligned card grids (header/body/footer alignment)
- **USE** `container-name` for named containers in complex layouts
- **KNOW** container queries: Chrome 105+, Firefox 110+, Safari 16+ (wide support)
- **KNOW** `:has()`: Chrome 105+, Firefox 121+, Safari 15.4+ (wide support)
- **KNOW** CSS nesting: Chrome 120+, Firefox 117+, Safari 17.2+
- **KNOW** subgrid: Chrome 117+, Firefox 71+, Safari 16+ (wide support)

---

## 9. Accessibility (WCAG 2.2)

### Color Contrast

```
AA Standard (minimum):
  - Normal text (< 18pt): 4.5:1 contrast ratio
  - Large text (≥ 18pt or 14pt bold): 3:1 contrast ratio
  - UI components & graphics: 3:1 contrast ratio

AAA Standard (enhanced):
  - Normal text: 7:1 contrast ratio
  - Large text: 4.5:1 contrast ratio

Apple convention:
  - #1d1d1f on #fbfbfd = 15.4:1 ✅ (exceeds AAA)
  - #86868b on #fbfbfd = 4.68:1 ✅ (meets AA)
```

### Focus Management

```css
/* Visible focus indicator (WCAG 2.4.7 + 2.4.11) */
:focus-visible {
  outline: 2px solid var(--color-blue);
  outline-offset: 2px;
  border-radius: var(--radius-sm);
}

/* Remove default only when custom focus exists */
:focus:not(:focus-visible) {
  outline: none;
}

/* Focus indicator must have 3:1 contrast against adjacent colors */
/* Focus indicator area must be at least 2px thick perimeter */
```

### Target Size (WCAG 2.5.8)

```css
/* Minimum target size: 24×24px (AA) */
/* Recommended: 44×44px (Apple HIG) */
.interactive {
  min-width: 44px;
  min-height: 44px;
  /* If visually smaller, use padding to expand hit area */
  padding: 8px;
}

/* Spacing between targets: at least 8px */
.button-group {
  gap: 8px;
}
```

### ARIA Patterns

```html
<!-- Live region for dynamic content -->
<div aria-live="polite" aria-atomic="true">
  <!-- Screen reader announces changes here -->
</div>

<!-- Landmark roles -->
<header role="banner">
<nav role="navigation" aria-label="Main">
<main role="main">
<footer role="contentinfo">

<!-- Loading states -->
<button aria-busy="true" aria-disabled="true">
  <span aria-hidden="true">⏳</span>
  Loading...
</button>

<!-- Disclosure pattern -->
<button aria-expanded="false" aria-controls="panel-1">
  Show details
</button>
<div id="panel-1" hidden>Details content</div>

<!-- Tab pattern -->
<div role="tablist" aria-label="Settings">
  <button role="tab" aria-selected="true" aria-controls="tab-panel-1">General</button>
  <button role="tab" aria-selected="false" aria-controls="tab-panel-2">Privacy</button>
</div>
<div role="tabpanel" id="tab-panel-1">...</div>
```

### prefers-reduced-motion (WCAG 2.3.3)

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

### Rules

- **ALWAYS** test with screen reader (VoiceOver on Mac: Cmd+F5)
- **ALWAYS** ensure all interactive elements are keyboard accessible (Tab, Enter, Escape, Arrow keys)
- **ALWAYS** provide `:focus-visible` styles — never remove focus without replacement
- **ALWAYS** respect `prefers-reduced-motion` — animations are optional, content is not
- **ALWAYS** use semantic HTML first (`<button>`, `<nav>`, `<main>`) before ARIA
- **NEVER** use `aria-label` on non-interactive elements (use `aria-labelledby` instead)
- **NEVER** use `role="button"` on a `<div>` — use `<button>` element
- **PREFER** `aria-live="polite"` over `"assertive"` (less disruptive)
- **MINIMUM** 44×44px touch targets (Apple HIG) — 24×24px is WCAG minimum
- **MINIMUM** 4.5:1 contrast ratio for normal text, 3:1 for large text and UI elements
- **TEST** with keyboard-only navigation — every interaction must be reachable
- **TEST** with browser zoom at 200% — layout must not break
- **SKIP LINK** required: `<a href="#main" class="sr-only focus:not-sr-only">Skip to content</a>`

---

## Quick Reference: Apple HIG Design Tokens

```css
:root {
  /* Typography */
  font-family: -apple-system, BlinkMacSystemFont, sans-serif;
  --font-weight-regular: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;

  /* Colors */
  --text-primary: #1d1d1f;
  --text-secondary: #86868b;
  --bg-primary: #fbfbfd;
  --bg-secondary: #f5f5f7;
  --accent: #007AFF;

  /* Spacing (8pt grid) */
  --space-unit: 8px;

  /* Radius */
  --radius-default: 10px;

  /* Transitions */
  --ease-default: cubic-bezier(0.25, 0.1, 0.25, 1);
  --duration-fast: 200ms;
  --duration-normal: 350ms;
  --duration-slow: 500ms;

  /* Elevation */
  --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.06);
  --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.08);
  --shadow-lg: 0 8px 28px rgba(0, 0, 0, 0.12);

  /* Materials */
  --blur-standard: blur(20px) saturate(180%);

  /* Content widths */
  --content-width: 980px;

  /* Touch targets */
  --min-target: 44px;
}
```

## Universal Design Rules

1. **Semantic HTML first** — `<button>`, `<nav>`, `<main>`, `<article>` before ARIA
2. **8pt grid** — all spacing in multiples of 8px (4px for fine adjustments)
3. **44px touch targets** — minimum interactive element size
4. **4.5:1 contrast** — minimum for all text
5. **Dark mode** — always provide, using semantic color tokens
6. **Safe areas** — always respect on mobile
7. **Concentric radii** — inner = outer - padding
8. **System fonts first** — -apple-system before custom fonts
9. **Reduced motion** — always respect prefers-reduced-motion
10. **Progressive enhancement** — core content works without JS
