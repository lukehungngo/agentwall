"""Benchmark suite — detection quality tests for AgentWall.

Tests true positive and false positive rates across fixture repos.
Each rule is tested against known-vulnerable and known-safe fixtures.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from agentwall.models import Severity
from agentwall.scanner import scan

FIXTURES = Path(__file__).parent / "fixtures"


# ── True Positive Tests ──────────────────────────────────────────────────────
# These fixtures SHOULD trigger specific rules.


class TestTruePositives:
    """Verify that vulnerable fixtures trigger the expected rules."""

    def test_unsafe_triggers_mem001(self) -> None:
        """langchain_unsafe has unfiltered similarity_search -> AW-MEM-001."""
        result = scan(FIXTURES / "langchain_unsafe")
        rule_ids = {f.rule_id for f in result.findings}
        assert "AW-MEM-001" in rule_ids

    def test_unsafe_triggers_mem003(self) -> None:
        """langchain_unsafe has no access control -> AW-MEM-003."""
        result = scan(FIXTURES / "langchain_unsafe")
        rule_ids = {f.rule_id for f in result.findings}
        assert "AW-MEM-003" in rule_ids

    def test_unsafe_triggers_tool001(self) -> None:
        """langchain_unsafe has destructive tools without approval -> AW-TOOL-001."""
        result = scan(FIXTURES / "langchain_unsafe")
        rule_ids = {f.rule_id for f in result.findings}
        assert "AW-TOOL-001" in rule_ids

    def test_unsafe_triggers_tool002(self) -> None:
        """langchain_unsafe has shell execution tool -> AW-TOOL-002."""
        result = scan(FIXTURES / "langchain_unsafe")
        rule_ids = {f.rule_id for f in result.findings}
        assert "AW-TOOL-002" in rule_ids

    def test_basic_triggers_mem001(self) -> None:
        """langchain_basic has unfiltered retriever -> AW-MEM-001."""
        result = scan(FIXTURES / "langchain_basic")
        rule_ids = {f.rule_id for f in result.findings}
        assert "AW-MEM-001" in rule_ids

    def test_injection_triggers_mem004(self) -> None:
        """langchain_injection has memory injection risk -> AW-MEM-004."""
        result = scan(FIXTURES / "langchain_injection")
        rule_ids = {f.rule_id for f in result.findings}
        assert "AW-MEM-004" in rule_ids

    def test_unsafe_has_critical_findings(self) -> None:
        """langchain_unsafe should produce at least one CRITICAL finding."""
        result = scan(FIXTURES / "langchain_unsafe")
        assert any(f.severity == Severity.CRITICAL for f in result.findings)

    def test_injection_has_high_findings(self) -> None:
        """langchain_injection should produce at least one HIGH finding."""
        result = scan(FIXTURES / "langchain_injection")
        assert any(f.severity in (Severity.CRITICAL, Severity.HIGH) for f in result.findings)


# ── False Positive Tests ─────────────────────────────────────────────────────
# These fixtures should NOT trigger certain rules.


class TestFalsePositives:
    """Verify that safe fixtures do NOT trigger rules incorrectly."""

    def test_safe_no_critical(self) -> None:
        """langchain_safe should NOT produce CRITICAL findings."""
        result = scan(FIXTURES / "langchain_safe")
        critical = [f for f in result.findings if f.severity == Severity.CRITICAL]
        assert not critical, f"Unexpected CRITICAL findings: {[f.rule_id for f in critical]}"

    def test_safe_no_mem001(self) -> None:
        """langchain_safe uses filter on retrieval -> no AW-MEM-001."""
        result = scan(FIXTURES / "langchain_safe")
        rule_ids = {f.rule_id for f in result.findings}
        assert "AW-MEM-001" not in rule_ids

    def test_safe_no_tool002(self) -> None:
        """langchain_safe has no code execution tools -> no AW-TOOL-002."""
        result = scan(FIXTURES / "langchain_safe")
        rule_ids = {f.rule_id for f in result.findings}
        assert "AW-TOOL-002" not in rule_ids

    def test_safe_no_tool001(self) -> None:
        """langchain_safe has no destructive tools -> no AW-TOOL-001."""
        result = scan(FIXTURES / "langchain_safe")
        rule_ids = {f.rule_id for f in result.findings}
        assert "AW-TOOL-001" not in rule_ids


# ── Per-Rule Coverage Matrix ─────────────────────────────────────────────────


class TestRuleCoverage:
    """Ensure each rule fires on at least one fixture and does NOT fire on safe."""

    @pytest.mark.parametrize(
        "fixture,expected_rule",
        [
            ("langchain_unsafe", "AW-MEM-001"),
            ("langchain_unsafe", "AW-MEM-003"),
            ("langchain_unsafe", "AW-MEM-005"),
            ("langchain_unsafe", "AW-TOOL-001"),
            ("langchain_unsafe", "AW-TOOL-002"),
            ("langchain_unsafe", "AW-TOOL-003"),
            ("langchain_basic", "AW-MEM-001"),
            ("langchain_injection", "AW-MEM-004"),
            ("langchain_cross_file", "AW-MEM-001"),
            ("langchain_cross_file", "AW-MEM-003"),
            ("langchain_taint", "AW-MEM-001"),
            ("langchain_taint", "AW-MEM-002"),
            ("langchain_branching", "AW-MEM-001"),
        ],
    )
    def test_rule_fires_on_vulnerable_fixture(self, fixture: str, expected_rule: str) -> None:
        result = scan(FIXTURES / fixture)
        rule_ids = {f.rule_id for f in result.findings}
        assert expected_rule in rule_ids, (
            f"Expected {expected_rule} in {fixture}, got: {sorted(rule_ids)}"
        )

    @pytest.mark.parametrize(
        "rule_id",
        [
            "AW-MEM-001",
            "AW-TOOL-001",
            "AW-TOOL-002",
            "AW-TOOL-003",
        ],
    )
    def test_rule_does_not_fire_on_safe_fixture(self, rule_id: str) -> None:
        result = scan(FIXTURES / "langchain_safe")
        rule_ids = {f.rule_id for f in result.findings}
        assert rule_id not in rule_ids, f"False positive: {rule_id} fired on langchain_safe"


# ── Detection Quality Metrics ────────────────────────────────────────────────


class TestDetectionQuality:
    """Aggregate detection quality metrics across all fixtures."""

    # Expected findings for each fixture (rule_id -> should be present)
    _EXPECTED: dict[str, set[str]] = {
        "langchain_unsafe": {"AW-MEM-001", "AW-MEM-003", "AW-TOOL-001", "AW-TOOL-002"},
        "langchain_basic": {"AW-MEM-001"},
        "langchain_injection": {"AW-MEM-004"},
        "langchain_cross_file": {"AW-MEM-001", "AW-MEM-003"},
        "langchain_taint": {"AW-MEM-001", "AW-MEM-002"},
        "langchain_branching": {"AW-MEM-001"},
    }

    # Rules that should NOT fire on safe fixture
    _SAFE_NEGATIVE: set[str] = {
        "AW-MEM-001",
        "AW-MEM-002",
        "AW-MEM-003",
        "AW-TOOL-001",
        "AW-TOOL-002",
        "AW-TOOL-003",
    }

    def test_true_positive_rate(self) -> None:
        """TP rate should be >= 85%."""
        total_expected = 0
        total_detected = 0

        for fixture, expected_rules in self._EXPECTED.items():
            result = scan(FIXTURES / fixture)
            found_rules = {f.rule_id for f in result.findings}
            for rule in expected_rules:
                total_expected += 1
                if rule in found_rules:
                    total_detected += 1

        tp_rate = total_detected / total_expected if total_expected > 0 else 0.0
        assert tp_rate >= 0.85, f"TP rate {tp_rate:.0%} < 85% ({total_detected}/{total_expected})"

    def test_false_positive_rate(self) -> None:
        """FP rate on safe fixture should be < 15%."""
        result = scan(FIXTURES / "langchain_safe")
        found_rules = {f.rule_id for f in result.findings}

        checked = len(self._SAFE_NEGATIVE)
        false_positives = len(found_rules & self._SAFE_NEGATIVE)

        fp_rate = false_positives / checked if checked > 0 else 0.0
        assert fp_rate < 0.15, (
            f"FP rate {fp_rate:.0%} >= 15% (false positives: {found_rules & self._SAFE_NEGATIVE})"
        )

    # Fixtures that are LangChain projects (detectable framework)
    _LANGCHAIN_FIXTURES = {
        "langchain_unsafe",
        "langchain_basic",
        "langchain_safe",
        "langchain_injection",
        "langchain_cross_file",
        "langchain_taint",
        "langchain_branching",
    }

    def test_all_langchain_fixtures_scan_without_error(self) -> None:
        """Every LangChain fixture directory should scan without errors."""
        for name in self._LANGCHAIN_FIXTURES:
            fixture_dir = FIXTURES / name
            if fixture_dir.is_dir():
                result = scan(fixture_dir)
                assert not result.errors, f"Scan errors in {name}: {result.errors}"
