"""Tests for L4 ConfigAuditor."""

from __future__ import annotations

from pathlib import Path

from agentwall.analyzers.config import ConfigAuditor
from agentwall.context import AnalysisContext
from agentwall.models import ScanConfig

FIXTURES = Path(__file__).parent / "fixtures" / "config_unsafe"


def _ctx(target: Path) -> AnalysisContext:
    return AnalysisContext(target=target, config=ScanConfig.default())


class TestConfigAuditorDockerCompose:
    def test_detects_exposed_ports(self) -> None:
        findings = ConfigAuditor().analyze(_ctx(FIXTURES))
        rule_ids = [f.rule_id for f in findings]
        assert "AW-CFG-exposed-port" in rule_ids

    def test_detects_docker_no_auth(self) -> None:
        findings = ConfigAuditor().analyze(_ctx(FIXTURES))
        # qdrant has no auth env vars near it
        docker_findings = [f for f in findings if f.rule_id == "AW-CFG-docker-no-auth"]
        assert len(docker_findings) >= 1


class TestConfigAuditorEnvFile:
    def test_detects_debug_mode(self) -> None:
        findings = ConfigAuditor().analyze(_ctx(FIXTURES))
        rule_ids = [f.rule_id for f in findings]
        assert "AW-CFG-debug-mode" in rule_ids

    def test_detects_hardcoded_secrets(self) -> None:
        findings = ConfigAuditor().analyze(_ctx(FIXTURES))
        rule_ids = [f.rule_id for f in findings]
        assert "AW-CFG-hardcoded-secret" in rule_ids

    def test_detects_empty_auth(self) -> None:
        findings = ConfigAuditor().analyze(_ctx(FIXTURES))
        rule_ids = [f.rule_id for f in findings]
        assert "AW-CFG-no-password" in rule_ids


class TestConfigAuditorPythonConfig:
    def test_detects_ephemeral_client(self) -> None:
        findings = ConfigAuditor().analyze(_ctx(FIXTURES))
        rule_ids = [f.rule_id for f in findings]
        assert "AW-CFG-chroma-ephemeral" in rule_ids


class TestConfigAuditorNoFalsePositives:
    def test_safe_directory_no_config_findings(self) -> None:
        safe = Path(__file__).parent / "fixtures" / "langchain_safe"
        findings = ConfigAuditor().analyze(_ctx(safe))
        # Config auditor should find nothing in a clean Python-only fixture
        config_findings = [f for f in findings if f.rule_id.startswith("AW-CFG-")]
        assert config_findings == []
