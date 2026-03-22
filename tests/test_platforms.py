import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from platforms import generate_project_rules, init_platform, list_platforms, detect_platforms, auto_init, PLATFORMS

def test_generate_project_rules():
    rules = generate_project_rules()
    assert "Apple HIG" in rules
    assert "4.5:1" in rules  # accessibility
    assert "44pt" in rules  # touch targets
    assert "spring" in rules.lower()  # animation
    assert "#007AFF" in rules  # system blue
    assert "Inter" in rules  # web fallback font

def test_platforms_config():
    assert len(PLATFORMS) >= 11
    assert "claude-code" in PLATFORMS
    assert "cursor" in PLATFORMS
    assert "windsurf" in PLATFORMS
    assert "copilot" in PLATFORMS

def test_list_platforms():
    results = list_platforms()
    assert len(results) >= 11
    names = [r["platform"] for r in results]
    assert "cursor" in names
    assert "claude-code" in names

def test_init_project_cursor(tmp_path):
    result = init_platform("cursor", project_dir=tmp_path)
    assert result["status"] == "installed"
    target = tmp_path / ".cursor" / "rules" / "onemore.mdc"
    assert target.exists()
    content = target.read_text()
    assert "description:" in content  # Cursor frontmatter
    assert "Apple HIG" in content

def test_init_project_windsurf(tmp_path):
    result = init_platform("windsurf", project_dir=tmp_path)
    assert result["status"] == "installed"
    target = tmp_path / ".windsurf" / "rules" / "onemore.md"
    assert target.exists()
    assert "Apple HIG" in target.read_text()

def test_init_project_copilot_append(tmp_path):
    # Create existing file
    github_dir = tmp_path / ".github"
    github_dir.mkdir()
    existing = github_dir / "copilot-instructions.md"
    existing.write_text("# Existing rules\nDo stuff.\n")

    result = init_platform("copilot", project_dir=tmp_path)
    assert result["status"] == "installed"
    content = existing.read_text()
    assert "Existing rules" in content  # preserved
    assert "OneMore" in content  # appended

def test_init_project_copilot_already_installed(tmp_path):
    init_platform("copilot", project_dir=tmp_path)
    result = init_platform("copilot", project_dir=tmp_path)
    assert result["status"] == "already_installed"

def test_init_unknown_platform():
    result = init_platform("nonexistent")
    assert "error" in result

def test_init_project_gemini(tmp_path):
    result = init_platform("gemini", project_dir=tmp_path)
    assert result["status"] == "installed"
    target = tmp_path / "GEMINI.md"
    assert target.exists()

def test_init_project_cline(tmp_path):
    result = init_platform("cline", project_dir=tmp_path)
    assert result["status"] == "installed"
    target = tmp_path / ".clinerules" / "onemore.md"
    assert target.exists()

def test_init_project_roo(tmp_path):
    result = init_platform("roo", project_dir=tmp_path)
    assert result["status"] == "installed"

def test_init_project_kiro(tmp_path):
    result = init_platform("kiro", project_dir=tmp_path)
    assert result["status"] == "installed"


def test_detect_platforms():
    results = detect_platforms()
    assert len(results) == 11
    # At least claude-code should be detected (we have ~/.claude)
    claude = next(r for r in results if r["platform"] == "claude-code")
    assert claude["detected"] == True


def test_detect_platforms_project_dir(tmp_path):
    # Create .cursor dir to simulate Cursor project
    (tmp_path / ".cursor").mkdir()
    results = detect_platforms(project_dir=tmp_path)
    cursor = next(r for r in results if r["platform"] == "cursor")
    assert cursor["detected"] == True
    assert "project" in cursor["reason"]


def test_auto_init(tmp_path):
    # Create .windsurf dir to simulate detection
    (tmp_path / ".windsurf").mkdir()
    result = auto_init(project_dir=tmp_path)
    assert len(result["detected"]) > 0
    # Windsurf should be in detected
    windsurf_detected = any(p["platform"] == "windsurf" for p in result["detected"])
    assert windsurf_detected


def test_auto_init_skip_already_installed(tmp_path):
    (tmp_path / ".cursor").mkdir()
    # First install
    auto_init(project_dir=tmp_path)
    # Second install should skip
    result = auto_init(project_dir=tmp_path)
    cursor_skipped = any(p["platform"] == "cursor" for p in result["skipped"])
    assert cursor_skipped
