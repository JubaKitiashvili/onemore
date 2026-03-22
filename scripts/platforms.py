#!/usr/bin/env python3
"""OneMore Multi-Platform Distribution"""

import os
import shutil
from pathlib import Path

PROJECT_DIR = Path(__file__).parent.parent

PLATFORMS = {
    "claude-code": {
        "type": "global", "path": "~/.claude/skills/onemore", "name": "Claude Code",
        "detect": {"dirs": ["~/.claude"], "commands": ["claude"]}
    },
    "codex": {
        "type": "global", "path": "~/.codex/skills/onemore", "name": "Codex",
        "detect": {"dirs": ["~/.codex"], "commands": ["codex"]}
    },
    "qoder": {
        "type": "global", "path": "~/.qoder/skills/onemore", "name": "Qoder",
        "detect": {"dirs": ["~/.qoder"], "commands": ["qoder"]}
    },
    "antigravity": {
        "type": "global", "path": "~/.antigravity/plugins/onemore", "name": "Antigravity",
        "detect": {"dirs": ["~/.antigravity"], "commands": ["antigravity"]}
    },
    "cursor": {
        "type": "project", "path": ".cursor/rules/onemore.mdc", "name": "Cursor",
        "detect": {"project_dirs": [".cursor"], "commands": ["cursor"]}
    },
    "windsurf": {
        "type": "project", "path": ".windsurf/rules/onemore.md", "name": "Windsurf",
        "detect": {"project_dirs": [".windsurf"], "commands": ["windsurf"]}
    },
    "copilot": {
        "type": "project", "path": ".github/copilot-instructions.md", "name": "GitHub Copilot", "mode": "append",
        "detect": {"project_dirs": [".github"], "commands": ["gh"]}
    },
    "gemini": {
        "type": "project", "path": "GEMINI.md", "name": "Gemini CLI", "mode": "append",
        "detect": {"dirs": [], "commands": ["gemini"]}
    },
    "cline": {
        "type": "project", "path": ".clinerules/onemore.md", "name": "Cline",
        "detect": {"project_dirs": [".clinerules"], "commands": []}
    },
    "roo": {
        "type": "project", "path": ".roo/rules/onemore.md", "name": "Roo Code",
        "detect": {"project_dirs": [".roo"], "commands": []}
    },
    "kiro": {
        "type": "project", "path": ".kiro/rules/onemore.md", "name": "Kiro",
        "detect": {"project_dirs": [".kiro"], "commands": ["kiro"]}
    },
}

def generate_project_rules():
    """Generate condensed Apple HIG rules for project-level installs."""
    return '''# OneMore — Apple HIG Design Rules

> Apply these rules when building UI. Every element should look like an Apple product.

## Core Principles
1. **Clarity** — Legible text, precise icons, subtle adornments
2. **Deference** — UI serves content, never competes
3. **Depth** — Visual layers and motion convey hierarchy
4. **Consistency** — Familiar standards and paradigms
5. **Direct Manipulation** — Immediate visible results
6. **Feedback** — Perceptible response to every action

## Priority Rules

| # | Category | Key Rule |
|---|----------|----------|
| 1 | Accessibility | 4.5:1 contrast, VoiceOver/aria labels, Dynamic Type |
| 2 | Touch Targets | 44pt min (iOS), 60pt (visionOS), 20pt (macOS) |
| 3 | Typography | SF Pro (native) or Inter/system-ui (web). Body: 17pt iOS, 13pt macOS |
| 4 | Colors | Semantic tokens only. Support dark mode. Never hardcode hex |
| 5 | Spacing | 4pt grid: 4/8/12/16/20/24/32/48 |
| 6 | Components | Native controls. Continuous corners (borderCurve: continuous) |
| 7 | Animation | Spring physics only. Never linear/ease for UI transitions |
| 8 | Platform | iOS != macOS != visionOS. Use platform-appropriate patterns |

## Apple Color System
- Text: semantic `label` color (#1d1d1f on web, NOT pure black)
- Background: semantic `systemBackground` (#fbfbfd on web, NOT pure white)
- Accent: `systemBlue` #007AFF (light) / #0A84FF (dark)
- Destructive: `systemRed` #FF3B30 / #FF453A
- Success: `systemGreen` #34C759 / #30D158
- Grays: systemGray through systemGray6 (6 levels, different light/dark)

## Apple Typography Scale (iOS)
| Style | Size | Weight |
|-------|------|--------|
| largeTitle | 34pt | Regular |
| title1 | 28pt | Regular |
| title2 | 22pt | Regular |
| headline | 17pt | Semibold |
| body | 17pt | Regular |
| callout | 16pt | Regular |
| subheadline | 15pt | Regular |
| footnote | 13pt | Regular |
| caption1 | 12pt | Regular |

## Apple Spacing Scale
4 → 8 → 12 → 16 → 20 → 24 → 32 → 40 → 48 (pt)

## Spring Animation Presets
| Preset | Response | Damping | Use |
|--------|----------|---------|-----|
| smooth | 0.5 | 1.0 | General transitions |
| snappy | 0.35 | 1.0 | Quick actions |
| bouncy | 0.5 | 0.7 | Playful interactions |
| interactive | 0.15 | 0.86 | Gesture-driven |

## Web Font Stack
```css
font-family: -apple-system, BlinkMacSystemFont, "Inter", system-ui, sans-serif;
```
SF Pro only on Apple platforms. Inter is the closest web fallback.

## Pre-Delivery Checklist
- [ ] 4pt grid spacing, no arbitrary values
- [ ] SF Pro (native) or Inter/system-ui (web) typography
- [ ] Semantic color tokens, dark mode working
- [ ] Continuous corners (not standard border-radius)
- [ ] Touch targets >= 44pt
- [ ] Spring animations, no linear/ease
- [ ] Dynamic Type / font scaling
- [ ] No emoji icons — SF Symbols or Lucide
- [ ] Platform-appropriate navigation
- [ ] VoiceOver/aria labels, 4.5:1 contrast
- [ ] Safe areas respected

## Anti-Patterns
| Don\'t | Do |
|--------|-----|
| border-radius: 8px | Continuous corners, correct radii (12pt buttons, 16pt cards) |
| Arial/Helvetica | SF Pro (native), Inter (web) |
| Random spacing | 4pt grid |
| Flat UI | Materials, vibrancy, shadows |
| ease-in-out | Spring physics |
| #000000 text | Semantic label color |
| Emoji icons | SF Symbols or SVG icon set |

---
*Generated by [OneMore](https://github.com/onemore) — Apple HIG Design Intelligence*
'''


def init_platform(platform_name, project_dir=None):
    """Initialize OneMore for a specific platform."""
    if platform_name not in PLATFORMS:
        return {"error": f"Unknown platform: {platform_name}", "available": list(PLATFORMS.keys())}

    config = PLATFORMS[platform_name]

    if config["type"] == "global":
        return _init_global(platform_name, config)
    else:
        return _init_project(platform_name, config, project_dir or Path.cwd())


def _init_global(platform_name, config):
    """Install OneMore globally for a platform (symlink or copy)."""
    target = Path(config["path"]).expanduser()
    target.parent.mkdir(parents=True, exist_ok=True)

    if target.exists() or target.is_symlink():
        return {"status": "already_installed", "platform": config["name"], "path": str(target)}

    # Symlink the entire project directory
    os.symlink(str(PROJECT_DIR), str(target))
    return {"status": "installed", "platform": config["name"], "path": str(target), "method": "symlink"}


def _init_project(platform_name, config, project_dir):
    """Install OneMore rules into a project directory."""
    target = Path(project_dir) / config["path"]
    target.parent.mkdir(parents=True, exist_ok=True)

    rules = generate_project_rules()

    # Cursor needs frontmatter
    if platform_name == "cursor":
        content = f"---\ndescription: Apple HIG design rules - apply when building UI\nglobs: \"**/*.{{tsx,jsx,vue,svelte,swift,html,css,scss}}\"\nalwaysApply: false\n---\n\n{rules}"
    elif config.get("mode") == "append":
        # Append mode: add to existing file
        header = "\n\n<!-- OneMore: Apple HIG Design Rules -->\n"
        footer = "\n<!-- /OneMore -->\n"
        if target.exists():
            existing = target.read_text()
            if "OneMore" in existing:
                return {"status": "already_installed", "platform": config["name"], "path": str(target)}
            content = existing + header + rules + footer
        else:
            content = header.lstrip() + rules + footer
    else:
        content = rules

    target.write_text(content)
    return {"status": "installed", "platform": config["name"], "path": str(target)}


def detect_platforms(project_dir=None):
    """Auto-detect which AI platforms are installed.

    Detection strategy:
    - Global platforms: check if config dir exists in home (~/.claude, ~/.codex, etc) OR command in PATH
    - Project platforms: check if project dir exists (.cursor/, .windsurf/, etc) OR command in PATH

    Returns list of dicts with platform name, detected (bool), and reason.
    """
    project_dir = Path(project_dir) if project_dir else Path.cwd()
    results = []

    for name, config in PLATFORMS.items():
        detect = config.get("detect", {})
        detected = False
        reason = ""

        # Check global dirs (home directory)
        for d in detect.get("dirs", []):
            expanded = Path(d).expanduser()
            if expanded.exists():
                detected = True
                reason = f"found {d}"
                break

        # Check project dirs (current project)
        if not detected:
            for d in detect.get("project_dirs", []):
                if (project_dir / d).exists():
                    detected = True
                    reason = f"found {d}/ in project"
                    break

        # Check commands in PATH
        if not detected:
            for cmd in detect.get("commands", []):
                if shutil.which(cmd):
                    detected = True
                    reason = f"'{cmd}' command found"
                    break

        # Check if OneMore already installed for this platform
        if config["type"] == "global":
            install_path = Path(config["path"]).expanduser()
        else:
            install_path = project_dir / config["path"]
        already_installed = install_path.exists() or install_path.is_symlink()

        results.append({
            "platform": name,
            "name": config["name"],
            "type": config["type"],
            "detected": detected,
            "reason": reason,
            "already_installed": already_installed
        })

    return results


def auto_init(project_dir=None):
    """Detect platforms and install OneMore for all detected ones.

    Returns dict with detected platforms, installed platforms, and skipped (already installed).
    """
    detected = detect_platforms(project_dir)
    installed = []
    skipped = []
    not_detected = []

    for p in detected:
        if not p["detected"]:
            not_detected.append(p)
            continue
        if p["already_installed"]:
            skipped.append(p)
            continue
        result = init_platform(p["platform"], project_dir=project_dir)
        if result.get("status") == "installed":
            installed.append(p)
        else:
            skipped.append(p)

    return {
        "detected": [p for p in detected if p["detected"]],
        "installed": installed,
        "skipped": skipped,
        "not_detected": not_detected
    }


def list_platforms():
    """List all platforms with install status."""
    results = []
    for name, config in PLATFORMS.items():
        path = Path(config["path"]).expanduser() if config["type"] == "global" else Path(config["path"])
        installed = path.exists() or path.is_symlink()
        results.append({
            "platform": name,
            "name": config["name"],
            "type": config["type"],
            "path": config["path"],
            "installed": installed
        })
    return results
