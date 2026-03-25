# OneMore — Visual Polish & Demo Upgrade Plan

## Overview

The landing page structure, animations, and content are solid. The new Video Analysis section proves the quality bar we should hit everywhere. Now: upgrade all existing sections + demos to this level.

## Phase 1: Landing Page Section Upgrades (Priority: HIGH)

Each section needs to match the Visual Analysis section's quality — informative, interactive-looking visuals, not just decorative.

### 1.1 Hero Section
**Current:** Dark bg, floating layer cards (Colors, Typography, Spacing, Components, Animation), orbs, stars canvas
**Upgrade:**
- Replace abstract layer cards with a **live terminal/code preview** showing OneMore in action
- Add a **before/after** split showing generic AI output vs OneMore output
- Animated gradient mesh behind hero text (not just static orbs)
- Particle constellation connecting to the layer cards

### 1.2 Pitch Section
**Current:** "Your AI agent writes code. OneMore makes it beautiful." + text
**Upgrade:**
- Add a visual **comparison strip** — "Without OneMore" vs "With OneMore" side by side
- Show actual UI screenshots, not just text claims

### 1.3 Compatibility Section (compat-dark)
**Current:** Framework logos in a grid
**Upgrade:**
- Add **code export previews** next to each framework logo (mini code snippet)
- Animated transition between frameworks when hovered

### 1.4 "Design" BigText Section
**Current:** Just large text + paragraph
**Upgrade:**
- Add an animated **design token visualization** that builds up as you scroll

### 1.5 Terminal/Showcase Section
**Current:** Animated terminal showing 3 commands
**Upgrade:**
- Add the **Video Analysis** command as a 4th demo
- Show output appearing in real-time (not just typed commands)

### 1.6 Numbers Section
**Current:** 4 counting numbers (146 tests, 700+ rules, 25 pages, 13 frameworks)
**Upgrade:**
- Add **Video Analysis stats**: "3 Providers", "15s Analysis", "5/6 Accuracy"
- Animated rings or progress bars instead of just numbers

### 1.7 Design System Capability Section
**Current:** Color swatch card with tokens
**Upgrade:**
- Add **interactive theme switcher** (light/dark preview)
- Show tokens generating in real-time animation

### 1.8 Redesign Scanner Section
**Current:** Activity rings + scan results
**Upgrade:**
- Add **animated scanning** effect (progress animation)
- Show before/after of a real fix

### 1.9 Export Section
**Current:** Code snippet showing tailwind.config.js
**Upgrade:**
- Add **tab switcher** between all 7 formats (Tailwind, CSS, SwiftUI, Flutter, SCSS, JSON, RN)
- Each tab shows real export output

### 1.10 Gallery Section
**Current:** Horizontal scroll of 12 demo screenshots
**Upgrade:**
- Add **category filters** (SaaS, Mobile, Creative, etc.)
- Hover shows demo name + "View Demo" link
- Lazy-load higher quality screenshots

### 1.11 CTA Section
**Current:** "Get Started" button
**Upgrade:**
- Add **3-step quick start** (Install → Configure → Build)
- npm install command with copy button

## Phase 2: Demo Visual Polish (Priority: MEDIUM)

### Tier 1 (Flagship — do first)
1. **saas-dashboard.html** (DataPulse) — the demo most people will see first
2. **crypto-web3.html** (Nexus) — dark theme showcase
3. **creative-tools.html** (Prismix) — visual-heavy, proves animation quality

### Tier 2 (Important)
4. finance-banking.html
5. media-entertainment.html
6. food-delivery.html

### Tier 3 (Nice to have)
7-12. education, health-fitness, travel, social, ecommerce, productivity

### What "polish" means for each demo:
- [ ] SVG illustrations instead of gradient placeholders
- [ ] Proper hover states on all interactive elements
- [ ] Scroll animations (stagger reveals, parallax where appropriate)
- [ ] Dark mode support (prefers-color-scheme)
- [ ] Reduced motion support (prefers-reduced-motion)
- [ ] Consistent Apple HIG color system
- [ ] Touch target compliance (44px min)

## Phase 3: Infrastructure (Priority: LOW)

### 3.1 Screenshot Updates
After visual polish, retake all demo screenshots for gallery

### 3.2 Performance Audit
- Lighthouse score for landing page
- Image optimization (WebP, lazy loading)
- CSS/JS minification

### 3.3 SEO
- Meta tags per demo page
- Structured data (JSON-LD)
- Sitemap.xml

## Execution Order

```
Session 1: Phase 1.1-1.5 (Hero → Pitch → Compat → BigText → Terminal)
Session 2: Phase 1.6-1.11 (Numbers → Capabilities → Gallery → CTA)
Session 3: Phase 2 Tier 1 (DataPulse, Nexus, Prismix)
Session 4: Phase 2 Tier 2-3 (remaining demos)
Session 5: Phase 3 (screenshots, performance, SEO)
```

Each session: build → review → commit → push → next

## What's NOT in This Plan (Already Done)

- ✅ README.md — created with full docs, video prompting guide, 5 examples
- ✅ npm publish — v2.3.0 on npmjs.com
- ✅ Video Analysis integration — Gemini + OpenAI + ffmpeg, auto-detect stack
- ✅ Video Analyzer agent upgrade — 5/6 accuracy, 4 interpretation rules, composites
- ✅ Video Analysis section on landing page
- ✅ .firecrawl removed from git tracking
- ✅ 9 bugs fixed from code review
- ⏳ Custom domain — waiting on domain purchase (not in this plan)

## Reminders for Each Session

- Use `/onemore` skill for all visual work (dogfooding)
- Reference `docs/apple-patterns-analysis.md` for apple.com source patterns
- Keep single HTML file per page (no external dependencies)
- `prefers-reduced-motion` on every animation
- `prefers-color-scheme` dark mode where applicable
- Test in browser after each section upgrade
- Commit after each phase sub-section (1.1, 1.2, etc.), not at end
