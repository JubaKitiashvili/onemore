#!/usr/bin/env python3
"""OneMore CLI — Apple HIG design intelligence search."""
import argparse
import json
import sys
from pathlib import Path

# Allow running as a script from any working directory
_SCRIPTS_DIR = Path(__file__).parent
_PROJECT_ROOT = _SCRIPTS_DIR.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.core import (
    CSV_CONFIG,
    PLATFORM_CONFIG,
    STACK_CONFIG,
    search,
    search_platform,
    search_stack,
)

# ---------------------------------------------------------------------------
# Output Formatting
# ---------------------------------------------------------------------------

_TRUNCATE = 200


def _truncate(value: str, limit: int = _TRUNCATE) -> str:
    if len(value) <= limit:
        return value
    return value[:limit] + "…"


def format_output(
    results: list[dict[str, str]],
    *,
    query: str = "",
    domain: str | None = None,
    stack: str | None = None,
    platform: str | None = None,
    fmt: str = "ascii",
) -> str:
    """Render results as a human-readable string."""
    lines: list[str] = []

    # --- Header ---
    scope_parts: list[str] = []
    if domain:
        scope_parts.append(f"domain={domain}")
    if stack:
        scope_parts.append(f"stack={stack}")
    if platform:
        scope_parts.append(f"platform={platform}")
    scope = ", ".join(scope_parts) if scope_parts else "auto"

    if fmt == "markdown":
        lines.append(f"## OneMore Search")
        if query:
            lines.append(f"**Query:** {query}  ")
        lines.append(f"**Scope:** {scope}  ")
        lines.append(f"**Results:** {len(results)}")
        lines.append("")
    else:
        separator = "=" * 60
        lines.append(separator)
        lines.append("  OneMore")
        if query:
            lines.append(f"  Query   : {query}")
        lines.append(f"  Scope   : {scope}")
        lines.append(f"  Results : {len(results)}")
        lines.append(separator)

    if not results:
        lines.append("")
        lines.append("  No results found.")
        hints: list[str] = []
        if domain and domain not in CSV_CONFIG:
            hints.append(f"  '{domain}' is not a known domain. Valid domains: {', '.join(sorted(CSV_CONFIG))}")
        if stack and stack not in STACK_CONFIG:
            hints.append(f"  '{stack}' is not a known stack. Valid stacks: {', '.join(sorted(STACK_CONFIG))}")
        if platform and platform not in PLATFORM_CONFIG:
            hints.append(f"  '{platform}' is not a known platform. Valid platforms: {', '.join(sorted(PLATFORM_CONFIG))}")
        if not hints:
            hints.append("  Try broadening your query or checking a different domain.")
        lines.extend(hints)
        lines.append("")
        return "\n".join(lines)

    # --- Results ---
    for idx, row in enumerate(results, start=1):
        if fmt == "markdown":
            lines.append(f"### Result {idx}")
            for key, value in row.items():
                lines.append(f"- **{key}**: {_truncate(str(value))}")
            lines.append("")
        else:
            lines.append(f"\n  [{idx}]")
            for key, value in row.items():
                lines.append(f"    {key:<20} {_truncate(str(value))}")

    if fmt != "markdown":
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Argument Parser
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="onemore",
        description="Search Apple HIG design intelligence from the command line.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="\n".join([
            "Examples:",
            "  onemore 'blue accent color'",
            "  onemore 'button' --domain controls",
            "  onemore 'navigation' --platform ios",
            "  onemore 'button' --stack swiftui",
            "  onemore 'button' --json",
            "  onemore --design-system --project-name MyApp",
        ]),
    )

    parser.add_argument(
        "query",
        nargs="?",
        default="",
        help="Search query text",
    )
    parser.add_argument(
        "-d", "--domain",
        choices=list(CSV_CONFIG.keys()),
        metavar="DOMAIN",
        help=f"Force a specific domain. Choices: {', '.join(sorted(CSV_CONFIG))}",
    )
    parser.add_argument(
        "-s", "--stack",
        choices=list(STACK_CONFIG.keys()),
        metavar="STACK",
        help=f"Stack-specific search. Choices: {', '.join(sorted(STACK_CONFIG))}",
    )
    parser.add_argument(
        "-p", "--platform",
        choices=list(PLATFORM_CONFIG.keys()),
        metavar="PLATFORM",
        help=f"Platform-specific search. Choices: {', '.join(sorted(PLATFORM_CONFIG))}",
    )
    parser.add_argument(
        "-n", "--max-results",
        type=int,
        default=5,
        metavar="N",
        help="Maximum number of results to return (default: 5)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="json_output",
        help="Output results as JSON",
    )
    parser.add_argument(
        "--design-system",
        action="store_true",
        help="Generate a full design system (stub)",
    )
    parser.add_argument(
        "--project-name",
        default="MyApp",
        metavar="NAME",
        help="Project name for design system generation (default: MyApp)",
    )
    parser.add_argument(
        "-f", "--format",
        choices=["ascii", "markdown"],
        default="ascii",
        help="Output format: ascii or markdown (default: ascii)",
    )
    parser.add_argument(
        "--persist",
        action="store_true",
        help="Save design system output to files",
    )
    parser.add_argument(
        "--page",
        metavar="PAGE",
        help="Page-specific override for design system generation",
    )

    return parser


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def _handle_init(args: list[str]) -> int:
    """Handle the 'init' subcommand for multi-platform distribution."""
    from scripts.platforms import init_platform, list_platforms, detect_platforms, auto_init, PLATFORMS

    if "--list" in args:
        platforms = list_platforms()
        print(f"{'Platform':<16} {'Name':<18} {'Type':<10} {'Status':<12} Path")
        print("-" * 80)
        for p in platforms:
            status = "installed" if p["installed"] else "-"
            print(f"{p['platform']:<16} {p['name']:<18} {p['type']:<10} {status:<12} {p['path']}")
        return 0

    # Find --ai value
    ai_value = None
    for i, arg in enumerate(args):
        if arg == "--ai" and i + 1 < len(args):
            ai_value = args[i + 1]
            break

    if not ai_value:
        # Auto-detect mode: no --ai flag given
        print("OneMore — Auto-Detecting AI Platforms...\n")

        detected_list = detect_platforms()
        for p in detected_list:
            mark = "✓" if p["detected"] else "✗"
            reason = p["reason"] if p["detected"] else "not detected"
            print(f"  {mark} {p['name']:<16} {reason}")

        detected_count = sum(1 for p in detected_list if p["detected"])
        if detected_count == 0:
            print("\nNo AI platforms detected. Use --ai <platform> to install manually.")
            print(f"Available platforms: {', '.join(sorted(PLATFORMS.keys()))}")
            return 0

        print(f"\nInstalling OneMore for {detected_count} detected platform(s)...\n")

        result = auto_init()
        installed_names = {p["platform"] for p in result["installed"]}
        skipped_names = {p["platform"] for p in result["skipped"]}

        for p in detected_list:
            if not p["detected"]:
                continue
            platform_key = p["platform"]
            config = PLATFORMS[platform_key]
            install_path = config["path"]
            if platform_key in installed_names:
                print(f"  ✓ {p['name']:<16} → {install_path}")
            elif platform_key in skipped_names:
                print(f"  ✓ {p['name']:<16} → {install_path} (already installed)")

        newly_installed = len(result["installed"])
        already_installed = len(result["skipped"])
        total = newly_installed + already_installed
        if already_installed > 0:
            print(f"\nDone! OneMore installed for {total} platform(s) ({already_installed} already installed).")
        else:
            print(f"\nDone! OneMore installed for {total} platform(s).")
        return 0

    # Determine which platforms to init
    if ai_value == "all":
        targets = [name for name, cfg in PLATFORMS.items() if cfg["type"] == "project"]
    else:
        targets = [t.strip() for t in ai_value.split(",")]

    for platform_name in targets:
        result = init_platform(platform_name)
        if "error" in result:
            print(f"  ERROR  {platform_name}: {result['error']}")
        else:
            print(f"  {result['status'].upper():<18} {result['platform']:<18} {result.get('path', '')}")

    return 0


def _handle_export(args: list[str]) -> int:
    """Handle the 'export' subcommand for design token code generation."""
    from scripts.exporter import EXPORT_FORMATS, export_tokens

    if "--list" in args:
        print(f"{'Format':<16} {'Output File':<24}")
        print("-" * 40)
        for name, cfg in EXPORT_FORMATS.items():
            print(f"{name:<16} {cfg['filename']:<24}")
        return 0

    # Parse --format and --output
    fmt_value = None
    output_value = None
    for i, arg in enumerate(args):
        if arg == "--format" and i + 1 < len(args):
            fmt_value = args[i + 1]
        elif arg == "--output" and i + 1 < len(args):
            output_value = args[i + 1]

    if not fmt_value:
        print("Usage: onemore export --format <format|all> [--output <dir>]")
        print("       onemore export --list")
        print(f"\nAvailable formats: {', '.join(EXPORT_FORMATS.keys())}")
        return 1

    if fmt_value == "all":
        targets = list(EXPORT_FORMATS.keys())
    else:
        targets = [fmt_value]

    for target in targets:
        result = export_tokens(target, output_dir=output_value)
        if "error" in result:
            print(f"  ERROR  {result['error']}")
        else:
            print(f"  {result['status'].upper():<12} {result['format']:<16} -> {result['file']}")

    return 0


def _handle_redesign(args: list[str]) -> int:
    """Handle the 'redesign' subcommand for HIG violation scanning."""
    from scripts.redesign import cli_main
    return cli_main(args)


def main() -> int:
    # Handle subcommands before argparse
    raw_args = sys.argv[1:]
    if raw_args and raw_args[0] == "export":
        return _handle_export(raw_args[1:])
    if raw_args and raw_args[0] == "init":
        return _handle_init(raw_args[1:])
    if raw_args and raw_args[0] == "redesign":
        return _handle_redesign(raw_args[1:])

    # Use parse_known_args to allow unknown domain/stack/platform values
    # without crashing, then validate manually so we can surface helpful messages.
    parser = build_parser()

    # Patch: temporarily widen domain/stack/platform to accept any string so
    # unknown values are handled gracefully rather than argparse error-exiting.
    _patched_parser = argparse.ArgumentParser(
        prog="onemore",
        description=parser.description,
        formatter_class=parser.formatter_class,
        epilog=parser.epilog,
        add_help=True,
    )
    _patched_parser.add_argument("query", nargs="?", default="")
    _patched_parser.add_argument("-d", "--domain", default=None, metavar="DOMAIN")
    _patched_parser.add_argument("-s", "--stack", default=None, metavar="STACK")
    _patched_parser.add_argument("-p", "--platform", default=None, metavar="PLATFORM")
    _patched_parser.add_argument("-n", "--max-results", type=int, default=5, metavar="N")
    _patched_parser.add_argument("--json", action="store_true", dest="json_output")
    _patched_parser.add_argument("--design-system", action="store_true")
    _patched_parser.add_argument("--project-name", default="MyApp", metavar="NAME")
    _patched_parser.add_argument("-f", "--format", choices=["ascii", "markdown"], default="ascii")
    _patched_parser.add_argument("--persist", action="store_true")
    _patched_parser.add_argument("--page", default=None, metavar="PAGE")

    # Show proper help from the nicer parser if --help requested
    if "-h" in raw_args or "--help" in raw_args:
        parser.print_help()
        return 0

    args = _patched_parser.parse_args(raw_args)

    query: str = args.query or ""
    domain: str | None = args.domain
    stack: str | None = args.stack
    platform: str | None = args.platform
    max_results: int = args.max_results
    json_output: bool = args.json_output
    fmt: str = args.format

    # ------------------------------------------------------------------
    # Priority 1: --design-system
    # ------------------------------------------------------------------
    if args.design_system:
        try:
            from scripts.design_system import DesignSystemGenerator  # type: ignore
            generator = DesignSystemGenerator(project_name=args.project_name)
            output = generator.generate(fmt=fmt, persist=args.persist, page=args.page)
            print(output)
        except ImportError:
            print(
                f"Design system generator for '{args.project_name}' is not yet implemented.\n"
                "Run without --design-system to search the design token database."
            )
        return 0

    # ------------------------------------------------------------------
    # Priority 2: --stack
    # ------------------------------------------------------------------
    if stack:
        results = search_stack(query, stack, max_results=max_results)
        if json_output:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            print(format_output(results, query=query, stack=stack, fmt=fmt))
        return 0

    # ------------------------------------------------------------------
    # Priority 3: --platform (without --domain)
    # ------------------------------------------------------------------
    if platform and not domain:
        results = search_platform(query, platform, max_results=max_results)
        if json_output:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            print(format_output(results, query=query, platform=platform, fmt=fmt))
        return 0

    # ------------------------------------------------------------------
    # Default: search() with optional domain and platform filter
    # ------------------------------------------------------------------
    results = search(query, domain=domain, max_results=max_results, platform=platform)
    if json_output:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print(format_output(results, query=query, domain=domain, platform=platform, fmt=fmt))
    return 0


if __name__ == "__main__":
    sys.exit(main())
