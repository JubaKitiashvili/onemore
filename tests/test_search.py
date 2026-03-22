"""Tests for CSV config and search functions in scripts/core.py."""
import pytest
from scripts.core import _load_csv, search, detect_domain, search_stack


class TestLoadCSV:
    def test_load_csv_colors(self):
        rows = _load_csv("foundations", "colors.csv")
        assert len(rows) > 0
        assert "keyword" in rows[0]
        assert "name" in rows[0]

    def test_load_csv_missing_file(self):
        rows = _load_csv("foundations", "nonexistent.csv")
        assert rows == []


class TestSearchColors:
    def test_search_colors_blue(self):
        results = search("blue color interactive", domain="colors")
        assert len(results) > 0
        # The top result should relate to blue
        found_blue = any("blue" in r.get("keyword", "").lower() for r in results)
        assert found_blue

    def test_search_no_results(self):
        results = search("xyznonexistent987", domain="colors")
        assert results == []


class TestDetectDomain:
    def test_detect_colors(self):
        assert detect_domain("what color should I use for accent") == "colors"

    def test_detect_typography(self):
        assert detect_domain("which font for headings") == "typography"

    def test_detect_components(self):
        assert detect_domain("button style and toggle") == "controls"

    def test_detect_animation(self):
        assert detect_domain("spring animation easing") == "animation"

    def test_detect_default_fallback(self):
        assert detect_domain("something completely unrelated") == "colors"


# ---------------------------------------------------------------------------
# NativeWind stack search
# ---------------------------------------------------------------------------


def test_search_nativewind_stack():
    """Verify nativewind stack is searchable and returns results."""
    r = search_stack("className Pressable", "nativewind")
    assert "error" not in r
    assert len(r) > 0


def test_search_nativewind_pressable():
    """Pressable keyword should rank well in nativewind stack."""
    r = search_stack("Pressable touch target", "nativewind")
    assert len(r) > 0
    keywords = [row.get("keyword", "") for row in r]
    assert any("pressable" in k.lower() or "touch" in k.lower() for k in keywords)


def test_search_nativewind_haptics():
    """expo-haptics should be findable in nativewind stack."""
    r = search_stack("haptics feedback onPress", "nativewind")
    assert len(r) > 0


def test_search_nativewind_unknown_stack():
    """Unknown stack name returns empty list not error."""
    r = search_stack("anything", "nonexistent-stack")
    assert r == []
