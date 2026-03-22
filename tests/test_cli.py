"""Tests for the search.py CLI entry point."""
import json
import subprocess
import sys
from pathlib import Path

# Path to the CLI script
CLI = Path(__file__).parent.parent / "scripts" / "search.py"
PYTHON = sys.executable


def run_cli(*args, **kwargs):
    """Run the CLI with given args. Returns CompletedProcess."""
    return subprocess.run(
        [PYTHON, str(CLI)] + list(args),
        capture_output=True,
        text=True,
        **kwargs,
    )


class TestHelp:
    def test_help_exits_zero(self):
        result = run_cli("--help")
        assert result.returncode == 0

    def test_help_contains_program_name(self):
        result = run_cli("--help")
        output = result.stdout + result.stderr
        assert "onemore" in output.lower() or "search" in output.lower()

    def test_help_mentions_domain(self):
        result = run_cli("--help")
        assert "domain" in result.stdout.lower() or "domain" in result.stderr.lower()


class TestBasicSearch:
    def test_search_basic_exits_zero(self):
        result = run_cli("button toggle")
        assert result.returncode == 0

    def test_search_produces_output(self):
        result = run_cli("blue accent color")
        assert result.returncode == 0
        # Should produce some output (header at minimum)
        assert len(result.stdout) > 0

    def test_search_no_query_exits_zero(self):
        """Running with no query should not crash."""
        result = run_cli()
        assert result.returncode == 0


class TestDomainSearch:
    def test_search_domain_colors(self):
        result = run_cli("blue accent", "--domain", "colors")
        assert result.returncode == 0

    def test_search_domain_short_flag(self):
        result = run_cli("blue", "-d", "colors")
        assert result.returncode == 0

    def test_search_domain_output_contains_header(self):
        result = run_cli("blue accent", "--domain", "colors")
        assert result.returncode == 0
        assert len(result.stdout) > 0


class TestPlatformSearch:
    def test_search_platform_ios(self):
        result = run_cli("navigation", "--platform", "ios")
        assert result.returncode == 0

    def test_search_platform_short_flag(self):
        result = run_cli("navigation", "-p", "ios")
        assert result.returncode == 0

    def test_search_platform_macos(self):
        result = run_cli("sidebar", "--platform", "macos")
        assert result.returncode == 0


class TestStackSearch:
    def test_search_stack_swiftui(self):
        result = run_cli("button", "--stack", "swiftui")
        assert result.returncode == 0

    def test_search_stack_short_flag(self):
        result = run_cli("button", "-s", "swiftui")
        assert result.returncode == 0

    def test_search_stack_react_native(self):
        result = run_cli("button", "--stack", "react-native")
        assert result.returncode == 0


class TestMaxResults:
    def test_max_results_flag(self):
        result = run_cli("color", "--max-results", "3")
        assert result.returncode == 0

    def test_max_results_short_flag(self):
        result = run_cli("color", "-n", "3")
        assert result.returncode == 0


class TestJsonOutput:
    def test_json_flag_exits_zero(self):
        result = run_cli("blue accent", "--domain", "colors", "--json")
        assert result.returncode == 0

    def test_json_output_is_valid_json(self):
        result = run_cli("blue accent", "--domain", "colors", "--json")
        assert result.returncode == 0
        # Output should be parseable as JSON
        data = json.loads(result.stdout)
        assert isinstance(data, list)

    def test_json_no_results_is_empty_list(self):
        result = run_cli("xyznonexistent987", "--domain", "colors", "--json")
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert data == []


class TestFormatFlag:
    def test_format_ascii(self):
        result = run_cli("blue", "--format", "ascii")
        assert result.returncode == 0

    def test_format_markdown(self):
        result = run_cli("blue", "--format", "markdown")
        assert result.returncode == 0

    def test_format_short_flag(self):
        result = run_cli("blue", "-f", "markdown")
        assert result.returncode == 0


class TestInvalidInputsGraceful:
    def test_invalid_domain_graceful(self):
        """Unknown domain should not crash the CLI."""
        result = run_cli("test", "--domain", "nonexistent")
        assert result.returncode == 0

    def test_invalid_stack_graceful(self):
        """Unknown stack should not crash."""
        result = run_cli("test", "--stack", "nonexistent")
        assert result.returncode == 0

    def test_invalid_platform_graceful(self):
        """Unknown platform should not crash."""
        result = run_cli("test", "--platform", "nonexistent")
        assert result.returncode == 0


class TestDesignSystemFlag:
    def test_design_system_flag_exits_zero(self):
        result = run_cli("--design-system")
        assert result.returncode == 0

    def test_design_system_with_project_name(self):
        result = run_cli("--design-system", "--project-name", "TestApp")
        assert result.returncode == 0

    def test_design_system_produces_output(self):
        result = run_cli("--design-system")
        assert result.returncode == 0
        assert len(result.stdout) > 0


class TestInitSubcommand:
    def test_init_list(self):
        r = run_cli("init", "--list")
        assert r.returncode == 0
        assert "cursor" in r.stdout.lower()

    def test_init_auto(self):
        r = run_cli("init")
        assert r.returncode == 0
        assert "detect" in r.stdout.lower() or "platform" in r.stdout.lower()
