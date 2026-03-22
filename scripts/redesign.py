#!/usr/bin/env python3
"""OneMore Redesign Scanner — Apple HIG violation detection and AI-actionable reports."""
import json
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# File Detection
# ---------------------------------------------------------------------------

UI_FILE_EXTENSIONS = {
    ".tsx": "react",
    ".jsx": "react",
    ".vue": "vue",
    ".svelte": "svelte",
    ".swift": "swiftui",
    ".dart": "flutter",
    ".html": "html",
    ".css": "css",
    ".scss": "scss",
    ".ts": "react",
}

IGNORED_DIRS = {
    "node_modules", ".git", "__pycache__", "dist", "build",
    ".next", ".nuxt", "vendor", "Pods",
}


# ---------------------------------------------------------------------------
# Expo / React Native Project Context Detection
# ---------------------------------------------------------------------------

def detect_project_context(path) -> dict:
    """Detect if a project is Expo, React Native, or NativeWind.

    Walks up from *path* looking for app.json / app.config.js / app.config.ts
    that reference "expo", and inspects package.json for relevant dependencies.

    Returns:
        {
            "is_expo": bool,
            "is_react_native": bool,
            "has_nativewind": bool,
            "framework_override": "nativewind" | "react-native" | None,
        }
    """
    path = Path(path)

    is_expo = False
    is_react_native = False
    has_nativewind = False

    # Search current dir and up to 3 parent levels for Expo config files
    search_paths = [path] + list(path.parents)[:3]

    for search_dir in search_paths:
        for config_name in ("app.json", "app.config.js", "app.config.ts"):
            config_file = search_dir / config_name
            if config_file.exists():
                try:
                    content = config_file.read_text(errors="ignore")
                    if "expo" in content.lower():
                        is_expo = True
                except Exception:
                    pass

        pkg_file = search_dir / "package.json"
        if pkg_file.exists():
            try:
                content = pkg_file.read_text(errors="ignore")
                pkg = json.loads(content)
                all_deps = {}
                all_deps.update(pkg.get("dependencies", {}))
                all_deps.update(pkg.get("devDependencies", {}))
                all_deps.update(pkg.get("peerDependencies", {}))
                dep_str = " ".join(all_deps.keys()).lower()
                if "react-native" in dep_str:
                    is_react_native = True
                if "expo" in dep_str:
                    is_expo = True
                if "nativewind" in dep_str:
                    has_nativewind = True
            except Exception:
                pass
        # Stop climbing once we find a package.json
        if pkg_file.exists():
            break

    if has_nativewind:
        framework_override = "nativewind"
    elif is_expo or is_react_native:
        framework_override = "react-native"
    else:
        framework_override = None

    return {
        "is_expo": is_expo,
        "is_react_native": is_react_native,
        "has_nativewind": has_nativewind,
        "framework_override": framework_override,
    }

# ---------------------------------------------------------------------------
# HIG Violation Rules
# ---------------------------------------------------------------------------

HIG_RULES = [
    # ── Colors ──────────────────────────────────────────────────────────
    {
        "id": "COLOR-001",
        "category": "colors",
        "description": "Pure black text detected — Apple uses warm near-black, not pure black",
        "patterns": [
            r"""#000000""",
            r"""#000(?![\da-fA-F])""",
            r"""rgb\(\s*0\s*,\s*0\s*,\s*0\s*\)""",
            r"""\bcolor:\s*black\b""",
        ],
        "fix": "Use semantic label color: '#1d1d1f' on web, Color.label in SwiftUI, var(--apple-label) with CSS variables",
        "severity": "critical",
        "platforms": ["all"],
    },
    {
        "id": "COLOR-002",
        "category": "colors",
        "description": "Pure white background — Apple uses slightly warm off-white",
        "patterns": [
            r"""#ffffff""",
            r"""#fff(?![\da-fA-F])""",
            r"""rgb\(\s*255\s*,\s*255\s*,\s*255\s*\)""",
        ],
        "fix": "Use '#fbfbfd' on web, Color.systemBackground in SwiftUI",
        "severity": "high",
        "platforms": ["all"],
    },
    {
        "id": "COLOR-003",
        "category": "colors",
        "description": "Hardcoded hex color that should be a CSS variable / semantic token",
        "patterns": [
            r"""(?:color|background|background-color|border-color)\s*:\s*#[0-9a-fA-F]{3,8}\b""",
        ],
        "fix": "Use --apple-* CSS custom properties or semantic color tokens",
        "severity": "medium",
        "platforms": ["css", "scss", "html"],
    },
    {
        "id": "COLOR-004",
        "category": "colors",
        "description": "Non-Apple blue detected — Apple system blue is #007AFF",
        "patterns": [
            r"""#0000ff""",
            r"""\bdodgerblue\b""",
            r"""\bcornflowerblue\b""",
            r"""\broyalblue\b""",
        ],
        "fix": "Use Apple systemBlue: '#007AFF'",
        "severity": "high",
        "platforms": ["all"],
    },
    # ── Typography ──────────────────────────────────────────────────────
    {
        "id": "TYPO-001",
        "category": "typography",
        "description": "Non-Apple font stack — missing system font",
        "patterns": [
            r"""font-family\s*:\s*(?:['"]?Arial['"]?\s*,?\s*)?(?:['"]?Helvetica['"]?\s*,?\s*)?sans-serif""",
            r"""fontFamily\s*:\s*['"](?:Arial|Helvetica)['"]""",
        ],
        "fix": "Use font-family: -apple-system, BlinkMacSystemFont, 'Inter', system-ui, sans-serif",
        "severity": "high",
        "platforms": ["all"],
    },
    {
        "id": "TYPO-002",
        "category": "typography",
        "description": "Body text size not aligned with Apple type scale",
        "patterns": [
            r"""font-size\s*:\s*14px""",
            r"""font-size\s*:\s*15px""",
            r"""fontSize\s*:\s*14\b""",
            r"""fontSize\s*:\s*15\b""",
        ],
        "fix": "Apple body text is 17px (iOS) or 13px (macOS). Use 17px for mobile, 13px for desktop",
        "severity": "medium",
        "platforms": ["all"],
    },
    {
        "id": "TYPO-003",
        "category": "typography",
        "description": "Missing letter-spacing on large/headline text",
        "patterns": [
            r"""font-size\s*:\s*(?:2[4-9]|[3-9]\d|\d{3,})px(?!.*letter-spacing)""",
            r"""fontSize\s*:\s*(?:2[4-9]|[3-9]\d|\d{3,})\b(?!.*letterSpacing)""",
        ],
        "fix": "Apple uses tight tracking on headlines. Add letter-spacing: -0.02em for 24px+",
        "severity": "low",
        "platforms": ["all"],
    },
    # ── Spacing ─────────────────────────────────────────────────────────
    {
        "id": "SPACE-001",
        "category": "spacing",
        "description": "Odd spacing value — not aligned to 4pt grid",
        "patterns": [
            r"""(?:padding|margin|gap)\s*:\s*['"]?(?:5|7|9|11|13|15|17|19)px""",
            r"""(?:padding|margin|gap)\s*:\s*(?:5|7|9|11|13|15|17|19)\b""",
        ],
        "fix": "Align to 4pt grid: use 4/8/12/16/20/24/32/48 values",
        "severity": "medium",
        "platforms": ["all"],
    },
    {
        "id": "SPACE-002",
        "category": "spacing",
        "description": "Non-grid spacing value on padding/margin",
        "patterns": [
            r"""(?:padding|margin)\s*:\s*['"]?(?:3|5|6|7|9|10|11|13|14|15|17|18|19|21|22|23|25|26|27|28|29|30|31|33)px""",
        ],
        "fix": "Use 4pt-grid values: 4/8/12/16/20/24/32/48",
        "severity": "low",
        "platforms": ["all"],
    },
    {
        "id": "SPACE-003",
        "category": "spacing",
        "description": "Section padding less than 100px — Apple uses 100-120px section padding minimum",
        "patterns": [
            r"""padding:\s*\d{1,2}px\s+0""",
            r"""padding-top:\s*[4-9]\dpx""",
            r"""padding-bottom:\s*[4-9]\dpx""",
            r"""\bpy-[0-9]\b""",
            r"""\bpy-1[0-6]\b""",
        ],
        "fix": "Use minimum 100px (py-24 in Tailwind) vertical section padding for Apple-quality spacing",
        "severity": "medium",
        "platforms": ["all"],
    },
    # ── Corners ─────────────────────────────────────────────────────────
    {
        "id": "CORNER-001",
        "category": "corners",
        "description": "Button border-radius too small — Apple buttons use 12px",
        "patterns": [
            r"""border-radius\s*:\s*[1-9]px""",
            r"""borderRadius\s*:\s*[1-9]\b""",
        ],
        "fix": "Use borderRadius: 12 for buttons, 10/16/24 for other elements",
        "severity": "high",
        "platforms": ["all"],
    },
    {
        "id": "CORNER-002",
        "category": "corners",
        "description": "Missing borderCurve: 'continuous' — needed for Apple squircle shape",
        "patterns": [
            r"""borderRadius\s*:\s*\d+(?!.*borderCurve)""",
        ],
        "fix": "Add borderCurve: 'continuous' alongside borderRadius for Apple squircle corners",
        "severity": "medium",
        "platforms": ["react"],
    },
    {
        "id": "CORNER-003",
        "category": "corners",
        "description": "Generic border-radius on cards — use Apple-standard radii",
        "patterns": [
            r"""border-radius\s*:\s*(?:3|5|6|7|9|11|13|14|15|17|18|19)px""",
        ],
        "fix": "Use Apple corner radii: 10px (small), 16px (medium), 24px (large)",
        "severity": "low",
        "platforms": ["all"],
    },
    # ── Animation ───────────────────────────────────────────────────────
    {
        "id": "ANIM-001",
        "category": "animation",
        "description": "Non-Apple easing curve — avoid ease-in-out and linear",
        "patterns": [
            r"""transition.*ease-in-out""",
            r"""transition.*\blinear\b""",
            r"""animation.*ease-in-out""",
            r"""animation.*\blinear\b""",
        ],
        "fix": "Use cubic-bezier(0.25, 0.1, 0.25, 1) or spring animations",
        "severity": "medium",
        "platforms": ["all"],
    },
    {
        "id": "ANIM-002",
        "category": "animation",
        "description": "Transition duration outside Apple range (200-400ms)",
        "patterns": [
            r"""transition.*(?:0\.0[1-9]|0\.[0-1])s[^0-9]""",
            r"""transition.*(?:0\.[5-9]|[1-9]\.)s[^0-9]""",
            r"""transition.*(?:5\d\d|[6-9]\d\d|\d{4,})ms""",
            r"""transition.*\b[1-9]\dms\b""",
        ],
        "fix": "Apple uses 200-400ms transitions. Use 0.2s-0.4s or 200ms-400ms",
        "severity": "low",
        "platforms": ["all"],
    },
    {
        "id": "ANIM-003",
        "category": "animation",
        "description": "Missing prefers-reduced-motion — must respect user accessibility settings",
        "patterns": [
            r"""@keyframes\b""",
            r"""animation\s*:""",
            r"""animation-name\s*:""",
        ],
        "fix": "Add @media (prefers-reduced-motion: reduce) to disable or simplify animations",
        "severity": "high",
        "platforms": ["css", "scss", "html"],
    },
    # ── Touch Targets ───────────────────────────────────────────────────
    {
        "id": "TOUCH-001",
        "category": "touch",
        "description": "Touch target too small — minimum 44px per Apple HIG",
        "patterns": [
            r"""(?:height|min-height)\s*:\s*(?:[1-3]\d|4[0-3])px""",
            r"""(?:height|minHeight)\s*:\s*(?:[1-3]\d|4[0-3])\b""",
        ],
        "fix": "Set minimum height to 44px for all interactive elements",
        "severity": "critical",
        "platforms": ["all"],
    },
    {
        "id": "TOUCH-002",
        "category": "touch",
        "description": "Missing cursor: pointer on clickable element",
        "patterns": [
            r"""<button(?!.*cursor).*>""",
            r"""<a\s+(?!.*cursor).*>""",
        ],
        "fix": "Add cursor: pointer to all clickable elements",
        "severity": "low",
        "platforms": ["html", "vue", "svelte"],
    },
    # ── Icons ───────────────────────────────────────────────────────────
    {
        "id": "ICON-001",
        "category": "icons",
        "description": "Emoji used as UI icon — use SF Symbols or SVG icons instead",
        "patterns": [
            r"""[\U0001F50D\U0001F3E0\u2699\uFE0F\U0001F4E6\U0001F4AC\U0001F514\u2764\u2B50\U0001F4DD\U0001F527\u2795\u2796\u274C\u2714\u2716\U0001F504\U0001F5D1\u270F\U0001F4CB\U0001F4C4]""",
        ],
        "fix": "Replace emoji with SF Symbols (iOS/macOS) or SVG/icon-font icons",
        "severity": "medium",
        "platforms": ["all"],
    },
    # ── Dark Mode ───────────────────────────────────────────────────────
    {
        "id": "DARK-001",
        "category": "dark-mode",
        "description": "No prefers-color-scheme media query — dark mode not supported in CSS",
        "patterns": [],  # handled by file-level check
        "fix": "Add @media (prefers-color-scheme: dark) { ... } with dark mode colors",
        "severity": "high",
        "platforms": ["css", "scss"],
    },
    {
        "id": "DARK-002",
        "category": "dark-mode",
        "description": "No colorScheme / useColorScheme handling — dark mode not supported",
        "patterns": [],  # handled by file-level check
        "fix": "Import and use useColorScheme hook or Appearance API for dark mode support",
        "severity": "high",
        "platforms": ["react"],
    },
]

# ---------------------------------------------------------------------------
# Expo / React Native Specific Violation Rules
# ---------------------------------------------------------------------------

EXPO_RULES = [
    {
        "id": "EXPO-001",
        "category": "expo",
        "description": "Using TouchableOpacity instead of Pressable",
        "patterns": [
            r"""\bTouchableOpacity\b""",
        ],
        "fix": "Use Pressable, not TouchableOpacity",
        "severity": "high",
        "platforms": ["react-native", "nativewind"],
    },
    {
        "id": "EXPO-002",
        "category": "expo",
        "description": "Missing expo-haptics for interactive elements",
        "patterns": [
            r"""onPress\s*=\s*\{(?!.*[Hh]aptic)""",
        ],
        "fix": "Add haptic feedback with expo-haptics",
        "severity": "low",
        "platforms": ["react-native", "nativewind"],
    },
    {
        "id": "EXPO-003",
        "category": "expo",
        "description": "Using Image from react-native instead of expo-image",
        "patterns": [
            r"""import\s+.*\bImage\b.*from\s+['"]react-native['"]""",
            r"""from\s+['"]react-native['"]\s*.*\bImage\b""",
        ],
        "fix": "Use expo-image for better performance and blurhash",
        "severity": "high",
        "platforms": ["react-native", "nativewind"],
    },
    {
        "id": "EXPO-004",
        "category": "expo",
        "description": "Missing borderCurve: 'continuous' on rounded elements",
        "patterns": [
            r"""borderRadius\s*:\s*\d+(?!.*borderCurve)""",
        ],
        "fix": "Add borderCurve: 'continuous' for Apple squircle corners",
        "severity": "medium",
        "platforms": ["react-native", "nativewind"],
    },
]

# ---------------------------------------------------------------------------
# Scanner
# ---------------------------------------------------------------------------

def scan_directory(path, project_context=None):
    """Recursively find all UI files, returning (filepath, framework) tuples.

    When *project_context* is provided (from detect_project_context()), .tsx
    and .jsx files are re-tagged to "react-native" or "nativewind" so that
    Expo-specific rules are applied to them.
    """
    path = Path(path)
    results = []
    if not path.is_dir():
        return results

    framework_override = (project_context or {}).get("framework_override")

    for item in path.rglob("*"):
        # Skip ignored directories
        if any(part in IGNORED_DIRS for part in item.parts):
            continue
        if not item.is_file():
            continue
        ext = item.suffix.lower()
        if ext in UI_FILE_EXTENSIONS:
            framework = UI_FILE_EXTENSIONS[ext]
            # Override framework for .tsx/.jsx files in Expo/RN projects
            if framework_override and ext in (".tsx", ".jsx", ".ts"):
                framework = framework_override
            # For .ts files, only include if they contain JSX-like patterns
            if ext == ".ts":
                try:
                    content = item.read_text(errors="ignore")
                    if not re.search(r"<\w+[\s/>]|jsx|tsx", content):
                        continue
                except Exception:
                    continue
            results.append((item, framework))
    return results


def analyze_file(filepath, framework):
    """Analyze a single file for HIG violations."""
    filepath = Path(filepath)
    try:
        content = filepath.read_text(errors="ignore")
    except Exception:
        return []

    lines = content.split("\n")
    violations = []

    all_rules = list(HIG_RULES)
    if framework in ("react-native", "nativewind"):
        all_rules = all_rules + list(EXPO_RULES)

    for rule in all_rules:
        platforms = rule.get("platforms", ["all"])
        if "all" not in platforms and framework not in platforms:
            continue

        # Pattern-based checks
        for pattern in rule["patterns"]:
            for i, line in enumerate(lines, 1):
                if re.search(pattern, line, re.IGNORECASE):
                    violations.append({
                        "rule_id": rule["id"],
                        "category": rule["category"],
                        "severity": rule["severity"],
                        "description": rule["description"],
                        "file": str(filepath),
                        "line": i,
                        "current": line.strip(),
                        "fix": rule["fix"],
                    })

    # File-level checks (dark mode)
    if framework in ("css", "scss") and not re.search(r"prefers-color-scheme", content):
        # Only flag if file has actual styles
        if re.search(r"[{;]", content):
            dark_rule = next(r for r in HIG_RULES if r["id"] == "DARK-001")
            violations.append({
                "rule_id": "DARK-001",
                "category": dark_rule["category"],
                "severity": dark_rule["severity"],
                "description": dark_rule["description"],
                "file": str(filepath),
                "line": 1,
                "current": "(file-level: no dark mode support detected)",
                "fix": dark_rule["fix"],
            })

    if framework == "react" and not re.search(r"useColorScheme|colorScheme|Appearance|dark\s*mode", content, re.IGNORECASE):
        # Only flag if file has style-like content
        if re.search(r"style|color|background|theme", content, re.IGNORECASE):
            dark_rule = next(r for r in HIG_RULES if r["id"] == "DARK-002")
            violations.append({
                "rule_id": "DARK-002",
                "category": dark_rule["category"],
                "severity": dark_rule["severity"],
                "description": dark_rule["description"],
                "file": str(filepath),
                "line": 1,
                "current": "(file-level: no dark mode handling detected)",
                "fix": dark_rule["fix"],
            })

    return violations


def scan_project(path):
    """Full project scan — returns dict with files_scanned, violations, summary."""
    path = Path(path)
    project_context = detect_project_context(path)
    files = scan_directory(path, project_context=project_context)
    all_violations = []
    for filepath, framework in files:
        violations = analyze_file(filepath, framework)
        all_violations.extend(violations)
    result = {
        "files_scanned": len(files),
        "violations": all_violations,
        "summary": summarize(all_violations),
    }
    if project_context["framework_override"]:
        result["project_context"] = project_context
    return result


def summarize(violations):
    """Count violations by category and severity, compute HIG score."""
    by_category = {}
    by_severity = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    for v in violations:
        cat = v["category"]
        by_category[cat] = by_category.get(cat, 0) + 1
        by_severity[v["severity"]] += 1
    score = max(
        0,
        100
        - by_severity["critical"] * 5
        - by_severity["high"] * 3
        - by_severity["medium"] * 1
        - by_severity["low"] * 0.5,
    )
    return {
        "by_category": by_category,
        "by_severity": by_severity,
        "score": round(score),
    }


# ---------------------------------------------------------------------------
# Grade
# ---------------------------------------------------------------------------

def _grade(score):
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"


# ---------------------------------------------------------------------------
# Category Impact Descriptions
# ---------------------------------------------------------------------------

_CATEGORY_IMPACT = {
    "colors": "Replace hardcoded colors with Apple semantic tokens",
    "typography": "Update font stack and sizes to Apple type scale",
    "spacing": "Align to 4pt grid",
    "corners": "Use Apple corner radii",
    "animation": "Replace easing with Apple curves",
    "touch": "Increase touch targets to 44px minimum",
    "icons": "Replace emoji icons with SF Symbols or SVG",
    "dark-mode": "Add dark mode support",
}

# ---------------------------------------------------------------------------
# Report Generator
# ---------------------------------------------------------------------------

_SEVERITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3}
_SEVERITY_LABEL = {"critical": "CRITICAL", "high": "HIGH", "medium": "MEDIUM", "low": "LOW"}


def generate_report(scan_result, output_path=None):
    """Generate an AI-actionable redesign report in markdown format.

    Returns the report string. If *output_path* is given, also writes to disk.
    """
    violations = scan_result["violations"]
    summary = scan_result["summary"]
    files_scanned = scan_result["files_scanned"]
    score = summary["score"]
    grade = _grade(score)
    total = len(violations)
    sev = summary["by_severity"]

    lines = []
    lines.append("# OneMore Redesign Report [BETA]")
    lines.append("")
    lines.append(f"**Files scanned:** {files_scanned}")
    lines.append(f"**HIG Score:** {score}/100 (Grade: {grade})")
    lines.append(
        f"**Violations:** {total} total "
        f"({sev['critical']} critical, {sev['high']} high, "
        f"{sev['medium']} medium, {sev['low']} low)"
    )
    lines.append("")

    # ── Summary table ───────────────────────────────────────────────────
    lines.append("## Summary")
    lines.append("")
    if summary["by_category"]:
        lines.append("| Category | Violations | Impact |")
        lines.append("|----------|-----------|--------|")
        for cat, count in sorted(summary["by_category"].items(), key=lambda x: -x[1]):
            impact = _CATEGORY_IMPACT.get(cat, "Review and fix")
            lines.append(f"| {cat.replace('-', ' ').title()} | {count} | {impact} |")
        lines.append("")
    else:
        lines.append("No violations found. Your project is HIG-compliant!")
        lines.append("")

    # ── Violations by file ──────────────────────────────────────────────
    if violations:
        lines.append("## Violations by File")
        lines.append("")

        # Group by file
        by_file = {}
        for v in violations:
            by_file.setdefault(v["file"], []).append(v)

        for filepath in sorted(by_file):
            lines.append(f"### {filepath}")
            lines.append("")
            file_violations = sorted(
                by_file[filepath],
                key=lambda v: (_SEVERITY_ORDER.get(v["severity"], 9), v["line"]),
            )
            for v in file_violations:
                label = _SEVERITY_LABEL.get(v["severity"], v["severity"].upper())
                lines.append(f"**[{label}] {v['rule_id']}** (line {v['line']})")
                lines.append("```")
                lines.append(f"Current:  {v['current']}")
                lines.append(f"Fix:      {v['fix']}")
                lines.append(f"Reason:   {v['description']}")
                lines.append("```")
                lines.append("")

    # ── Quick fix guide ─────────────────────────────────────────────────
    lines.append("## Quick Fix Guide")
    lines.append("")
    lines.append("To apply these changes, ask your AI agent:")
    lines.append('"Read the redesign report at ./redesign-report.md and apply all fixes"')
    lines.append("")
    lines.append("---")
    lines.append("*Generated by OneMore [BETA] — Apple HIG Design Intelligence*")
    lines.append("")

    report = "\n".join(lines)

    if output_path:
        Path(output_path).write_text(report, encoding="utf-8")

    return report


# ---------------------------------------------------------------------------
# CLI Entry Point
# ---------------------------------------------------------------------------

def cli_main(args=None):
    """Handle `onemore redesign <path> [options]`."""
    import argparse

    parser = argparse.ArgumentParser(
        prog="onemore redesign",
        description="Scan a project for Apple HIG violations and generate a redesign report.",
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Directory to scan (default: current directory)",
    )
    parser.add_argument(
        "--output", "-o",
        metavar="FILE",
        help="Output file path (default: redesign-report.md in scanned directory)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="json_output",
        help="Output as JSON instead of markdown",
    )

    parsed = parser.parse_args(args)
    scan_path = Path(parsed.path).resolve()

    if not scan_path.is_dir():
        print(f"Error: '{scan_path}' is not a directory.", file=sys.stderr)
        return 1

    result = scan_project(scan_path)

    if parsed.json_output:
        print(json.dumps(result, indent=2, default=str))
    else:
        output_path = parsed.output
        if not output_path:
            output_path = scan_path / "redesign-report.md"
        report = generate_report(result, output_path=output_path)
        print(report)
        print(f"\nReport saved to {output_path}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(cli_main())
