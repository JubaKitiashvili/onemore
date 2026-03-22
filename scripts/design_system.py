"""Apple HIG design system generator — builds complete design systems from CSV data."""
import csv
import os
from pathlib import Path

from scripts.core import search, DATA_DIR


class DesignSystemGenerator:
    """Generates complete Apple HIG design systems for projects."""

    def __init__(self, project_name=None):
        self.project_name = project_name or "Untitled"
        self.reasoning_rules = self._load_reasoning()

    def _load_reasoning(self):
        """Load apple-reasoning.csv."""
        filepath = DATA_DIR / "reasoning" / "apple-reasoning.csv"
        if not filepath.exists():
            return []
        with open(filepath, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return list(reader)

    def _find_reasoning_rule(self, query):
        """Match query to Apple app category. 3-tier: exact, partial, keyword."""
        query_lower = query.lower()
        # Exact match on category
        for rule in self.reasoning_rules:
            if rule.get("category", "").lower() == query_lower:
                return rule
        # Partial match
        for rule in self.reasoning_rules:
            cat = rule.get("category", "").lower()
            if cat in query_lower or query_lower in cat:
                return rule
        # Keyword match
        best_rule = None
        best_score = 0
        for rule in self.reasoning_rules:
            row_text = " ".join(str(v) for v in rule.values()).lower()
            score = sum(1 for word in query_lower.split() if word in row_text)
            if score > best_score:
                best_score = score
                best_rule = rule
        return best_rule

    def _build_result(self, query, project_name=None):
        """Build the design system data structure from CSV searches."""
        name = project_name or self.project_name
        result = {
            "project_name": name,
            "query": query,
            "reasoning": None,
            "foundations": {},
            "components": {},
            "patterns": {},
            "checklist": [],
        }

        # 1. Find matching reasoning rule
        rule = self._find_reasoning_rule(query)
        if rule:
            result["reasoning"] = {
                "category": rule.get("category", ""),
                "navigation": rule.get("recommended_navigation", ""),
                "style": rule.get("style_priority", ""),
                "color_approach": rule.get("color_approach", ""),
                "typography_mood": rule.get("typography_mood", ""),
                "key_patterns": rule.get("key_patterns", ""),
                "anti_patterns": rule.get("anti_patterns", ""),
            }

        # 2. Search foundations
        result["foundations"]["colors"] = search(query, domain="colors", max_results=5)
        result["foundations"]["typography"] = search(query, domain="typography", max_results=3)
        result["foundations"]["spacing"] = search("default standard", domain="spacing", max_results=5)
        result["foundations"]["corners"] = search(query, domain="corners", max_results=3)
        result["foundations"]["elevation"] = search(query, domain="elevation", max_results=3)

        # 3. Search relevant components
        nav_query = rule.get("recommended_navigation", "tab navigation") if rule else "tab navigation"
        result["components"]["navigation"] = search(nav_query, domain="navigation", max_results=3)
        result["components"]["controls"] = search("button toggle", domain="controls", max_results=5)
        result["components"]["content"] = search("list cell card", domain="content", max_results=3)

        # 4. Search patterns
        result["patterns"]["animation"] = search("spring transition", domain="animation", max_results=3)
        result["patterns"]["interaction"] = search("haptic feedback", domain="interaction", max_results=3)

        # 5. Get audit checklist
        result["checklist"] = search("spacing typography color touch", domain="audit", max_results=10)

        return result

    def generate(self, query=None, project_name=None, fmt="ascii", persist=False, page=None):
        """Generate complete Apple HIG design system.

        Supports two calling conventions:
        - Direct: generate(query, project_name=...) -> returns result dict
        - CLI:    generate(fmt=..., persist=..., page=...) -> returns formatted string
        """
        # Use project_name from arg or fall back to instance attribute
        name = project_name or self.project_name
        # Use query if provided, otherwise use project_name as query
        q = query or name

        result = self._build_result(q, name)

        # If called with fmt/persist/page kwargs (CLI mode), return formatted string
        if query is None:
            # CLI mode: format and optionally persist
            if persist:
                path = self.persist(result, name, page=page)
                return f"Design system saved to: {path}"
            if fmt == "markdown":
                return self.format_markdown(result)
            return self.format_ascii(result)

        # Direct mode: return raw result dict
        return result

    def format_ascii(self, result):
        """Format as ASCII box for terminal display."""
        lines = []
        name = result["project_name"]
        lines.append(f"{'=' * 60}")
        lines.append(f"  OneMore Design System: {name}")
        lines.append(f"{'=' * 60}")

        # Reasoning
        r = result.get("reasoning")
        if r:
            lines.append(f"\n  App Category: {r['category']}")
            lines.append(f"  Navigation: {r['navigation']}")
            lines.append(f"  Style: {r['style']}")
            lines.append(f"  Color Approach: {r['color_approach']}")
            lines.append(f"  Typography: {r['typography_mood']}")
            if r["key_patterns"]:
                lines.append(f"  Key Patterns: {r['key_patterns']}")
            if r["anti_patterns"]:
                lines.append(f"  Anti-Patterns: {r['anti_patterns']}")

        # Foundations
        lines.append(f"\n  {chr(9472) * 56}")
        lines.append("  FOUNDATIONS")
        lines.append(f"  {chr(9472) * 56}")

        for category, items in result.get("foundations", {}).items():
            if items:
                lines.append(f"\n  {category.upper()}:")
                for item in items[:3]:
                    display = " | ".join(
                        f"{k}: {str(v)[:40]}" for k, v in item.items() if v and k != "platform"
                    )
                    lines.append(f"    {display}")

        # Components
        lines.append(f"\n  {chr(9472) * 56}")
        lines.append("  COMPONENTS")
        lines.append(f"  {chr(9472) * 56}")

        for category, items in result.get("components", {}).items():
            if items:
                lines.append(f"\n  {category.upper()}:")
                for item in items[:3]:
                    display = " | ".join(
                        f"{k}: {str(v)[:40]}"
                        for k, v in item.items()
                        if v and k not in ("platform", "priority")
                    )
                    lines.append(f"    {display}")

        # Patterns
        lines.append(f"\n  {chr(9472) * 56}")
        lines.append("  PATTERNS")
        lines.append(f"  {chr(9472) * 56}")

        for category, items in result.get("patterns", {}).items():
            if items:
                lines.append(f"\n  {category.upper()}:")
                for item in items[:3]:
                    display = " | ".join(
                        f"{k}: {str(v)[:40]}"
                        for k, v in item.items()
                        if v and k not in ("platform", "priority", "source")
                    )
                    lines.append(f"    {display}")

        # Checklist
        checklist = result.get("checklist", [])
        if checklist:
            lines.append(f"\n  {chr(9472) * 56}")
            lines.append("  HIG CHECKLIST")
            lines.append(f"  {chr(9472) * 56}")
            for item in checklist:
                rule_id = item.get("rule_id", "")
                desc = item.get("description", "")[:60]
                severity = item.get("severity", "")
                lines.append(f"    [{severity.upper()}] {rule_id}: {desc}")

        lines.append(f"\n{'=' * 60}")
        return "\n".join(lines)

    def format_markdown(self, result):
        """Format as Markdown document."""
        lines = []
        name = result["project_name"]
        lines.append(f"# {name} — OneMore Design System\n")

        r = result.get("reasoning")
        if r:
            lines.append(f"## App Category: {r['category']}\n")
            lines.append("| Property | Value |")
            lines.append("|---|---|")
            lines.append(f"| Navigation | {r['navigation']} |")
            lines.append(f"| Style | {r['style']} |")
            lines.append(f"| Color Approach | {r['color_approach']} |")
            lines.append(f"| Typography | {r['typography_mood']} |")
            if r["key_patterns"]:
                lines.append(f"| Key Patterns | {r['key_patterns']} |")
            if r["anti_patterns"]:
                lines.append(f"| Anti-Patterns | {r['anti_patterns']} |")
            lines.append("")

        lines.append("## Foundations\n")
        for category, items in result.get("foundations", {}).items():
            if items:
                lines.append(f"### {category.title()}\n")
                headers = list(items[0].keys())
                lines.append("| " + " | ".join(headers) + " |")
                lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
                for item in items:
                    row = " | ".join(str(item.get(h, ""))[:40] for h in headers)
                    lines.append(f"| {row} |")
                lines.append("")

        lines.append("## Components\n")
        for category, items in result.get("components", {}).items():
            if items:
                lines.append(f"### {category.title()}\n")
                headers = [k for k in items[0].keys() if k not in ("platform", "priority")]
                lines.append("| " + " | ".join(headers) + " |")
                lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
                for item in items:
                    row = " | ".join(str(item.get(h, ""))[:40] for h in headers)
                    lines.append(f"| {row} |")
                lines.append("")

        lines.append("## Patterns\n")
        for category, items in result.get("patterns", {}).items():
            if items:
                lines.append(f"### {category.title()}\n")
                headers = [k for k in items[0].keys() if k not in ("platform", "priority", "source")]
                lines.append("| " + " | ".join(headers) + " |")
                lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
                for item in items:
                    row = " | ".join(str(item.get(h, ""))[:40] for h in headers)
                    lines.append(f"| {row} |")
                lines.append("")

        checklist = result.get("checklist", [])
        if checklist:
            lines.append("## HIG Compliance Checklist\n")
            for item in checklist:
                rule_id = item.get("rule_id", "")
                desc = item.get("description", "")
                severity = item.get("severity", "")
                check = item.get("check_instruction", "")
                lines.append(f"- **[{severity.upper()}] {rule_id}**: {desc}")
                if check:
                    lines.append(f"  - Check: {check}")
            lines.append("")

        return "\n".join(lines)

    def persist(self, result, project_name, page=None):
        """Save design system to files."""
        output_dir = Path.cwd() / "design-system" / project_name.lower().replace(" ", "-")
        os.makedirs(output_dir / "pages", exist_ok=True)

        if page:
            filepath = output_dir / "pages" / f"{page.lower()}.md"
            with open(filepath, "w") as f:
                f.write(self.format_markdown(result))
            return str(filepath)
        else:
            filepath = output_dir / "MASTER.md"
            with open(filepath, "w") as f:
                f.write(self.format_markdown(result))
            return str(filepath)
