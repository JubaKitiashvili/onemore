# OneMore — Apple HIG Design Intelligence

**One more thing your design needs.**

OneMore is an Apple Human Interface Guidelines (HIG) design intelligence skill for AI coding agents. Say `/onemore` — it generates Apple-quality UI across every platform.

[![npm version](https://img.shields.io/npm/v/onemore-design)](https://www.npmjs.com/package/onemore-design)
[![tests](https://img.shields.io/badge/tests-146%20passing-brightgreen)]()
[![license](https://img.shields.io/badge/license-MIT-blue)]()

---

## Quick Start

```bash
# Install for Claude Code
npx onemore-design init

# Or add manually
# Copy SKILL.md + agents/ + docs/ to ~/.claude/skills/onemore/
```

Then in Claude Code:
```
/onemore "build me a SaaS landing page"
/onemore "fix the hover animation on these cards"
/onemore "check accessibility"
```

---

## Features

### 6 Specialized Agents

| Agent | Role | What it does |
|-------|------|-------------|
| **Vision** | Steve Jobs | Transforms vague prompts into opinionated creative briefs |
| **Build** | Jony Ive | Turns briefs into production code |
| **Review** | Quality Gate | Pass/fail checklist against Apple HIG |
| **Animate** | Motion Expert | Spring physics, scroll animations, GSAP, Framer Motion |
| **A11y** | Accessibility | WCAG 2.2 audit with auto-fixes |
| **Analyze** | Video Analyzer | Reverse-engineers UI from screen recordings |

### Video Analysis (New)

Record any website or app, send the video to OneMore, and get a complete implementation blueprint — animations, design tokens, component specs, ready-to-paste code.

**Three analysis tiers:**

| Tier | Method | Speed | Accuracy | Cost |
|------|--------|-------|----------|------|
| **Gemini API** | Google Gemini 2.5 native video | ~15-30s | Best | ~$0.01-0.04/video |
| **OpenAI API** | GPT-4o vision | ~20-40s | Great | ~$0.04/video |
| **Built-in** | ffmpeg frames + Claude vision | ~3-4min | Good | Free |

Auto-fallback: Gemini → OpenAI → Built-in (based on available API keys).

#### Auto-Detect Project Stack

OneMore reads your `package.json` (or `pubspec.yaml`, `Package.swift`, etc.) and automatically targets your stack:

```
/onemore [video.mp4] "make my app look like this"

> Detected: React Native (Expo) with Reanimated 3, NativeWind
> Analyzing video... (Gemini 2.5 Flash, 14s)
> Blueprint ready — 7 animations, 5 components, RN code snippets
```

#### Setup Video Analysis API (Optional)

```bash
# Edit ~/.claude/skills/onemore/onemore.local.md
# Add your API key(s):
```

```yaml
---
gemini_api_key: "AIzaSy..."    # Google Gemini (recommended)
openai_api_key: "sk-..."       # OpenAI GPT-4o (alternative)
video_model: "auto"             # auto | gemini-2.5-pro | gemini-2.5-flash | gpt-4o
---
```

Get a free Gemini key: https://aistudio.google.com/apikey

Without API keys, OneMore uses its built-in ffmpeg analysis — completely free, no cloud dependency.

#### Video Prompting Guide

Adding context with your video dramatically improves analysis quality. Here are the 5 best prompting patterns:

**1. Full App Recreation (Mobile)**
```
/onemore [video.mp4]
"Analyze this and produce a complete implementation spec for React Native
with Reanimated 3. Focus on: gesture interactions, shared element transitions,
spring physics, SVG shapes, and component hierarchy."
```

**2. Web Landing Page with Scroll Effects**
```
/onemore [video.mp4]
"Analyze this scroll-driven website for Next.js with GSAP ScrollTrigger +
Lenis smooth scroll. Focus on: parallax layer rates, scroll-linked scale/opacity,
section transitions, text stagger timing, and hover states."
```

**3. Specific Component Extraction**
```
/onemore [video.mp4]
"Extract the card slider component. I need: the custom shape (SVG path),
drag gesture logic, value interpolation, spring config, and all visual specs
(gradients, shadows, border-radius) for my React Native app."
```

**4. Animation-Only Analysis**
```
/onemore [video.mp4]
"Focus ONLY on animations. For each: exact trigger, properties with
from→to values, duration in ms, easing curve, stagger delay, and whether
it's scroll-linked or triggered. Produce a choreography timeline."
```

**5. Design System Extraction**
```
/onemore [video.mp4]
"Extract the complete design system: color tokens (hex), typography scale,
spacing system, border-radius, shadows, gradients, and component variants.
Output as CSS custom properties and React Native StyleSheet."
```

> **Tip:** You don't need to specify your stack if you're running `/onemore` inside your project directory — it auto-detects from `package.json`.

### 13 Framework Stacks

SwiftUI, React, React Native, Flutter, Tailwind CSS, Vue, Svelte, Next.js, shadcn/ui, NativeWind, UIKit, Nuxt, Astro

### 42 Design Topics

Organized in 6 rule files:
- **Craft** — Spring physics, rubber banding, gesture velocity, optical corrections, materials, P3 color
- **Design System** — Typography, layout, color system, accessibility, Tailwind v4, shadcn/ui, NativeWind
- **Animation** — Framer Motion, GSAP, Three.js, Lottie, CSS scroll-driven, SVG, View Transitions
- **Vision** — Creative brief generation, Steve Jobs product thinking
- **Visual** — SVG illustrations, gradient art, canvas generative, CSS device mockups
- **Patterns** — Liquid Glass, navigation patterns, modality

### Python CLI

```bash
python3 scripts/search.py "button" -d controls    # Search components
python3 scripts/search.py init --list              # Show AI platform status
python3 scripts/search.py export --format tailwind # Export design tokens
python3 scripts/search.py redesign ./src/          # Scan for HIG violations
```

---

## How Routing Works

OneMore auto-classifies your intent:

```
/onemore "build me a SaaS landing page"
    → Vision → [confirm brief] → Build → Review

/onemore "fix the hover animation on cards"
    → Build (directly)

/onemore "check accessibility"
    → A11y (specialist)

/onemore [video.mp4] "make it like this"
    → Analyze → Build
```

---

## Project Structure

```
SKILL.md              — Orchestrator: classifies intent, routes to agents
agents/               — 6 specialized agents
docs/                 — Design rules (craft, animation, design-system, vision, visual, patterns)
scripts/              — Python CLI + Gemini/OpenAI video analysis
data/                 — 34 CSV databases (foundations, components, patterns, platforms)
tests/                — 146 tests
showcase/demos/       — 12 HTML showcase demos
index.html            — Landing page (GitHub Pages)
```

---

## Contributing

```bash
git clone https://github.com/JubaKitiashvili/onemore.git
cd onemore
python3 -m pytest tests/ -v  # 146 tests should pass
```

---

## License

MIT

---

Built with ◆ by [Juba Kitiashvili](https://github.com/JubaKitiashvili)
