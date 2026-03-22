# OneMore Multi-Platform Distribution Design

## Overview

Make OneMore available on every AI coding platform: Claude Code, Cursor, Windsurf, GitHub Copilot, Codex, Antigravity, Kiro, Qoder, Gemini CLI, Cline, Roo Code.

**Approach**: Single source of truth (SKILL.md) + auto-generated platform-specific configs + `onemore init --ai <platform>` CLI command for one-command setup.

## Architecture

### Single Source → Multi-Platform Transform

```
SKILL.md (source of truth)
    ↓ onemore init --ai <platform>
    ├── Claude Code  → ~/.claude/skills/onemore/SKILL.md (symlink)
    ├── Cursor       → .cursor/rules/onemore.mdc
    ├── Windsurf     → .windsurf/rules/onemore.md
    ├── Copilot      → .github/copilot-instructions.md (append)
    ├── Codex        → ~/.codex/skills/onemore/SKILL.md
    ├── Antigravity  → plugin format
    ├── Kiro         → .kiro/rules/onemore.md
    ├── Qoder        → ~/.qoder/skills/onemore/SKILL.md
    ├── Gemini CLI   → GEMINI.md (append)
    ├── Cline        → .clinerules/onemore.md
    └── Roo Code     → .roo/rules/onemore.md
```

### Platform Config Formats

Each platform has slightly different requirements:

| Platform | File Location | Format | Scope |
|---|---|---|---|
| Claude Code | ~/.claude/skills/onemore/SKILL.md | YAML frontmatter + Markdown | Global |
| Cursor | .cursor/rules/onemore.mdc | Markdown with frontmatter | Project |
| Windsurf | .windsurf/rules/onemore.md | Markdown | Project |
| GitHub Copilot | .github/copilot-instructions.md | Markdown | Project |
| Codex | ~/.codex/skills/onemore/SKILL.md | Markdown | Global |
| Gemini CLI | GEMINI.md | Markdown | Project |
| Cline | .clinerules/onemore.md | Markdown | Project |
| Roo Code | .roo/rules/onemore.md | Markdown | Project |
| Kiro | .kiro/rules/onemore.md | Markdown | Project |
| Antigravity | Plugin directory | Markdown + config | Global |
| Qoder | ~/.qoder/skills/onemore/ | Markdown | Global |

### Content Transformation

The core content is identical across platforms — Apple HIG rules don't change. But the format and CLI references differ:

**Global installs** (Claude Code, Codex, Qoder, Antigravity): Full SKILL.md with CLI workflow referencing the absolute path to scripts.

**Project installs** (Cursor, Windsurf, Copilot, Gemini, Cline, Roo, Kiro): Condensed rules + inline guidelines (no CLI dependency, since project-level rules can't rely on global scripts). These include:
- Apple HIG principles
- Priority rules quick reference
- Key rules per category (inline, no CLI)
- Pre-delivery checklist
- Anti-patterns table

### CLI Command: `onemore init`

Added to `scripts/search.py`:

```bash
# Install globally for Claude Code
onemore init --ai claude-code

# Add to current project for Cursor
onemore init --ai cursor

# Add to current project for multiple platforms
onemore init --ai cursor,windsurf,copilot

# List available platforms
onemore init --list

# Install for all supported platforms (project-level)
onemore init --ai all
```

**Behavior**:
- `claude-code`: Creates symlink `~/.claude/skills/onemore/` → project dir
- `codex`: Copies SKILL.md to `~/.codex/skills/onemore/`
- `qoder`: Copies SKILL.md to `~/.qoder/skills/onemore/`
- `cursor`: Creates `.cursor/rules/onemore.mdc` with condensed rules
- `windsurf`: Creates `.windsurf/rules/onemore.md`
- `copilot`: Creates/appends to `.github/copilot-instructions.md`
- `gemini`: Creates/appends to `GEMINI.md`
- `cline`: Creates `.clinerules/onemore.md`
- `roo`: Creates `.roo/rules/onemore.md`
- `kiro`: Creates `.kiro/rules/onemore.md`
- `antigravity`: Creates plugin config in Antigravity format

### Project Structure (New Files)

```
~/Desktop/Projects/onemore/
├── ... (existing)
├── scripts/
│   ├── search.py          — (modify: add init subcommand)
│   └── platforms.py       — (new: platform init logic + content transforms)
├── templates/
│   ├── project-rules.md   — Condensed rules template for project-level installs
│   ├── cursor.mdc         — Cursor-specific frontmatter wrapper
│   └── copilot-header.md  — Copilot append header
└── tests/
    └── test_platforms.py  — Tests for platform init
```

### templates/project-rules.md

Condensed version of SKILL.md for project-level installs (~80 lines):
- Apple HIG principles (6 lines)
- Priority rules table
- Key rules inline (spacing, typography, colors, touch targets, animation, corners)
- Pre-delivery checklist
- Anti-patterns table
- Note: "For full search capabilities, install OneMore CLI: pip install onemore"

### scripts/platforms.py

```python
PLATFORMS = {
    "claude-code": {"type": "global", "path": "~/.claude/skills/onemore"},
    "codex": {"type": "global", "path": "~/.codex/skills/onemore"},
    "qoder": {"type": "global", "path": "~/.qoder/skills/onemore"},
    "cursor": {"type": "project", "path": ".cursor/rules/onemore.mdc"},
    "windsurf": {"type": "project", "path": ".windsurf/rules/onemore.md"},
    "copilot": {"type": "project", "path": ".github/copilot-instructions.md", "mode": "append"},
    "gemini": {"type": "project", "path": "GEMINI.md", "mode": "append"},
    "cline": {"type": "project", "path": ".clinerules/onemore.md"},
    "roo": {"type": "project", "path": ".roo/rules/onemore.md"},
    "kiro": {"type": "project", "path": ".kiro/rules/onemore.md"},
    "antigravity": {"type": "global", "path": "~/.antigravity/plugins/onemore"},
}
```

Functions:
- `init_platform(platform)` — route to correct installer
- `init_global(platform, config)` — symlink or copy SKILL.md + scripts
- `init_project(platform, config)` — generate condensed rules file
- `generate_project_rules()` — transform SKILL.md → condensed project rules
- `list_platforms()` — show available platforms with status (installed/not)

## Success Criteria

1. `onemore init --ai cursor` creates working Cursor rules in < 2 seconds
2. `onemore init --ai all` sets up all project-level platforms at once
3. Every platform gets Apple HIG rules that actually work in that context
4. Global installs include full CLI capabilities
5. Project installs work standalone (no CLI dependency)
6. `onemore init --list` shows clear status of what's installed
