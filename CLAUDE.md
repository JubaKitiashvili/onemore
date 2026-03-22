# OneMore — Apple HIG Design Intelligence

## Project Overview

OneMore is an Apple Human Interface Guidelines (HIG) design intelligence skill for AI coding agents. It generates Apple-quality UI across all platforms.

**Repo:** https://github.com/JubaKitiashvili/onemore
**Live site:** https://jubakitiashvili.github.io/onemore/
**Status:** v1.0.0 — core complete, visual polish in progress

## Tech Stack

- **Core:** Python 3.10+ (stdlib only), BM25 search engine over CSV databases
- **Skill:** SKILL.md entry point for Claude Code
- **Website:** Pure HTML/CSS/JS, zero external dependencies, GitHub Pages

## Project Structure

```
scripts/           — Python CLI (search.py, core.py, design_system.py, exporter.py, platforms.py, redesign.py)
data/              — 34 CSV files (foundations, components, patterns, platforms, stacks, audit, reasoning)
tests/             — 146 tests (pytest)
showcase/demos/    — 12 HTML showcase demos
docs/              — Specs, plans, Apple patterns analysis (1,981 lines from 25 apple.com pages)
index.html         — Landing page (GitHub Pages)
SKILL.md           — Claude Code skill entry point
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
