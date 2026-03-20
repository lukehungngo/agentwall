"""Integration tests: verify engine produces correct results through full pipeline."""

from __future__ import annotations

from pathlib import Path

from agentwall.scanner import scan

FIXTURES = Path(__file__).parent / "fixtures"


def test_scan_basic_fixture_still_finds_issues() -> None:
    """Existing langchain_basic fixture still produces findings (no regression)."""
    result = scan(FIXTURES / "langchain_basic")
    mem_findings = [f for f in result.findings if f.rule_id.startswith("AW-MEM")]
    assert len(mem_findings) > 0


def test_scan_safe_fixture_still_clean() -> None:
    """Existing langchain_safe fixture produces no CRITICAL findings."""
    result = scan(FIXTURES / "langchain_safe")
    critical = [f for f in result.findings if f.severity.value == "critical"]
    assert len(critical) == 0


def test_scan_engine_basic_finds_issues() -> None:
    """New engine_basic fixture (no filter) produces findings."""
    result = scan(FIXTURES / "engine_basic")
    mem_findings = [f for f in result.findings if f.rule_id.startswith("AW-MEM")]
    assert len(mem_findings) > 0


def test_scan_engine_tenant_collection() -> None:
    """Per-tenant collection fixture still flags missing filter on similarity_search.

    Using a per-tenant collection_name does not eliminate the requirement to
    pass filter= on retrieval calls — the scanner flags both patterns.
    """
    result = scan(FIXTURES / "engine_tenant_collection")
    mem_findings = [f for f in result.findings if f.rule_id.startswith("AW-MEM")]
    assert len(mem_findings) > 0


def test_scan_static_filter_still_flagged() -> None:
    """Static filter (not tenant-scoped) should still produce findings."""
    result = scan(FIXTURES / "engine_static_filter")
    mem_findings = [f for f in result.findings if f.rule_id.startswith("AW-MEM")]
    assert len(mem_findings) > 0


def test_scan_branching_finds_issues() -> None:
    """Branching fixture (filter on some paths) should produce findings."""
    result = scan(FIXTURES / "engine_branching")
    mem_findings = [f for f in result.findings if f.rule_id.startswith("AW-MEM")]
    assert len(mem_findings) > 0


def test_engine_context_populated() -> None:
    """After scan, engine fields on context should be populated for langchain."""
    # Run scan on a fixture and check that the engine ran.
    # We can't access ctx directly from scan(), but we can verify
    # the scan doesn't crash with the engine wired in.
    result = scan(FIXTURES / "engine_basic")
    assert result.framework == "langchain"
    assert result.scanned_files > 0


def test_no_regression_full_suite() -> None:
    """Run on langchain_unsafe and verify findings exist."""
    result = scan(FIXTURES / "langchain_unsafe")
    assert len(result.findings) > 0
