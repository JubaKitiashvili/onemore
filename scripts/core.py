"""BM25 search engine and CSV-based design intelligence for Apple HIG."""
import csv
import math
import re
from pathlib import Path
from typing import Optional

DATA_DIR = Path(__file__).parent.parent / "data"
MAX_RESULTS = 5

# ---------------------------------------------------------------------------
# BM25 Search Engine (pure Python, zero deps)
# ---------------------------------------------------------------------------

class BM25:
    """Okapi BM25 ranking function."""

    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.n_docs = 0
        self.avg_dl = 0.0
        self.doc_lengths: list[int] = []
        self.doc_freqs: dict[str, int] = {}       # term -> num docs containing it
        self.term_freqs: list[dict[str, int]] = [] # per-doc term frequencies

    @staticmethod
    def tokenize(text: str) -> list[str]:
        """Lowercase, strip punctuation, filter words <= 2 chars."""
        text = text.lower()
        text = re.sub(r"[^\w\s]", "", text)
        return [w for w in text.split() if len(w) > 2]

    def fit(self, documents: list[str]) -> None:
        """Build the BM25 index from a list of document strings."""
        self.n_docs = len(documents)
        self.doc_lengths = []
        self.term_freqs = []
        self.doc_freqs = {}

        for doc in documents:
            tokens = self.tokenize(doc)
            self.doc_lengths.append(len(tokens))
            tf: dict[str, int] = {}
            for t in tokens:
                tf[t] = tf.get(t, 0) + 1
            self.term_freqs.append(tf)
            for t in set(tokens):
                self.doc_freqs[t] = self.doc_freqs.get(t, 0) + 1

        total = sum(self.doc_lengths)
        self.avg_dl = total / self.n_docs if self.n_docs else 0.0

    def score(self, query: str) -> list[float]:
        """Score all documents against a query. Returns list of floats."""
        tokens = self.tokenize(query)
        scores = [0.0] * self.n_docs
        for t in tokens:
            if t not in self.doc_freqs:
                continue
            df = self.doc_freqs[t]
            idf = math.log((self.n_docs - df + 0.5) / (df + 0.5) + 1.0)
            for i in range(self.n_docs):
                tf = self.term_freqs[i].get(t, 0)
                if tf == 0:
                    continue
                dl = self.doc_lengths[i]
                numerator = tf * (self.k1 + 1)
                denominator = tf + self.k1 * (1 - self.b + self.b * dl / self.avg_dl)
                scores[i] += idf * numerator / denominator
        return scores


# ---------------------------------------------------------------------------
# CSV Configuration
# ---------------------------------------------------------------------------

CSV_CONFIG = {
    "colors":     {"dir": "foundations", "file": "colors.csv"},
    "spacing":    {"dir": "foundations", "file": "spacing.csv"},
    "typography": {"dir": "foundations", "file": "typography.csv"},
    "elevation":  {"dir": "foundations", "file": "elevation.csv"},
    "corners":    {"dir": "foundations", "file": "corners.csv"},
    "navigation": {"dir": "components", "file": "navigation.csv"},
    "controls":   {"dir": "components", "file": "controls.csv"},
    "content":    {"dir": "components", "file": "content.csv"},
    "feedback":   {"dir": "components", "file": "feedback.csv"},
    "input":      {"dir": "components", "file": "input.csv"},
    "animation":  {"dir": "patterns",   "file": "animation.csv"},
    "gestures":   {"dir": "patterns",   "file": "gestures.csv"},
    "layout":     {"dir": "patterns",   "file": "layout.csv"},
    "interaction":{"dir": "patterns",   "file": "interaction.csv"},
    "audit":      {"dir": "audit",      "file": "audit.csv"},
}

PLATFORM_CONFIG = {
    "ios":       {"dir": "platforms", "file": "ios.csv"},
    "macos":     {"dir": "platforms", "file": "macos.csv"},
    "watchos":   {"dir": "platforms", "file": "watchos.csv"},
    "visionos":  {"dir": "platforms", "file": "visionos.csv"},
    "web":       {"dir": "platforms", "file": "web.csv"},
}

STACK_CONFIG = {
    "swiftui":        {"dir": "stacks", "file": "swiftui.csv"},
    "react":          {"dir": "stacks", "file": "react.csv"},
    "react-native":   {"dir": "stacks", "file": "react-native.csv"},
    "html-tailwind":  {"dir": "stacks", "file": "html-tailwind.csv"},
    "flutter":        {"dir": "stacks", "file": "flutter.csv"},
    "nextjs":         {"dir": "stacks", "file": "nextjs.csv"},
    "shadcn":         {"dir": "stacks", "file": "shadcn.csv"},
    "vue":            {"dir": "stacks", "file": "vue.csv"},
    "svelte":         {"dir": "stacks", "file": "svelte.csv"},
    "uikit":          {"dir": "stacks", "file": "uikit.csv"},
    "nuxtjs":         {"dir": "stacks", "file": "nuxtjs.csv"},
    "astro":          {"dir": "stacks", "file": "astro.csv"},
}

# ---------------------------------------------------------------------------
# Domain Detection Keywords
# ---------------------------------------------------------------------------

_DOMAIN_KEYWORDS: dict[str, list[str]] = {
    "colors":      ["color", "palette", "hex", "rgb", "tint", "semantic", "accent"],
    "spacing":     ["spacing", "padding", "margin", "gap", "grid", "inset"],
    "typography":  ["font", "typography", "text", "type scale", "dynamic type", "sf pro", "heading"],
    "elevation":   ["shadow", "elevation", "blur", "material", "vibrancy", "depth", "glass"],
    "corners":     ["corner", "radius", "rounded", "squircle", "continuous"],
    "navigation":  ["navigation", "navbar", "tab bar", "toolbar", "sidebar"],
    "controls":    ["button", "toggle", "switch", "slider", "stepper", "picker", "segmented"],
    "content":     ["list", "cell", "card", "grid", "collection", "table"],
    "feedback":    ["alert", "sheet", "modal", "toast", "progress", "action sheet", "popover"],
    "input":       ["text field", "search bar", "form", "input", "secure field"],
    "animation":   ["animation", "spring", "transition", "motion", "easing", "bounce"],
    "gestures":    ["gesture", "swipe", "pinch", "drag", "long press", "tap"],
    "layout":      ["layout", "safe area", "hierarchy", "stack", "split view"],
    "interaction": ["haptic", "feedback", "progressive disclosure", "pull to refresh"],
    "audit":       ["audit", "check", "compliance", "score", "review"],
}


# ---------------------------------------------------------------------------
# CSV Loading & Search Functions
# ---------------------------------------------------------------------------

def _load_csv(subdir: str, filename: str) -> list[dict[str, str]]:
    """Load a CSV file from DATA_DIR/subdir/filename. Returns list of row dicts."""
    path = DATA_DIR / subdir / filename
    if not path.exists():
        return []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def _search_csv(
    rows: list[dict[str, str]],
    query: str,
    max_results: int = MAX_RESULTS,
    platform: Optional[str] = None,
) -> list[dict[str, str]]:
    """BM25-rank CSV rows against a query. Optional platform filter."""
    if not rows:
        return []

    # Platform filter
    if platform:
        rows = [
            r for r in rows
            if r.get("platform", "all") in ("all", platform)
        ]
        if not rows:
            return []

    # Build searchable text from all fields per row
    docs = [" ".join(str(v) for v in row.values() if v is not None) for row in rows]

    bm25 = BM25()
    bm25.fit(docs)
    scores = bm25.score(query)

    # Pair scores with rows, filter zero-score, sort descending
    scored = [(s, row) for s, row in zip(scores, rows) if s > 0]
    scored.sort(key=lambda x: x[0], reverse=True)

    return [row for _, row in scored[:max_results]]


def detect_domain(query: str) -> str:
    """Detect which domain a query belongs to using keyword matching."""
    query_lower = query.lower()
    best_domain = "colors"  # default fallback
    best_count = 0
    for domain, keywords in _DOMAIN_KEYWORDS.items():
        count = sum(1 for kw in keywords if kw in query_lower)
        if count > best_count:
            best_count = count
            best_domain = domain
    return best_domain


def search(
    query: str,
    domain: Optional[str] = None,
    max_results: int = MAX_RESULTS,
    platform: Optional[str] = None,
) -> list[dict[str, str]]:
    """Search a domain's CSV data. Auto-detects domain if not specified."""
    if domain is None:
        domain = detect_domain(query)
    cfg = CSV_CONFIG.get(domain)
    if not cfg:
        return []
    rows = _load_csv(cfg["dir"], cfg["file"])
    return _search_csv(rows, query, max_results, platform)


def search_platform(
    query: str,
    platform: str,
    max_results: int = MAX_RESULTS,
) -> list[dict[str, str]]:
    """Search platform-specific CSV data."""
    cfg = PLATFORM_CONFIG.get(platform)
    if not cfg:
        return []
    rows = _load_csv(cfg["dir"], cfg["file"])
    return _search_csv(rows, query, max_results)


def search_stack(
    query: str,
    stack: str,
    max_results: int = MAX_RESULTS,
) -> list[dict[str, str]]:
    """Search stack-specific CSV data."""
    cfg = STACK_CONFIG.get(stack)
    if not cfg:
        return []
    rows = _load_csv(cfg["dir"], cfg["file"])
    return _search_csv(rows, query, max_results)
