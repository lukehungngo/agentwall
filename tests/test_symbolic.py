"""Tests for L6 SymbolicAnalyzer."""

from __future__ import annotations

from pathlib import Path

from agentwall.adapters.langchain import LangChainAdapter
from agentwall.analyzers.symbolic import FilterState, SymbolicAnalyzer, _join
from agentwall.context import AnalysisContext
from agentwall.models import AgentSpec, ScanConfig

FIXTURES_BRANCH = Path(__file__).parent / "fixtures" / "langchain_branching"
FIXTURES_SAFE = Path(__file__).parent / "fixtures" / "langchain_safe"


def _ctx(spec: AgentSpec, target: Path = Path("/tmp")) -> AnalysisContext:
    ctx = AnalysisContext(target=target, config=ScanConfig.default())
    ctx.spec = spec
    return ctx


class TestFilterStateLattice:
    def test_join_same_returns_same(self) -> None:
        assert _join(FilterState.FILTERED, FilterState.FILTERED) == FilterState.FILTERED
        assert _join(FilterState.UNFILTERED, FilterState.UNFILTERED) == FilterState.UNFILTERED

    def test_join_bottom_returns_other(self) -> None:
        assert _join(FilterState.BOTTOM, FilterState.FILTERED) == FilterState.FILTERED
        assert _join(FilterState.FILTERED, FilterState.BOTTOM) == FilterState.FILTERED

    def test_join_filtered_unfiltered_returns_top(self) -> None:
        assert _join(FilterState.FILTERED, FilterState.UNFILTERED) == FilterState.TOP

    def test_join_with_top(self) -> None:
        assert _join(FilterState.TOP, FilterState.FILTERED) == FilterState.TOP
        assert _join(FilterState.UNFILTERED, FilterState.TOP) == FilterState.TOP


class TestSymbolicAnalyzer:
    def test_detects_mixed_paths(self) -> None:
        """search_mixed_paths has filter on admin path only → should flag."""
        spec = LangChainAdapter().parse(FIXTURES_BRANCH)
        findings = SymbolicAnalyzer().analyze(_ctx(spec, FIXTURES_BRANCH))
        # Should detect the mixed-path function
        descriptions = [f.description for f in findings]
        assert any("search_mixed_paths" in d for d in descriptions)

    def test_mixed_path_finding_has_high_or_critical(self) -> None:
        spec = LangChainAdapter().parse(FIXTURES_BRANCH)
        findings = SymbolicAnalyzer().analyze(_ctx(spec, FIXTURES_BRANCH))
        mixed = [f for f in findings if "search_mixed_paths" in f.description]
        assert len(mixed) >= 1
        # Mixed paths should be HIGH (TOP state)
        assert mixed[0].severity.value in {"high", "critical"}

    def test_always_filtered_not_flagged(self) -> None:
        """search_always_filtered has filter on all paths → should NOT be flagged."""
        spec = LangChainAdapter().parse(FIXTURES_BRANCH)
        findings = SymbolicAnalyzer().analyze(_ctx(spec, FIXTURES_BRANCH))
        always_filtered = [f for f in findings if "search_always_filtered" in f.description]
        assert len(always_filtered) == 0

    def test_layer_is_l6(self) -> None:
        spec = LangChainAdapter().parse(FIXTURES_BRANCH)
        findings = SymbolicAnalyzer().analyze(_ctx(spec, FIXTURES_BRANCH))
        for f in findings:
            assert f.layer == "L6"

    def test_no_findings_on_safe_fixture(self) -> None:
        spec = LangChainAdapter().parse(FIXTURES_SAFE)
        findings = SymbolicAnalyzer().analyze(_ctx(spec, FIXTURES_SAFE))
        # Safe fixture has filter on retrieval — no symbolic findings
        unfiltered = [f for f in findings if f.severity.value == "critical"]
        assert len(unfiltered) == 0
