"""Tests for the redesign scanner (scripts/redesign.py)."""
import json
import subprocess
import sys
from pathlib import Path

import pytest

# Ensure project root is importable
_PROJECT_ROOT = Path(__file__).parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.redesign import (
    analyze_file,
    generate_report,
    scan_directory,
    scan_project,
    summarize,
)

CLI = Path(__file__).parent.parent / "scripts" / "search.py"
PYTHON = sys.executable


def run_cli(*args, **kwargs):
    """Run the CLI with given args."""
    return subprocess.run(
        [PYTHON, str(CLI)] + list(args),
        capture_output=True,
        text=True,
        **kwargs,
    )


# ---------------------------------------------------------------------------
# scan_project tests
# ---------------------------------------------------------------------------


class TestColorViolations:
    def test_finds_hex_black(self, tmp_path):
        f = tmp_path / "App.tsx"
        f.write_text("const style = { color: '#000000', background: '#ffffff' };")
        result = scan_project(tmp_path)
        assert result["violations"]
        rule_ids = {v["rule_id"] for v in result["violations"]}
        assert "COLOR-001" in rule_ids

    def test_finds_hex_white(self, tmp_path):
        f = tmp_path / "App.tsx"
        f.write_text("const style = { background: '#ffffff' };")
        result = scan_project(tmp_path)
        rule_ids = {v["rule_id"] for v in result["violations"]}
        assert "COLOR-002" in rule_ids

    def test_finds_short_hex_black(self, tmp_path):
        f = tmp_path / "App.tsx"
        f.write_text("const style = { color: '#000' };")
        result = scan_project(tmp_path)
        rule_ids = {v["rule_id"] for v in result["violations"]}
        assert "COLOR-001" in rule_ids

    def test_finds_rgb_black(self, tmp_path):
        f = tmp_path / "App.tsx"
        f.write_text("const c = 'rgb(0, 0, 0)';")
        result = scan_project(tmp_path)
        assert any(v["rule_id"] == "COLOR-001" for v in result["violations"])

    def test_finds_non_apple_blue(self, tmp_path):
        f = tmp_path / "styles.css"
        f.write_text("a { color: #0000ff; }")
        result = scan_project(tmp_path)
        assert any(v["rule_id"] == "COLOR-004" for v in result["violations"])


class TestTypographyViolations:
    def test_finds_arial_font(self, tmp_path):
        f = tmp_path / "styles.css"
        f.write_text("body { font-family: Arial, sans-serif; font-size: 14px; }")
        result = scan_project(tmp_path)
        assert any(v["category"] == "typography" for v in result["violations"])

    def test_finds_font_size_14(self, tmp_path):
        f = tmp_path / "styles.css"
        f.write_text("p { font-size: 14px; }")
        result = scan_project(tmp_path)
        assert any(v["rule_id"] == "TYPO-002" for v in result["violations"])


class TestSpacingViolations:
    def test_finds_odd_spacing(self, tmp_path):
        f = tmp_path / "Card.tsx"
        f.write_text("const style = { padding: '5px', margin: '7px' };")
        result = scan_project(tmp_path)
        assert any(v["category"] == "spacing" for v in result["violations"])

    def test_finds_5px_padding(self, tmp_path):
        f = tmp_path / "Card.tsx"
        f.write_text("const style = { padding: '5px' };")
        result = scan_project(tmp_path)
        assert any(v["rule_id"] == "SPACE-001" for v in result["violations"])


class TestCornerViolations:
    def test_finds_small_border_radius(self, tmp_path):
        f = tmp_path / "Button.tsx"
        f.write_text("const s = { borderRadius: 5 };")
        result = scan_project(tmp_path)
        assert any(v["category"] == "corners" for v in result["violations"])

    def test_finds_missing_border_curve(self, tmp_path):
        f = tmp_path / "Card.tsx"
        f.write_text("const s = { borderRadius: 12 };")
        result = scan_project(tmp_path)
        assert any(v["rule_id"] == "CORNER-002" for v in result["violations"])


class TestAnimationViolations:
    def test_finds_ease_in_out(self, tmp_path):
        f = tmp_path / "styles.css"
        f.write_text(".btn { transition: all 0.3s ease-in-out; }")
        result = scan_project(tmp_path)
        assert any(v["category"] == "animation" for v in result["violations"])

    def test_finds_missing_reduced_motion(self, tmp_path):
        f = tmp_path / "styles.css"
        f.write_text(".spinner { animation: spin 1s linear infinite; }")
        result = scan_project(tmp_path)
        assert any(v["rule_id"] == "ANIM-003" for v in result["violations"])


class TestIconViolations:
    def test_finds_emoji_icons(self, tmp_path):
        f = tmp_path / "Nav.tsx"
        f.write_text('return <button>\U0001F50D Search</button>;')
        result = scan_project(tmp_path)
        assert any(v["category"] == "icons" for v in result["violations"])


class TestDarkModeViolations:
    def test_css_missing_dark_mode(self, tmp_path):
        f = tmp_path / "styles.css"
        f.write_text("body { color: red; }")
        result = scan_project(tmp_path)
        assert any(v["rule_id"] == "DARK-001" for v in result["violations"])

    def test_react_missing_color_scheme(self, tmp_path):
        f = tmp_path / "App.tsx"
        f.write_text("const style = { color: 'red', background: 'blue' };")
        result = scan_project(tmp_path)
        assert any(v["rule_id"] == "DARK-002" for v in result["violations"])


class TestTouchViolations:
    def test_small_touch_target(self, tmp_path):
        f = tmp_path / "Button.tsx"
        f.write_text("const s = { height: 30 };")
        result = scan_project(tmp_path)
        assert any(v["rule_id"] == "TOUCH-001" for v in result["violations"])


# ---------------------------------------------------------------------------
# Directory scanning
# ---------------------------------------------------------------------------


class TestScanDirectory:
    def test_ignores_node_modules(self, tmp_path):
        nm = tmp_path / "node_modules" / "lib"
        nm.mkdir(parents=True)
        (nm / "index.js").write_text("color: '#000000';")
        result = scan_project(tmp_path)
        assert result["files_scanned"] == 0

    def test_ignores_dot_git(self, tmp_path):
        gd = tmp_path / ".git" / "hooks"
        gd.mkdir(parents=True)
        (gd / "pre-commit.tsx").write_text("color: black;")
        result = scan_project(tmp_path)
        assert result["files_scanned"] == 0

    def test_finds_multiple_file_types(self, tmp_path):
        (tmp_path / "App.tsx").write_text("hello")
        (tmp_path / "styles.css").write_text("body {}")
        (tmp_path / "page.vue").write_text("<template></template>")
        files = scan_directory(tmp_path)
        extensions = {f[0].suffix for f in files}
        assert ".tsx" in extensions
        assert ".css" in extensions
        assert ".vue" in extensions


# ---------------------------------------------------------------------------
# summarize()
# ---------------------------------------------------------------------------


class TestSummarize:
    def test_score_decreases_with_violations(self):
        violations = [
            {"category": "colors", "severity": "critical"},
            {"category": "colors", "severity": "high"},
            {"category": "spacing", "severity": "medium"},
        ]
        summary = summarize(violations)
        assert summary["score"] < 100
        assert summary["by_severity"]["critical"] == 1
        assert summary["by_severity"]["high"] == 1
        assert summary["by_severity"]["medium"] == 1

    def test_perfect_score_with_no_violations(self):
        summary = summarize([])
        assert summary["score"] == 100

    def test_score_never_negative(self):
        violations = [{"category": "x", "severity": "critical"} for _ in range(50)]
        summary = summarize(violations)
        assert summary["score"] == 0

    def test_by_category_counts(self):
        violations = [
            {"category": "colors", "severity": "low"},
            {"category": "colors", "severity": "low"},
            {"category": "spacing", "severity": "low"},
        ]
        summary = summarize(violations)
        assert summary["by_category"]["colors"] == 2
        assert summary["by_category"]["spacing"] == 1


# ---------------------------------------------------------------------------
# generate_report()
# ---------------------------------------------------------------------------


class TestGenerateReport:
    def test_report_contains_header(self, tmp_path):
        f = tmp_path / "App.tsx"
        f.write_text("const s = { color: '#000', borderRadius: 5 };")
        result = scan_project(tmp_path)
        report = generate_report(result)
        assert "OneMore Redesign Report" in report
        assert "BETA" in report

    def test_report_contains_violations(self, tmp_path):
        f = tmp_path / "App.tsx"
        f.write_text("const s = { color: '#000000' };")
        result = scan_project(tmp_path)
        report = generate_report(result)
        assert "COLOR" in report

    def test_report_saves_to_file(self, tmp_path):
        f = tmp_path / "App.tsx"
        f.write_text("const s = { color: '#000' };")
        result = scan_project(tmp_path)
        out = tmp_path / "report.md"
        generate_report(result, output_path=out)
        assert out.exists()
        content = out.read_text()
        assert "OneMore Redesign Report" in content

    def test_report_has_quick_fix_guide(self, tmp_path):
        f = tmp_path / "App.tsx"
        f.write_text("// clean file")
        result = scan_project(tmp_path)
        report = generate_report(result)
        assert "Quick Fix Guide" in report

    def test_report_grade(self, tmp_path):
        f = tmp_path / "App.tsx"
        f.write_text("// clean")
        result = scan_project(tmp_path)
        report = generate_report(result)
        assert "Grade: A" in report


# ---------------------------------------------------------------------------
# Empty / perfect projects
# ---------------------------------------------------------------------------


class TestEdgeCases:
    def test_empty_project(self, tmp_path):
        result = scan_project(tmp_path)
        assert result["files_scanned"] == 0
        assert len(result["violations"]) == 0

    def test_perfect_project(self, tmp_path):
        f = tmp_path / "App.tsx"
        f.write_text("// This file has no UI styling")
        result = scan_project(tmp_path)
        assert result["summary"]["score"] == 100

    def test_non_ui_files_ignored(self, tmp_path):
        (tmp_path / "README.md").write_text("# Hello")
        (tmp_path / "data.json").write_text("{}")
        (tmp_path / "script.py").write_text("print('hi')")
        result = scan_project(tmp_path)
        assert result["files_scanned"] == 0


# ---------------------------------------------------------------------------
# CLI integration
# ---------------------------------------------------------------------------


class TestCLI:
    def test_redesign_help(self):
        r = run_cli("redesign", "--help")
        assert r.returncode == 0
        output = r.stdout + r.stderr
        assert "scan" in output.lower() or "redesign" in output.lower() or "usage" in output.lower()

    def test_redesign_scan_empty_dir(self, tmp_path):
        r = run_cli("redesign", str(tmp_path))
        assert r.returncode == 0
        output = r.stdout
        assert "OneMore Redesign Report" in output

    def test_redesign_json_output(self, tmp_path):
        f = tmp_path / "App.tsx"
        f.write_text("const s = { color: '#000' };")
        r = run_cli("redesign", str(tmp_path), "--json")
        assert r.returncode == 0
        data = json.loads(r.stdout)
        assert "violations" in data
        assert "files_scanned" in data

    def test_redesign_custom_output(self, tmp_path):
        f = tmp_path / "App.tsx"
        f.write_text("const s = { color: '#000' };")
        out = tmp_path / "custom-report.md"
        r = run_cli("redesign", str(tmp_path), "--output", str(out))
        assert r.returncode == 0
        assert out.exists()
