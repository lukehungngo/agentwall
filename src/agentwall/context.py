"""AnalysisContext — shared mutable state flowing through the analysis pipeline.

Each analyzer reads what it needs from ctx, may write intermediate results
for downstream analyzers, and returns findings. The depends_on metadata
on each analyzer declares which fields it expects to be populated.

WARNING: Analyzer ordering is load-bearing. The registry topologically sorts
by depends_on. Do not reorder or parallelize without verifying data dependencies.
"""
from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Protocol, runtime_checkable

from agentwall.models import Finding, ScanConfig

if TYPE_CHECKING:
    from agentwall.models import AgentSpec, CallGraph, TaintResult


@dataclass
class AnalysisContext:
    """Shared state that flows through the analysis pipeline."""

    target: Path
    config: ScanConfig

    # Populated by L0+L1 (adapter)
    spec: AgentSpec | None = None

    # Populated by L2 (call graph), consumed by L3 and L6
    call_graph: CallGraph | None = None

    # Populated by L3 (taint), consumed by L6
    taint_results: list[TaintResult] | None = None

    # Accumulated findings from all layers
    findings: list[Finding] = field(default_factory=list)

    # Errors from failed layers (non-fatal)
    errors: list[str] = field(default_factory=list)


@runtime_checkable
class Analyzer(Protocol):
    """Protocol that all analyzers must satisfy.

    - name: layer identifier (e.g. "L1", "L2", "ASM")
    - depends_on: layers that must run before this one
    - analyze(ctx): read from ctx, optionally write to ctx, return findings
    """

    name: str
    depends_on: Sequence[str]
    replace: bool
    opt_in: bool

    def analyze(self, ctx: AnalysisContext) -> list[Finding]: ...
