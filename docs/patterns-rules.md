# UI Patterns Rules — Liquid Glass, Navigation & Modality

Apple's latest design patterns: Liquid Glass material system, navigation hierarchies, and modal presentation patterns.

---

## 1. Liquid Glass

Apple's new dynamic material (WWDC 2025) that combines optical glass properties with fluid motion. It forms a distinct functional layer for controls and navigation elements.

### Core Principles

```
1. HIERARCHY: Liquid Glass creates a clear separation between
   navigation/controls layer and content layer.

2. RESTRAINT: Use sparingly — only on the most important functional
   elements. Overuse distracts from content.

3. ADAPTIVITY: The material adapts to context — scrolling, focus state,
   element overlap, accessibility settings.

4. CONCENTRIC DESIGN: Controls, windows, sheets all use rounded forms
   that nest concentrically with hardware curves.
```

### Applying Liquid Glass on Web (CSS Approximation)

```css
/* Liquid Glass material — web approximation */
.liquid-glass {
  background: rgba(255, 255, 255, 0.45);
  backdrop-filter: blur(24px) saturate(200%) brightness(1.05);
  -webkit-backdrop-filter: blur(24px) saturate(200%) brightness(1.05);
  border: 0.5px solid rgba(255, 255, 255, 0.35);
  border-radius: 20px;
  box-shadow:
    0 0.5px 0 rgba(255, 255, 255, 0.5) inset,   /* top highlight */
    0 -0.5px 0 rgba(0, 0, 0, 0.05) inset,        /* bottom shadow */
    0 4px 16px rgba(0, 0, 0, 0.06);               /* elevation */
  transition: all 0.35s cubic-bezier(0.25, 0.1, 0.25, 1);
}

/* Dark mode */
@media (prefers-color-scheme: dark) {
  .liquid-glass {
    background: rgba(40, 40, 40, 0.5);
    border-color: rgba(255, 255, 255, 0.12);
    box-shadow:
      0 0.5px 0 rgba(255, 255, 255, 0.1) inset,
      0 -0.5px 0 rgba(0, 0, 0, 0.2) inset,
      0 4px 16px rgba(0, 0, 0, 0.2);
  }
}

/* Prominent variant (for primary actions) */
.liquid-glass-prominent {
  background: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(30px) saturate(220%) brightness(1.1);
  -webkit-backdrop-filter: blur(30px) saturate(220%) brightness(1.1);
}

/* Clear variant (minimal) */
.liquid-glass-clear {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(16px) saturate(180%);
  -webkit-backdrop-filter: blur(16px) saturate(180%);
  border-color: rgba(255, 255, 255, 0.15);
}
```

### Liquid Glass Controls

```css
/* Glass button */
.glass-button {
  padding: 10px 20px;
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.35);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  border: 0.5px solid rgba(255, 255, 255, 0.3);
  color: var(--color-label);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.25, 0.1, 0.25, 1);
  min-height: 44px;
}

.glass-button:hover {
  background: rgba(255, 255, 255, 0.5);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.glass-button:active {
  transform: scale(0.97);
  background: rgba(255, 255, 255, 0.3);
}

/* Glass prominent button (with accent color) */
.glass-button-prominent {
  background: color-mix(in oklch, var(--accent) 70%, transparent);
  color: white;
  border-color: transparent;
}

/* Glass segmented control */
.glass-segmented {
  display: inline-flex;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(16px) saturate(180%);
  -webkit-backdrop-filter: blur(16px) saturate(180%);
  border-radius: 12px;
  padding: 3px;
  gap: 2px;
}

.glass-segment {
  padding: 8px 16px;
  border-radius: 10px; /* concentric: 12 - 2 */
  border: none;
  background: transparent;
  color: var(--color-secondary-label);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.25, 0.1, 0.25, 1);
}

.glass-segment.active {
  background: rgba(255, 255, 255, 0.5);
  color: var(--color-label);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
}
```

### Scroll Edge Effect

```css
/* Content fades/blurs when scrolling beneath glass controls */
.glass-toolbar {
  position: sticky;
  top: 0;
  z-index: 100;
  /* The toolbar itself */
  background: rgba(255, 255, 255, 0.45);
  backdrop-filter: blur(24px) saturate(200%);
  -webkit-backdrop-filter: blur(24px) saturate(200%);
}

/* Scroll edge gradient that maintains legibility */
.glass-toolbar::after {
  content: "";
  position: absolute;
  bottom: -20px;
  left: 0;
  right: 0;
  height: 20px;
  background: linear-gradient(
    to bottom,
    rgba(255, 255, 255, 0.3),
    transparent
  );
  pointer-events: none;
}
```

### Liquid Glass App Icons (Layered Structure)

```
Layer structure (from Apple's Icon Composer):
  Background (layer 3) — base fill, receives blur/translucency
  Middle (layer 2)     — secondary shapes, semi-transparent
  Foreground (layer 1) — primary symbol, can have specular highlights

Design principles:
  - Use solid, filled, overlapping semi-transparent shapes
  - No outlines — fill everything
  - Let system handle masking, blur, reflections, shadows
  - Provide layers as separate SVGs
  - Test across all 6 appearances: default, dark, clear-light,
    clear-dark, tinted-light, tinted-dark

Icon Composer JSON structure: see data/resources/icon-composer/icon.json
Layer SVGs: see data/resources/icon-composer/*.svg
```

### Rules for Liquid Glass

- **ALWAYS** include `-webkit-backdrop-filter` alongside `backdrop-filter` (Safari)
- **ALWAYS** use `saturate(180-220%)` with blur — prevents washed-out appearance
- **NEVER** overuse glass effects — limit to navigation bars, toolbars, tab bars, and primary controls
- **NEVER** layer glass elements on top of glass elements — creates visual noise
- **PREFER** `rgba()` backgrounds over solid colors for glass containers
- **PREFER** rounder corner radii than before — match hardware curves
- **USE** concentric radii: `inner_radius = outer_radius - padding`
- **USE** 0.5px borders with low-opacity white/black for edge definition
- **USE** inset box-shadow for top highlight + bottom shadow (gives depth)
- **PROVIDE** dark mode variant with slightly more opaque backgrounds
- **RESPECT** `prefers-reduced-transparency` — fall back to solid backgrounds:
  ```css
  @media (prefers-reduced-transparency: reduce) {
    .liquid-glass {
      background: var(--bg-secondary);
      backdrop-filter: none;
    }
  }
  ```

---

## 2. Navigation Patterns

### Navigation Hierarchy Types

```
FLAT NAVIGATION (Tab Bar)
├── Tab 1 (equal weight)
├── Tab 2
├── Tab 3
└── Tab 4
Best for: apps with 3-5 equal top-level sections
Components: Tab bar (bottom), sidebar (iPad/desktop)

HIERARCHICAL NAVIGATION (Push/Pop)
Root List → Detail → Sub-detail → ...
Best for: content drill-down (settings, file browsers, mail)
Components: Navigation bar with back button

CONTENT-DRIVEN NAVIGATION (Page/Scroll)
Page 1 → Page 2 → Page 3
Best for: onboarding, stories, media galleries
Components: Page dots, swipe gestures

COMBINED (Most Common)
Tab Bar (flat) → each tab has its own NavigationStack (hierarchical)
```

### Tab Bar

```css
/* Apple-style tab bar */
.tab-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  justify-content: space-around;
  align-items: center;
  height: 83px; /* 49px bar + 34px safe area on iPhone */
  padding-bottom: env(safe-area-inset-bottom, 0);
  /* Liquid Glass material */
  background: rgba(255, 255, 255, 0.45);
  backdrop-filter: blur(24px) saturate(200%);
  -webkit-backdrop-filter: blur(24px) saturate(200%);
  border-top: 0.5px solid rgba(0, 0, 0, 0.08);
  z-index: 100;
}

.tab-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
  padding: 6px 0;
  min-width: 44px;
  min-height: 44px;
  color: var(--color-secondary-label);
  text-decoration: none;
  transition: color 0.2s cubic-bezier(0.25, 0.1, 0.25, 1);
}

.tab-item.active {
  color: var(--accent);
}

.tab-item .icon { width: 24px; height: 24px; }
.tab-item .label { font-size: 10px; font-weight: 500; }
```

### Navigation Bar (Top Bar)

```css
/* Apple-style navigation bar */
.nav-bar {
  position: sticky;
  top: 0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 44px;
  padding: 0 16px;
  padding-top: env(safe-area-inset-top, 0);
  /* Liquid Glass */
  background: rgba(255, 255, 255, 0.45);
  backdrop-filter: blur(24px) saturate(200%);
  -webkit-backdrop-filter: blur(24px) saturate(200%);
  border-bottom: 0.5px solid rgba(0, 0, 0, 0.06);
  z-index: 100;
}

.nav-bar .back-button {
  display: flex;
  align-items: center;
  gap: 4px;
  color: var(--accent);
  background: none;
  border: none;
  font-size: 17px;
  font-weight: 400;
  cursor: pointer;
  min-height: 44px;
  padding: 0 4px;
}

.nav-bar .title {
  font-size: 17px;
  font-weight: 600;
  color: var(--color-label);
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
}

/* Large title (scrolls to inline) */
.large-title {
  font-size: 34px;
  font-weight: 700;
  padding: 0 16px;
  color: var(--color-label);
}
```

### Sidebar (iPad/Desktop)

```css
/* Apple-style sidebar */
.sidebar {
  width: 320px;
  height: 100vh;
  overflow-y: auto;
  padding: 12px;
  /* Liquid Glass */
  background: rgba(255, 255, 255, 0.3);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  border-right: 0.5px solid rgba(0, 0, 0, 0.06);
}

.sidebar-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 12px;
  border-radius: 10px;
  color: var(--color-label);
  text-decoration: none;
  font-size: 15px;
  min-height: 44px;
  transition: background 0.15s cubic-bezier(0.25, 0.1, 0.25, 1);
}

.sidebar-item:hover {
  background: rgba(0, 0, 0, 0.04);
}

.sidebar-item.active {
  background: color-mix(in oklch, var(--accent) 12%, transparent);
  color: var(--accent);
  font-weight: 500;
}

.sidebar-section-title {
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--color-secondary-label);
  padding: 16px 12px 4px;
}
```

### Rules for Navigation

- **ALWAYS** use safe area insets: `env(safe-area-inset-top)`, `env(safe-area-inset-bottom)`
- **ALWAYS** make tab bar items 44px minimum touch target
- **ALWAYS** center the navigation title horizontally
- **PREFER** tab bar for 3-5 top-level sections on mobile
- **PREFER** sidebar for iPad/desktop — tab bar adapts to sidebar on larger screens
- **USE** Liquid Glass material on navigation bars and tab bars
- **USE** large title (34px, bold) for root views, inline title (17px, semibold) for detail views
- **LIMIT** tab bar to 5 items maximum — use "More" tab if needed
- **PLACE** search in tab bar (trailing) on iOS, in toolbar on iPad/macOS
- **MINIMIZE** tab bar on scroll: it recedes when scrolling down, returns when scrolling up
- **BACK BUTTON** always includes chevron icon + previous page title (not just "Back")

---

## 3. Modality Patterns

### When to Use Modality

```
USE modal presentation when:
  - Requesting specific information (form, settings)
  - Presenting a scoped task (compose email, edit photo)
  - Showing critical information (alert, confirmation)
  - The task has a clear begin/end

DON'T use modal when:
  - Content can be shown inline
  - Navigation can handle the flow
  - The task is part of the main workflow
  - Users need to reference content behind the modal
```

### Sheet (Half Sheet / Full Sheet)

```css
/* Sheet — slides up from bottom */
.sheet-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.3);
  z-index: 200;
  opacity: 0;
  transition: opacity 0.3s cubic-bezier(0.25, 0.1, 0.25, 1);
  pointer-events: none;
}

.sheet-overlay.active {
  opacity: 1;
  pointer-events: auto;
}

.sheet {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  /* Half sheet: ~50vh, inset from edges */
  max-height: 85vh;
  margin: 0 8px 8px; /* inset from display edges — Liquid Glass style */
  border-radius: 20px;
  /* Liquid Glass */
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(40px) saturate(200%);
  -webkit-backdrop-filter: blur(40px) saturate(200%);
  box-shadow: 0 -4px 24px rgba(0, 0, 0, 0.08);
  transform: translateY(100%);
  transition: transform 0.4s cubic-bezier(0.25, 0.1, 0.25, 1);
  overflow: hidden;
  z-index: 201;
}

.sheet.active {
  transform: translateY(0);
}

/* Drag handle */
.sheet-handle {
  width: 36px;
  height: 5px;
  border-radius: 3px;
  background: rgba(0, 0, 0, 0.15);
  margin: 8px auto 0;
}

/* Sheet header */
.sheet-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  border-bottom: 0.5px solid rgba(0, 0, 0, 0.06);
}

.sheet-content {
  padding: 16px;
  overflow-y: auto;
  max-height: calc(85vh - 60px);
  -webkit-overflow-scrolling: touch;
}

/* Full sheet (expands from half) */
.sheet.full {
  max-height: 100vh;
  margin: 0;
  border-radius: 0;
  background: rgba(255, 255, 255, 0.95); /* more opaque when full */
}

@media (prefers-color-scheme: dark) {
  .sheet {
    background: rgba(30, 30, 30, 0.9);
  }
  .sheet-handle {
    background: rgba(255, 255, 255, 0.2);
  }
}
```

### Alert / Dialog

```css
/* Alert — centered, critical information */
.alert-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 300;
}

.alert {
  width: 270px;
  border-radius: 14px;
  /* Liquid Glass */
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(40px) saturate(200%);
  -webkit-backdrop-filter: blur(40px) saturate(200%);
  text-align: center;
  overflow: hidden;
  /* Entry animation */
  animation: alert-enter 0.25s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

@keyframes alert-enter {
  from {
    opacity: 0;
    transform: scale(0.85);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.alert-content {
  padding: 20px 16px;
}

.alert-title {
  font-size: 17px;
  font-weight: 600;
  color: var(--color-label);
  margin-bottom: 4px;
}

.alert-message {
  font-size: 13px;
  color: var(--color-secondary-label);
  line-height: 1.4;
}

.alert-actions {
  display: flex;
  border-top: 0.5px solid rgba(0, 0, 0, 0.1);
}

.alert-action {
  flex: 1;
  padding: 12px 8px;
  border: none;
  background: none;
  font-size: 17px;
  cursor: pointer;
  min-height: 44px;
  color: var(--accent);
  transition: background 0.15s;
}

.alert-action:active {
  background: rgba(0, 0, 0, 0.04);
}

.alert-action + .alert-action {
  border-left: 0.5px solid rgba(0, 0, 0, 0.1);
}

/* Destructive action */
.alert-action.destructive { color: #FF3B30; }

/* Default (bold) action */
.alert-action.default { font-weight: 600; }

/* Stacked layout for long button text */
.alert-actions.stacked {
  flex-direction: column;
}
.alert-actions.stacked .alert-action + .alert-action {
  border-left: none;
  border-top: 0.5px solid rgba(0, 0, 0, 0.1);
}
```

### Popover

```css
/* Popover — anchored to source element */
.popover {
  position: absolute;
  min-width: 200px;
  max-width: 320px;
  border-radius: 14px;
  /* Liquid Glass */
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(40px) saturate(200%);
  -webkit-backdrop-filter: blur(40px) saturate(200%);
  box-shadow:
    0 4px 16px rgba(0, 0, 0, 0.08),
    0 0 0 0.5px rgba(0, 0, 0, 0.06);
  z-index: 250;
  /* Entry */
  animation: popover-enter 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

@keyframes popover-enter {
  from { opacity: 0; transform: scale(0.9) translateY(4px); }
  to { opacity: 1; transform: scale(1) translateY(0); }
}

/* Arrow pointing to source */
.popover::before {
  content: "";
  position: absolute;
  top: -8px;
  left: 50%;
  transform: translateX(-50%);
  border-left: 8px solid transparent;
  border-right: 8px solid transparent;
  border-bottom: 8px solid rgba(255, 255, 255, 0.85);
}
```

### Action Sheet

```css
/* Action sheet — originates from source element (Liquid Glass style) */
.action-sheet {
  position: fixed;
  bottom: 8px;
  left: 8px;
  right: 8px;
  border-radius: 14px;
  overflow: hidden;
  /* Liquid Glass */
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(40px) saturate(200%);
  -webkit-backdrop-filter: blur(40px) saturate(200%);
  z-index: 201;
  transform: translateY(100%);
  transition: transform 0.35s cubic-bezier(0.25, 0.1, 0.25, 1);
}

.action-sheet.active {
  transform: translateY(0);
}

.action-sheet-item {
  padding: 16px;
  text-align: center;
  font-size: 20px;
  color: var(--accent);
  border-bottom: 0.5px solid rgba(0, 0, 0, 0.08);
  cursor: pointer;
  min-height: 57px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.1s;
}

.action-sheet-item:active {
  background: rgba(0, 0, 0, 0.04);
}

.action-sheet-item.destructive {
  color: #FF3B30;
}

/* Cancel button — separate with gap */
.action-sheet-cancel {
  margin-top: 8px;
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(40px) saturate(200%);
  -webkit-backdrop-filter: blur(40px) saturate(200%);
  font-weight: 600;
}
```

### Loading States

```css
/* Skeleton loader */
.skeleton {
  background: linear-gradient(
    90deg,
    var(--bg-secondary) 25%,
    color-mix(in oklch, var(--bg-secondary) 80%, white) 50%,
    var(--bg-secondary) 75%
  );
  background-size: 200% 100%;
  animation: skeleton-shimmer 1.5s ease-in-out infinite;
  border-radius: 8px;
}

@keyframes skeleton-shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

.skeleton-text { height: 16px; margin-bottom: 8px; }
.skeleton-title { height: 24px; width: 60%; margin-bottom: 12px; }
.skeleton-avatar { width: 48px; height: 48px; border-radius: 50%; }
.skeleton-image { width: 100%; aspect-ratio: 16/9; }

/* Spinner (Apple style — thin arc) */
.spinner {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(0, 0, 0, 0.08);
  border-top-color: var(--accent);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Progress bar */
.progress-bar {
  height: 4px;
  background: var(--bg-secondary);
  border-radius: 2px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: var(--accent);
  border-radius: 2px;
  transition: width 0.3s cubic-bezier(0.25, 0.1, 0.25, 1);
}

@media (prefers-reduced-motion: reduce) {
  .skeleton { animation: none; }
  .spinner { animation: none; border-top-color: var(--accent); }
}
```

### Rules for Modality

- **ALWAYS** include a way to dismiss (close button, swipe down, cancel, or tap outside)
- **ALWAYS** add scrim/overlay behind modals (rgba(0,0,0,0.3-0.4))
- **ALWAYS** trap focus inside modal for keyboard users
- **ALWAYS** close on Escape key
- **PREFER** sheet over alert when content is complex
- **PREFER** non-modal sheet when users need to reference content behind it
- **USE** spring animation for alert entry: `scale(0.85)→scale(1)` with overshoot
- **USE** slide-up for sheets, scale-fade for alerts, scale-down-fade for popovers
- **USE** drag-to-dismiss on sheets — detect velocity for commit/cancel
- **INSET** half sheets from display edges (8px margin) — Liquid Glass style
- **INCREASE** sheet opacity when expanded to full height
- **LIMIT** alert to 2 actions side-by-side, 3+ stacked vertically
- **DESTRUCTIVE** actions always in red (#FF3B30), never as the default
- **CANCEL** always at bottom of action sheet

---

## Quick Reference: Component Selection

| Need | Component | Notes |
|------|-----------|-------|
| Top-level app sections | Tab bar (mobile), Sidebar (desktop) | Max 5 tabs |
| Content drill-down | Navigation bar with back button | Large → inline title |
| Quick task / form | Sheet (half or full) | Drag-to-dismiss |
| Critical decision | Alert dialog | 2 buttons max side-by-side |
| Contextual options | Action sheet | Anchored to source |
| Tooltip/info | Popover | Anchored with arrow |
| Content loading | Skeleton loader | Shimmer animation |
| Action in progress | Spinner or progress bar | Pair with status text |
| Background surface | Liquid Glass material | Sparingly, never stacked |
