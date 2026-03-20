"""Tests for the declarative framework model schema."""

from __future__ import annotations

import pytest

from agentwall.frameworks.base import (
    DecoratorPattern,
    FactoryPattern,
    FrameworkModel,
    PipePattern,
    StoreModel,
)

# ── StoreModel ────────────────────────────────────────────────────────────────


def test_store_model_required_fields() -> None:
    store = StoreModel(
        backend="chromadb",
        isolation_params=["collection_name"],
        write_methods={"add_texts": "metadata"},
        read_methods={"similarity_search": "filter"},
    )
    assert store.backend == "chromadb"
    assert store.isolation_params == ["collection_name"]
    assert store.write_methods == {"add_texts": "metadata"}
    assert store.read_methods == {"similarity_search": "filter"}


def test_store_model_defaults() -> None:
    store = StoreModel(
        backend="faiss",
        isolation_params=[],
        write_methods={},
        read_methods={},
    )
    assert store.retriever_factory is None
    assert store.retriever_filter_path is None
    assert store.auth_params == []
    assert store.persistence_params == []
    assert store.has_builtin_acl is False


def test_store_model_retriever_fields() -> None:
    store = StoreModel(
        backend="chromadb",
        isolation_params=["collection_name"],
        write_methods={"add_texts": "metadata"},
        read_methods={"similarity_search": "filter"},
        retriever_factory="as_retriever",
        retriever_filter_path="search_kwargs.filter",
    )
    assert store.retriever_factory == "as_retriever"
    assert store.retriever_filter_path == "search_kwargs.filter"


def test_store_model_auth_and_persistence_params() -> None:
    store = StoreModel(
        backend="pgvector",
        isolation_params=["namespace"],
        write_methods={"add_texts": "metadata"},
        read_methods={"similarity_search": "filter"},
        auth_params=["connection_string"],
        persistence_params=["persist_directory"],
    )
    assert store.auth_params == ["connection_string"]
    assert store.persistence_params == ["persist_directory"]


def test_store_model_has_builtin_acl() -> None:
    store = StoreModel(
        backend="pinecone",
        isolation_params=["namespace"],
        write_methods={"upsert": "metadata"},
        read_methods={"query": "filter"},
        has_builtin_acl=True,
    )
    assert store.has_builtin_acl is True


# ── PipePattern ───────────────────────────────────────────────────────────────


def test_pipe_pattern_creation() -> None:
    p = PipePattern(operator="|")
    assert p.operator == "|"


def test_pipe_pattern_is_frozen() -> None:
    p = PipePattern(operator="|")
    with pytest.raises((AttributeError, TypeError)):
        p.operator = ">>"  # type: ignore[misc]


# ── FactoryPattern ────────────────────────────────────────────────────────────


def test_factory_pattern_creation() -> None:
    f = FactoryPattern(method="from_llm", kwarg="retriever", role="retriever")
    assert f.method == "from_llm"
    assert f.kwarg == "retriever"
    assert f.role == "retriever"


def test_factory_pattern_is_frozen() -> None:
    f = FactoryPattern(method="from_llm", kwarg="retriever", role="retriever")
    with pytest.raises((AttributeError, TypeError)):
        f.method = "from_chain"  # type: ignore[misc]


# ── DecoratorPattern ──────────────────────────────────────────────────────────


def test_decorator_pattern_creation() -> None:
    d = DecoratorPattern(decorator="tool", registers_as="tool")
    assert d.decorator == "tool"
    assert d.registers_as == "tool"


def test_decorator_pattern_is_frozen() -> None:
    d = DecoratorPattern(decorator="tool", registers_as="tool")
    with pytest.raises((AttributeError, TypeError)):
        d.decorator = "agent"  # type: ignore[misc]


# ── FrameworkModel ────────────────────────────────────────────────────────────


def test_framework_model_stores_lookup() -> None:
    chroma = StoreModel(
        backend="chromadb",
        isolation_params=["collection_name"],
        write_methods={"add_texts": "metadata"},
        read_methods={"similarity_search": "filter"},
    )
    model = FrameworkModel(name="langchain", stores={"Chroma": chroma})
    assert model.stores["Chroma"] is chroma
    assert model.stores["Chroma"].backend == "chromadb"


def test_framework_model_empty_stores() -> None:
    model = FrameworkModel(name="custom", stores={})
    assert model.stores == {}


def test_framework_model_tenant_param_names_defaults() -> None:
    model = FrameworkModel(name="langchain", stores={})
    assert "user_id" in model.tenant_param_names
    assert "tenant_id" in model.tenant_param_names
    assert "org_id" in model.tenant_param_names
    assert "owner_id" in model.tenant_param_names


def test_framework_model_auth_sources_defaults() -> None:
    model = FrameworkModel(name="langchain", stores={})
    assert "request.user" in model.auth_sources
    assert "current_user" in model.auth_sources
    assert "jwt.sub" in model.auth_sources


def test_framework_model_pipe_patterns_default_empty() -> None:
    model = FrameworkModel(name="langchain", stores={})
    assert model.pipe_patterns == []


def test_framework_model_factory_patterns_default_empty() -> None:
    model = FrameworkModel(name="langchain", stores={})
    assert model.factory_patterns == []


def test_framework_model_decorator_patterns_default_empty() -> None:
    model = FrameworkModel(name="langchain", stores={})
    assert model.decorator_patterns == []


def test_framework_model_memory_classes_default_empty() -> None:
    model = FrameworkModel(name="langchain", stores={})
    assert model.memory_classes == []


def test_framework_model_with_all_pattern_types() -> None:
    chroma = StoreModel(
        backend="chromadb",
        isolation_params=["collection_name"],
        write_methods={"add_texts": "metadata"},
        read_methods={"similarity_search": "filter"},
        retriever_factory="as_retriever",
        retriever_filter_path="search_kwargs.filter",
    )
    model = FrameworkModel(
        name="langchain",
        stores={"Chroma": chroma},
        pipe_patterns=[PipePattern(operator="|")],
        factory_patterns=[FactoryPattern(method="from_llm", kwarg="retriever", role="retriever")],
        decorator_patterns=[DecoratorPattern(decorator="tool", registers_as="tool")],
        memory_classes=["ConversationBufferMemory"],
    )
    assert len(model.pipe_patterns) == 1
    assert model.pipe_patterns[0].operator == "|"
    assert len(model.factory_patterns) == 1
    assert model.factory_patterns[0].method == "from_llm"
    assert len(model.decorator_patterns) == 1
    assert model.decorator_patterns[0].decorator == "tool"
    assert "ConversationBufferMemory" in model.memory_classes


def test_framework_model_stores_missing_key() -> None:
    model = FrameworkModel(name="langchain", stores={})
    assert model.stores.get("NonExistent") is None
