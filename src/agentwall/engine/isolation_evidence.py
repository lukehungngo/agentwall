"""Evidence-based MEM-001 classification (OCP design).

Separates evidence collection (open for extension) from verdict decision
(closed for modification). Adding a new signal = add a field to the evidence
struct. The verdict function stays the same.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

from agentwall.models import ConfidenceLevel, Severity

if TYPE_CHECKING:
    from agentwall.context import AnalysisContext
    from agentwall.models import MemoryConfig


# Web framework import names that indicate a multi-tenant application.
_WEB_FRAMEWORKS: frozenset[str] = frozenset(
    {
        "fastapi",
        "flask",
        "django",
        "starlette",
        "sanic",
        "tornado",
        "bottle",
        "falcon",
    }
)

# aiohttp.web is special: the import is "aiohttp" but we need "aiohttp.web"
_WEB_FRAMEWORK_DOTTED: frozenset[str] = frozenset({"aiohttp.web"})

# Directories that contain non-production code (tests, examples, templates).
# Web framework imports in these dirs should not make the project "multi-tenant",
# and findings in these dirs should be treated as library/non-production code.
_NON_PRODUCTION_DIRS: frozenset[str] = frozenset(
    {
        "tests",
        "test",
        "testing",
        "standard-tests",
        "examples",
        "example",
        "demos",
        "demo",
        "templates",
        "starters",
        "cookbooks",
        "tutorials",
        "benchmarks",
        "benchmark",
        "mock_servers",
    }
)


@dataclass
class IsolationEvidence:
    """Evidence collected about a store's isolation context.

    Open for extension: add new fields when new signals become available
    (runtime context, deployment config, user annotations).
    The verdict function consumes whatever fields are present.
    """

    # Current static signals
    has_web_framework: bool = False
    collection_is_dynamic: bool = False
    has_filter: bool = False
    filter_is_tenant_scoped: bool = False
    is_library_code: bool = False
    has_retrieval: bool = False


def classify_isolation(
    evidence: IsolationEvidence,
) -> tuple[Severity, ConfidenceLevel, str]:
    """Determine MEM-001 severity from collected evidence.

    Returns (severity, confidence, reason).

    Closed for modification: this function's logic should rarely change.
    New signals are added as IsolationEvidence fields; the classification
    tiers remain stable.
    """
    # Tier 0: No retrieval in file -> not applicable
    if not evidence.has_retrieval:
        return (
            Severity.INFO,
            ConfidenceLevel.LOW,
            "No retrieval calls detected in file",
        )

    # Tier 1: Filter present and tenant-scoped -> safe
    if evidence.has_filter and evidence.filter_is_tenant_scoped:
        return (
            Severity.INFO,
            ConfidenceLevel.HIGH,
            "Filter present with tenant-scoped value",
        )

    # Tier 2: Library/framework code -> INFO (by design)
    if evidence.is_library_code:
        return (
            Severity.INFO,
            ConfidenceLevel.MEDIUM,
            "Framework library code -- filter expected from caller",
        )

    # Tier 3: Dynamic collection name + no web framework -> INFO (per-entity isolation)
    # When a web framework IS present, dynamic collection alone is not enough
    # (Tier 6 handles that case with higher severity).
    if (
        evidence.collection_is_dynamic
        and not evidence.has_filter
        and not evidence.has_web_framework
    ):
        return (
            Severity.INFO,
            ConfidenceLevel.MEDIUM,
            "Collection name is dynamic -- verify it provides tenant isolation",
        )

    # Tier 4: Filter present but not tenant-scoped (static filter)
    if evidence.has_filter and not evidence.filter_is_tenant_scoped:
        return (
            Severity.MEDIUM,
            ConfidenceLevel.MEDIUM,
            "Filter present but appears static -- not tenant-scoped",
        )

    # Tier 5: Web framework + no filter + static collection -> CRITICAL
    if (
        evidence.has_web_framework
        and not evidence.has_filter
        and not evidence.collection_is_dynamic
    ):
        return (
            Severity.CRITICAL,
            ConfidenceLevel.HIGH,
            "Multi-tenant app with unfiltered shared vector store",
        )

    # Tier 6: Web framework + no filter + dynamic collection -> HIGH
    if evidence.has_web_framework and not evidence.has_filter:
        return (
            Severity.HIGH,
            ConfidenceLevel.MEDIUM,
            "Web app without retrieval filter -- verify tenant isolation",
        )

    # Tier 7: No web framework + no filter -> INFO (single-user tool)
    if not evidence.has_web_framework and not evidence.has_filter:
        return (
            Severity.INFO,
            ConfidenceLevel.MEDIUM,
            "No web framework detected -- likely single-user tool. "
            "Verify if deployed as shared service",
        )

    # Fallback
    return (
        Severity.MEDIUM,
        ConfidenceLevel.LOW,
        "Insufficient evidence to classify isolation status",
    )


def collect_evidence(
    mc: MemoryConfig,
    ctx: AnalysisContext,
    engine_isolation: dict[str, str] | None = None,
    *,
    has_web_framework: bool | None = None,
) -> IsolationEvidence:
    """Collect all available evidence about a store's isolation context.

    Args:
        mc: The memory config for the store being analyzed.
        ctx: Analysis context with project-level information.
        engine_isolation: Per-backend isolation strategy from engine store profiles.
        has_web_framework: Pre-computed web framework flag (avoids recomputation).
            If None, will be computed from ctx.source_files.
    """
    evidence = IsolationEvidence()

    # has_retrieval: check if file has retrieval method calls
    evidence.has_retrieval = _file_has_retrieval(mc.source_file)

    # has_filter: from MemoryConfig
    evidence.has_filter = mc.has_metadata_filter_on_retrieval

    # filter_is_tenant_scoped: from engine StoreProfile if available
    iso = (engine_isolation or {}).get(mc.backend, "")
    if iso == "filter_on_read":
        evidence.has_filter = True
        evidence.filter_is_tenant_scoped = True

    # collection_is_dynamic: from MemoryConfig + engine
    evidence.collection_is_dynamic = (
        mc.collection_name is None  # wasn't a string literal
        or mc.has_tenant_isolation  # adapter detected isolation
        or iso == "collection_per_tenant"
    )

    # has_web_framework: scan project imports once
    if has_web_framework is not None:
        evidence.has_web_framework = has_web_framework
    else:
        evidence.has_web_framework = project_has_web_framework(ctx)

    # is_library_code: check source file path
    evidence.is_library_code = _is_library_file(mc.source_file, ctx.target)

    return evidence


def _file_has_retrieval(source_file: Path | None) -> bool:
    """Check if a file contains any vector store retrieval method call."""
    if source_file is None:
        return True  # fail open -- assume retrieval exists

    try:
        from agentwall.patterns import RETRIEVAL_METHODS

        source = source_file.read_text(encoding="utf-8")
        tree = ast.parse(source)
        for node in ast.walk(tree):
            if isinstance(node, ast.Attribute) and node.attr in RETRIEVAL_METHODS:
                return True
        return False
    except Exception:  # noqa: BLE001
        return True  # fail open on parse errors


def project_has_web_framework(ctx: AnalysisContext) -> bool:
    """Scan project source files for web framework imports.

    Checks top-level import statements for known web framework names.
    Skips files in test/example/template directories since web framework
    imports there (e.g., test mock servers) don't indicate the project
    is a multi-tenant web application.
    """
    for source_file in ctx.source_files:
        # Skip non-production files — a Flask import in tests/mock_server.py
        # does not make the project a multi-tenant web app.
        if _is_non_production_path(source_file, ctx.target):
            continue

        try:
            source = source_file.read_text(encoding="utf-8")
            tree = ast.parse(source)
        except Exception:  # noqa: BLE001
            continue

        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    root_module = alias.name.split(".")[0]
                    if root_module in _WEB_FRAMEWORKS:
                        return True
                    if alias.name in _WEB_FRAMEWORK_DOTTED:
                        return True
            elif isinstance(node, ast.ImportFrom) and node.module:
                root_module = node.module.split(".")[0]
                if root_module in _WEB_FRAMEWORKS:
                    return True
                if node.module in _WEB_FRAMEWORK_DOTTED:
                    return True

    return False


def _is_non_production_path(source_file: Path, target: Path) -> bool:
    """Check if a file is in a non-production directory relative to the target.

    Only checks path components within the scan target, so that
    test fixtures (which are themselves valid scan targets) are not
    incorrectly classified as non-production.
    """
    try:
        relative = source_file.resolve().relative_to(target.resolve())
    except ValueError:
        return False
    rel_parts = {p.lower() for p in relative.parts}
    return bool(rel_parts & _NON_PRODUCTION_DIRS)


def _is_library_file(source_file: Path | None, target: Path) -> bool:
    """Check if a source file is library/framework code (not user code).

    A file is considered library code if:
    - Its path contains "site-packages/"
    - It is outside the scan target directory
    - It is in a test/example/template directory relative to the target
    """
    if source_file is None:
        return False

    source_str = str(source_file)
    if "site-packages" in source_str:
        return True

    # File is outside the target directory -> dependency
    try:
        relative = source_file.resolve().relative_to(target.resolve())
    except ValueError:
        return True

    # File is in a non-production directory relative to the scan target
    # (tests/, examples/, templates/, etc.)
    rel_parts = {p.lower() for p in relative.parts}
    return bool(rel_parts & _NON_PRODUCTION_DIRS)
