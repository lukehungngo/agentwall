"""Tests for evidence-based MEM-001 classification."""

from __future__ import annotations

from pathlib import Path

import pytest

from agentwall.engine.isolation_evidence import (
    IsolationEvidence,
    _file_has_retrieval,
    _is_library_file,
    classify_isolation,
    collect_evidence,
    project_has_web_framework,
)
from agentwall.models import ConfidenceLevel, MemoryConfig, Severity

# ---------------------------------------------------------------------------
# classify_isolation — verdict tests
# ---------------------------------------------------------------------------


class TestClassifyIsolation:
    """Test the classification tiers in order."""

    def test_tier0_no_retrieval_returns_info(self) -> None:
        e = IsolationEvidence(has_retrieval=False)
        sev, conf, reason = classify_isolation(e)
        assert sev == Severity.INFO
        assert conf == ConfidenceLevel.LOW
        assert "No retrieval" in reason

    def test_tier1_filter_tenant_scoped_returns_info(self) -> None:
        e = IsolationEvidence(
            has_retrieval=True,
            has_filter=True,
            filter_is_tenant_scoped=True,
            has_web_framework=True,
        )
        sev, conf, reason = classify_isolation(e)
        assert sev == Severity.INFO
        assert conf == ConfidenceLevel.HIGH

    def test_tier2_library_code_returns_info(self) -> None:
        e = IsolationEvidence(
            has_retrieval=True,
            is_library_code=True,
            has_web_framework=True,
        )
        sev, conf, reason = classify_isolation(e)
        assert sev == Severity.INFO
        assert conf == ConfidenceLevel.MEDIUM
        assert "library" in reason.lower()

    def test_tier3_dynamic_collection_no_filter_returns_info(self) -> None:
        e = IsolationEvidence(
            has_retrieval=True,
            collection_is_dynamic=True,
        )
        sev, conf, reason = classify_isolation(e)
        assert sev == Severity.INFO
        assert "dynamic" in reason.lower()

    def test_tier4_filter_not_tenant_scoped_returns_medium(self) -> None:
        e = IsolationEvidence(
            has_retrieval=True,
            has_filter=True,
            filter_is_tenant_scoped=False,
            has_web_framework=True,
        )
        sev, conf, reason = classify_isolation(e)
        assert sev == Severity.MEDIUM
        assert "not tenant-scoped" in reason

    def test_tier5_web_framework_no_filter_static_collection_returns_critical(self) -> None:
        e = IsolationEvidence(
            has_retrieval=True,
            has_web_framework=True,
            has_filter=False,
            collection_is_dynamic=False,
        )
        sev, conf, reason = classify_isolation(e)
        assert sev == Severity.CRITICAL
        assert conf == ConfidenceLevel.HIGH

    def test_tier6_web_framework_no_filter_dynamic_collection_returns_high(self) -> None:
        e = IsolationEvidence(
            has_retrieval=True,
            has_web_framework=True,
            has_filter=False,
            collection_is_dynamic=True,
        )
        sev, conf, reason = classify_isolation(e)
        assert sev == Severity.HIGH
        assert conf == ConfidenceLevel.MEDIUM

    def test_tier7_no_web_framework_no_filter_returns_info(self) -> None:
        e = IsolationEvidence(
            has_retrieval=True,
            has_web_framework=False,
            has_filter=False,
        )
        sev, conf, reason = classify_isolation(e)
        assert sev == Severity.INFO
        assert "single-user" in reason.lower()

    def test_all_defaults_no_retrieval_returns_info(self) -> None:
        """Default IsolationEvidence has has_retrieval=False -> INFO."""
        e = IsolationEvidence()
        sev, _, _ = classify_isolation(e)
        assert sev == Severity.INFO


# ---------------------------------------------------------------------------
# classify_isolation — tier priority tests (higher tiers don't shadow lower)
# ---------------------------------------------------------------------------


class TestClassifyIsolationPriority:
    def test_tenant_filter_beats_web_framework(self) -> None:
        """Even with web framework, tenant-scoped filter -> INFO."""
        e = IsolationEvidence(
            has_retrieval=True,
            has_web_framework=True,
            has_filter=True,
            filter_is_tenant_scoped=True,
        )
        sev, _, _ = classify_isolation(e)
        assert sev == Severity.INFO

    def test_library_code_beats_web_framework(self) -> None:
        """Library code in a web app -> INFO, not CRITICAL."""
        e = IsolationEvidence(
            has_retrieval=True,
            has_web_framework=True,
            is_library_code=True,
        )
        sev, _, _ = classify_isolation(e)
        assert sev == Severity.INFO

    def test_dynamic_collection_without_web_framework_is_info(self) -> None:
        """Dynamic collection + no web framework + no filter -> tier 3 (INFO)."""
        e = IsolationEvidence(
            has_retrieval=True,
            has_web_framework=False,
            collection_is_dynamic=True,
            has_filter=False,
        )
        sev, _, _ = classify_isolation(e)
        assert sev == Severity.INFO

    def test_dynamic_collection_with_web_framework_is_high(self) -> None:
        """Dynamic collection + web framework + no filter -> tier 6 (HIGH)."""
        e = IsolationEvidence(
            has_retrieval=True,
            has_web_framework=True,
            collection_is_dynamic=True,
            has_filter=False,
        )
        sev, _, _ = classify_isolation(e)
        assert sev == Severity.HIGH


# ---------------------------------------------------------------------------
# collect_evidence — integration with MemoryConfig
# ---------------------------------------------------------------------------


def _make_ctx(tmp_path: Path, files: dict[str, str] | None = None):  # type: ignore[no-untyped-def]
    from agentwall.context import AnalysisContext
    from agentwall.models import ScanConfig

    source_files: list[Path] = []
    if files:
        for name, content in files.items():
            p = tmp_path / name
            p.write_text(content)
            source_files.append(p)
    return AnalysisContext(target=tmp_path, config=ScanConfig.default(), source_files=source_files)


class TestCollectEvidence:
    def test_basic_no_source_file(self, tmp_path: Path) -> None:
        """MemoryConfig with no source_file -> has_retrieval=True (fail open)."""
        mc = MemoryConfig(backend="chroma")
        ctx = _make_ctx(tmp_path)
        evidence = collect_evidence(mc, ctx)
        assert evidence.has_retrieval is True

    def test_has_filter_from_mc(self, tmp_path: Path) -> None:
        mc = MemoryConfig(backend="chroma", has_metadata_filter_on_retrieval=True)
        ctx = _make_ctx(tmp_path)
        evidence = collect_evidence(mc, ctx)
        assert evidence.has_filter is True

    def test_engine_filter_on_read_sets_tenant_scoped(self, tmp_path: Path) -> None:
        mc = MemoryConfig(backend="chroma")
        ctx = _make_ctx(tmp_path)
        evidence = collect_evidence(mc, ctx, engine_isolation={"chroma": "filter_on_read"})
        assert evidence.has_filter is True
        assert evidence.filter_is_tenant_scoped is True

    def test_engine_collection_per_tenant_sets_dynamic(self, tmp_path: Path) -> None:
        mc = MemoryConfig(backend="chroma")
        ctx = _make_ctx(tmp_path)
        evidence = collect_evidence(mc, ctx, engine_isolation={"chroma": "collection_per_tenant"})
        assert evidence.collection_is_dynamic is True

    def test_collection_name_none_is_dynamic(self, tmp_path: Path) -> None:
        mc = MemoryConfig(backend="chroma", collection_name=None)
        ctx = _make_ctx(tmp_path)
        evidence = collect_evidence(mc, ctx)
        assert evidence.collection_is_dynamic is True

    def test_collection_name_literal_is_static(self, tmp_path: Path) -> None:
        mc = MemoryConfig(backend="chroma", collection_name="my_docs")
        ctx = _make_ctx(tmp_path)
        evidence = collect_evidence(mc, ctx)
        assert evidence.collection_is_dynamic is False

    def test_has_tenant_isolation_makes_dynamic(self, tmp_path: Path) -> None:
        mc = MemoryConfig(backend="chroma", collection_name="docs", has_tenant_isolation=True)
        ctx = _make_ctx(tmp_path)
        evidence = collect_evidence(mc, ctx)
        assert evidence.collection_is_dynamic is True

    def test_web_framework_precomputed(self, tmp_path: Path) -> None:
        """When has_web_framework kwarg is passed, don't scan files."""
        mc = MemoryConfig(backend="chroma")
        ctx = _make_ctx(tmp_path)
        evidence = collect_evidence(mc, ctx, has_web_framework=True)
        assert evidence.has_web_framework is True

    def test_web_framework_detected_from_files(self, tmp_path: Path) -> None:
        mc = MemoryConfig(backend="chroma")
        ctx = _make_ctx(tmp_path, {"app.py": "from fastapi import FastAPI\napp = FastAPI()\n"})
        evidence = collect_evidence(mc, ctx)
        assert evidence.has_web_framework is True

    def test_no_web_framework(self, tmp_path: Path) -> None:
        mc = MemoryConfig(backend="chroma")
        ctx = _make_ctx(tmp_path, {"script.py": "import json\nprint('hello')\n"})
        evidence = collect_evidence(mc, ctx)
        assert evidence.has_web_framework is False


# ---------------------------------------------------------------------------
# _file_has_retrieval
# ---------------------------------------------------------------------------


class TestFileHasRetrieval:
    def test_none_source_file_fails_open(self) -> None:
        assert _file_has_retrieval(None) is True

    def test_file_with_similarity_search(self, tmp_path: Path) -> None:
        p = tmp_path / "agent.py"
        p.write_text("db.similarity_search('query')\n")
        assert _file_has_retrieval(p) is True

    def test_file_without_retrieval(self, tmp_path: Path) -> None:
        p = tmp_path / "agent.py"
        p.write_text("db.add_texts(['hello'])\n")
        assert _file_has_retrieval(p) is False

    def test_nonexistent_file_fails_open(self, tmp_path: Path) -> None:
        p = tmp_path / "nonexistent.py"
        assert _file_has_retrieval(p) is True

    def test_syntax_error_fails_open(self, tmp_path: Path) -> None:
        p = tmp_path / "bad.py"
        p.write_text("def broken(:\n")
        assert _file_has_retrieval(p) is True


# ---------------------------------------------------------------------------
# project_has_web_framework
# ---------------------------------------------------------------------------


class TestProjectHasWebFramework:
    @pytest.mark.parametrize(
        "import_line",
        [
            "import fastapi",
            "from fastapi import FastAPI",
            "import flask",
            "from flask import Flask",
            "import django",
            "from django.conf import settings",
            "import starlette",
            "from sanic import Sanic",
            "import tornado",
            "import bottle",
            "import falcon",
            "from aiohttp.web import Application",
        ],
    )
    def test_detects_framework(self, tmp_path: Path, import_line: str) -> None:
        ctx = _make_ctx(tmp_path, {"app.py": f"{import_line}\n"})
        assert project_has_web_framework(ctx) is True

    def test_no_framework(self, tmp_path: Path) -> None:
        ctx = _make_ctx(tmp_path, {"script.py": "import json\nimport os\n"})
        assert project_has_web_framework(ctx) is False

    def test_empty_source_files(self, tmp_path: Path) -> None:
        ctx = _make_ctx(tmp_path)
        assert project_has_web_framework(ctx) is False

    def test_unparseable_file_skipped(self, tmp_path: Path) -> None:
        ctx = _make_ctx(tmp_path, {"bad.py": "def broken(:\n"})
        assert project_has_web_framework(ctx) is False

    def test_flask_in_tests_dir_not_detected(self, tmp_path: Path) -> None:
        """Web framework imports in tests/ should not make project multi-tenant."""
        tests_dir = tmp_path / "tests"
        tests_dir.mkdir()
        test_file = tests_dir / "mock_server.py"
        test_file.write_text("from flask import Flask\n")

        from agentwall.context import AnalysisContext
        from agentwall.models import ScanConfig

        ctx = AnalysisContext(
            target=tmp_path,
            config=ScanConfig.default(),
            source_files=[test_file],
        )
        assert project_has_web_framework(ctx) is False

    def test_flask_in_src_is_detected(self, tmp_path: Path) -> None:
        """Web framework imports in src/ should still be detected."""
        src_dir = tmp_path / "src"
        src_dir.mkdir()
        app_file = src_dir / "app.py"
        app_file.write_text("from flask import Flask\n")

        from agentwall.context import AnalysisContext
        from agentwall.models import ScanConfig

        ctx = AnalysisContext(
            target=tmp_path,
            config=ScanConfig.default(),
            source_files=[app_file],
        )
        assert project_has_web_framework(ctx) is True


# ---------------------------------------------------------------------------
# _is_library_file
# ---------------------------------------------------------------------------


class TestIsLibraryFile:
    def test_none_source_file(self) -> None:
        assert _is_library_file(None, Path("/project")) is False

    def test_site_packages(self, tmp_path: Path) -> None:
        p = Path("/usr/lib/python3.10/site-packages/langchain/vectorstores/chroma.py")
        assert _is_library_file(p, tmp_path) is True

    def test_file_inside_target(self, tmp_path: Path) -> None:
        p = tmp_path / "src" / "app.py"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.touch()
        assert _is_library_file(p, tmp_path) is False

    def test_file_outside_target(self, tmp_path: Path) -> None:
        other = tmp_path / "other_project" / "lib.py"
        other.parent.mkdir(parents=True, exist_ok=True)
        other.touch()
        target = tmp_path / "my_project"
        target.mkdir()
        assert _is_library_file(other, target) is True

    def test_file_in_tests_dir(self, tmp_path: Path) -> None:
        """Files in tests/ relative to target are non-production code."""
        p = tmp_path / "tests" / "test_store.py"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.touch()
        assert _is_library_file(p, tmp_path) is True

    def test_file_in_examples_dir(self, tmp_path: Path) -> None:
        """Files in examples/ relative to target are non-production code."""
        p = tmp_path / "examples" / "demo.py"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.touch()
        assert _is_library_file(p, tmp_path) is True

    def test_file_in_templates_dir(self, tmp_path: Path) -> None:
        """Files in templates/ relative to target are non-production code."""
        p = tmp_path / "templates" / "starter.py"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.touch()
        assert _is_library_file(p, tmp_path) is True

    def test_nested_tests_dir(self, tmp_path: Path) -> None:
        """Files in nested tests/ relative to target are non-production code."""
        p = tmp_path / "libs" / "core" / "tests" / "test_store.py"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.touch()
        assert _is_library_file(p, tmp_path) is True

    def test_src_not_classified_as_nonprod(self, tmp_path: Path) -> None:
        """Files in src/ should not be classified as non-production."""
        p = tmp_path / "src" / "app.py"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.touch()
        assert _is_library_file(p, tmp_path) is False
