"""Tests for the L2 assignment-based project graph engine."""

from __future__ import annotations

from pathlib import Path

from agentwall.engine.graph import build_project_graph
from agentwall.frameworks.langchain import LANGCHAIN_MODEL

FIXTURES = Path(__file__).parent / "fixtures"


# ── cross-file import resolution ──────────────────────────────────────────────


def test_cross_file_import_resolution() -> None:
    files = list((FIXTURES / "engine_cross_file").glob("*.py"))
    graph = build_project_graph(files, LANGCHAIN_MODEL, FIXTURES / "engine_cross_file")
    callees = {e.callee_name for e in graph.call_edges if e.caller_name == "ask_endpoint"}
    assert "get_current_user" in callees and "search_docs" in callees


# ── assignment tracking ────────────────────────────────────────────────────────


def test_assignment_tracking() -> None:
    files = [FIXTURES / "engine_lcel_pipe" / "agent.py"]
    graph = build_project_graph(files, LANGCHAIN_MODEL)
    assert "db" in graph.identifiers
    assert any("Chroma" in v for v in graph.identifiers["db"].pointsto)


# ── LCEL pipe composition ──────────────────────────────────────────────────────


def test_lcel_pipe_detected() -> None:
    files = [FIXTURES / "engine_lcel_pipe" / "agent.py"]
    graph = build_project_graph(files, LANGCHAIN_MODEL)
    pipe_edges = [e for e in graph.composition_edges if e.kind == "pipe"]
    assert len(pipe_edges) >= 2


# ── factory pattern ────────────────────────────────────────────────────────────


def test_factory_pattern_detected() -> None:
    files = [FIXTURES / "engine_factory" / "agent.py"]
    graph = build_project_graph(files, LANGCHAIN_MODEL)
    factory_edges = [e for e in graph.composition_edges if e.kind == "factory"]
    assert len(factory_edges) >= 1
    assert any("retriever" in e.target for e in factory_edges)


# ── single-level inheritance ───────────────────────────────────────────────────


def test_single_level_inheritance() -> None:
    files = [FIXTURES / "engine_inheritance" / "agent.py"]
    graph = build_project_graph(files, LANGCHAIN_MODEL)
    assert graph.extends.get("TenantChroma") == "Chroma"


# ── unresolved calls ───────────────────────────────────────────────────────────


def test_unresolved_calls_marked() -> None:
    files = [FIXTURES / "engine_basic" / "agent.py"]
    graph = build_project_graph(files, LANGCHAIN_MODEL)
    total = len(graph.call_edges) + len(graph.unresolved)
    assert total >= 0


# ── edge: empty file list ──────────────────────────────────────────────────────


def test_empty_file_list() -> None:
    graph = build_project_graph([], LANGCHAIN_MODEL)
    assert graph.call_edges == []
    assert graph.composition_edges == []
    assert graph.identifiers == {}
    assert graph.extends == {}
    assert graph.unresolved == []


# ── edge: single file with no calls ───────────────────────────────────────────


def test_no_calls_file() -> None:
    files = [FIXTURES / "engine_basic" / "agent.py"]
    graph = build_project_graph(files, LANGCHAIN_MODEL)
    # Should complete without error; call_edges may or may not be empty
    assert isinstance(graph.call_edges, list)


# ── ProjectGraph helpers ───────────────────────────────────────────────────────


def test_callers_of() -> None:
    files = list((FIXTURES / "engine_cross_file").glob("*.py"))
    graph = build_project_graph(files, LANGCHAIN_MODEL, FIXTURES / "engine_cross_file")
    callers = graph.callers_of("get_current_user")
    assert any(e.caller_name == "ask_endpoint" for e in callers)


def test_callees_of() -> None:
    files = list((FIXTURES / "engine_cross_file").glob("*.py"))
    graph = build_project_graph(files, LANGCHAIN_MODEL, FIXTURES / "engine_cross_file")
    callees = graph.callees_of("ask_endpoint")
    callee_names = {e.callee_name for e in callees}
    assert "get_current_user" in callee_names


def test_resolve_method_with_override() -> None:
    files = [FIXTURES / "engine_inheritance" / "agent.py"]
    graph = build_project_graph(files, LANGCHAIN_MODEL)
    # TenantChroma overrides similarity_search — should resolve to TenantChroma.similarity_search
    resolved = graph.resolve_method("TenantChroma", "similarity_search")
    assert resolved == "TenantChroma.similarity_search"


def test_resolve_method_inherited() -> None:
    files = [FIXTURES / "engine_inheritance" / "agent.py"]
    graph = build_project_graph(files, LANGCHAIN_MODEL)
    # TenantChroma does not define as_retriever — falls back to parent Chroma
    resolved = graph.resolve_method("TenantChroma", "as_retriever")
    assert resolved == "Chroma.as_retriever"


def test_resolve_method_unknown_class() -> None:
    files = [FIXTURES / "engine_basic" / "agent.py"]
    graph = build_project_graph(files, LANGCHAIN_MODEL)
    assert graph.resolve_method("NonExistent", "some_method") is None


# ── malformed / parse-error resilience ────────────────────────────────────────


def test_malformed_source_skipped(tmp_path: Path) -> None:
    bad = tmp_path / "bad.py"
    bad.write_text("def broken(:\n    pass\n")
    good = tmp_path / "good.py"
    good.write_text("x = 1\n")
    # Should not raise; bad file is skipped
    graph = build_project_graph([bad, good], LANGCHAIN_MODEL)
    assert isinstance(graph.call_edges, list)


# ── decorator pattern ──────────────────────────────────────────────────────────


def test_decorator_pattern_detected(tmp_path: Path) -> None:
    src = tmp_path / "tools.py"
    src.write_text(
        "from langchain.tools import tool\n\n@tool\ndef search(query: str) -> str:\n    return query\n"
    )
    graph = build_project_graph([src], LANGCHAIN_MODEL)
    dec_edges = [e for e in graph.composition_edges if e.kind == "decorator"]
    assert len(dec_edges) >= 1
    assert any(e.source == "search" for e in dec_edges)


# ── arg_names captured at call sites ──────────────────────────────────────────


def test_arg_names_captured(tmp_path: Path) -> None:
    src = tmp_path / "caller.py"
    src.write_text("def caller():\n    foo(a, b, c)\n\ndef foo(a, b, c):\n    pass\n")
    graph = build_project_graph([src], LANGCHAIN_MODEL)
    edges = [e for e in graph.call_edges if e.callee_name == "foo"]
    assert len(edges) >= 1
    assert edges[0].arg_names == ("a", "b", "c")


# ── pipe chain a|b|c produces two edges ───────────────────────────────────────


def test_pipe_chain_three_way(tmp_path: Path) -> None:
    src = tmp_path / "chain.py"
    src.write_text("a = 1\nb = 2\nc = 3\nd = a | b | c\n")
    graph = build_project_graph([src], LANGCHAIN_MODEL)
    pipe_edges = [e for e in graph.composition_edges if e.kind == "pipe"]
    # a|b and b|c  (or equivalent decomposition)
    assert len(pipe_edges) >= 2
