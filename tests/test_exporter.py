"""Tests for the OneMore design token exporter."""
import json
import sys
from pathlib import Path

import pytest

# Ensure project root is importable
_PROJECT_ROOT = Path(__file__).parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.exporter import EXPORT_FORMATS, export_tokens


def test_export_tailwind(tmp_path):
    result = export_tokens("tailwind", output_dir=tmp_path)
    assert result["status"] == "generated"
    filepath = tmp_path / "tailwind.config.js"
    assert filepath.exists()
    content = filepath.read_text()
    assert "module.exports" in content
    assert "#007AFF" in content  # systemBlue
    assert "apple" in content.lower()


def test_export_css(tmp_path):
    result = export_tokens("css", output_dir=tmp_path)
    filepath = tmp_path / "apple-tokens.css"
    assert filepath.exists()
    content = filepath.read_text()
    assert ":root" in content
    assert "prefers-color-scheme: dark" in content
    # Check for color variables
    assert "--system-blue" in content or "--apple-blue" in content


def test_export_swiftui(tmp_path):
    result = export_tokens("swiftui", output_dir=tmp_path)
    filepath = tmp_path / "AppleTokens.swift"
    assert filepath.exists()
    content = filepath.read_text()
    assert "import SwiftUI" in content
    assert "CGFloat" in content


def test_export_flutter(tmp_path):
    result = export_tokens("flutter", output_dir=tmp_path)
    filepath = tmp_path / "apple_theme.dart"
    assert filepath.exists()
    content = filepath.read_text()
    assert "import" in content
    assert "CupertinoColors" in content or "Color(" in content


def test_export_scss(tmp_path):
    result = export_tokens("scss", output_dir=tmp_path)
    filepath = tmp_path / "_apple-tokens.scss"
    assert filepath.exists()
    content = filepath.read_text()
    assert "$" in content
    assert "@mixin" in content


def test_export_json(tmp_path):
    result = export_tokens("json", output_dir=tmp_path)
    filepath = tmp_path / "apple-tokens.json"
    assert filepath.exists()
    data = json.loads(filepath.read_text())
    assert "colors" in data
    assert "spacing" in data
    assert "typography" in data
    assert "borderRadius" in data
    assert "shadows" in data


def test_export_react_native(tmp_path):
    result = export_tokens("react-native", output_dir=tmp_path)
    filepath = tmp_path / "appleTheme.ts"
    assert filepath.exists()
    content = filepath.read_text()
    assert "StyleSheet" in content
    assert "AppleColors" in content
    assert "AppleColorsDark" in content
    assert "AppleSpacing" in content
    assert "AppleRadius" in content


def test_export_unknown():
    result = export_tokens("nonexistent")
    assert "error" in result
    assert "available" in result


def test_export_list():
    assert len(EXPORT_FORMATS) == 7
    expected = {"tailwind", "css", "swiftui", "flutter", "scss", "json", "react-native"}
    assert set(EXPORT_FORMATS.keys()) == expected


def test_export_all_formats(tmp_path):
    """Ensure every registered format generates successfully."""
    for fmt_name in EXPORT_FORMATS:
        result = export_tokens(fmt_name, output_dir=tmp_path)
        assert result["status"] == "generated", f"Failed for format: {fmt_name}"
        filepath = tmp_path / result["filename"]
        assert filepath.exists(), f"File not created for format: {fmt_name}"
        content = filepath.read_text()
        assert len(content) > 100, f"Output too short for format: {fmt_name}"


def test_tailwind_has_spacing(tmp_path):
    export_tokens("tailwind", output_dir=tmp_path)
    content = (tmp_path / "tailwind.config.js").read_text()
    assert "spacing" in content
    assert "apple-xs" in content


def test_tailwind_has_font_size(tmp_path):
    export_tokens("tailwind", output_dir=tmp_path)
    content = (tmp_path / "tailwind.config.js").read_text()
    assert "fontSize" in content
    assert "large-title" in content


def test_css_dark_mode_overrides(tmp_path):
    export_tokens("css", output_dir=tmp_path)
    content = (tmp_path / "apple-tokens.css").read_text()
    # Dark mode block should contain the dark hex for systemBlue
    assert "#0A84FF" in content


def test_json_valid_structure(tmp_path):
    export_tokens("json", output_dir=tmp_path)
    data = json.loads((tmp_path / "apple-tokens.json").read_text())
    assert data["generated_by"] == "OneMore \u2014 Apple HIG Design Tokens"
    # systemBlue should be present
    assert "systemBlue" in data["colors"]
    assert data["colors"]["systemBlue"]["light"] == "#007AFF"
    assert data["colors"]["systemBlue"]["dark"] == "#0A84FF"


def test_react_native_has_dark_colors(tmp_path):
    export_tokens("react-native", output_dir=tmp_path)
    content = (tmp_path / "appleTheme.ts").read_text()
    assert "#0A84FF" in content  # dark systemBlue


def test_swiftui_has_fonts(tmp_path):
    export_tokens("swiftui", output_dir=tmp_path)
    content = (tmp_path / "AppleTokens.swift").read_text()
    assert ".largeTitle" in content
    assert "AppleSpacing" in content
    assert "AppleRadius" in content


def test_flutter_has_typography(tmp_path):
    export_tokens("flutter", output_dir=tmp_path)
    content = (tmp_path / "apple_theme.dart").read_text()
    assert "AppleTypography" in content
    assert "TextStyle" in content
    assert "fontSize: 34" in content  # largeTitle


def test_scss_has_dark_variables(tmp_path):
    export_tokens("scss", output_dir=tmp_path)
    content = (tmp_path / "_apple-tokens.scss").read_text()
    assert "-dark:" in content
    assert "$space-" in content
