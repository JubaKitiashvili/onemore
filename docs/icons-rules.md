# Icon System Rules

NEVER use emojis, keyboard symbols, or Unicode characters as icons in UI. Always use proper SVG icons with consistent stroke weight, optical sizing, and color inheritance.

---

## The Rule

```
NEVER USE:                        ALWAYS USE:
  ❌  →  ← ↑ ↓ ↗                   ✅  SVG arrow icons
  ❌  ✓  ✗  ✕                      ✅  SVG check/close icons
  ❌  ⚡ 🔒 📊 🎨 ⚙️ 💡            ✅  SVG semantic icons
  ❌  •  ▸  ▾  ■  ●                ✅  SVG shapes or CSS
  ❌  &rarr; &check; &times;       ✅  SVG inline icons
  ❌  Font Awesome / icon fonts     ✅  Inline SVG (zero dependencies)
```

---

## Icon Component System

### Base Icon Wrapper

```css
/* All icons inherit text color and size */
.icon {
  width: 1em;
  height: 1em;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  vertical-align: -0.125em; /* optical baseline alignment */
}

.icon svg {
  width: 100%;
  height: 100%;
  fill: none;
  stroke: currentColor;
  stroke-width: 1.5;
  stroke-linecap: round;
  stroke-linejoin: round;
}

/* Size variants */
.icon-sm { width: 0.875em; height: 0.875em; }
.icon-lg { width: 1.25em; height: 1.25em; }
.icon-xl { width: 1.5em; height: 1.5em; }

/* Standalone icon (not inline with text) */
.icon-standalone {
  width: 24px;
  height: 24px;
  vertical-align: middle;
}

/* Match stroke weight to font weight */
.font-light .icon svg,
.icon-light svg     { stroke-width: 1.2; }

.font-normal .icon svg,
.icon-regular svg   { stroke-width: 1.5; }

.font-medium .icon svg,
.icon-medium svg    { stroke-width: 1.75; }

.font-semibold .icon svg,
.icon-semibold svg  { stroke-width: 2; }

.font-bold .icon svg,
.icon-bold svg      { stroke-width: 2.25; }
```

### Usage Pattern

```html
<!-- Inline with text -->
<a href="/settings">
  <span class="icon"><svg viewBox="0 0 24 24"><!-- path --></svg></span>
  Settings
</a>

<!-- Button with icon -->
<button>
  <span class="icon"><svg viewBox="0 0 24 24"><!-- path --></svg></span>
  Get Started
</button>

<!-- Icon-only button (requires aria-label) -->
<button aria-label="Close" class="icon-button">
  <span class="icon"><svg viewBox="0 0 24 24"><!-- path --></svg></span>
</button>

<!-- Feature card icon (larger, with color) -->
<div class="feature-icon" style="color: var(--accent);">
  <span class="icon-xl"><svg viewBox="0 0 24 24"><!-- path --></svg></span>
</div>
```

---

## Core Icon Library

Every icon uses `viewBox="0 0 24 24"`, `fill="none"`, `stroke="currentColor"`, `stroke-width="1.5"`, `stroke-linecap="round"`, `stroke-linejoin="round"`.

### Navigation & Actions

```html
<!-- Arrow Right -->
<svg viewBox="0 0 24 24"><path d="M5 12h14M12 5l7 7-7 7"/></svg>

<!-- Arrow Left -->
<svg viewBox="0 0 24 24"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>

<!-- Arrow Up -->
<svg viewBox="0 0 24 24"><path d="M12 19V5M5 12l7-7 7 7"/></svg>

<!-- Arrow Down -->
<svg viewBox="0 0 24 24"><path d="M12 5v14M19 12l-7 7-7-7"/></svg>

<!-- Arrow Up Right (external link) -->
<svg viewBox="0 0 24 24"><path d="M7 17L17 7M7 7h10v10"/></svg>

<!-- Chevron Right -->
<svg viewBox="0 0 24 24"><path d="M9 18l6-6-6-6"/></svg>

<!-- Chevron Down -->
<svg viewBox="0 0 24 24"><path d="M6 9l6 6 6-6"/></svg>

<!-- Chevron Left -->
<svg viewBox="0 0 24 24"><path d="M15 18l-6-6 6-6"/></svg>

<!-- Chevron Up -->
<svg viewBox="0 0 24 24"><path d="M18 15l-6-6-6 6"/></svg>

<!-- Close / X -->
<svg viewBox="0 0 24 24"><path d="M18 6L6 18M6 6l12 12"/></svg>

<!-- Menu / Hamburger -->
<svg viewBox="0 0 24 24"><path d="M4 6h16M4 12h16M4 18h16"/></svg>

<!-- Plus -->
<svg viewBox="0 0 24 24"><path d="M12 5v14M5 12h14"/></svg>

<!-- Minus -->
<svg viewBox="0 0 24 24"><path d="M5 12h14"/></svg>

<!-- Search -->
<svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/></svg>

<!-- More Horizontal (dots) -->
<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="1"/><circle cx="19" cy="12" r="1"/><circle cx="5" cy="12" r="1"/></svg>
```

### Status & Feedback

```html
<!-- Check / Success -->
<svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg>

<!-- Check Circle -->
<svg viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 11-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>

<!-- Alert Triangle -->
<svg viewBox="0 0 24 24"><path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>

<!-- Alert Circle -->
<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>

<!-- Info -->
<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/></svg>

<!-- X Circle -->
<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M15 9l-6 6M9 9l6 6"/></svg>

<!-- Loading Spinner (animated) -->
<svg viewBox="0 0 24 24" class="animate-spin"><circle cx="12" cy="12" r="10" stroke-width="2" stroke-dasharray="32" stroke-dashoffset="32" opacity="0.25"/><path d="M12 2a10 10 0 019.95 9" stroke-width="2"/></svg>
```

### Content & Media

```html
<!-- Image -->
<svg viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>

<!-- Video / Play -->
<svg viewBox="0 0 24 24"><polygon points="5 3 19 12 5 21 5 3"/></svg>

<!-- Pause -->
<svg viewBox="0 0 24 24"><rect x="6" y="4" width="4" height="16"/><rect x="14" y="4" width="4" height="16"/></svg>

<!-- File / Document -->
<svg viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>

<!-- Copy -->
<svg viewBox="0 0 24 24"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1"/></svg>

<!-- Download -->
<svg viewBox="0 0 24 24"><path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>

<!-- Upload -->
<svg viewBox="0 0 24 24"><path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>

<!-- Link -->
<svg viewBox="0 0 24 24"><path d="M10 13a5 5 0 007.54.54l3-3a5 5 0 00-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 00-7.54-.54l-3 3a5 5 0 007.07 7.07l1.71-1.71"/></svg>

<!-- Code -->
<svg viewBox="0 0 24 24"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg>

<!-- Terminal -->
<svg viewBox="0 0 24 24"><polyline points="4 17 10 11 4 5"/><line x1="12" y1="19" x2="20" y2="19"/></svg>
```

### Objects & Concepts

```html
<!-- Settings / Gear -->
<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 00.33 1.82l.06.06a2 2 0 010 2.83 2 2 0 01-2.83 0l-.06-.06a1.65 1.65 0 00-1.82-.33 1.65 1.65 0 00-1 1.51V21a2 2 0 01-4 0v-.09A1.65 1.65 0 009 19.4a1.65 1.65 0 00-1.82.33l-.06.06a2 2 0 01-2.83-2.83l.06-.06A1.65 1.65 0 004.68 15a1.65 1.65 0 00-1.51-1H3a2 2 0 010-4h.09A1.65 1.65 0 004.6 9a1.65 1.65 0 00-.33-1.82l-.06-.06a2 2 0 012.83-2.83l.06.06A1.65 1.65 0 009 4.68a1.65 1.65 0 001-1.51V3a2 2 0 014 0v.09a1.65 1.65 0 001 1.51 1.65 1.65 0 001.82-.33l.06-.06a2 2 0 012.83 2.83l-.06.06A1.65 1.65 0 0019.4 9a1.65 1.65 0 001.51 1H21a2 2 0 010 4h-.09a1.65 1.65 0 00-1.51 1z"/></svg>

<!-- Lock -->
<svg viewBox="0 0 24 24"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0110 0v4"/></svg>

<!-- Unlock -->
<svg viewBox="0 0 24 24"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 019.9-1"/></svg>

<!-- Shield -->
<svg viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>

<!-- Eye -->
<svg viewBox="0 0 24 24"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>

<!-- Heart -->
<svg viewBox="0 0 24 24"><path d="M20.84 4.61a5.5 5.5 0 00-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 00-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 000-7.78z"/></svg>

<!-- Star -->
<svg viewBox="0 0 24 24"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>

<!-- Lightning / Zap -->
<svg viewBox="0 0 24 24"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>

<!-- Globe -->
<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 014 10 15.3 15.3 0 01-4 10 15.3 15.3 0 01-4-10 15.3 15.3 0 014-10z"/></svg>

<!-- Mail -->
<svg viewBox="0 0 24 24"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22 6 12 13 2 6"/></svg>

<!-- Users / Team -->
<svg viewBox="0 0 24 24"><path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 00-3-3.87M16 3.13a4 4 0 010 7.75"/></svg>

<!-- Clock -->
<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>

<!-- Calendar -->
<svg viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>

<!-- Chart / Analytics -->
<svg viewBox="0 0 24 24"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>

<!-- Sparkles / Magic -->
<svg viewBox="0 0 24 24"><path d="M12 3l1.912 5.813a2 2 0 001.275 1.275L21 12l-5.813 1.912a2 2 0 00-1.275 1.275L12 21l-1.912-5.813a2 2 0 00-1.275-1.275L3 12l5.813-1.912a2 2 0 001.275-1.275L12 3z"/></svg>

<!-- Palette / Color -->
<svg viewBox="0 0 24 24"><circle cx="13.5" cy="6.5" r="2.5"/><circle cx="17.5" cy="10.5" r="2.5"/><circle cx="8.5" cy="7.5" r="2.5"/><circle cx="6.5" cy="12.5" r="2.5"/><path d="M12 2C6.49 2 2 6.49 2 12s4.49 10 10 10c.93 0 1.75-.63 1.96-1.55.09-.38-.01-.78-.27-1.07l-.36-.42c-.58-.67-.12-1.71.75-1.71h2.1c2.96 0 5.38-2.42 5.38-5.38 0-5.18-4.93-9.37-9.56-8.87z"/></svg>

<!-- Layers -->
<svg viewBox="0 0 24 24"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg>

<!-- Compass / Explore -->
<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/></svg>

<!-- Rocket / Launch -->
<svg viewBox="0 0 24 24"><path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 00-2.91-.09z"/><path d="M12 15l-3-3a22 22 0 012-3.95A12.88 12.88 0 0122 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 01-4 2z"/><path d="M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0"/><path d="M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5"/></svg>
```

### Data & Commerce

```html
<!-- Credit Card -->
<svg viewBox="0 0 24 24"><rect x="1" y="4" width="22" height="16" rx="2"/><line x1="1" y1="10" x2="23" y2="10"/></svg>

<!-- Dollar Sign -->
<svg viewBox="0 0 24 24"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6"/></svg>

<!-- Package / Box -->
<svg viewBox="0 0 24 24"><line x1="16.5" y1="9.4" x2="7.5" y2="4.21"/><path d="M21 16V8a2 2 0 00-1-1.73l-7-4a2 2 0 00-2 0l-7 4A2 2 0 003 8v8a2 2 0 001 1.73l7 4a2 2 0 002 0l7-4A2 2 0 0021 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/></svg>

<!-- Trending Up -->
<svg viewBox="0 0 24 24"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/></svg>

<!-- Database -->
<svg viewBox="0 0 24 24"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/></svg>

<!-- Cloud -->
<svg viewBox="0 0 24 24"><path d="M18 10h-1.26A8 8 0 109 20h9a5 5 0 000-10z"/></svg>

<!-- Server -->
<svg viewBox="0 0 24 24"><rect x="2" y="2" width="20" height="8" rx="2"/><rect x="2" y="14" width="20" height="8" rx="2"/><line x1="6" y1="6" x2="6.01" y2="6"/><line x1="6" y1="18" x2="6.01" y2="18"/></svg>
```

### Social & Communication

```html
<!-- GitHub -->
<svg viewBox="0 0 24 24"><path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 00-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0020 4.77 5.07 5.07 0 0019.91 1S18.73.65 16 2.48a13.38 13.38 0 00-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 005 4.77a5.44 5.44 0 00-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 009 18.13V22"/></svg>

<!-- Twitter / X -->
<svg viewBox="0 0 24 24"><path d="M4 4l11.733 16h4.267l-11.733-16zM4 20l6.768-6.768M20 4l-6.768 6.768"/></svg>

<!-- Share -->
<svg viewBox="0 0 24 24"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/></svg>

<!-- Message / Chat -->
<svg viewBox="0 0 24 24"><path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/></svg>

<!-- Bell / Notification -->
<svg viewBox="0 0 24 24"><path d="M18 8A6 6 0 006 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 01-3.46 0"/></svg>
```

---

## Feature Icon Patterns

For landing page feature sections, wrap icons with accent backgrounds:

### Filled Circle Background

```html
<div class="feature-icon" style="--icon-color: var(--accent);">
  <span class="icon">
    <svg viewBox="0 0 24 24"><!-- icon path --></svg>
  </span>
</div>

<style>
.feature-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: color-mix(in oklch, var(--icon-color) 10%, transparent);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--icon-color);
}
.feature-icon .icon {
  width: 24px;
  height: 24px;
}
</style>
```

### Gradient Icon Background

```html
<div class="feature-icon-gradient">
  <span class="icon">
    <svg viewBox="0 0 24 24"><!-- icon path --></svg>
  </span>
</div>

<style>
.feature-icon-gradient {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: linear-gradient(135deg, var(--accent), color-mix(in oklch, var(--accent) 80%, black));
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}
</style>
```

---

## List Bullets & Decorators

Replace CSS `list-style` bullets with proper check marks or custom SVG:

```html
<!-- Check list -->
<ul class="check-list">
  <li>
    <svg viewBox="0 0 24 24" class="check-icon"><polyline points="20 6 9 17 4 12"/></svg>
    Feature included
  </li>
</ul>

<style>
.check-list {
  list-style: none;
  padding: 0;
}
.check-list li {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 8px 0;
}
.check-icon {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
  stroke: var(--color-green, #34C759);
  stroke-width: 2;
  fill: none;
  margin-top: 2px; /* optical align with text */
}
</style>
```

---

## Rules

### Never Do

- **NEVER** use emoji as icons (no lightning bolt emoji for "fast", no lock emoji for "secure")
- **NEVER** use keyboard symbols as arrows or bullets (no `→`, `•`, `▸`, `×`)
- **NEVER** use Unicode symbols as UI elements (no `✓`, `✗`, `★`)
- **NEVER** use icon fonts (Font Awesome, Material Icons as fonts) — use inline SVG
- **NEVER** use `<img>` tags for icons — use inline `<svg>`
- **NEVER** mix icon styles (don't combine outlined and filled icons in same context)

### Always Do

- **ALWAYS** use inline SVG for all icons — zero external dependencies
- **ALWAYS** set `fill="none" stroke="currentColor"` — icons inherit text color
- **ALWAYS** use `viewBox="0 0 24 24"` for consistency across all icons
- **ALWAYS** match stroke-width to adjacent font-weight (1.5 for regular, 2 for semibold)
- **ALWAYS** add `aria-label` on icon-only buttons
- **ALWAYS** set `aria-hidden="true"` on decorative icons next to text
- **ALWAYS** use `vertical-align: -0.125em` for optical baseline alignment inline with text
- **ALWAYS** use `flex-shrink: 0` on icons to prevent squishing in flex layouts
- **ALWAYS** use `currentColor` so icons adapt to dark mode automatically

### Sizing

```
Inline with text:     1em (matches text size)
In buttons:           20px (with 16px text)
Feature cards:        24px inside 48px container
Hero/large:           32-48px
Navigation:           20-24px
Status indicators:    16px
```

### Accessibility

- Icon-only buttons MUST have `aria-label`
- Decorative icons (next to text) MUST have `aria-hidden="true"`
- Interactive icons must meet 3:1 contrast ratio
- Minimum touch target for icon buttons: 44×44px (even if icon is 24px, pad with spacing)
