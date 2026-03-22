# OneMore Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build an Apple HIG design intelligence skill that generates Apple-quality UI across all platforms via a CSV-backed Python CLI search engine.

**Architecture:** Adapt ui-ux-pro-max's BM25 search engine + CSV database pattern. Replace all generic design data with Apple HIG-specific data. Add platform awareness (iOS/macOS/watchOS/visionOS/web) and audit mode.

**Tech Stack:** Python 3.10+ (stdlib only), CSV databases, Claude Code skill system

**Spec:** `docs/superpowers/specs/2026-03-22-onemore-design.md`

**Reference codebase:** `~/.claude/skills/ui-ux-pro-max/` (read-only, for structural reference)

---

### Task 1: Project scaffolding and core.py search engine

**Files:**
- Create: `scripts/__init__.py`
- Create: `scripts/core.py`
- Create: `tests/__init__.py`
- Create: `tests/test_core.py`

- [ ] **Step 1: Create directory structure**

```bash
cd ~/Desktop/Projects/onemore
mkdir -p scripts tests data/foundations data/components data/patterns data/platforms data/stacks data/audit data/reasoning sync
touch scripts/__init__.py tests/__init__.py
```

- [ ] **Step 2: Write test for BM25 tokenizer**

```python
# tests/test_core.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from core import BM25

def test_tokenize_basic():
    bm25 = BM25()
    tokens = bm25.tokenize("Navigation Bar Height iOS")
    assert "navigation" in tokens
    assert "bar" in tokens
    assert "height" in tokens
    assert "ios" in tokens

def test_tokenize_removes_short_words():
    bm25 = BM25()
    tokens = bm25.tokenize("a UI to be designed")
    assert "a" not in tokens
    assert "to" not in tokens
    assert "be" not in tokens
    assert "designed" in tokens

def test_tokenize_strips_punctuation():
    bm25 = BM25()
    tokens = bm25.tokenize("color: #007AFF (blue)")
    assert "color" in tokens
    assert "007aff" in tokens
    assert "blue" in tokens
```

- [ ] **Step 3: Run tests to verify they fail**

```bash
cd ~/Desktop/Projects/onemore
python3 -m pytest tests/test_core.py -v
```
Expected: ModuleNotFoundError

- [ ] **Step 4: Implement BM25 class in core.py**

```python
# scripts/core.py
#!/usr/bin/env python3
"""OneMore Core - BM25 search engine for Apple HIG guidelines"""

import csv
import re
from pathlib import Path
from math import log
from collections import defaultdict

DATA_DIR = Path(__file__).parent.parent / "data"
MAX_RESULTS = 5

class BM25:
    """BM25 ranking algorithm for text search"""

    def __init__(self, k1=1.5, b=0.75):
        self.k1 = k1
        self.b = b
        self.corpus = []
        self.doc_lengths = []
        self.avgdl = 0
        self.idf = {}
        self.doc_freqs = defaultdict(int)
        self.N = 0

    def tokenize(self, text):
        text = re.sub(r'[^\w\s]', ' ', str(text).lower())
        return [w for w in text.split() if len(w) > 2]

    def fit(self, documents):
        self.corpus = [self.tokenize(doc) for doc in documents]
        self.N = len(self.corpus)
        if self.N == 0:
            return
        self.doc_lengths = [len(doc) for doc in self.corpus]
        self.avgdl = sum(self.doc_lengths) / self.N

        for doc in self.corpus:
            seen = set()
            for word in doc:
                if word not in seen:
                    self.doc_freqs[word] += 1
                    seen.add(word)

        for word, freq in self.doc_freqs.items():
            self.idf[word] = log((self.N - freq + 0.5) / (freq + 0.5) + 1)

    def score(self, query):
        query_tokens = self.tokenize(query)
        scores = []
        for idx, doc in enumerate(self.corpus):
            score = 0
            doc_len = self.doc_lengths[idx]
            term_freqs = defaultdict(int)
            for word in doc:
                term_freqs[word] += 1
            for token in query_tokens:
                if token in self.idf:
                    tf = term_freqs[token]
                    idf = self.idf[token]
                    numerator = tf * (self.k1 + 1)
                    denominator = tf + self.k1 * (1 - self.b + self.b * doc_len / self.avgdl)
                    score += idf * numerator / denominator
            scores.append((idx, score))
        return sorted(scores, key=lambda x: x[1], reverse=True)
```

- [ ] **Step 5: Run tests to verify they pass**

```bash
python3 -m pytest tests/test_core.py -v
```
Expected: 3 passed

- [ ] **Step 6: Commit**

```bash
git add scripts/ tests/
git commit -m "feat: add BM25 search engine core"
```

---

### Task 2: CSV configuration and search functions

**Files:**
- Modify: `scripts/core.py`
- Create: `tests/test_search.py`
- Create: `data/foundations/colors.csv` (minimal test data)

- [ ] **Step 1: Create minimal test CSV**

```csv
keyword,name,light_hex,dark_hex,usage,semantic_role,platform
blue,systemBlue,#007AFF,#0A84FF,Links and interactive,accent,all
green,systemGreen,#34C759,#30D158,Success and confirmation,success,all
red,systemRed,#FF3B30,#FF453A,Errors and destructive,destructive,all
label,label,#000000,#FFFFFF,Primary text,text-primary,all
```

Save to `data/foundations/colors.csv`

- [ ] **Step 2: Write search function tests**

```python
# tests/test_search.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from core import search, detect_domain, _load_csv

def test_load_csv():
    data_dir = Path(__file__).parent.parent / "data"
    rows = _load_csv(data_dir / "foundations" / "colors.csv")
    assert len(rows) >= 4
    assert "name" in rows[0]

def test_search_colors():
    result = search("blue accent link", domain="colors")
    assert result["count"] > 0
    assert result["results"][0]["name"] == "systemBlue"

def test_search_no_results():
    result = search("xyznonexistent", domain="colors")
    assert result["count"] == 0

def test_detect_domain_colors():
    assert detect_domain("color palette blue") == "colors"

def test_detect_domain_typography():
    assert detect_domain("font size heading SF Pro") == "typography"

def test_detect_domain_components():
    assert detect_domain("button toggle switch slider") == "components"

def test_detect_domain_animation():
    assert detect_domain("spring animation transition") == "animation"

def test_detect_domain_default():
    assert detect_domain("something generic") == "foundations"
```

- [ ] **Step 3: Run tests to verify they fail**

```bash
python3 -m pytest tests/test_search.py -v
```
Expected: ImportError (search/detect_domain not yet defined)

- [ ] **Step 4: Add CSV_CONFIG, PLATFORM_CONFIG, STACK_CONFIG, detect_domain, search functions to core.py**

Add after the BM25 class in `scripts/core.py`:

```python
# ============ CONFIGURATION ============

CSV_CONFIG = {
    "colors": {
        "file": "foundations/colors.csv",
        "search_cols": ["keyword", "name", "usage", "semantic_role"],
        "output_cols": ["name", "light_hex", "dark_hex", "usage", "semantic_role", "platform"]
    },
    "spacing": {
        "file": "foundations/spacing.csv",
        "search_cols": ["keyword", "name", "usage"],
        "output_cols": ["name", "value_pt", "value_px", "usage", "platform", "priority"]
    },
    "typography": {
        "file": "foundations/typography.csv",
        "search_cols": ["keyword", "style_name", "usage"],
        "output_cols": ["style_name", "size_pt", "weight", "tracking", "line_height", "platform", "priority"]
    },
    "elevation": {
        "file": "foundations/elevation.csv",
        "search_cols": ["keyword", "name", "usage"],
        "output_cols": ["name", "blur", "opacity", "color", "offset_y", "material", "platform"]
    },
    "corners": {
        "file": "foundations/corners.csv",
        "search_cols": ["keyword", "component", "usage"],
        "output_cols": ["component", "radius_pt", "style", "usage", "platform"]
    },
    "navigation": {
        "file": "components/navigation.csv",
        "search_cols": ["keyword", "component", "variant", "usage"],
        "output_cols": ["component", "variant", "height_pt", "usage", "platform", "priority"]
    },
    "controls": {
        "file": "components/controls.csv",
        "search_cols": ["keyword", "component", "variant"],
        "output_cols": ["component", "variant", "height_pt", "corner_radius", "font_weight", "font_size", "states", "platform", "priority"]
    },
    "content": {
        "file": "components/content.csv",
        "search_cols": ["keyword", "component", "variant", "usage"],
        "output_cols": ["component", "variant", "height_pt", "usage", "platform", "priority"]
    },
    "feedback": {
        "file": "components/feedback.csv",
        "search_cols": ["keyword", "component", "variant", "usage"],
        "output_cols": ["component", "variant", "usage", "platform", "priority"]
    },
    "input": {
        "file": "components/input.csv",
        "search_cols": ["keyword", "component", "variant", "usage"],
        "output_cols": ["component", "variant", "height_pt", "corner_radius", "usage", "platform", "priority"]
    },
    "animation": {
        "file": "patterns/animation.csv",
        "search_cols": ["keyword", "name", "usage"],
        "output_cols": ["name", "type", "response", "damping_fraction", "usage", "source", "platform"]
    },
    "gestures": {
        "file": "patterns/gestures.csv",
        "search_cols": ["keyword", "name", "usage"],
        "output_cols": ["name", "type", "usage", "platform", "priority"]
    },
    "layout": {
        "file": "patterns/layout.csv",
        "search_cols": ["keyword", "pattern", "usage"],
        "output_cols": ["pattern", "usage", "platform", "priority"]
    },
    "interaction": {
        "file": "patterns/interaction.csv",
        "search_cols": ["keyword", "name", "usage"],
        "output_cols": ["name", "type", "usage", "platform", "priority"]
    },
    "audit": {
        "file": "audit/hig-checklist.csv",
        "search_cols": ["keyword", "rule_id", "category", "description", "check_instruction"],
        "output_cols": ["rule_id", "category", "description", "check_instruction", "severity", "weight"]
    }
}

PLATFORM_CONFIG = {
    "ios": {"file": "platforms/ios.csv"},
    "macos": {"file": "platforms/macos.csv"},
    "watchos": {"file": "platforms/watchos.csv"},
    "visionos": {"file": "platforms/visionos.csv"},
    "web": {"file": "platforms/web-apple.csv"}
}

_PLATFORM_COLS = {
    "search_cols": ["keyword", "element", "context"],
    "output_cols": ["element", "metric", "value", "unit", "context", "priority"]
}

STACK_CONFIG = {
    "swiftui": {"file": "stacks/swiftui.csv"},
    "react": {"file": "stacks/react.csv"},
    "react-native": {"file": "stacks/react-native.csv"},
    "html-tailwind": {"file": "stacks/html-tailwind.csv"},
    "flutter": {"file": "stacks/flutter.csv"},
    "nextjs": {"file": "stacks/nextjs.csv"},
    "shadcn": {"file": "stacks/shadcn.csv"},
    "vue": {"file": "stacks/vue.csv"},
    "svelte": {"file": "stacks/svelte.csv"},
    "uikit": {"file": "stacks/uikit.csv"},
    "nuxtjs": {"file": "stacks/nuxtjs.csv"},
    "astro": {"file": "stacks/astro.csv"}
}

_STACK_COLS = {
    "search_cols": ["keyword", "pattern", "implementation", "notes"],
    "output_cols": ["keyword", "pattern", "implementation", "anti_pattern", "notes", "priority"]
}

AVAILABLE_STACKS = list(STACK_CONFIG.keys())
AVAILABLE_PLATFORMS = list(PLATFORM_CONFIG.keys())

# ============ SEARCH FUNCTIONS ============

def _load_csv(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def _search_csv(filepath, search_cols, output_cols, query, max_results):
    if not filepath.exists():
        return []
    data = _load_csv(filepath)
    if not data:
        return []
    documents = [" ".join(str(row.get(col, "")) for col in search_cols) for row in data]
    bm25 = BM25()
    bm25.fit(documents)
    ranked = bm25.score(query)
    results = []
    for idx, score in ranked[:max_results]:
        if score > 0:
            row = data[idx]
            results.append({col: row.get(col, "") for col in output_cols if col in row})
    return results


def detect_domain(query):
    query_lower = query.lower()
    domain_keywords = {
        "colors": ["color", "palette", "hex", "rgb", "tint", "semantic", "system color", "dark mode color", "accent"],
        "spacing": ["spacing", "padding", "margin", "gap", "grid", "inset"],
        "typography": ["font", "typography", "text", "type scale", "dynamic type", "sf pro", "heading", "body text", "caption"],
        "elevation": ["shadow", "elevation", "blur", "material", "vibrancy", "depth", "glass"],
        "corners": ["corner", "radius", "rounded", "squircle", "continuous"],
        "navigation": ["navigation", "navbar", "tab bar", "toolbar", "sidebar"],
        "controls": ["button", "toggle", "switch", "slider", "stepper", "picker", "segmented"],
        "content": ["list", "cell", "card", "grid", "collection", "table"],
        "feedback": ["alert", "sheet", "modal", "toast", "progress", "action sheet", "popover"],
        "input": ["text field", "search bar", "form", "input", "secure field"],
        "animation": ["animation", "spring", "transition", "motion", "easing", "bounce"],
        "gestures": ["gesture", "swipe", "pinch", "drag", "long press", "tap"],
        "layout": ["layout", "safe area", "hierarchy", "stack", "split view"],
        "interaction": ["haptic", "feedback", "progressive disclosure", "pull to refresh"],
        "audit": ["audit", "check", "compliance", "score", "review"]
    }
    scores = {domain: sum(1 for kw in keywords if kw in query_lower) for domain, keywords in domain_keywords.items()}
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "foundations"


def search(query, domain=None, max_results=MAX_RESULTS, platform=None):
    if domain is None:
        domain = detect_domain(query)

    # Map "foundations" fallback to colors
    if domain == "foundations":
        domain = "colors"

    config = CSV_CONFIG.get(domain)
    if not config:
        return {"error": f"Unknown domain: {domain}", "available": list(CSV_CONFIG.keys())}

    filepath = DATA_DIR / config["file"]
    if not filepath.exists():
        return {"domain": domain, "query": query, "count": 0, "results": [],
                "warning": f"Data file not found: {config['file']}"}

    results = _search_csv(filepath, config["search_cols"], config["output_cols"], query, max_results)

    # Filter by platform if specified
    if platform and results:
        results = [r for r in results if r.get("platform", "all") in (platform, "all")]

    return {"domain": domain, "query": query, "count": len(results), "results": results}


def search_platform(query, platform, max_results=MAX_RESULTS):
    if platform not in PLATFORM_CONFIG:
        return {"error": f"Unknown platform: {platform}. Available: {', '.join(AVAILABLE_PLATFORMS)}"}
    filepath = DATA_DIR / PLATFORM_CONFIG[platform]["file"]
    if not filepath.exists():
        return {"error": f"Platform file not found: {filepath}", "platform": platform}
    results = _search_csv(filepath, _PLATFORM_COLS["search_cols"], _PLATFORM_COLS["output_cols"], query, max_results)
    return {"domain": "platform", "platform": platform, "query": query, "count": len(results), "results": results}


def search_stack(query, stack, max_results=MAX_RESULTS):
    if stack not in STACK_CONFIG:
        return {"error": f"Unknown stack: {stack}. Available: {', '.join(AVAILABLE_STACKS)}"}
    filepath = DATA_DIR / STACK_CONFIG[stack]["file"]
    if not filepath.exists():
        return {"error": f"Stack file not found: {filepath}", "stack": stack}
    results = _search_csv(filepath, _STACK_COLS["search_cols"], _STACK_COLS["output_cols"], query, max_results)
    return {"domain": "stack", "stack": stack, "query": query, "count": len(results), "results": results}
```

- [ ] **Step 5: Run tests to verify they pass**

```bash
python3 -m pytest tests/test_search.py -v
```
Expected: All 8 tests pass

- [ ] **Step 6: Commit**

```bash
git add scripts/core.py tests/test_search.py data/foundations/colors.csv
git commit -m "feat: add CSV config, search functions, domain detection"
```

---

### Task 3: Foundations CSV data (colors, spacing, typography, elevation, corners)

**Files:**
- Create: `data/foundations/colors.csv` (expand from test data)
- Create: `data/foundations/spacing.csv`
- Create: `data/foundations/typography.csv`
- Create: `data/foundations/elevation.csv`
- Create: `data/foundations/corners.csv`

All values from the spec's Deep Research Findings section. This is a data-authoring task — no Python code changes.

- [ ] **Step 1: Create full colors.csv**

Populate with all Apple system colors (9 system + 6 grays + 4 labels + 4 fills + 6 backgrounds + separators) from spec section "Complete Color System". Each row needs: keyword, name, light_hex, dark_hex, usage, semantic_role, platform.

~40 rows total.

- [ ] **Step 2: Create spacing.csv**

Values from spec: 2, 4, 8, 12, 16, 20, 24, 32, 40, 48pt. Plus component-specific spacing (card padding 16pt, section spacing 32pt, icon-to-label 4pt, etc).

~20 rows. Columns: keyword, name, value_pt, value_px, usage, platform, priority.

- [ ] **Step 3: Create typography.csv**

All iOS text styles (13 styles from extraLargeTitle to caption2) + macOS text styles (9 styles). Include size, weight, tracking, line_height.

~25 rows. Columns: keyword, style_name, size_pt, weight, tracking, line_height, font_family, platform, priority.

- [ ] **Step 4: Create elevation.csv**

Apple materials (ultraThinMaterial through chrome), shadow levels, vibrancy levels, Liquid Glass variants.

~15 rows. Columns: keyword, name, blur, opacity, color, offset_y, material, platform.

- [ ] **Step 5: Create corners.csv**

UI component corner radii (buttons 12pt, cards 16-24pt, alerts 14pt, sheets 10-21pt, toggle 16pt, text fields 8-10pt). Include app icon formula note.

~12 rows. Columns: keyword, component, radius_pt, style, usage, platform.

- [ ] **Step 6: Run search tests against new data**

```bash
python3 -m pytest tests/ -v
```
Expected: All pass (colors test now has full data)

- [ ] **Step 7: Commit**

```bash
git add data/foundations/
git commit -m "feat: add Apple HIG foundations data (colors, spacing, typography, elevation, corners)"
```

---

### Task 4: Components CSV data (navigation, controls, content, feedback, input)

**Files:**
- Create: `data/components/navigation.csv`
- Create: `data/components/controls.csv`
- Create: `data/components/content.csv`
- Create: `data/components/feedback.csv`
- Create: `data/components/input.csv`

- [ ] **Step 1: Create navigation.csv**

Navigation bars (44pt inline, 96pt large title), tab bars (49pt + 34pt safe area), toolbars, sidebars. Platform-specific heights.

~15 rows. Columns: keyword, component, variant, height_pt, usage, platform, priority.

- [ ] **Step 2: Create controls.csv**

Buttons (filled/tinted/bordered/plain, 50pt height, 12pt radius), toggles (31pt height, 51pt width), sliders, steppers, pickers, segmented controls.

~20 rows. Columns: keyword, component, variant, height_pt, corner_radius, font_weight, font_size, padding_h, states, platform, priority.

- [ ] **Step 3: Create content.csv**

Lists (inset grouped, sidebar, plain), cells (44pt standard, 60pt subtitle), cards, grids, collections.

~15 rows. Columns: keyword, component, variant, height_pt, usage, platform, priority.

- [ ] **Step 4: Create feedback.csv**

Alerts (14pt radius), action sheets (13pt radius), sheets (modal/formSheet/fullScreen/pageSheet), toasts, progress indicators.

~12 rows. Columns: keyword, component, variant, corner_radius, usage, platform, priority.

- [ ] **Step 5: Create input.csv**

Text fields (44pt min height, 8-10pt radius), search bars, secure fields, forms with labels.

~10 rows. Columns: keyword, component, variant, height_pt, corner_radius, usage, platform, priority.

- [ ] **Step 6: Test component search**

```bash
cd ~/Desktop/Projects/onemore
python3 -c "from scripts.core import search; r = search('button toggle', domain='controls'); print(r['count'], 'results'); [print(x.get('component',''), x.get('variant','')) for x in r['results']]"
```
Expected: Results for button and toggle components

- [ ] **Step 7: Commit**

```bash
git add data/components/
git commit -m "feat: add Apple HIG components data (navigation, controls, content, feedback, input)"
```

---

### Task 5: Patterns CSV data (animation, gestures, layout, interaction)

**Files:**
- Create: `data/patterns/animation.csv`
- Create: `data/patterns/gestures.csv`
- Create: `data/patterns/layout.csv`
- Create: `data/patterns/interaction.csv`

- [ ] **Step 1: Create animation.csv**

iOS 17+ presets (.smooth, .snappy, .bouncy, .interactive) + tuned use-case values (button press, card expansion, sheet, keyboard). From spec "Animation Presets" section.

~12 rows. Columns: keyword, name, type, response, damping_fraction, blend_duration, usage, source, platform.

- [ ] **Step 2: Create gestures.csv**

Swipe actions, pinch-to-zoom, long press, drag & drop, rotation, edge pan (back navigation), double-tap (watchOS).

~10 rows. Columns: keyword, name, type, min_duration, usage, platform, priority.

- [ ] **Step 3: Create layout.csv**

Navigation stack, tab-based, split view, sidebar, disclosure groups, safe areas, dynamic island avoidance.

~12 rows. Columns: keyword, pattern, description, usage, platform, priority.

- [ ] **Step 4: Create interaction.csv**

Haptic feedback (impact light/medium/heavy, notification success/warning/error, selection), progressive disclosure, pull-to-refresh, rubber banding.

~12 rows. Columns: keyword, name, type, description, usage, platform, priority.

- [ ] **Step 5: Test pattern search**

```bash
python3 -c "from scripts.core import search; r = search('spring animation bounce', domain='animation'); print(r['count'], 'results'); [print(x.get('name',''), x.get('response',''), x.get('damping_fraction','')) for x in r['results']]"
```

- [ ] **Step 6: Commit**

```bash
git add data/patterns/
git commit -m "feat: add Apple HIG patterns data (animation, gestures, layout, interaction)"
```

---

### Task 6: Platform CSV data (ios, macos, watchos, visionos, web-apple)

**Files:**
- Create: `data/platforms/ios.csv`
- Create: `data/platforms/macos.csv`
- Create: `data/platforms/watchos.csv`
- Create: `data/platforms/visionos.csv`
- Create: `data/platforms/web-apple.csv`

- [ ] **Step 1: Create ios.csv**

Navbar heights, tab bar, status bar, safe areas, Dynamic Island, home indicator, touch targets 44pt, screen dimensions.

~20 rows. Columns: keyword, element, metric, value, unit, context, min_os, priority.

- [ ] **Step 2: Create macos.csv**

Menu bar, title bar, traffic lights, sidebar widths, toolbar heights, window chrome, keyboard shortcuts, mouse vs trackpad.

~15 rows. Columns: keyword, element, metric, value, unit, context, min_os, priority.

- [ ] **Step 3: Create watchos.csv**

Screen dimensions per model, Digital Crown, complications, compact layouts, SF Compact font.

~10 rows.

- [ ] **Step 4: Create visionos.csv**

60pt touch targets, 4pt minimum spacing, vertical tab bar, ornaments, volumes, spatial layout, eye tracking.

~10 rows.

- [ ] **Step 5: Create web-apple.csv**

apple.com values: #1d1d1f text, #fbfbfd background, #86868b secondary, #2997ff link, backdrop-filter blur, font stack, hero sizes, section padding, transition easing.

~20 rows. Columns: keyword, pattern, implementation, anti_pattern, notes, priority.

- [ ] **Step 6: Test platform search**

```bash
python3 -c "from scripts.core import search_platform; r = search_platform('navigation bar height', 'ios'); print(r['count'], 'results'); [print(x.get('element',''), x.get('value',''), x.get('unit','')) for x in r['results']]"
```

- [ ] **Step 7: Commit**

```bash
git add data/platforms/
git commit -m "feat: add platform-specific data (iOS, macOS, watchOS, visionOS, web)"
```

---

### Task 7: Tier 1 stack CSV data (swiftui, react, react-native, html-tailwind)

**Files:**
- Create: `data/stacks/swiftui.csv`
- Create: `data/stacks/react.csv`
- Create: `data/stacks/react-native.csv`
- Create: `data/stacks/html-tailwind.csv`

All stacks use columns: keyword, pattern, implementation, anti_pattern, notes, priority.

- [ ] **Step 1: Create swiftui.csv**

Apple-native patterns: .font(.body), Color.accentColor, .cornerRadius with .continuous, .spring() animations, NavigationStack, .sheet(), .alert(), @Observable, .sensoryFeedback(). ~30 rows.

- [ ] **Step 2: Create react.csv**

Apple aesthetic on React: CSS custom properties for Apple tokens, framer-motion spring animations, -apple-system font stack, Inter fallback, semantic color variables, dark mode via prefers-color-scheme. ~25 rows.

- [ ] **Step 3: Create react-native.csv**

borderCurve: 'continuous', expo-haptics, expo-symbols, Platform.select for iOS-specific, Animated.spring(), react-native-bottom-sheet for sheets. ~25 rows.

- [ ] **Step 4: Create html-tailwind.csv**

Tailwind config: Apple color tokens, spacing scale, font stack, backdrop-blur for nav, rounded-xl with squircle mask, transition-all duration-300. ~25 rows.

- [ ] **Step 5: Test stack search**

```bash
python3 -c "from scripts.core import search_stack; r = search_stack('spring animation', 'swiftui'); print(r['count'], 'results'); [print(x.get('pattern','')[:60]) for x in r['results']]"
```

- [ ] **Step 6: Commit**

```bash
git add data/stacks/
git commit -m "feat: add Tier 1 stack data (SwiftUI, React, React Native, HTML/Tailwind)"
```

---

### Task 8: Audit checklist and reasoning data

**Files:**
- Create: `data/audit/hig-checklist.csv`
- Create: `data/reasoning/apple-reasoning.csv`

- [ ] **Step 1: Create hig-checklist.csv**

From spec Pre-Delivery Checklist + expanded HIG rules. Categories: spacing, typography, color, touch, animation, corners, accessibility, components.

~30 rows. Columns: keyword, rule_id, category, description, check_instruction, severity, weight.

- [ ] **Step 2: Create apple-reasoning.csv**

Apple app categories mapped to HIG patterns. Categories: Health, Finance, Social, Productivity, Media, Navigation, Weather, Camera, Shopping, Gaming.

Each maps to: navigation style, component choices, color approach, animation feel, platform specifics.

~15 rows. Columns: category, recommended_navigation, style_priority, color_approach, typography_mood, key_patterns, anti_patterns, decision_rules.

- [ ] **Step 3: Test audit search**

```bash
python3 -c "from scripts.core import search; r = search('spacing grid alignment', domain='audit'); print(r['count'], 'results')"
```

- [ ] **Step 4: Commit**

```bash
git add data/audit/ data/reasoning/
git commit -m "feat: add HIG audit checklist and Apple app category reasoning"
```

---

### Task 9: search.py CLI entry point

**Files:**
- Create: `scripts/search.py`
- Create: `tests/test_cli.py`

- [ ] **Step 1: Write CLI tests**

```python
# tests/test_cli.py
import subprocess
import sys
from pathlib import Path

SCRIPT = str(Path(__file__).parent.parent / "scripts" / "search.py")

def run_cli(*args):
    result = subprocess.run([sys.executable, SCRIPT, *args], capture_output=True, text=True)
    return result

def test_help():
    r = run_cli("--help")
    assert r.returncode == 0
    assert "onemore" in r.stdout.lower() or "search" in r.stdout.lower()

def test_search_basic():
    r = run_cli("button toggle")
    assert r.returncode == 0

def test_search_domain():
    r = run_cli("blue accent", "--domain", "colors")
    assert r.returncode == 0

def test_search_stack():
    r = run_cli("spring animation", "--stack", "swiftui")
    assert r.returncode == 0

def test_search_platform():
    r = run_cli("navigation bar", "--platform", "ios")
    assert r.returncode == 0

def test_invalid_stack():
    r = run_cli("test", "--stack", "nonexistent")
    assert r.returncode != 0 or "error" in r.stdout.lower() or "unknown" in r.stdout.lower()
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
python3 -m pytest tests/test_cli.py -v
```
Expected: FileNotFoundError (search.py doesn't exist)

- [ ] **Step 3: Implement search.py**

```python
#!/usr/bin/env python3
"""OneMore CLI - Apple HIG Design Intelligence"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from core import search, search_stack, search_platform, AVAILABLE_STACKS, AVAILABLE_PLATFORMS, CSV_CONFIG

def format_output(result):
    """Format search results for display"""
    if "error" in result:
        print(f"Error: {result['error']}")
        return

    domain = result.get("domain", "")
    stack = result.get("stack", "")
    platform = result.get("platform", "")
    query = result.get("query", "")
    count = result.get("count", 0)

    header = f"OneMore | {domain}"
    if stack:
        header += f" ({stack})"
    if platform:
        header += f" ({platform})"
    header += f" | '{query}' | {count} result(s)"

    print(f"\n{'='*len(header)}")
    print(header)
    print(f"{'='*len(header)}")

    if result.get("warning"):
        print(f"\n⚠ {result['warning']}")

    for i, item in enumerate(result.get("results", []), 1):
        print(f"\n--- Result {i} ---")
        for key, value in item.items():
            if value:
                val_str = str(value)[:200]
                print(f"  {key}: {val_str}")

    if count == 0:
        print("\nNo matching guidelines found. Try broader keywords or check --domain options.")
        print(f"Available domains: {', '.join(CSV_CONFIG.keys())}")


def main():
    parser = argparse.ArgumentParser(
        prog="onemore",
        description="OneMore - Apple HIG Design Intelligence"
    )
    parser.add_argument("query", nargs="?", default="", help="Search query")
    parser.add_argument("-d", "--domain", help=f"Search domain: {', '.join(CSV_CONFIG.keys())}")
    parser.add_argument("-s", "--stack", help=f"Stack: {', '.join(AVAILABLE_STACKS)}")
    parser.add_argument("-p", "--platform", help=f"Platform: {', '.join(AVAILABLE_PLATFORMS)}")
    parser.add_argument("-n", "--max-results", type=int, default=5, help="Max results (default: 5)")
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--design-system", action="store_true", help="Generate full design system")
    parser.add_argument("--project-name", help="Project name for design system")
    parser.add_argument("-f", "--format", choices=["ascii", "markdown"], default="ascii")
    parser.add_argument("--persist", action="store_true", help="Save design system to files")
    parser.add_argument("--page", help="Page-specific override")

    args = parser.parse_args()

    if not args.query and not args.design_system:
        parser.print_help()
        sys.exit(0)

    if args.design_system:
        # Design system generation (Task 10)
        try:
            from design_system import DesignSystemGenerator
            gen = DesignSystemGenerator()
            result = gen.generate(args.query, project_name=args.project_name)
            if args.json:
                print(json.dumps(result, indent=2))
            elif args.format == "markdown":
                print(gen.format_markdown(result))
            else:
                print(gen.format_ascii(result))
            if args.persist:
                gen.persist(result, args.project_name or "onemore-project", page=args.page)
        except ImportError:
            print("Design system generator not yet implemented. Use domain/stack/platform search.")
        sys.exit(0)

    # Stack search
    if args.stack:
        result = search_stack(args.query, args.stack, args.max_results)
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            format_output(result)
        sys.exit(0)

    # Platform search
    if args.platform and not args.domain:
        result = search_platform(args.query, args.platform, args.max_results)
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            format_output(result)
        sys.exit(0)

    # Domain search (with optional platform filter)
    result = search(args.query, domain=args.domain, max_results=args.max_results, platform=args.platform)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        format_output(result)


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run tests**

```bash
python3 -m pytest tests/test_cli.py -v
```
Expected: All pass

- [ ] **Step 5: Commit**

```bash
git add scripts/search.py tests/test_cli.py
git commit -m "feat: add CLI entry point with domain/stack/platform search"
```

---

### Task 10: Design system generator

**Files:**
- Create: `scripts/design_system.py`
- Create: `tests/test_design_system.py`

- [ ] **Step 1: Write design system test**

```python
# tests/test_design_system.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from design_system import DesignSystemGenerator

def test_generator_init():
    gen = DesignSystemGenerator()
    assert gen is not None

def test_generate_basic():
    gen = DesignSystemGenerator()
    result = gen.generate("health app dashboard", project_name="HealthKit Pro")
    assert "project_name" in result
    assert result["project_name"] == "HealthKit Pro"
    assert "foundations" in result
    assert "components" in result

def test_format_ascii():
    gen = DesignSystemGenerator()
    result = gen.generate("productivity app", project_name="TaskFlow")
    output = gen.format_ascii(result)
    assert "TaskFlow" in output
    assert len(output) > 100

def test_format_markdown():
    gen = DesignSystemGenerator()
    result = gen.generate("finance banking", project_name="WalletPro")
    output = gen.format_markdown(result)
    assert "# " in output
    assert "WalletPro" in output
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
python3 -m pytest tests/test_design_system.py -v
```
Expected: ImportError

- [ ] **Step 3: Implement design_system.py**

Adapt from ui-ux-pro-max's design_system.py structure. Key changes:
- Replace web patterns with Apple HIG patterns
- Search foundations (colors, spacing, typography) + components + patterns
- Load apple-reasoning.csv for app category matching
- Generate Apple design tokens instead of CSS variables
- Format with Apple-specific sections (Materials, SF Symbols, Dynamic Type, Haptics)

The generator should:
1. Match query to Apple app category via reasoning CSV
2. Search foundations (colors, typography, spacing)
3. Search relevant components
4. Search animation/interaction patterns
5. Assemble into design system dict
6. Format as ASCII box or Markdown

~200 lines of Python. Follow the same class pattern as ui-ux-pro-max's DesignSystemGenerator.

- [ ] **Step 4: Run tests**

```bash
python3 -m pytest tests/test_design_system.py -v
```
Expected: All pass

- [ ] **Step 5: Test end-to-end via CLI**

```bash
python3 scripts/search.py "health app dashboard" --design-system -p "HealthKit Pro"
python3 scripts/search.py "social media feed" --design-system -p "Connect" -f markdown
```

- [ ] **Step 6: Commit**

```bash
git add scripts/design_system.py tests/test_design_system.py
git commit -m "feat: add Apple HIG design system generator"
```

---

### Task 11: SKILL.md and VERSION

**Files:**
- Create: `SKILL.md`
- Create: `VERSION`
- Create: `sync/hig-changelog.md`

- [ ] **Step 1: Create SKILL.md**

Full skill file with:
- Frontmatter (name: onemore, description with comprehensive trigger keywords)
- Apple HIG core principles
- Priority rules table
- Quick reference (most critical rules per category)
- CLI workflow (Step 1-4)
- Font licensing note
- Pre-delivery checklist
- Anti-patterns table

Content from spec section "SKILL.md Content".

- [ ] **Step 2: Create VERSION**

```
1.0.0
```

- [ ] **Step 3: Create hig-changelog.md**

```markdown
# HIG Changelog

## 1.0.0 — 2026-03-22 (iOS 18 / macOS 15 / iOS 26 Liquid Glass)
- Initial data created from Apple HIG documentation
- Sources: developer.apple.com/design/human-interface-guidelines/, Flutter Cupertino source, Apple Design Resources Figma
- Includes Liquid Glass (iOS 26) preliminary data
```

- [ ] **Step 4: Test the skill can be found**

```bash
ls -la ~/Desktop/Projects/onemore/SKILL.md
head -5 ~/Desktop/Projects/onemore/SKILL.md
```

- [ ] **Step 5: Commit**

```bash
git add SKILL.md VERSION sync/
git commit -m "feat: add SKILL.md entry point, VERSION tracking, HIG changelog"
```

---

### Task 12: Integration testing and cleanup

**Files:**
- Create: `tests/test_integration.py`
- Modify: various (fixes from testing)

- [ ] **Step 1: Write integration tests**

```python
# tests/test_integration.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from core import search, search_stack, search_platform, detect_domain

def test_full_workflow_colors():
    """Search colors, get results with hex values"""
    r = search("blue accent interactive", domain="colors")
    assert r["count"] > 0
    assert any("#" in str(v) for item in r["results"] for v in item.values())

def test_full_workflow_stack():
    """Search SwiftUI stack for animation guidance"""
    r = search_stack("spring animation", "swiftui")
    assert r["count"] > 0

def test_full_workflow_platform():
    """Search iOS platform for navbar metrics"""
    r = search_platform("navigation bar", "ios")
    assert r["count"] > 0

def test_cross_domain_consistency():
    """Same concept should be findable across domains"""
    r1 = search("button", domain="controls")
    r2 = search("button", domain="corners")
    # Button should appear in both controls and corners
    assert r1["count"] > 0 or r2["count"] > 0

def test_all_domains_loadable():
    """Every configured domain should load without error"""
    from core import CSV_CONFIG, DATA_DIR
    for domain, config in CSV_CONFIG.items():
        filepath = DATA_DIR / config["file"]
        if filepath.exists():
            r = search("test", domain=domain)
            assert "error" not in r, f"Domain {domain} returned error"

def test_all_tier1_stacks_loadable():
    """Tier 1 stacks should all work"""
    for stack in ["swiftui", "react", "react-native", "html-tailwind"]:
        r = search_stack("layout", stack)
        assert "error" not in r, f"Stack {stack} returned error: {r.get('error')}"

def test_all_platforms_loadable():
    """All platforms should load"""
    for platform in ["ios", "macos", "watchos", "visionos", "web"]:
        r = search_platform("layout", platform)
        assert "error" not in r, f"Platform {platform} returned error: {r.get('error')}"
```

- [ ] **Step 2: Run full test suite**

```bash
cd ~/Desktop/Projects/onemore
python3 -m pytest tests/ -v --tb=short
```

- [ ] **Step 3: Fix any failures**

Address test failures by fixing CSV data or search logic.

- [ ] **Step 4: Run final validation**

```bash
python3 -m pytest tests/ -v
python3 scripts/search.py "button" -d controls
python3 scripts/search.py "spring animation" -s swiftui
python3 scripts/search.py "navigation bar" -p ios
python3 scripts/search.py "health fitness" --design-system -p "FitTrack"
```

- [ ] **Step 5: Commit**

```bash
git add tests/test_integration.py
git commit -m "feat: add integration tests, complete OneMore v1.0.0"
```

---

### Task 13: Install as Claude Code skill

**Files:**
- No new files — copy/symlink to Claude Code skills directory

- [ ] **Step 1: Symlink to Claude Code skills**

```bash
ln -sf ~/Desktop/Projects/onemore ~/.claude/skills/onemore
```

- [ ] **Step 2: Verify skill is discoverable**

```bash
ls -la ~/.claude/skills/onemore/SKILL.md
head -4 ~/.claude/skills/onemore/SKILL.md
```

- [ ] **Step 3: Test skill invocation**

In Claude Code, ask: "Design a settings screen for a health app using onemore"

Verify the skill triggers and generates Apple HIG-compliant recommendations.

- [ ] **Step 4: Final commit with any fixes**

```bash
cd ~/Desktop/Projects/onemore
git add -A
git commit -m "chore: finalize OneMore v1.0.0 installation"
```
