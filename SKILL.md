---
name: onemore
description: "Apple HIG design intelligence with 6 specialized agents. Use this skill whenever the user asks to build, create, design, or implement ANY user interface — landing pages, dashboards, mobile apps, web apps, components, or screens. Also use when they ask to fix, improve, or polish UI elements (buttons, cards, hover effects, animations, spacing, colors), review or audit design quality, check accessibility or WCAG compliance, analyze a reference video for motion patterns, or redesign anything visual. Triggers on: 'build me a landing page', 'make this look like apple.com', 'fix the animation', 'the hover feels jerky', 'check accessibility', 'WCAG audit', 'redesign this page', 'add scroll animations', 'dark mode', 'make it feel premium', reference video files (.mp4/.mov/.webm/.gif), and any mention of Apple HIG, spring physics, materials, vibrancy, SF Symbols, SwiftUI design, React Native UI, Tailwind styling, shadcn/ui theming, Framer Motion, GSAP, Three.js, or Lottie in a UI context. Do NOT trigger for backend code, database queries, API endpoints, CI/CD, deployment, testing frameworks, or non-visual programming tasks."
---

# OneMore — Apple HIG Design Intelligence

One more thing your design needs.

OneMore is an Apple HIG design intelligence system with specialized agents. You say `/onemore` — it figures out the rest. Creative vision, implementation, animation, accessibility review, and video motion analysis — each handled by a dedicated specialist loaded with the exact rules it needs.

---

## How It Works

When the user invokes `/onemore`, classify their intent and dispatch the right agent(s) automatically. The user never needs to know which agent runs — they just get Apple-quality results.

---

## Pipeline Status Tracking

IMPORTANT: Use TaskCreate for every pipeline step to show visual progress in the terminal. Each task MUST have an `activeForm` for the spinner text.

### Task Pattern for Each Route

For **Build from Scratch** (vision → build → review):
```
TaskCreate: "Classify intent"           activeForm: "Classifying intent"
TaskCreate: "Run Creative Director"     activeForm: "Running Creative Director"
TaskCreate: "Present brief for approval" activeForm: "Preparing creative brief"
TaskCreate: "Build with Apple HIG"      activeForm: "Building with Apple HIG rules"
TaskCreate: "Run quality review"        activeForm: "Running quality review"
```

For **Fix / Improve**:
```
TaskCreate: "Analyze existing code"     activeForm: "Analyzing existing code"
TaskCreate: "Apply HIG improvements"    activeForm: "Applying Apple HIG improvements"
```

For **Animate**:
```
TaskCreate: "Analyze motion requirements" activeForm: "Analyzing motion requirements"
TaskCreate: "Implement animations"        activeForm: "Implementing spring animations"
```

For **Review / Audit**:
```
TaskCreate: "Run HIG quality checklist"  activeForm: "Running 39-rule HIG checklist"
```

For **Accessibility**:
```
TaskCreate: "Run WCAG 2.2 audit"        activeForm: "Running WCAG 2.2 accessibility audit"
```

For **Video Reference**:
```
TaskCreate: "Analyze reference video"    activeForm: "Analyzing reference video"
TaskCreate: "Generate motion spec"       activeForm: "Generating motion specification"
TaskCreate: "Implement from spec"        activeForm: "Implementing from motion spec"
```

Mark each task `in_progress` before starting and `completed` when done. This creates the visual pipeline:
```
⠋ Classifying intent...
✓ Classify intent
⠋ Running Creative Director...
✓ Run Creative Director
⠋ Building with Apple HIG rules...
```

---

## Intent Classification & Routing

Read the user's message and match to ONE of these routes:

### Route 1: BUILD FROM SCRATCH
**Triggers:** "build", "create", "design", "make me", "landing page", "new website", "new app", "new dashboard"
**Also triggers on:** vague prompts like "SaaS analytics product" with no existing code referenced

```
Pipeline: onemore-vision → [user confirms brief] → onemore-build → onemore-review
```

**Steps:**
1. Dispatch `onemore-vision` agent — it produces a creative brief
2. Present the brief to the user, ask for confirmation
3. On confirmation, dispatch `onemore-build` agent with the brief
4. After build completes, dispatch `onemore-review` agent for quality gate
5. If review finds critical issues, fix them. Then ship.

### Route 2: FIX / IMPROVE / UPDATE
**Triggers:** "fix", "improve", "update", "change", "modify", "refactor", "adjust", "tweak"
**Context:** references existing code or components

```
Pipeline: onemore-build (directly)
```

**Steps:**
1. Dispatch `onemore-build` agent with the task
2. No vision needed — working on existing code
3. Optional: dispatch `onemore-review` if the change is significant

### Route 3: ANIMATE / MOTION
**Triggers:** "animate", "animation", "scroll", "transition", "hover effect", "parallax", "motion", "GSAP", "Framer Motion", "Three.js", "Lottie", "spring"

```
Pipeline: onemore-animate (specialist)
```

**Steps:**
1. Dispatch `onemore-animate` agent — it has deep animation knowledge
2. Focused context: only animation + craft physics rules loaded
3. Optional: dispatch `onemore-review` for quality check

### Route 4: REVIEW / AUDIT
**Triggers:** "review", "check", "audit", "quality", "is this good", "what's wrong"

```
Pipeline: onemore-review (directly)
```

**Steps:**
1. Dispatch `onemore-review` agent on the specified code
2. It runs all checklists and reports pass/fail with fixes

### Route 5: ACCESSIBILITY
**Triggers:** "accessibility", "a11y", "contrast", "screen reader", "keyboard", "WCAG", "focus", "reduced motion", "VoiceOver"

```
Pipeline: onemore-a11y (specialist)
```

**Steps:**
1. Dispatch `onemore-a11y` agent — WCAG 2.2 + Apple HIG accessibility specialist
2. It audits and auto-fixes what it can

### Route 6: VIDEO REFERENCE
**Triggers:** user attaches a video file (.mp4, .mov, .webm, .gif), or says "like this video", "match this animation", "reference video"

```
Pipeline: onemore-analyze → onemore-animate or onemore-build
```

**Steps:**
1. Check if user provided context (target platform, focus area). If only a video with no description — the analyze agent will ask one clarifying question before proceeding.
2. Dispatch `onemore-analyze` agent — uses Gemini API (if configured) or ffmpeg frame analysis
3. Produces implementation blueprint (blueprint.md + build-prompt.md)
4. Dispatch `onemore-animate` or `onemore-build` with build-prompt.md

**Best results when user provides context with video:**
- "Recreate this in React Native" → RN-focused analysis
- "I want these scroll animations on my Next.js site" → GSAP/Framer focus
- "Extract the card component design" → component-specific analysis

### Route 7: REDESIGN
**Triggers:** "redesign", "rethink", "reimagine", "redo", "start over"

```
Pipeline: onemore-vision → [user confirms brief] → onemore-build → onemore-review
```

Same as Route 1, but the vision agent also reads the existing code to understand what's being redesigned.

---

## Agent Dispatch Reference

| Agent | File | Knowledge | Role |
|-------|------|-----------|------|
| `onemore-vision` | `agents/onemore-vision.md` | vision-rules.md | Creative brief from vague prompts |
| `onemore-build` | `agents/onemore-build.md` | craft + design-system + animation rules | Implementation |
| `onemore-animate` | `agents/onemore-animate.md` | animation-rules + craft sections 1-3, 7 | Motion specialist |
| `onemore-review` | `agents/onemore-review.md` | All rules (checklists only) | Quality gate |
| `onemore-a11y` | `agents/onemore-a11y.md` | design-system section 9, craft section 12 | Accessibility audit |
| `onemore-analyze` | `agents/onemore-analyze.md` | Gemini API + OpenAI API (optional) + ffmpeg + motion analysis | Video reference → motion spec |

---

## Dispatching Agents

When dispatching an agent, use the Agent tool:
- Read the agent's `.md` file from the `agents/` directory
- Include the agent's instructions as the prompt
- Pass the user's request and any relevant context (brief, code paths, video path)
- Set appropriate tools for the agent

Example dispatch pattern:
```
1. Read agents/onemore-vision.md
2. Agent tool: prompt = [agent instructions] + [user request]
3. Wait for agent output
4. Present to user or chain to next agent
```

---

## Apple HIG Core Principles

These apply to ALL agents:

- **Clarity** — Text is legible, icons precise, adornments subtle
- **Deference** — UI helps people understand content without competing with it
- **Depth** — Visual layers and realistic motion convey hierarchy
- **Consistency** — Familiar standards let people transfer knowledge across apps
- **Direct Manipulation** — Interaction feels immediate, results visible
- **Feedback** — Every action has a response, status always communicated

---

## Priority Rules

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

## Quick Reference

- **Font stack (web):** `-apple-system, BlinkMacSystemFont, Inter, system-ui, sans-serif`
- **Easing:** `cubic-bezier(0.25, 0.1, 0.25, 1)` — Apple's standard (springs preferred)
- **Spacing:** 4pt grid — 4 / 8 / 12 / 16 / 20 / 24 / 32 / 48
- **Touch targets:** 44px minimum (60px visionOS)
- **Contrast:** 4.5:1 minimum for text
- **Content width:** 980px text, 1200px grids
- **Colors:** Never #000 or #fff — use #1d1d1f and #fbfbfd
- **Corners:** Continuous corners, concentric radii (inner = outer - padding)
- **Motion:** prefers-reduced-motion always respected
- **SF Pro:** Apple platforms only — never serve on web

---

## Anti-Patterns

| Anti-Pattern | Fix |
|---|---|
| `border-radius: 8px` | Continuous corners, platform-correct radii |
| Arial/Helvetica | SF Pro (native), Inter (web) |
| Random spacing | 4pt grid |
| Flat lifeless UI | Materials, vibrancy, depth layers |
| `ease-in-out` | Spring physics |
| `#000000` text | Semantic label color (`#1d1d1f`) |
| Emoji icons | SF Symbols or Lucide/Heroicons |
| Feature dump landing page | Story arc: hook → problem → reveal → wow → close |
| Same animation everywhere | Choreography: stagger, sequence, hierarchy |
