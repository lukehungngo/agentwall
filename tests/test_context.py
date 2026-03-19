"""Tests for AnalysisContext and Analyzer protocol."""
from pathlib import Path

from agentwall.context import AnalysisContext, Analyzer
from agentwall.models import Category, Finding, ScanConfig, Severity


class TestAnalysisContext:
    def test_creates_with_defaults(self) -> None:
        ctx = AnalysisContext(target=Path("/tmp"), config=ScanConfig.default())
        assert ctx.spec is None
        assert ctx.call_graph is None
        assert ctx.taint_results is None
        assert ctx.findings == []
        assert ctx.errors == []

    def test_findings_mutable(self) -> None:
        ctx = AnalysisContext(target=Path("/tmp"), config=ScanConfig.default())
        ctx.findings.append(
            Finding(
                rule_id="TEST",
                title="t",
                severity=Severity.CRITICAL,
                category=Category.MEMORY,
                description="t",
            )
        )
        assert len(ctx.findings) == 1


class TestAnalyzerProtocol:
    def test_concrete_class_satisfies_protocol(self) -> None:
        """A class with name, depends_on, and analyze(ctx) satisfies Analyzer."""

        class FakeAnalyzer:
            name = "FAKE"
            depends_on: list[str] = []

            def analyze(self, ctx: AnalysisContext) -> list[Finding]:
                return []

        analyzer: Analyzer = FakeAnalyzer()
        result = analyzer.analyze(
            AnalysisContext(target=Path("/tmp"), config=ScanConfig.default())
        )
        assert result == []
