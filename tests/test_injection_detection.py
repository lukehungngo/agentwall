"""Tests for MEM-004/005 detection in LangChain adapter."""

from __future__ import annotations

from pathlib import Path

from agentwall.adapters.langchain import LangChainAdapter
from agentwall.analyzers.memory import MemoryAnalyzer

FIXTURES = Path(__file__).parent / "fixtures" / "langchain_injection"


class TestAdapterMemoryClassDetection:
    def test_detects_conversation_buffer_memory(self) -> None:
        spec = LangChainAdapter().parse(FIXTURES)
        backends = [mc.backend for mc in spec.memory_configs]
        assert "conversation_buffer" in backends

    def test_memory_class_has_injection_risk(self) -> None:
        spec = LangChainAdapter().parse(FIXTURES)
        mem_class_configs = [mc for mc in spec.memory_configs if mc.backend == "conversation_buffer"]
        assert len(mem_class_configs) >= 1
        assert mem_class_configs[0].has_injection_risk is True

    def test_vector_store_also_detected(self) -> None:
        spec = LangChainAdapter().parse(FIXTURES)
        backends = [mc.backend for mc in spec.memory_configs]
        assert "chroma" in backends


class TestMEM004FiringOnInjectionFixture:
    def test_mem004_fires_for_memory_class(self) -> None:
        spec = LangChainAdapter().parse(FIXTURES)
        findings = MemoryAnalyzer().analyze(spec)
        rule_ids = [f.rule_id for f in findings]
        assert "AW-MEM-004" in rule_ids

    def test_mem005_fires_for_no_sanitization(self) -> None:
        spec = LangChainAdapter().parse(FIXTURES)
        findings = MemoryAnalyzer().analyze(spec)
        rule_ids = [f.rule_id for f in findings]
        assert "AW-MEM-005" in rule_ids


class TestMEM004DoesNotFireOnSafe:
    def test_safe_fixture_no_mem004(self) -> None:
        safe = Path(__file__).parent / "fixtures" / "langchain_safe"
        spec = LangChainAdapter().parse(safe)
        findings = MemoryAnalyzer().analyze(spec)
        rule_ids = [f.rule_id for f in findings]
        assert "AW-MEM-004" not in rule_ids
