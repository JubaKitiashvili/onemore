"""Tests for the Apple HIG design system generator."""
import os
from pathlib import Path

import pytest

from scripts.design_system import DesignSystemGenerator


def test_generator_init():
    gen = DesignSystemGenerator()
    assert gen is not None


def test_reasoning_rules_loaded():
    gen = DesignSystemGenerator()
    assert isinstance(gen.reasoning_rules, list)
    assert len(gen.reasoning_rules) > 0


def test_find_reasoning_exact_match():
    gen = DesignSystemGenerator()
    rule = gen._find_reasoning_rule("Health")
    assert rule is not None
    assert rule.get("category", "").lower() == "health"


def test_find_reasoning_partial_match():
    gen = DesignSystemGenerator()
    rule = gen._find_reasoning_rule("health fitness tracking")
    assert rule is not None
    assert "health" in rule.get("category", "").lower()


def test_find_reasoning_keyword_match():
    gen = DesignSystemGenerator()
    rule = gen._find_reasoning_rule("dashboard cards metrics")
    assert rule is not None
    assert rule.get("category", "") != ""


def test_generate_basic():
    gen = DesignSystemGenerator()
    result = gen.generate("health app dashboard", project_name="HealthKit Pro")
    assert result["project_name"] == "HealthKit Pro"
    assert "foundations" in result
    assert "components" in result
    assert "patterns" in result


def test_generate_default_project_name():
    gen = DesignSystemGenerator()
    result = gen.generate("productivity app")
    assert result["project_name"] == "Untitled"


def test_generate_has_reasoning():
    gen = DesignSystemGenerator()
    result = gen.generate("health fitness tracking")
    if result.get("reasoning"):
        assert result["reasoning"]["category"] != ""


def test_generate_foundations_structure():
    gen = DesignSystemGenerator()
    result = gen.generate("finance banking", project_name="WalletPro")
    foundations = result["foundations"]
    assert "colors" in foundations
    assert "typography" in foundations
    assert "spacing" in foundations
    assert "corners" in foundations
    assert "elevation" in foundations


def test_generate_components_structure():
    gen = DesignSystemGenerator()
    result = gen.generate("social media app")
    components = result["components"]
    assert "navigation" in components
    assert "controls" in components
    assert "content" in components


def test_generate_patterns_structure():
    gen = DesignSystemGenerator()
    result = gen.generate("productivity app")
    patterns = result["patterns"]
    assert "animation" in patterns
    assert "interaction" in patterns


def test_format_ascii():
    gen = DesignSystemGenerator()
    result = gen.generate("productivity app", project_name="TaskFlow")
    output = gen.format_ascii(result)
    assert "TaskFlow" in output
    assert len(output) > 100
    assert "FOUNDATIONS" in output
    assert "COMPONENTS" in output
    assert "PATTERNS" in output


def test_format_ascii_contains_reasoning():
    gen = DesignSystemGenerator()
    result = gen.generate("health app", project_name="HealthApp")
    output = gen.format_ascii(result)
    assert "App Category:" in output


def test_format_markdown():
    gen = DesignSystemGenerator()
    result = gen.generate("finance banking", project_name="WalletPro")
    output = gen.format_markdown(result)
    assert "# " in output
    assert "WalletPro" in output
    assert "## Foundations" in output
    assert "## Components" in output
    assert "## Patterns" in output


def test_format_markdown_has_tables():
    gen = DesignSystemGenerator()
    result = gen.generate("health app", project_name="HealthApp")
    output = gen.format_markdown(result)
    assert "|" in output
    assert "---" in output


def test_persist(tmp_path):
    os.chdir(tmp_path)
    gen = DesignSystemGenerator()
    result = gen.generate("shopping app", project_name="ShopEasy")
    path = gen.persist(result, "ShopEasy")
    assert Path(path).exists()
    content = Path(path).read_text()
    assert "ShopEasy" in content
    assert path.endswith("MASTER.md")


def test_persist_page(tmp_path):
    os.chdir(tmp_path)
    gen = DesignSystemGenerator()
    result = gen.generate("shopping app", project_name="ShopEasy")
    path = gen.persist(result, "ShopEasy", page="colors")
    assert Path(path).exists()
    assert "colors.md" in path
    content = Path(path).read_text()
    assert "ShopEasy" in content


def test_persist_creates_directories(tmp_path):
    os.chdir(tmp_path)
    gen = DesignSystemGenerator()
    result = gen.generate("fitness app", project_name="Fit Tracker")
    path = gen.persist(result, "Fit Tracker")
    assert Path(path).exists()
    assert "fit-tracker" in path
