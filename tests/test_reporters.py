"""Tests for terminal and JSON reporters."""

from __future__ import annotations

import json
from pathlib import Path

from rich.console import Console

from agentwall.models import Category, Finding, ScanResult, Severity
from agentwall.reporters.json_reporter import JsonReporter
from agentwall.reporters.terminal import TerminalReporter


def _make_result(findings: list[Finding] | None = None) -> ScanResult:
    return ScanResult(
        target=Path("/fake/project"),
        framework="langchain",
        findings=findings or [],
        scanned_files=3,
    )


def _make_finding(
    rule_id: str = "AW-MEM-001",
    severity: Severity = Severity.CRITICAL,
    file: Path | None = Path("/fake/agent.py"),
    line: int | None = 42,
) -> Finding:
    return Finding(
        rule_id=rule_id,
        title="Test finding",
        severity=severity,
        category=Category.MEMORY,
        description="Test description",
        fix="Test fix",
        file=file,
        line=line,
    )


class TestTerminalReporter:
    def test_render_no_findings(self) -> None:
        console = Console(file=None, force_terminal=True, width=120)
        reporter = TerminalReporter(console=console)
        result = _make_result()
        # Should not raise
        reporter.render(result)

    def test_render_with_findings(self) -> None:
        console = Console(file=None, force_terminal=True, width=120)
        reporter = TerminalReporter(console=console)
        result = _make_result([
            _make_finding(severity=Severity.CRITICAL),
            _make_finding(rule_id="AW-TOOL-001", severity=Severity.HIGH),
            _make_finding(rule_id="AW-MEM-005", severity=Severity.MEDIUM),
        ])
        reporter.render(result)

    def test_render_finding_no_file(self) -> None:
        console = Console(file=None, force_terminal=True, width=120)
        reporter = TerminalReporter(console=console)
        result = _make_result([_make_finding(file=None, line=None)])
        reporter.render(result)

    def test_render_finding_no_fix(self) -> None:
        console = Console(file=None, force_terminal=True, width=120)
        reporter = TerminalReporter(console=console)
        f = Finding(
            rule_id="AW-MEM-001",
            title="No fix",
            severity=Severity.HIGH,
            category=Category.MEMORY,
            description="Desc",
        )
        result = _make_result([f])
        reporter.render(result)


class TestJsonReporter:
    def test_render_creates_file(self, tmp_path: Path) -> None:
        out = tmp_path / "report.json"
        reporter = JsonReporter()
        result = _make_result([_make_finding()])
        reporter.render(result, out)
        assert out.exists()
        data = json.loads(out.read_text())
        assert "findings" in data
        assert len(data["findings"]) == 1

    def test_render_empty_findings(self, tmp_path: Path) -> None:
        out = tmp_path / "report.json"
        reporter = JsonReporter()
        result = _make_result()
        reporter.render(result, out)
        data = json.loads(out.read_text())
        assert data["findings"] == []

    def test_json_round_trip(self, tmp_path: Path) -> None:
        out = tmp_path / "report.json"
        reporter = JsonReporter()
        result = _make_result([
            _make_finding(severity=Severity.CRITICAL),
            _make_finding(rule_id="AW-TOOL-002", severity=Severity.MEDIUM),
        ])
        reporter.render(result, out)
        data = json.loads(out.read_text())
        assert data["framework"] == "langchain"
        assert data["scanned_files"] == 3
        assert len(data["findings"]) == 2
