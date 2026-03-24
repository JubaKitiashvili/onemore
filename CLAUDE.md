# OneMore — Apple HIG Design Intelligence

## Project Overview

OneMore is an Apple Human Interface Guidelines (HIG) design intelligence skill for AI coding agents. It generates Apple-quality UI across all platforms.

**Repo:** https://github.com/JubaKitiashvili/onemore
**Live site:** https://jubakitiashvili.github.io/onemore/
**Status:** v1.0.0 — core complete, visual polish in progress

## Tech Stack

- **Core:** Python 3.10+ (stdlib only), BM25 search engine over CSV databases
- **Skill:** SKILL.md orchestrator + 6 specialized agents
- **Website:** Pure HTML/CSS/JS, zero external dependencies, GitHub Pages

## Project Structure

```
SKILL.md           — Orchestrator: classifies intent, routes to agents
agents/            — 6 specialized agents:
  onemore-vision.md    — Steve Jobs: prompt → creative brief (vision-rules.md)
  onemore-build.md     — Jony Ive: brief → production code (craft + design-system + animation rules)
  onemore-review.md    — Quality Gate: code → pass/fail checklist (all rules)
  onemore-animate.md   — Motion Expert: animation tasks (animation-rules + craft 1-3, 7)
  onemore-a11y.md      — Accessibility Auditor: WCAG 2.2 audit (design-system 9, craft 12)
  onemore-analyze.md   — Video Analyzer: reference video → motion spec (ffmpeg mosaic)
docs/              — 4 rules files + Apple patterns analysis
scripts/           — Python CLI (search.py, core.py, design_system.py, exporter.py, platforms.py, redesign.py)
data/              — 34 CSV files (foundations, components, patterns, platforms, stacks, audit, reasoning)
tests/             — 146 tests (pytest)
showcase/demos/    — 12 HTML showcase demos
index.html         — Landing page (GitHub Pages)
```

## Key Features

- 13 framework stacks (SwiftUI, React, RN, Flutter, Tailwind, Vue, Svelte, Next.js, shadcn, NativeWind, UIKit, Nuxt, Astro)
- 11 AI platform integrations + auto-detect (`onemore init`)
- 7 export formats (`onemore export --format tailwind|css|swiftui|flutter|scss|json|react-native`)
- Redesign scanner [BETA] (`onemore redesign ./src/`) with Expo/NativeWind detection
- Design system generator (`onemore --design-system`)
- Apple Product Page Animation Standard (from 25-page apple.com analysis)

## Commands

```bash
python3 -m pytest tests/ -v              # Run tests (146 should pass)
python3 scripts/search.py "button" -d controls   # Search components
python3 scripts/search.py init --list             # Show AI platform status
python3 scripts/search.py export --list           # Show export formats
python3 scripts/search.py redesign ./src/         # Scan for HIG violations
```

## IMPORTANT: Use OneMore's Own Skill

When building UI for this project (landing page, demos, any visual work), you MUST use the OneMore skill (SKILL.md) as your design guide. This is dogfooding — OneMore's own website must be the best proof of its quality.

Load SKILL.md and follow:
- Apple HIG Core Principles
- Apple Product Page Animation Standard
- Apple Design Maxims
- Pre-Delivery Checklist
- Category-specific accent colors from data/reasoning/apple-reasoning.csv

## Current TODO (Next Session Priority)

### 1. Landing Page Visual Upgrade (HIGH PRIORITY)
The landing page structure and animations are solid, but it looks "empty" compared to apple.com. Needs:

- **SVG illustrations** — Custom vector art for hero, features, sections (not stock photos)
- **Gradient mesh backgrounds** — Complex multi-stop radial gradients for depth
- **Animated ambient effects** — Floating glow orbs, light beams, particle dots
- **Noise/grain texture** — SVG filter overlay for Apple-like texture
- **3D perspective elements** — CSS transforms for depth on mockups
- **Constellation/dot patterns** — Subtle background decoration
- **Morphing blobs** — Animated organic shapes as section backgrounds

Reference: docs/apple-patterns-analysis.md (1,981 lines of apple.com source analysis)

### 2. Demo Visual Polish
Apply same visual upgrade to the 12 showcase demos. Priority order:
1. DataPulse (SaaS) — flagship demo
2. Nexus (Crypto) — dark theme showcase
3. Prismix (Creative) — visual-heavy

### 3. README.md
Create proper GitHub README with:
- Badges (tests, license, version)
- Hero image/GIF
- Feature highlights
- Quick start guide
- Demo links
- Before/After showcase

### 4. Custom Domain
User plans to buy a custom domain. Setup:
- CNAME file in repo root
- GitHub Pages custom domain configuration
- DNS setup guide

### 5. npm Publish (Later)
Package for npm distribution — after visual polish and testing.

## Agent Architecture

OneMore uses a single `/onemore` command that intelligently routes to specialized agents:

```
/onemore "build me a SaaS landing page"
    → vision agent → [brief, user confirms] → build agent → review agent

/onemore "fix the hover animation on cards"
    → animate agent (directly)

/onemore "check accessibility"
    → a11y agent (directly)

/onemore [video.mp4] "make it like this"
    → analyze agent → mosaic frames → motion spec → animate/build agent
```

| Route | Triggers | Pipeline |
|-------|----------|----------|
| Build from scratch | build, create, design, make | vision → build → review |
| Fix / improve | fix, improve, update, change | build (directly) |
| Animate | animate, scroll, transition, hover, parallax | animate (specialist) |
| Review | review, check, audit, quality | review (directly) |
| Accessibility | a11y, contrast, screen reader, WCAG | a11y (specialist) |
| Video reference | video file attached | analyze → animate/build |
| Redesign | redesign, rethink, reimagine | vision → build → review |

## Design & Animation Rules Reference

**MUST read before any UI/animation work.** Two comprehensive rule files:

### `docs/animation-rules.md` — Animation & Motion (11 topics)
1. Framer Motion (variants, AnimatePresence, layout, gestures)
2. GSAP + ScrollTrigger + @gsap/react (useGSAP, timelines, pinning, scrub)
3. Three.js + R3F + Drei (scene setup, useFrame, dispose, helpers)
4. Lottie (loadAnimation, destroy, React integration)
5. CSS Scroll-Driven Animations (scroll(), view(), animation-range)
6. SVG Animation & Filters (path drawing, feTurbulence, noise/grain)
7. Modern CSS Color (oklch, color-mix, light-dark)
8. View Transitions API (SPA/MPA, view-transition-name)
9. Web Animations API (element.animate, promises, stagger)
10. GLSL Basics (vertex/fragment shaders, noise, uniforms)
11. Animation Performance (GPU compositing, will-change, CLS/INP, RAF)

### `docs/design-system-rules.md` — Design System & Platforms (9 topics)
1. Apple HIG Typography (text styles, SF Pro web stack, sizes, weights, tracking)
2. Apple HIG Layout & Spacing (8pt grid, content widths, corner radii, safe areas)
3. Apple HIG Color System (semantic colors, materials, vibrancy, dark mode)
4. SwiftUI Patterns (@Observable, NavigationStack, layout, state management)
5. Tailwind CSS v4 (@theme, oklch colors, container queries, CSS nesting)
6. shadcn/ui (oklch theming, CSS variables, component patterns, dark mode)
7. NativeWind v5 (setup, className, platform variants, dark mode)
8. Modern CSS (container queries, CSS nesting, :has(), subgrid)
9. Accessibility / WCAG 2.2 (contrast, focus, target size, ARIA, reduced motion)

### `docs/vision-rules.md` — Vision: "Think Like Steve Jobs" (prompt → brief pipeline)
- The 7 Questions (who, what, why, feel, one-more-thing, say-no, identity)
- One-Sentence Distillation (≤12 word hero headline formula)
- Narrative Arc (7-section story structure, not "sections")
- Creative Brief Template (complete handoff format for implementation)
- Full transformation example (vague prompt → detailed brief)
- Tone guide (Steve Jobs voice formula)
- When to ask user vs. decide yourself

**MUST run this process before ANY UI work — even "simple" requests.**

### `docs/visual-rules.md` — Visual Generation: Code-Based Art (6 topics)
1. SVG Illustrations (hero compositions, isometric cards, feature icons, abstract art)
2. CSS Gradient Art (gradient mesh, aurora effects, gradient text, glass cards, floating orbs)
3. Canvas Generative Art (particle constellation, wave animation, animated charts)
4. SVG Filters & Textures (noise/grain, glow, morphing blobs, gradient borders)
5. CSS Device Mockups (iPhone, browser window, MacBook frames)
6. Placeholder System (structured placeholders for real photos with data attributes)

### `docs/icons-rules.md` — Icon System: Zero Emoji, Pure SVG (4 topics)
1. Core Icon Library (70+ inline SVG icons: navigation, status, content, objects, data, social)
2. Icon Component System (CSS wrapper, size variants, stroke-weight matching font-weight)
3. Feature Icon Patterns (filled circle, gradient background, list decorators)
4. Rules (NEVER emoji/keyboard symbols/unicode — ALWAYS inline SVG with currentColor)

### `docs/patterns-rules.md` — UI Patterns: Liquid Glass, Navigation & Modality (3 topics)
1. Liquid Glass (CSS web approximation, glass buttons, segmented controls, scroll edge, app icons)
2. Navigation Patterns (tab bar, nav bar, sidebar, large title, hierarchy types)
3. Modality (sheets with drag-to-dismiss, alerts, popovers, action sheets, loading states)

### `docs/craft-rules.md` — Craft & Physics: "Feels Like Apple" (12 topics)
1. Spring Physics (mass, stiffness, damping — Apple presets, web equivalents)
2. Rubber Banding (overscroll physics, elastic bounds, iOS feel)
3. Gesture Velocity & Momentum (velocity-driven animations, deceleration curves)
4. Optical Corrections (visual centering, text alignment, icon weight compensation)
5. Material Depth System (5-layer hierarchy, blur levels, shadow mapping, scrim)
6. P3 Wide Gamut Color (Display P3 on web, oklch P3 extension, fallbacks)
7. Micro-Interactions (button press, toggle, checkbox, pull-to-refresh, long press)
8. Proportional Systems (modular scale, golden ratio, aspect ratios)
9. Icon Construction (Apple grid, SF Symbols principles, web icon rules)
10. Progressive Disclosure (information architecture, reveal patterns)
11. Sensory Pairing (haptic + visual + audio synchronization matrix)
12. Reduced Motion — Complete (replace, don't disable — crossfade over slide)

## Apple Design Analysis Reference

docs/apple-patterns-analysis.md contains analysis of 25 apple.com pages:
- 13 Product pages (MacBook, iPhone, iPad, Watch, AirPods, Vision Pro, Apple Intelligence)
- 7 Developer pages (developer.apple.com)
- 5 Service/Values pages (Services, Apple Card, Shop, Accessibility, Environment)

Key finding: Apple uses 3 animation tiers:
- Heavy (product pages): scroll-linked keyframes, stagger reveals, parallax, video scrubbing
- Moderate (services/values): some scroll animation, Lottie for data viz
- Zero (developer/shop): no scroll animation, content-first

OneMore defaults to Heavy (product page) tier.

## Conventions

- Single self-contained HTML files for demos (no external dependencies)
- Apple HIG color system (#1d1d1f text, #fbfbfd background, #86868b secondary)
- cubic-bezier(0.25, 0.1, 0.25, 1) for ALL transitions
- prefers-reduced-motion always respected
- prefers-color-scheme dark mode support on all pages
- Category-specific accent colors (not always #007AFF)
