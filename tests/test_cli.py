"""Tests for the CLI."""

from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from agentwall.cli import app

runner = CliRunner()

FIXTURES = Path(__file__).parent / "fixtures"


class TestCliScan:
    def test_scan_unsafe_exits_1(self) -> None:
        result = runner.invoke(app, ["scan", str(FIXTURES / "langchain_unsafe")])
        assert result.exit_code == 1

    def test_scan_safe_exits_0(self) -> None:
        result = runner.invoke(app, ["scan", str(FIXTURES / "langchain_safe"), "--fail-on", "critical"])
        assert result.exit_code == 0

    def test_scan_nonexistent_exits_2(self) -> None:
        result = runner.invoke(app, ["scan", "/nonexistent/path"])
        assert result.exit_code == 2
        assert "does not exist" in result.output

    def test_scan_invalid_fail_on_exits_2(self) -> None:
        result = runner.invoke(app, ["scan", str(FIXTURES / "langchain_basic"), "--fail-on", "bogus"])
        assert result.exit_code == 2

    def test_scan_fail_on_none_exits_0(self) -> None:
        result = runner.invoke(app, ["scan", str(FIXTURES / "langchain_unsafe"), "--fail-on", "none"])
        assert result.exit_code == 0

    def test_scan_fast_mode(self) -> None:
        result = runner.invoke(app, ["scan", str(FIXTURES / "langchain_basic"), "--fast", "--fail-on", "none"])
        assert result.exit_code == 0
        assert "AgentWall" in result.output

    def test_scan_custom_layers(self) -> None:
        result = runner.invoke(app, ["scan", str(FIXTURES / "langchain_basic"), "--layers", "L0,L1", "--fail-on", "none"])
        assert result.exit_code == 0

    def test_scan_invalid_layer_exits_2(self) -> None:
        result = runner.invoke(app, ["scan", str(FIXTURES / "langchain_basic"), "--layers", "L99"])
        assert result.exit_code == 2
        assert "unknown layers" in result.output

    def test_scan_json_output(self, tmp_path: Path) -> None:
        out = tmp_path / "report.json"
        result = runner.invoke(app, ["scan", str(FIXTURES / "langchain_basic"), "--output", str(out), "--fail-on", "none"])
        assert result.exit_code == 0
        assert out.exists()
        assert "JSON report written" in result.output

    def test_scan_framework_override(self) -> None:
        result = runner.invoke(app, ["scan", str(FIXTURES / "langchain_basic"), "--framework", "langchain", "--fail-on", "none"])
        assert result.exit_code == 0

    def test_scan_unsupported_framework_exits_2(self) -> None:
        result = runner.invoke(app, ["scan", str(FIXTURES / "langchain_basic"), "--framework", "crewai"])
        assert result.exit_code == 2


class TestCliVersion:
    def test_version_output(self) -> None:
        result = runner.invoke(app, ["version"])
        assert result.exit_code == 0
        assert "AgentWall v" in result.output
