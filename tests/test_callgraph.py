"""Tests for L2 CallGraphAnalyzer."""

from __future__ import annotations

from pathlib import Path

from agentwall.adapters.langchain import LangChainAdapter
from agentwall.analyzers.callgraph import CallGraphAnalyzer, build_call_graph
from agentwall.analyzers.memory import MemoryAnalyzer
from agentwall.context import AnalysisContext
from agentwall.models import AgentSpec, Finding, ScanConfig

FIXTURES_CROSS = Path(__file__).parent / "fixtures" / "langchain_cross_file"
FIXTURES_UNSAFE = Path(__file__).parent / "fixtures" / "langchain_unsafe"


def _ctx(
    spec: AgentSpec,
    target: Path,
    findings: list[Finding] | None = None,
) -> AnalysisContext:
    ctx = AnalysisContext(target=target, config=ScanConfig.default())
    ctx.spec = spec
    if findings is not None:
        ctx.findings = findings
    return ctx


class TestBuildCallGraph:
    def test_builds_graph_from_cross_file_fixture(self) -> None:
        spec = LangChainAdapter().parse(FIXTURES_CROSS)
        graph = build_call_graph(FIXTURES_CROSS, spec.source_files)
        assert len(graph.edges) > 0

    def test_resolves_function_calls(self) -> None:
        spec = LangChainAdapter().parse(FIXTURES_CROSS)
        graph = build_call_graph(FIXTURES_CROSS, spec.source_files)
        # do_search should be called somewhere
        callee_names = [e.callee.name for e in graph.edges]
        assert any("do_search" in name for name in callee_names)

    def test_handles_empty_project(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            graph = build_call_graph(Path(tmp), [])
            assert graph.edges == []


class TestCallGraphAnalyzer:
    def test_processes_l1_findings(self) -> None:
        spec = LangChainAdapter().parse(FIXTURES_UNSAFE)
        l1 = MemoryAnalyzer().analyze(_ctx(spec, FIXTURES_UNSAFE))
        l2 = CallGraphAnalyzer()
        refined = l2.analyze(_ctx(spec, FIXTURES_UNSAFE, findings=l1))
        # Should still have findings (no filter found in call chain)
        assert len(refined) >= len(l1)

    def test_annotates_findings_with_l2_layer(self) -> None:
        spec = LangChainAdapter().parse(FIXTURES_UNSAFE)
        l1 = MemoryAnalyzer().analyze(_ctx(spec, FIXTURES_UNSAFE))
        # Filter only MEM-001 findings for L2 analysis
        mem001 = [f for f in l1 if f.rule_id == "AW-MEM-001"]
        l2 = CallGraphAnalyzer()
        refined = l2.analyze(_ctx(spec, FIXTURES_UNSAFE, findings=mem001))
        for f in refined:
            if f.rule_id == "AW-MEM-001":
                assert f.layer == "L2"

    def test_passthrough_non_mem001_findings(self) -> None:
        spec = LangChainAdapter().parse(FIXTURES_UNSAFE)
        l1 = MemoryAnalyzer().analyze(_ctx(spec, FIXTURES_UNSAFE))
        l2 = CallGraphAnalyzer()
        refined = l2.analyze(_ctx(spec, FIXTURES_UNSAFE, findings=l1))
        # Non-MEM-001 findings should pass through unchanged
        non_mem001 = [f for f in refined if f.rule_id != "AW-MEM-001"]
        original_non_mem001 = [f for f in l1 if f.rule_id != "AW-MEM-001"]
        assert len(non_mem001) == len(original_non_mem001)
