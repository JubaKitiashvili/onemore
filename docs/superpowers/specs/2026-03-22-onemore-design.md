# OneMore — Apple HIG Design Intelligence Skill

> "One more thing..." — Steve Jobs

## Overview

OneMore is an Apple Human Interface Guidelines (HIG) design intelligence skill for Claude Code and other AI coding agents. It ensures every generated UI — across all platforms and tech stacks — looks and feels like an Apple product.

**Base**: Independent project, structurally inspired by ui-ux-pro-max's CSV database + Python CLI architecture. No upstream connection — standalone repo.

**Goal**: When a user requests UI creation with OneMore, the result should be indistinguishable from an Apple product — correct spacing, typography, animations, iconography, controls, and interaction patterns.

## Core Principles (Apple HIG Philosophy)

1. **Clarity** — Text is legible, icons are precise, adornments are subtle and appropriate
2. **Deference** — UI helps people understand and interact with content, never competes with it
3. **Depth** — Visual layers and realistic motion convey hierarchy and facilitate understanding
4. **Consistency** — Apps meet expectations through familiar standards and paradigms
5. **Direct Manipulation** — Direct engagement with on-screen content, immediate visible results
6. **Feedback** — Perceptible responses to every action confirm activity and show results

## Architecture

### Project Structure

```
~/Desktop/Projects/onemore/
├── SKILL.md                    — Main skill file (Claude Code entry point)
├── scripts/
│   ├── search.py               — CLI entry point
│   ├── core.py                 — Search engine (CSV-based, keyword matching)
│   └── design_system.py        — Design system generator with Apple reasoning
├── data/
│   ├── foundations/
│   │   ├── spacing.csv         — Apple spacing scale (4pt base grid)
│   │   ├── colors.csv          — Apple system colors + semantic colors + dynamic colors
│   │   ├── typography.csv      — SF Pro, SF Mono, SF Compact, New York, system type scale
│   │   ├── elevation.csv       — Shadows, blur, materials, vibrancy levels
│   │   └── corners.csv         — Continuous corner radius system (borderCurve: continuous)
│   ├── components/
│   │   ├── navigation.csv      — Navigation bars, tab bars, toolbars, sidebars
│   │   ├── controls.csv        — Buttons (filled/tinted/bordered/plain), toggles, sliders, steppers, pickers
│   │   ├── content.csv         — Lists (inset grouped, sidebar), cells, cards, grids
│   │   ├── feedback.csv        — Alerts, action sheets, sheets (modal/formSheet/fullScreen), toasts, progress
│   │   └── input.csv           — Text fields, secure fields, search bars, forms
│   ├── patterns/
│   │   ├── animation.csv       — Spring physics, transitions, easing curves
│   │   ├── gestures.csv        — Swipe actions, pinch, long press, drag, rotation
│   │   ├── layout.csv          — Navigation patterns (stack/tab/split), hierarchy, safe areas
│   │   └── interaction.csv     — Haptic feedback, progressive disclosure, pull-to-refresh
│   ├── platforms/
│   │   ├── ios.csv             — iOS/iPadOS specific patterns and metrics
│   │   ├── macos.csv           — macOS patterns (menu bars, window chrome, inspectors)
│   │   ├── watchos.csv         — watchOS patterns (complications, Digital Crown)
│   │   ├── visionos.csv        — visionOS patterns (spatial UI) [EXPERIMENTAL]
│   │   └── web-apple.csv       — Apple aesthetic on web with font fallbacks (Inter/system-ui for SF Pro)
│   ├── stacks/                 — Implementation guides per stack (tiered rollout)
│   │   ├── swiftui.csv         — [Tier 1] SwiftUI views, modifiers, state, navigation
│   │   ├── react.csv           — [Tier 1] React with Apple aesthetic
│   │   ├── react-native.csv    — [Tier 1] React Native Apple-style components
│   │   ├── html-tailwind.csv   — [Tier 1] Tailwind CSS Apple design tokens
│   │   ├── flutter.csv         — [Tier 2] Flutter Cupertino widgets + custom
│   │   ├── nextjs.csv          — [Tier 2] Next.js with Apple aesthetic
│   │   ├── shadcn.csv          — [Tier 2] shadcn/ui customized for Apple style
│   │   ├── vue.csv             — [Tier 3] Vue with Apple aesthetic
│   │   ├── svelte.csv          — [Tier 3] Svelte with Apple aesthetic
│   │   ├── uikit.csv           — [Tier 3] UIKit patterns for legacy/hybrid apps
│   │   ├── nuxtjs.csv          — [Tier 3] Nuxt.js with Apple aesthetic
│   │   └── astro.csv           — [Tier 3] Astro with Apple aesthetic
│   ├── audit/
│   │   └── hig-checklist.csv   — HIG compliance checklist with per-rule descriptions
│   └── reasoning/
│       └── apple-reasoning.csv — Design system reasoning rules for Apple context
├── sync/
│   └── hig-changelog.md        — Manual changelog tracking Apple HIG updates by version/date
└── VERSION                     — Data version tracking (semver for CSV content updates)
```

**Stack Tiers** (implementation priority):
- **Tier 1** (launch): SwiftUI, React, React Native, HTML/Tailwind — covers Apple-native + most popular web/mobile
- **Tier 2** (fast follow): Flutter, Next.js, shadcn — high demand frameworks
- **Tier 3** (later): Vue, Svelte, UIKit, Nuxt, Astro — niche or legacy

**Out of scope**: Jetpack Compose (Material Design framework, Apple aesthetic would be awkward on Android), tvOS (may add later if needed).

### CSV Schemas

Each CSV category has a specific schema. Sample rows included for clarity.

**Foundations — spacing.csv**:
```csv
keyword,name,value_pt,value_px,usage,platform,priority
compact,xxs,2,2,Icon internal padding,all,medium
tight,xs,4,4,Between icon and label,all,high
small,sm,8,8,Between related elements,all,critical
medium,md,12,12,Between semi-related elements,all,high
default,base,16,16,Default padding/margin,all,critical
comfortable,lg,20,20,Section internal padding,all,medium
spacious,xl,24,24,Between sections,all,high
```

**Foundations — colors.csv**:
```csv
keyword,name,light_hex,dark_hex,elevated_dark_hex,usage,semantic_role,platform
blue,systemBlue,#007AFF,#0A84FF,#409CFF,Links and interactive,accent,all
green,systemGreen,#34C759,#30D158,#30DB5B,Success and confirmation,success,all
red,systemRed,#FF3B30,#FF453A,#FF6961,Errors and destructive,destructive,all
label,label,#000000,#FFFFFF,#FFFFFF,Primary text,text-primary,all
secondaryLabel,secondaryLabel,#3C3C4399,#EBEBF599,#EBEBF599,Secondary text,text-secondary,all
separator,separator,#3C3C4349,#54545899,#54545899,Divider lines,border,all
systemBackground,systemBackground,#FFFFFF,#000000,#1C1C1E,Page background,bg-primary,ios
```

**Components — controls.csv**:
```csv
keyword,component,variant,height_pt,corner_radius,font_weight,font_size,padding_h,states,platform,priority
button,Button,filled,50,12,semibold,17,20,default|pressed|disabled,all,critical
button,Button,tinted,50,12,semibold,17,20,default|pressed|disabled,all,high
button,Button,bordered,50,12,semibold,17,20,default|pressed|disabled,all,high
button,Button,plain,44,0,regular,17,0,default|pressed|disabled,all,medium
toggle,Toggle,default,31,16,regular,17,51,on|off|disabled,ios,critical
slider,Slider,continuous,28,0,n/a,n/a,0,normal|disabled,all,medium
stepper,Stepper,default,32,8,regular,17,0,normal|disabled,ios,medium
```

**Patterns — animation.csv**:
```csv
keyword,name,type,response,damping_fraction,blend_duration,usage,source,platform
default,default,spring,0.55,1.0,0,General purpose transitions,SwiftUI default,all
bouncy,bouncy,spring,0.5,0.7,0,Playful interactions,SwiftUI preset,all
snappy,snappy,spring,0.35,1.0,0,Quick response actions,SwiftUI preset,all
smooth,smooth,spring,0.5,1.0,0,Smooth transitions,SwiftUI preset,all
interactive,interactiveSpring,spring,0.15,0.86,0.25,Drag and gesture-driven,SwiftUI preset,all
keyboard,keyboard,spring,0.35,1.0,0,Keyboard show/hide,Observed behavior,ios
sheet,sheet,spring,0.45,0.9,0,Sheet presentation,Observed behavior,ios
```

> **Note on animation values**: SwiftUI spring presets (response, dampingFraction) are documented by Apple. Values marked "Observed behavior" are reverse-engineered approximations and should be validated against device behavior.

**Platforms — ios.csv**:
```csv
keyword,element,metric,value,unit,context,min_os,priority
navbar,NavigationBar,height,44,pt,inline title,14.0,critical
navbar,NavigationBar,height,96,pt,large title expanded,11.0,critical
tabbar,TabBar,height,49,pt,standard,7.0,critical
tabbar,TabBar,height,83,pt,with home indicator,11.0,critical
statusbar,StatusBar,height,54,pt,with dynamic island,16.0,high
safe-area,SafeArea,bottom,34,pt,devices with home indicator,11.0,critical
touch,TouchTarget,minimum,44,pt,all interactive elements,2.0,critical
```

**Stacks — react.csv** (sample):
```csv
keyword,pattern,implementation,anti_pattern,notes,priority
spacing,Use CSS custom properties for Apple spacing scale,"--spacing-xs: 4px; --spacing-sm: 8px; --spacing-md: 12px;",Using arbitrary px values or rem without mapping,Map to Apple 4pt grid,critical
corners,Use borderRadius with smooth corners,"border-radius: 12px; mask-image for continuous corners",Using default browser border-radius rendering,CSS cannot natively do continuous corners; use SVG mask or canvas for true squircles,high
typography,Use system font stack mimicking SF Pro,"font-family: -apple-system BlinkMacSystemFont 'Inter' system-ui sans-serif",Using Arial Helvetica or custom display fonts for body text,SF Pro only on Apple platforms; Inter is closest web fallback,critical
animation,Use spring physics via framer-motion,"<motion.div transition={{ type: 'spring' response: 0.5 dampingRatio: 0.8 }}>",Using CSS ease-in-out or linear transitions,Apple never uses linear easing for UI transitions,high
dark-mode,Support system color scheme with semantic tokens,"@media (prefers-color-scheme: dark) { --color-bg: #000; }",Hardcoding colors without dark mode variants,All Apple UIs support dark mode,critical
```

### Python CLI Tool

Three main scripts, adapted from ui-ux-pro-max's architecture:

**search.py** — Entry point:
```bash
# Generate Apple design system for a project
python3 scripts/search.py "health app dashboard" --design-system -p "HealthKit Pro"

# Search specific domain
python3 scripts/search.py "navigation" --domain components -n 10

# Get platform-specific guidelines
python3 scripts/search.py "sidebar" --platform macos

# Get stack-specific implementation
python3 scripts/search.py "tab bar" --stack swiftui

# Combined: platform + stack
python3 scripts/search.py "sidebar" --platform macos --stack swiftui
```

**Flag interaction model**:
- `--platform` filters rules from foundations/components/patterns CSVs by the `platform` column
- `--stack` searches the stack-specific implementation CSV
- When both are used, results are merged: platform rules first (what to do), then stack rules (how to implement)
- If `--platform` is omitted, defaults to `all` (cross-platform rules)
- If `--stack` is omitted, no stack-specific implementation guidance is shown

**core.py** — Search engine (adapted from ui-ux-pro-max's `core.py`):
- `CSV_CONFIG` dictionary defining search_cols and output_cols per CSV category
- CSV loading with caching
- Keyword matching with relevance scoring (score > 0 filter)
- Platform-aware filtering via `platform` column
- Result ranking by priority

**design_system.py** — Design system generator:
- Multi-domain parallel search (foundations + components + patterns)
- Apple-specific reasoning rules from `apple-reasoning.csv`
- Output: complete design system with Apple tokens, components, and patterns
- Persist mode: saves as `design-system/MASTER.md` + page overrides

**Error handling**:
- No results: "No matching guidelines found. Try broader keywords or check --domain options."
- Missing CSV: Warning + skip (graceful degradation, not crash)
- Invalid flag combination: Clear error message with valid options
- Python < 3.10: Exit with version requirement message
- Malformed CSV rows: Skip row with warning, continue processing

### SKILL.md Content (OneMore Entry Point)

The SKILL.md frontmatter and trigger description:

```yaml
---
name: onemore
description: "Apple HIG design intelligence. Generates Apple-quality UI across all platforms (iOS, macOS, watchOS, visionOS, web). Actions: design, build, create, implement, review, audit, fix, improve UI/UX code. Styles: Apple HIG, Cupertino, SF Pro, system colors, spring animations, materials, vibrancy. Projects: iOS app, macOS app, website, landing page, dashboard, mobile app, SwiftUI, React, React Native, Flutter. Elements: navigation bar, tab bar, toolbar, button, toggle, slider, picker, sheet, alert, list, card, search bar. Topics: spacing, typography, color system, dark mode, accessibility, dynamic type, haptics, gestures, continuous corners, SF Symbols."
---
```

**SKILL.md sections**:
1. Apple HIG Core Principles (6 principles, 1 line each)
2. Priority Rules Quick Reference:

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

3. Quick reference rules (most critical per category)
4. CLI usage workflow (Step 1-4 matching ui-ux-pro-max pattern)
5. Font licensing note: SF Pro/NY only on Apple platforms; use Inter/system-ui on web
6. Pre-delivery checklist (Apple-specific)
7. Anti-patterns table

**Pre-Delivery Checklist**:
- [ ] Uses Apple spacing scale (4pt grid), no arbitrary values
- [ ] Typography uses SF Pro (native) or Inter/system-ui (web) with correct scale
- [ ] All colors use semantic tokens that adapt to dark mode
- [ ] Continuous corners (borderCurve: continuous on native, squircle on web)
- [ ] Touch targets minimum 44pt
- [ ] Spring animations, no linear/ease-in-out for UI transitions
- [ ] Supports Dynamic Type / font scaling
- [ ] Dark mode tested and working
- [ ] No emoji icons — SF Symbols or Lucide/Heroicons
- [ ] Platform-appropriate navigation pattern (not iOS patterns on macOS)
- [ ] Accessibility: VoiceOver labels, 4.5:1 contrast, focus states
- [ ] Materials/vibrancy used where appropriate (sidebars, overlays)
- [ ] Safe areas respected (no content under home indicator/notch)

### Audit Mode

**Approach**: Checklist-based audit powered by the AI agent (not a standalone linter). The agent reads the code, compares against `hig-checklist.csv` rules, and produces a report.

**hig-checklist.csv schema**:
```csv
keyword,rule_id,category,description,check_instruction,severity,weight
spacing,SP-01,spacing,Uses Apple 4pt grid,Check if spacing values are multiples of 4,critical,5
spacing,SP-02,spacing,No arbitrary magic numbers,Check for hardcoded px values not in Apple scale,high,3
typography,TY-01,typography,Uses SF Pro or approved fallback,Check font-family declarations,critical,5
typography,TY-02,typography,Follows Apple type scale,Check font-size values match Apple scale,high,4
color,CL-01,color,Uses semantic color tokens,Check for hardcoded hex values vs semantic names,critical,5
color,CL-02,color,Supports dark mode,Check for dark mode color variants,critical,5
touch,TC-01,touch,44pt minimum touch targets,Check interactive element dimensions,critical,5
animation,AN-01,animation,Spring physics used,Check for linear/ease transitions on UI elements,medium,3
corners,CR-01,corners,Continuous corners,Check borderRadius usage with continuous curve,high,4
a11y,AX-01,accessibility,VoiceOver/aria labels,Check interactive elements for labels,critical,5
```

**Workflow**: User runs `onemore audit` → agent reads code files → checks each rule → produces scored report:
- Overall score (0-100) with grade
- Per-category breakdown
- Specific issues with suggestions

**Scoring weights**: Accessibility 25%, Spacing & Layout 20%, Typography 15%, Colors 15%, Components 15%, Animation 10%

This approach avoids building a complex AST parser — the AI agent IS the parser.

### HIG Update Tracking

**Approach**: Manual changelog with optional crawl-assisted discovery (no auto-apply).

**sync/hig-changelog.md** — Tracks Apple HIG changes:
```markdown
# HIG Changelog

## 2026-03-22 — Initial data (iOS 18, macOS 15, watchOS 11, visionOS 2)
- Baseline CSV data created from current Apple HIG documentation

## [Future entries added manually after WWDC or major OS releases]
```

**Optional discovery workflow**:
1. User runs `onemore sync` or agent uses firecrawl to check HIG pages
2. Agent generates diff report of what changed
3. Human reviews and approves CSV updates
4. VERSION file bumped

This avoids legal/technical risks of automated scraping with auto-apply. Human stays in the loop.

**VERSION file**: Simple semver (e.g., `1.0.0`) bumped when CSV content is updated. Allows tracking data freshness.

## Anti-Patterns (What OneMore Prevents)

| Anti-Pattern | OneMore Fix |
|---|---|
| Generic rounded corners (border-radius: 8px) | Continuous corners with platform-correct radii |
| System default fonts | SF Pro/NY with correct weight/size scale (Inter on web) |
| Random spacing | 4pt grid alignment |
| Flat, lifeless UI | Proper depth with materials, vibrancy, shadows |
| Jarring animations | Spring physics with Apple-tuned parameters |
| Missing haptics | Haptic feedback patterns for all interactions |
| Incorrect touch targets | 44pt minimum, proper hit testing |
| Non-semantic colors | Apple system colors that adapt to dark mode/accessibility |
| Desktop-first thinking | Platform-appropriate patterns (iOS != macOS != web) |
| SF Pro on web without license | Font fallback chain: -apple-system, BlinkMacSystemFont, Inter, system-ui |

## Differences from ui-ux-pro-max

| Aspect | ui-ux-pro-max | OneMore |
|---|---|---|
| Philosophy | Generic best practices, 67 styles | Apple HIG only, one coherent vision |
| Colors | 96 palettes for various industries | Apple system colors + semantic tokens |
| Typography | 57 font pairings | SF Pro family + New York, dynamic type |
| Components | Generic web components | Apple-native components (toggles, sheets, pickers) |
| Animation | Generic 150-300ms guidelines | Spring physics with Apple presets |
| Audit | Manual pre-delivery checklist | Agent-powered scoring with HIG compliance % |
| Platforms | Mostly web-focused | iOS, macOS, watchOS, visionOS, web |
| Update tracking | None | Versioned changelog with manual review |
| Font licensing | Not addressed | Clear fallback chain for non-Apple platforms |

## Success Criteria

A UI generated with OneMore should:
1. Score 90+ on its own HIG audit checklist
2. Use only Apple-documented spacing, typography, and color values
3. Use correct platform-specific patterns (not iOS patterns on macOS)
4. Have proper spring animations, not linear/ease transitions
5. Support dynamic type, dark mode, and accessibility out of the box
6. Use SF Symbols (native) or equivalent icon set (web), never emoji
7. Pass WCAG 2.1 AA accessibility requirements
