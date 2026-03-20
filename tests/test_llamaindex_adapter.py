"""Tests for LlamaIndexAdapter."""

from __future__ import annotations

from pathlib import Path

import pytest

from agentwall.adapters.llamaindex import LlamaIndexAdapter

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture()
def adapter() -> LlamaIndexAdapter:
    return LlamaIndexAdapter()


class TestLlamaIndexAdapterBasic:
    def test_returns_agent_spec(self, adapter: LlamaIndexAdapter) -> None:
        spec = adapter.parse(FIXTURES / "llamaindex_basic")
        assert spec.framework == "llamaindex"

    def test_source_files_populated(self, adapter: LlamaIndexAdapter) -> None:
        spec = adapter.parse(FIXTURES / "llamaindex_basic")
        assert len(spec.source_files) >= 1

    def test_detects_vector_store_index(self, adapter: LlamaIndexAdapter) -> None:
        """VectorStoreIndex.from_documents() creates a MemoryConfig."""
        spec = adapter.parse(FIXTURES / "llamaindex_basic")
        backends = [m.backend for m in spec.memory_configs]
        assert "vectorstoreindex" in backends

    def test_detects_chroma_vector_store(self, adapter: LlamaIndexAdapter) -> None:
        """ChromaVectorStore() creates a MemoryConfig with backend=chromadb."""
        spec = adapter.parse(FIXTURES / "llamaindex_basic")
        backends = [m.backend for m in spec.memory_configs]
        assert "chromadb" in backends

    def test_detects_query_engine_tool(self, adapter: LlamaIndexAdapter) -> None:
        """QueryEngineTool.from_defaults() creates a ToolSpec."""
        spec = adapter.parse(FIXTURES / "llamaindex_basic")
        tool_names = [t.name for t in spec.tools]
        assert "search" in tool_names

    def test_detects_function_tool(self, adapter: LlamaIndexAdapter) -> None:
        """FunctionTool.from_defaults() creates a ToolSpec."""
        spec = adapter.parse(FIXTURES / "llamaindex_basic")
        tool_names = [t.name for t in spec.tools]
        assert "custom_func" in tool_names

    def test_detects_chat_memory_buffer(self, adapter: LlamaIndexAdapter) -> None:
        """ChatMemoryBuffer creates a MemoryConfig with injection_risk=True."""
        spec = adapter.parse(FIXTURES / "llamaindex_basic")
        mem = next(
            m for m in spec.memory_configs if m.backend == "chat_memory_buffer"
        )
        assert mem.has_injection_risk is True

    def test_no_retrieval_filter_by_default(self, adapter: LlamaIndexAdapter) -> None:
        """as_query_engine() and as_retriever() without filters."""
        spec = adapter.parse(FIXTURES / "llamaindex_basic")
        vs_configs = [
            m for m in spec.memory_configs if m.backend == "vectorstoreindex"
        ]
        assert len(vs_configs) >= 1
        assert not vs_configs[0].has_metadata_filter_on_retrieval


class TestLlamaIndexAdapterRetrieval:
    def test_query_with_filter(self, adapter: LlamaIndexAdapter, tmp_path: Path) -> None:
        (tmp_path / "agent.py").write_text(
            "from llama_index.core import VectorStoreIndex\n"
            "index = VectorStoreIndex.from_documents(docs)\n"
            "engine = index.as_query_engine(filters=tenant_filter)\n",
            encoding="utf-8",
        )
        spec = adapter.parse(tmp_path)
        mc = next(m for m in spec.memory_configs if m.backend == "vectorstoreindex")
        assert mc.has_metadata_filter_on_retrieval is True

    def test_retriever_without_filter(self, adapter: LlamaIndexAdapter, tmp_path: Path) -> None:
        (tmp_path / "agent.py").write_text(
            "from llama_index.core import VectorStoreIndex\n"
            "index = VectorStoreIndex.from_documents(docs)\n"
            "retriever = index.as_retriever(similarity_top_k=10)\n",
            encoding="utf-8",
        )
        spec = adapter.parse(tmp_path)
        mc = next(m for m in spec.memory_configs if m.backend == "vectorstoreindex")
        assert not mc.has_metadata_filter_on_retrieval

    def test_qdrant_query_filter(self, adapter: LlamaIndexAdapter, tmp_path: Path) -> None:
        """QdrantVectorStore uses query_filter= kwarg."""
        (tmp_path / "agent.py").write_text(
            "from llama_index.vector_stores.qdrant import QdrantVectorStore\n"
            "vs = QdrantVectorStore(collection_name='docs')\n"
            "results = vs.query(query_filter=tenant_filter)\n",
            encoding="utf-8",
        )
        spec = adapter.parse(tmp_path)
        mc = next(m for m in spec.memory_configs if m.backend == "qdrant")
        assert mc.has_metadata_filter_on_retrieval is True


class TestLlamaIndexAdapterEdgeCases:
    def test_empty_directory(self, adapter: LlamaIndexAdapter, tmp_path: Path) -> None:
        spec = adapter.parse(tmp_path)
        assert spec.tools == []
        assert spec.memory_configs == []
        assert spec.framework == "llamaindex"

    def test_parse_error_skips_file(self, adapter: LlamaIndexAdapter, tmp_path: Path) -> None:
        (tmp_path / "bad.py").write_text("def (\n", encoding="utf-8")
        spec = adapter.parse(tmp_path)
        assert len(spec.source_files) == 0

    def test_no_llamaindex_patterns(self, adapter: LlamaIndexAdapter, tmp_path: Path) -> None:
        (tmp_path / "main.py").write_text("x = 1\n", encoding="utf-8")
        spec = adapter.parse(tmp_path)
        assert spec.tools == []
        assert spec.memory_configs == []
        assert len(spec.source_files) == 1

    def test_tool_description_extracted(self, adapter: LlamaIndexAdapter, tmp_path: Path) -> None:
        (tmp_path / "agent.py").write_text(
            "from llama_index.core.tools import QueryEngineTool\n"
            "tool = QueryEngineTool.from_defaults(\n"
            "    query_engine=engine, name='search', description='Search docs'\n"
            ")\n",
            encoding="utf-8",
        )
        spec = adapter.parse(tmp_path)
        assert spec.tools[0].description == "Search docs"

    def test_destructive_tool_flagged(self, adapter: LlamaIndexAdapter, tmp_path: Path) -> None:
        (tmp_path / "agent.py").write_text(
            "from llama_index.core.tools import FunctionTool\n"
            "tool = FunctionTool.from_defaults(fn=delete_fn, name='delete_records')\n",
            encoding="utf-8",
        )
        spec = adapter.parse(tmp_path)
        assert spec.tools[0].is_destructive is True

    def test_pinecone_vector_store(self, adapter: LlamaIndexAdapter, tmp_path: Path) -> None:
        (tmp_path / "agent.py").write_text(
            "from llama_index.vector_stores.pinecone import PineconeVectorStore\n"
            "vs = PineconeVectorStore()\n",
            encoding="utf-8",
        )
        spec = adapter.parse(tmp_path)
        backends = [m.backend for m in spec.memory_configs]
        assert "pinecone" in backends
