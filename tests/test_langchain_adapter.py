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

    def test_similarity_search_with_score_filtered(self, adapter: LangChainAdapter, tmp_path: Path) -> None:
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
            "    \"\"\"Deletes a record from the database.\"\"\"\n"
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

    def test_detects_structured_tool_subclass(self, adapter: LangChainAdapter, tmp_path: Path) -> None:
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

    def test_basetool_with_user_scope_check(self, adapter: LangChainAdapter, tmp_path: Path) -> None:
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
            "from langchain.agents import load_tools\n"
            "tools = load_tools(['shell'])\n",
            encoding="utf-8",
        )
        spec = adapter.parse(tmp_path)
        shell = next(t for t in spec.tools if t.name == "shell")
        assert shell.accepts_code_execution is True

    def test_load_tools_no_description(self, adapter: LangChainAdapter, tmp_path: Path) -> None:
        (tmp_path / "agent.py").write_text(
            "from langchain.agents import load_tools\n"
            "tools = load_tools(['arxiv'])\n",
            encoding="utf-8",
        )
        spec = adapter.parse(tmp_path)
        assert spec.tools[0].description is None


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
