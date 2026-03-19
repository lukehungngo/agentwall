"""Tests for L5 SemgrepAnalyzer."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from agentwall.analyzers.semgrep import (
    SemgrepAnalyzer,
    _parse_semgrep_output,
    _result_to_finding,
)
from agentwall.context import AnalysisContext
from agentwall.models import ScanConfig


def _ctx(target: Path) -> AnalysisContext:
    return AnalysisContext(target=target, config=ScanConfig.default())


class TestSemgrepParsing:
    def test_parse_valid_output(self) -> None:
        raw = '{"results": [{"check_id": "test", "path": "a.py", "start": {"line": 1}, "extra": {"message": "msg", "severity": "ERROR", "metadata": {}}}]}'
        results = _parse_semgrep_output(raw)
        assert len(results) == 1
        assert results[0]["check_id"] == "test"

    def test_parse_empty_output(self) -> None:
        results = _parse_semgrep_output("")
        assert results == []

    def test_parse_invalid_json(self) -> None:
        results = _parse_semgrep_output("{invalid")
        assert results == []

    def test_result_to_finding(self) -> None:
        result = {
            "check_id": "aw-mem-001-test",
            "path": "agent.py",
            "start": {"line": 10},
            "extra": {
                "message": "Test finding",
                "severity": "ERROR",
                "metadata": {
                    "agentwall-id": "AW-MEM-001",
                    "category": "memory",
                    "confidence": "HIGH",
                },
            },
        }
        finding = _result_to_finding(result)
        assert finding is not None
        assert finding.rule_id == "AW-MEM-001"
        assert finding.severity.value == "high"
        assert finding.layer == "L5"

    def test_result_to_finding_handles_missing_fields(self) -> None:
        result = {"check_id": "test", "extra": {}}
        finding = _result_to_finding(result)
        assert finding is not None
        assert finding.rule_id == "test"


class TestSemgrepAnalyzer:
    def test_returns_empty_when_semgrep_not_available(self) -> None:
        with patch("agentwall.analyzers.semgrep._semgrep_available", return_value=False):
            analyzer = SemgrepAnalyzer()
            findings = analyzer.analyze(_ctx(Path(".")))
            assert findings == []

    def test_rules_dir_exists(self) -> None:
        """Bundled rules directory should exist."""
        from agentwall.analyzers.semgrep import _RULES_DIR

        assert _RULES_DIR.exists()
        yaml_files = list(_RULES_DIR.glob("*.yaml"))
        assert len(yaml_files) >= 3  # memory.yaml, tools.yaml, config.yaml
