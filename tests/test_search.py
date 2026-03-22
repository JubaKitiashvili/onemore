"""Tests for CSV config and search functions in scripts/core.py."""
import pytest
from scripts.core import _load_csv, search, detect_domain


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
