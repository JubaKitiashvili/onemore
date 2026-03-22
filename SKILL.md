---
name: onemore
description: "Apple HIG design intelligence. Generates Apple-quality UI across all platforms (iOS, macOS, watchOS, visionOS, web). Actions: design, build, create, implement, review, audit, fix, improve UI/UX code. Styles: Apple HIG, Cupertino, SF Pro, system colors, spring animations, materials, vibrancy. Projects: iOS app, macOS app, website, landing page, dashboard, mobile app, SwiftUI, React, React Native, Flutter. Elements: navigation bar, tab bar, toolbar, button, toggle, slider, picker, sheet, alert, list, card, search bar. Topics: spacing, typography, color system, dark mode, accessibility, dynamic type, haptics, gestures, continuous corners, SF Symbols."
---

# OneMore — Apple HIG Design Intelligence

One more thing your design needs.

OneMore is an Apple HIG design intelligence skill for Claude Code. It provides authoritative, up-to-date Apple Human Interface Guidelines data, searchable by domain, platform, and stack, so every UI decision you make is grounded in Apple-quality design principles.

---

## Apple HIG Core Principles

- **Clarity** — Text is legible, icons precise, adornments subtle. Function drives form.
- **Deference** — UI helps people understand and interact with content without competing with it.
- **Depth** — Visual layers and realistic motion convey hierarchy and aid understanding.
- **Consistency** — Familiar standards and paradigms let people transfer knowledge across apps.
- **Direct Manipulation** — Interaction with content feels immediate and results are visible.
- **Feedback** — Every action has a response; status is always communicated clearly.

---

## Priority Rules Quick Reference

| Priority | Category | Impact |
|----------|----------|--------|
| 1 | Accessibility & Dynamic Type | CRITICAL |
| 2 | Touch Targets & Safe Areas | CRITICAL |
| 3 | Typography (SF Pro/NY system) | HIGH |
| 4 | Color System (semantic, adaptive) | HIGH |
| 5 | Spacing (4pt grid) | HIGH |
| 6 | Components (native patterns) | MEDIUM |
| 7 | Animation (spring physics) | MEDIUM |
| 8 | Platform-Specific Patterns | MEDIUM |

---

## Apple Design Maxims

These rules separate Apple-quality design from generic AI output:

### One Focal Point Per Section
Every section gets ONE headline, ONE visual, ONE CTA. If you're adding a second visual or third button, the section is too busy. Split it or simplify.

### Dark for Product, Light for Text
Product showcases and hero visuals use dark/black backgrounds. Text-heavy sections (features, pricing, FAQ) use light backgrounds. Alternate between them for visual rhythm.

### Apple Product Page Animation Standard (Default)
The default animation approach matches Apple's product pages — the most iconic Apple experience:

**Hero (on load, not scroll):**
- Staggered entrance: tag → headline → subtitle → CTAs → visual mockup
- Each element: opacity 0→1, translateY(30px→0), 600ms cubic-bezier(0.25, 0.1, 0.25, 1)
- Stagger delay: 150-200ms between elements

**Every Section (scroll-triggered):**
- Use IntersectionObserver (threshold: 0.15) to trigger reveals
- Section headline fades up first, then content staggers in
- Each element: opacity 0→1, translateY(30px→0)
- Stagger delay: 100-150ms between sibling elements

**Visual Elements (scroll-linked):**
- Product mockups/dashboards: parallax effect (move at 0.3x scroll speed)
- Large visuals: clip-path reveal (inset 8%→0%) as they scroll into view
- Charts/graphs: draw animation (SVG stroke-dasharray)
- Numbers: count-up animation with ease-out cubic

**Hover Interactions:**
- Cards: translateY(-4px) + shadow increase, 200ms transition
- Buttons: subtle scale(1.02) or background shift
- Links: color transition 150ms

**Easing:** Always cubic-bezier(0.25, 0.1, 0.25, 1) — Apple's standard curve
**Performance:** Only animate transform and opacity (GPU-accelerated)
**Accessibility:** All animations disabled when prefers-reduced-motion is set

**When to use LESS animation:**
- Developer documentation / technical content → zero scroll animation
- E-commerce / transactional pages → minimal, speed-first
- Data-heavy dashboards → animate data viz only, not chrome

### Generous Negative Space
Apple's exact spacing scale from 25 pages analyzed:
- Between elements: 8, 16, 20, 24px
- Section internal padding: 32, 40, 48px
- Between sections: 56, 64, 72, 80, 96, 120px
- Desktop sections: 80-120px vertical padding
- Tablet sections: 72-96px
- Mobile sections: 40-72px
- Content max-width: 980px for text, 1200px for card grids

### Accent Color Identity
Every project gets ONE accent color (not always systemBlue). Choose from the reasoning database based on app category. Use it sparingly — primary CTAs and key highlights only.

---

## Quick Reference

- **Accessibility**: 4.5:1 contrast ratio minimum, VoiceOver labels on all interactive elements, Dynamic Type support required
- **Touch**: 44pt minimum touch target on iOS, 60pt minimum on visionOS
- **Typography**: SF Pro on native Apple platforms, Inter or system-ui on web; body text 17pt iOS / 13pt macOS
- **Colors**: Always use semantic color tokens, support dark mode, never hardcode hex values
- **Spacing**: 4pt grid — values: 4 / 8 / 12 / 16 / 20 / 24 / 32 / 48
- **Components**: Prefer native controls, use continuous corners on all rounded rects
- **Animation**: Spring physics only — never `linear` or `ease` for UI motion
- **Platform**: iOS, macOS, and visionOS have distinct patterns — verify per-platform before shipping

---

## How to Use

**Step 1: Analyze requirements**
Identify the product type (app, website, dashboard), target platform (iOS, macOS, visionOS, web), and tech stack (SwiftUI, React, React Native, Flutter).

**Step 2: Generate a design system**
```
python3 scripts/search.py "query" --design-system -p "ProjectName"
```

**Step 3: Search specific domains**
```
python3 scripts/search.py "keyword" --domain colors
```
Available domains: `colors`, `typography`, `spacing`, `components`, `animation`, `patterns`, `accessibility`

**Step 4: Get platform guidelines**
```
python3 scripts/search.py "keyword" --platform ios
```
Available platforms: `ios`, `macos`, `watchos`, `visionos`, `web`

**Step 5: Get stack implementation**
```
python3 scripts/search.py "keyword" --stack swiftui
```
Available stacks: `swiftui`, `react`, `react-native`, `flutter`, `html-tailwind`

---

## Font Licensing Note

SF Pro and SF New York are licensed exclusively for use on Apple platforms (iOS, macOS, watchOS, visionOS). Do not embed or serve them on the web.

For web projects, use the following font stack:
```css
font-family: -apple-system, BlinkMacSystemFont, Inter, system-ui, sans-serif;
```

---

## Pre-Delivery Checklist

- [ ] Uses Apple spacing scale (4pt grid)
- [ ] Typography: SF Pro (native) or Inter/system-ui (web)
- [ ] Semantic color tokens, dark mode tested
- [ ] Continuous corners (`borderCurve: continuous`)
- [ ] Touch targets min 44pt (60pt visionOS)
- [ ] Spring animations, no linear/ease
- [ ] Dynamic Type / font scaling supported
- [ ] No emoji icons — SF Symbols or Lucide/Heroicons
- [ ] Platform-appropriate patterns
- [ ] Accessibility: VoiceOver, 4.5:1 contrast, focus states
- [ ] Materials/vibrancy where appropriate
- [ ] Safe areas respected

---

## Anti-Patterns

| Anti-Pattern | Fix |
|---|---|
| `border-radius: 8px` | Continuous corners, platform-correct radii |
| Arial/Helvetica | SF Pro (native), Inter (web) |
| Random spacing | 4pt grid |
| Flat lifeless UI | Materials, vibrancy, shadows |
| `ease-in-out` | Spring physics |
| `#000000` text | Semantic label color (`#1d1d1f` on web) |
| Emoji icons | SF Symbols or equivalent SVG |
