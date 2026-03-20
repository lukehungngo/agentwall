"""Tests for rule definitions and registry completeness."""

from agentwall.models import Severity
from agentwall.rules import ALL_RULES


class TestRuleRegistry:
    def test_total_rule_count(self) -> None:
        assert len(ALL_RULES) == 27  # 10 existing + 17 new

    def test_sec_rules_exist(self) -> None:
        for i in range(1, 4):
            assert f"AW-SEC-00{i}" in ALL_RULES

    def test_rag_rules_exist(self) -> None:
        for i in range(1, 5):
            assert f"AW-RAG-00{i}" in ALL_RULES

    def test_mcp_rules_exist(self) -> None:
        for i in range(1, 4):
            assert f"AW-MCP-00{i}" in ALL_RULES

    def test_ser_rules_exist(self) -> None:
        for i in range(1, 4):
            assert f"AW-SER-00{i}" in ALL_RULES

    def test_agt_rules_exist(self) -> None:
        for i in range(1, 5):
            assert f"AW-AGT-00{i}" in ALL_RULES

    def test_existing_rules_unchanged(self) -> None:
        assert "AW-MEM-001" in ALL_RULES
        assert "AW-TOOL-005" in ALL_RULES

    def test_severity_discipline_no_new_critical(self) -> None:
        """CRITICAL is reserved for confirmed cross-tenant data access."""
        new_prefixes = ("AW-SEC-", "AW-RAG-", "AW-MCP-", "AW-SER-", "AW-AGT-")
        for rule_id, rule in ALL_RULES.items():
            if any(rule_id.startswith(p) for p in new_prefixes):
                assert rule.severity != Severity.CRITICAL, f"{rule_id} should not be CRITICAL"
