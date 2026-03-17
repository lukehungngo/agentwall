"""Tests for L8 ConfidenceScorer."""

from __future__ import annotations

from agentwall.analyzers.confidence import (
    ConfidenceScorer,
    _regex_score_collection,
    _regex_score_variable,
)
from agentwall.models import Category, ConfidenceLevel, Finding, Severity


def _make_finding(description: str = "test", **kwargs: object) -> Finding:
    return Finding(
        rule_id="AW-MEM-001",
        title="Test",
        severity=Severity.CRITICAL,
        category=Category.MEMORY,
        description=description,
        **kwargs,  # type: ignore[arg-type]
    )


class TestRegexHeuristic:
    def test_user_id_is_per_user(self) -> None:
        result = _regex_score_variable("user_id")
        assert result is not None
        assert result[0] == ConfidenceLevel.LOW

    def test_tenant_id_is_per_user(self) -> None:
        result = _regex_score_variable("tenant_id")
        assert result is not None
        assert result[0] == ConfidenceLevel.LOW

    def test_shared_is_shared(self) -> None:
        result = _regex_score_variable("shared_collection")
        assert result is not None
        assert result[0] == ConfidenceLevel.HIGH

    def test_global_is_shared(self) -> None:
        result = _regex_score_variable("global_store")
        assert result is not None
        assert result[0] == ConfidenceLevel.HIGH

    def test_ambiguous_returns_none(self) -> None:
        result = _regex_score_variable("data")
        assert result is None

    def test_collection_with_user(self) -> None:
        result = _regex_score_collection("user_documents")
        assert result is not None
        assert result[0] == ConfidenceLevel.LOW

    def test_collection_without_user(self) -> None:
        result = _regex_score_collection("shared_docs")
        assert result is None


class TestConfidenceScorer:
    def test_regex_resolves_user_id(self) -> None:
        finding = _make_finding(description="Filter uses user_id variable")
        scorer = ConfidenceScorer(allow_local_llm=False, allow_api=False)
        verdicts = scorer.score([finding])
        assert len(verdicts) == 1
        assert verdicts[0].scored_confidence == ConfidenceLevel.LOW
        assert verdicts[0].method == "regex"

    def test_unresolvable_keeps_original(self) -> None:
        finding = _make_finding(description="Vector store query without filter")
        scorer = ConfidenceScorer(allow_local_llm=False, allow_api=False)
        verdicts = scorer.score([finding])
        assert len(verdicts) == 1
        assert verdicts[0].method == "none"

    def test_apply_scores_updates_findings(self) -> None:
        finding = _make_finding(description="Filter uses user_id variable")
        scorer = ConfidenceScorer(allow_local_llm=False, allow_api=False)
        updated = scorer.apply_scores([finding])
        assert len(updated) == 1
        assert updated[0].confidence == ConfidenceLevel.LOW

    def test_apply_scores_preserves_unresolvable(self) -> None:
        finding = _make_finding(description="Some generic finding")
        scorer = ConfidenceScorer(allow_local_llm=False, allow_api=False)
        updated = scorer.apply_scores([finding])
        assert updated[0].confidence == finding.confidence
