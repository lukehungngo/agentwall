"""Tests for MemoryAnalyzer."""

from __future__ import annotations

from agentwall.analyzers.memory import MemoryAnalyzer
from agentwall.models import AgentSpec, MemoryConfig, Severity


def _spec(mc: MemoryConfig) -> AgentSpec:
    return AgentSpec(framework="langchain", memory_configs=[mc])


class TestMemoryAnalyzerMEM001:
    def test_fires_when_no_isolation_no_filter(self) -> None:
        mc = MemoryConfig(backend="chroma")
        findings = MemoryAnalyzer().analyze(_spec(mc))
        rule_ids = [f.rule_id for f in findings]
        assert "AW-MEM-001" in rule_ids

    def test_severity_is_critical(self) -> None:
        mc = MemoryConfig(backend="chroma")
        findings = MemoryAnalyzer().analyze(_spec(mc))
        mem001 = next(f for f in findings if f.rule_id == "AW-MEM-001")
        assert mem001.severity == Severity.CRITICAL

    def test_does_not_fire_when_filter_present(self) -> None:
        mc = MemoryConfig(backend="chroma", has_metadata_filter_on_retrieval=True)
        findings = MemoryAnalyzer().analyze(_spec(mc))
        rule_ids = [f.rule_id for f in findings]
        assert "AW-MEM-001" not in rule_ids


class TestMemoryAnalyzerMEM002:
    def test_fires_when_write_meta_but_no_retrieval_filter(self) -> None:
        mc = MemoryConfig(backend="chroma", has_metadata_on_write=True)
        findings = MemoryAnalyzer().analyze(_spec(mc))
        rule_ids = [f.rule_id for f in findings]
        assert "AW-MEM-002" in rule_ids

    def test_does_not_fire_when_retrieval_filter_also_present(self) -> None:
        mc = MemoryConfig(
            backend="chroma",
            has_metadata_on_write=True,
            has_metadata_filter_on_retrieval=True,
        )
        findings = MemoryAnalyzer().analyze(_spec(mc))
        rule_ids = [f.rule_id for f in findings]
        assert "AW-MEM-002" not in rule_ids


class TestMemoryAnalyzerMEM003:
    def test_fires_when_no_access_control_at_all(self) -> None:
        mc = MemoryConfig(backend="chroma")
        findings = MemoryAnalyzer().analyze(_spec(mc))
        rule_ids = [f.rule_id for f in findings]
        assert "AW-MEM-003" in rule_ids

    def test_does_not_fire_when_write_meta_present(self) -> None:
        mc = MemoryConfig(backend="chroma", has_metadata_on_write=True)
        findings = MemoryAnalyzer().analyze(_spec(mc))
        rule_ids = [f.rule_id for f in findings]
        assert "AW-MEM-003" not in rule_ids

    def test_does_not_fire_on_safe_config(self) -> None:
        mc = MemoryConfig(
            backend="chroma",
            has_tenant_isolation=True,
            has_metadata_filter_on_retrieval=True,
            has_metadata_on_write=True,
            sanitizes_retrieved_content=True,
        )
        findings = MemoryAnalyzer().analyze(_spec(mc))
        assert findings == []


class TestMemoryAnalyzerMEM004:
    def test_fires_when_injection_risk(self) -> None:
        mc = MemoryConfig(backend="conversation_buffer", has_injection_risk=True)
        findings = MemoryAnalyzer().analyze(_spec(mc))
        rule_ids = [f.rule_id for f in findings]
        assert "AW-MEM-004" in rule_ids

    def test_severity_is_high(self) -> None:
        mc = MemoryConfig(backend="conversation_buffer", has_injection_risk=True)
        findings = MemoryAnalyzer().analyze(_spec(mc))
        mem004 = next(f for f in findings if f.rule_id == "AW-MEM-004")
        assert mem004.severity == Severity.HIGH

    def test_does_not_fire_when_no_injection_risk(self) -> None:
        mc = MemoryConfig(
            backend="chroma",
            has_tenant_isolation=True,
            has_metadata_filter_on_retrieval=True,
            sanitizes_retrieved_content=True,
        )
        findings = MemoryAnalyzer().analyze(_spec(mc))
        rule_ids = [f.rule_id for f in findings]
        assert "AW-MEM-004" not in rule_ids


class TestMemoryAnalyzerMEM005:
    def test_fires_when_no_sanitization(self) -> None:
        mc = MemoryConfig(backend="chroma", sanitizes_retrieved_content=False)
        findings = MemoryAnalyzer().analyze(_spec(mc))
        rule_ids = [f.rule_id for f in findings]
        assert "AW-MEM-005" in rule_ids

    def test_severity_is_medium(self) -> None:
        mc = MemoryConfig(backend="chroma")
        findings = MemoryAnalyzer().analyze(_spec(mc))
        mem005 = next(f for f in findings if f.rule_id == "AW-MEM-005")
        assert mem005.severity == Severity.MEDIUM

    def test_does_not_fire_when_sanitized(self) -> None:
        mc = MemoryConfig(
            backend="chroma",
            has_tenant_isolation=True,
            has_metadata_filter_on_retrieval=True,
            sanitizes_retrieved_content=True,
        )
        findings = MemoryAnalyzer().analyze(_spec(mc))
        rule_ids = [f.rule_id for f in findings]
        assert "AW-MEM-005" not in rule_ids


class TestMemoryAnalyzerCoFiring:
    def test_mem001_and_mem002_both_fire_on_write_meta_no_filter(self) -> None:
        mc = MemoryConfig(backend="chroma", has_metadata_on_write=True)
        findings = MemoryAnalyzer().analyze(_spec(mc))
        rule_ids = [f.rule_id for f in findings]
        assert "AW-MEM-001" in rule_ids
        assert "AW-MEM-002" in rule_ids

    def test_mem004_fires_but_not_mem001_on_memory_class(self) -> None:
        """Memory classes get MEM-004 but not MEM-001/002/003 (those target vector stores)."""
        mc = MemoryConfig(backend="conversation_buffer", has_injection_risk=True)
        findings = MemoryAnalyzer().analyze(_spec(mc))
        rule_ids = [f.rule_id for f in findings]
        assert "AW-MEM-004" in rule_ids
        assert "AW-MEM-001" not in rule_ids
        assert "AW-MEM-005" not in rule_ids


class TestMemoryAnalyzerNoFindingsOnSafe:
    def test_fully_safe_config_no_findings(self) -> None:
        mc = MemoryConfig(
            backend="chroma",
            has_tenant_isolation=True,
            has_metadata_filter_on_retrieval=True,
            has_metadata_on_write=True,
            sanitizes_retrieved_content=True,
        )
        findings = MemoryAnalyzer().analyze(_spec(mc))
        assert findings == []

    def test_empty_spec_returns_empty(self) -> None:
        spec = AgentSpec(framework="langchain")
        findings = MemoryAnalyzer().analyze(spec)
        assert findings == []
