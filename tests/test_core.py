"""Tests for BM25 search engine in scripts/core.py."""
import pytest
from scripts.core import BM25


class TestTokenize:
    def test_tokenize_basic(self):
        bm25 = BM25()
        tokens = bm25.tokenize("Hello World Testing")
        assert tokens == ["hello", "world", "testing"]

    def test_tokenize_removes_short_words(self):
        bm25 = BM25()
        tokens = bm25.tokenize("I am a big test of it")
        # Words with len <= 2 removed: "I", "am", "a", "of", "it"
        assert tokens == ["big", "test"]

    def test_tokenize_strips_punctuation(self):
        bm25 = BM25()
        tokens = bm25.tokenize("Hello, world! This is a test.")
        assert tokens == ["hello", "world", "this", "test"]


class TestBM25FitAndScore:
    def test_fit_builds_index(self):
        bm25 = BM25()
        docs = ["the quick brown fox", "the lazy brown dog", "fox jumps over dog"]
        bm25.fit(docs)
        assert bm25.n_docs == 3
        assert len(bm25.doc_lengths) == 3

    def test_score_returns_ranked_results(self):
        bm25 = BM25()
        docs = ["the quick brown fox", "the lazy brown dog", "fox jumps over dog"]
        bm25.fit(docs)
        scores = bm25.score("fox")
        # docs 0 and 2 contain "fox", doc 1 does not
        assert scores[0] > 0
        assert scores[1] == 0.0
        assert scores[2] > 0

    def test_score_empty_query(self):
        bm25 = BM25()
        bm25.fit(["hello world"])
        scores = bm25.score("a")  # filtered out (len <= 2)
        assert scores == [0.0]
