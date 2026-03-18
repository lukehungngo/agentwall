"""Tests for LangChainAdapter."""

from __future__ import annotations

from pathlib import Path

import pytest

from agentwall.adapters.langchain import LangChainAdapter

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture()
def adapter() -> LangChainAdapter:
    return LangChainAdapter()


class TestLangChainAdapterBasic:
    def test_returns_agent_spec(self, adapter: LangChainAdapter) -> None:
        spec = adapter.parse(FIXTURES / "langchain_basic")
        assert spec.framework == "langchain"

    def test_detects_tool_decorator(self, adapter: LangChainAdapter) -> None:
        spec = adapter.parse(FIXTURES / "langchain_basic")
        tool_names = [t.name for t in spec.tools]
        assert "search_web" in tool_names

    def test_detects_chroma_backend(self, adapter: LangChainAdapter) -> None:
        spec = adapter.parse(FIXTURES / "langchain_basic")
        backends = [m.backend for m in spec.memory_configs]
        assert "chroma" in backends

    def test_basic_no_retrieval_filter(self, adapter: LangChainAdapter) -> None:
        spec = adapter.parse(FIXTURES / "langchain_basic")
        chroma = next(m for m in spec.memory_configs if m.backend == "chroma")
        # as_retriever() with no filter
        assert not chroma.has_metadata_filter_on_retrieval

    def test_source_files_populated(self, adapter: LangChainAdapter) -> None:
        spec = adapter.parse(FIXTURES / "langchain_basic")
        assert len(spec.source_files) >= 1


class TestLangChainAdapterUnsafe:
    def test_detects_tool_class(self, adapter: LangChainAdapter) -> None:
        spec = adapter.parse(FIXTURES / "langchain_unsafe")
        tool_names = [t.name for t in spec.tools]
        assert "RunShell" in tool_names
        assert "DeleteFile" in tool_names

    def test_shell_tool_flagged_exec(self, adapter: LangChainAdapter) -> None:
        spec = adapter.parse(FIXTURES / "langchain_unsafe")
        shell = next(t for t in spec.tools if t.name == "RunShell")
        assert shell.accepts_code_execution is True

    def test_delete_tool_flagged_destructive(self, adapter: LangChainAdapter) -> None:
        spec = adapter.parse(FIXTURES / "langchain_unsafe")
        delete = next(t for t in spec.tools if t.name == "DeleteFile")
        assert delete.is_destructive is True

    def test_no_retrieval_filter(self, adapter: LangChainAdapter) -> None:
        spec = adapter.parse(FIXTURES / "langchain_unsafe")
        chroma = next(m for m in spec.memory_configs if m.backend == "chroma")
        assert not chroma.has_metadata_filter_on_retrieval

    def test_no_write_metadata(self, adapter: LangChainAdapter) -> None:
        spec = adapter.parse(FIXTURES / "langchain_unsafe")
        chroma = next(m for m in spec.memory_configs if m.backend == "chroma")
        assert not chroma.has_metadata_on_write


class TestLangChainAdapterSafe:
    def test_tool_has_user_scope_check(self, adapter: LangChainAdapter) -> None:
        spec = adapter.parse(FIXTURES / "langchain_safe")
        tool = next(t for t in spec.tools if t.name == "get_user_data")
        assert tool.has_user_scope_check is True

    def test_has_retrieval_filter(self, adapter: LangChainAdapter) -> None:
        spec = adapter.parse(FIXTURES / "langchain_safe")
        chroma = next(m for m in spec.memory_configs if m.backend == "chroma")
        assert chroma.has_metadata_filter_on_retrieval is True

    def test_tool_has_description(self, adapter: LangChainAdapter) -> None:
        spec = adapter.parse(FIXTURES / "langchain_safe")
        tool = next(t for t in spec.tools if t.name == "get_user_data")
        assert tool.description is not None


class TestLangChainAdapterRetrievalVariants:
    """Test detection of all retrieval method variants."""

    def test_similarity_search_with_score(self, adapter: LangChainAdapter, tmp_path: Path) -> None:
        (tmp_path / "agent.py").write_text(
            "from langchain_community.vectorstores import Chroma\n"
            "vs = Chroma(collection_name='docs')\n"
            "results = vs.similarity_search_with_score(query)\n",
            encoding="utf-8",
        )
        spec = adapter.parse(tmp_path)
        mc = spec.memory_configs[0]
        assert not mc.has_metadata_filter_on_retrieval

    def test_similarity_search_with_score_filtered(
        self, adapter: LangChainAdapter, tmp_path: Path
    ) -> None:
        (tmp_path / "agent.py").write_text(
            "from langchain_community.vectorstores import Chroma\n"
            "vs = Chroma(collection_name='docs')\n"
            "results = vs.similarity_search_with_score(query, filter={'user_id': uid})\n",
            encoding="utf-8",
        )
        spec = adapter.parse(tmp_path)
        mc = spec.memory_configs[0]
        assert mc.has_metadata_filter_on_retrieval

    def test_mmr_search_detected(self, adapter: LangChainAdapter, tmp_path: Path) -> None:
        (tmp_path / "agent.py").write_text(
            "from langchain_community.vectorstores import Chroma\n"
            "vs = Chroma(collection_name='docs')\n"
            "results = vs.max_marginal_relevance_search(query)\n",
            encoding="utf-8",
        )
        spec = adapter.parse(tmp_path)
        mc = spec.memory_configs[0]
        assert not mc.has_metadata_filter_on_retrieval

    def test_mmr_search_filtered(self, adapter: LangChainAdapter, tmp_path: Path) -> None:
        (tmp_path / "agent.py").write_text(
            "from langchain_community.vectorstores import Chroma\n"
            "vs = Chroma(collection_name='docs')\n"
            "results = vs.max_marginal_relevance_search(query, filter={'user_id': uid})\n",
            encoding="utf-8",
        )
        spec = adapter.parse(tmp_path)
        mc = spec.memory_configs[0]
        assert mc.has_metadata_filter_on_retrieval


class TestLangChainAdapterBaseToolInheritance:
    """Test detection of tools defined as BaseTool subclasses."""

    def test_detects_basetool_subclass(self, adapter: LangChainAdapter, tmp_path: Path) -> None:
        (tmp_path / "tool.py").write_text(
            "from langchain.tools import BaseTool\n"
            "class DeleteRecordTool(BaseTool):\n"
            '    """Deletes a record from the database."""\n'
            "    name = 'delete_record'\n"
            "    def _run(self, record_id: str) -> str:\n"
            "        return 'deleted'\n",
            encoding="utf-8",
        )
        spec = adapter.parse(tmp_path)
        assert len(spec.tools) == 1
        tool = spec.tools[0]
        assert tool.name == "DeleteRecordTool"
        assert tool.is_destructive is True
        assert tool.description == "Deletes a record from the database."

    def test_detects_structured_tool_subclass(
        self, adapter: LangChainAdapter, tmp_path: Path
    ) -> None:
        (tmp_path / "tool.py").write_text(
            "from langchain.tools import StructuredTool\n"
            "class ExecuteCodeTool(StructuredTool):\n"
            "    name = 'execute_code'\n"
            "    def _run(self, code: str) -> str:\n"
            "        return eval(code)\n",
            encoding="utf-8",
        )
        spec = adapter.parse(tmp_path)
        tool = spec.tools[0]
        assert tool.name == "ExecuteCodeTool"
        assert tool.accepts_code_execution is True

    def test_basetool_with_user_scope_check(
        self, adapter: LangChainAdapter, tmp_path: Path
    ) -> None:
        (tmp_path / "tool.py").write_text(
            "from langchain.tools import BaseTool\n"
            "class SafeDeleteTool(BaseTool):\n"
            "    name = 'safe_delete'\n"
            "    def _run(self, record_id: str, user_id: str) -> str:\n"
            "        if user_id != record.owner_id:\n"
            "            raise PermissionError('not allowed')\n"
            "        return 'deleted'\n",
            encoding="utf-8",
        )
        spec = adapter.parse(tmp_path)
        tool = spec.tools[0]
        assert tool.has_user_scope_check is True


class TestLangChainAdapterLoadTools:
    """Test detection of load_tools() calls."""

    def test_detects_load_tools(self, adapter: LangChainAdapter, tmp_path: Path) -> None:
        (tmp_path / "agent.py").write_text(
            "from langchain.agents import load_tools\n"
            "tools = load_tools(['arxiv', 'ddg-search', 'shell'])\n",
            encoding="utf-8",
        )
        spec = adapter.parse(tmp_path)
        names = [t.name for t in spec.tools]
        assert "arxiv" in names
        assert "ddg-search" in names
        assert "shell" in names

    def test_load_tools_shell_flagged(self, adapter: LangChainAdapter, tmp_path: Path) -> None:
        (tmp_path / "agent.py").write_text(
            "from langchain.agents import load_tools\ntools = load_tools(['shell'])\n",
            encoding="utf-8",
        )
        spec = adapter.parse(tmp_path)
        shell = next(t for t in spec.tools if t.name == "shell")
        assert shell.accepts_code_execution is True

    def test_load_tools_no_description(self, adapter: LangChainAdapter, tmp_path: Path) -> None:
        (tmp_path / "agent.py").write_text(
            "from langchain.agents import load_tools\ntools = load_tools(['arxiv'])\n",
            encoding="utf-8",
        )
        spec = adapter.parse(tmp_path)
        assert spec.tools[0].description is None


class TestASMExtraction:
    """Test that parse() populates AgentSpec.asm."""

    def test_asm_populated_on_unsafe_fixture(self, adapter: LangChainAdapter) -> None:
        spec = adapter.parse(FIXTURES / "langchain_unsafe")
        assert spec.asm is not None
        assert len(spec.asm.stores) >= 1
        assert len(spec.asm.read_ops) >= 1

    def test_asm_stores_have_collection_info(self, adapter: LangChainAdapter) -> None:
        spec = adapter.parse(FIXTURES / "langchain_unsafe")
        assert spec.asm is not None
        store = spec.asm.stores[0]
        assert store.backend == "chroma"
        assert store.collection_name == "all_users"
        assert store.collection_name_is_static is True

    def test_asm_read_op_no_filter_on_unsafe(self, adapter: LangChainAdapter) -> None:
        spec = adapter.parse(FIXTURES / "langchain_unsafe")
        assert spec.asm is not None
        read = spec.asm.read_ops[0]
        assert read.has_filter is False
        assert read.filter_keys == frozenset()

    def test_asm_safe_fixture_has_filter(self, adapter: LangChainAdapter) -> None:
        spec = adapter.parse(FIXTURES / "langchain_safe")
        assert spec.asm is not None
        reads_with_filter = [r for r in spec.asm.read_ops if r.has_filter]
        assert len(reads_with_filter) >= 1

    def test_asm_safe_fixture_filter_keys(self, adapter: LangChainAdapter) -> None:
        spec = adapter.parse(FIXTURES / "langchain_safe")
        assert spec.asm is not None
        filtered_read = next(r for r in spec.asm.read_ops if r.has_filter)
        assert "user_id" in filtered_read.filter_keys

    def test_asm_entry_points_on_fastapi_fixture(self, adapter: LangChainAdapter) -> None:
        spec = adapter.parse(FIXTURES / "asm_unauth_write")
        assert spec.asm is not None
        assert len(spec.asm.entry_points) >= 1
        assert spec.asm.entry_points[0].kind == "http_route"

    def test_asm_write_ops_on_unauth_fixture(self, adapter: LangChainAdapter) -> None:
        spec = adapter.parse(FIXTURES / "asm_unauth_write")
        assert spec.asm is not None
        assert len(spec.asm.write_ops) >= 1
        write = spec.asm.write_ops[0]
        assert write.method == "add_documents"
        assert "source" in write.metadata_keys

    def test_asm_edges_linked(self, adapter: LangChainAdapter) -> None:
        spec = adapter.parse(FIXTURES / "asm_unauth_write")
        assert spec.asm is not None
        assert len(spec.asm.edges) >= 1
        edge_kinds = {e.kind for e in spec.asm.edges}
        assert "writes_to" in edge_kinds

    def test_asm_none_for_empty_dir(self, adapter: LangChainAdapter, tmp_path: Path) -> None:
        spec = adapter.parse(tmp_path)
        assert spec.asm is None

    def test_asm_none_for_no_vectorstore(self, adapter: LangChainAdapter, tmp_path: Path) -> None:
        (tmp_path / "main.py").write_text("x = 1\n", encoding="utf-8")
        spec = adapter.parse(tmp_path)
        assert spec.asm is None

    def test_existing_fields_unchanged(self, adapter: LangChainAdapter) -> None:
        spec = adapter.parse(FIXTURES / "langchain_unsafe")
        assert len(spec.tools) >= 1
        assert len(spec.memory_configs) >= 1

    def test_asm_store_ids_unique(self, adapter: LangChainAdapter, tmp_path: Path) -> None:
        (tmp_path / "agent.py").write_text(
            "from langchain_community.vectorstores import Chroma, FAISS\n"
            "vs1 = Chroma(collection_name='a')\n"
            "vs2 = FAISS()\n",
            encoding="utf-8",
        )
        spec = adapter.parse(tmp_path)
        assert spec.asm is not None
        ids = [s.id for s in spec.asm.stores]
        assert len(ids) == len(set(ids))

    def test_asm_read_op_linked_to_correct_store(
        self, adapter: LangChainAdapter, tmp_path: Path
    ) -> None:
        (tmp_path / "agent.py").write_text(
            "from langchain_community.vectorstores import Chroma\n"
            "vs = Chroma(collection_name='docs')\n"
            "docs = vs.similarity_search('q')\n",
            encoding="utf-8",
        )
        spec = adapter.parse(tmp_path)
        assert spec.asm is not None
        store = spec.asm.stores[0]
        read = spec.asm.read_ops[0]
        assert read.store_id == store.id


class TestLangChainAdapterEdgeCases:
    def test_parse_error_skips_file(self, adapter: LangChainAdapter, tmp_path: Path) -> None:
        bad = tmp_path / "bad.py"
        bad.write_text("def (\n", encoding="utf-8")
        spec = adapter.parse(tmp_path)
        assert spec.framework == "langchain"
        assert len(spec.source_files) == 0

    def test_empty_directory(self, adapter: LangChainAdapter, tmp_path: Path) -> None:
        spec = adapter.parse(tmp_path)
        assert spec.tools == []
        assert spec.memory_configs == []
