"""Verify shared detection constants are complete and consistent."""

from agentwall.patterns import (
    FILTER_KWARGS,
    RETRIEVAL_METHODS,
    SANITIZE_NAMES,
    SINK_METHODS,
    TENANT_KEYS,
)


class TestRetrievalMethods:
    def test_contains_core_methods(self) -> None:
        assert "similarity_search" in RETRIEVAL_METHODS
        assert "as_retriever" in RETRIEVAL_METHODS
        assert "get_relevant_documents" in RETRIEVAL_METHODS
        assert "similarity_search_with_score" in RETRIEVAL_METHODS
        assert "max_marginal_relevance_search" in RETRIEVAL_METHODS

    def test_is_frozenset(self) -> None:
        assert isinstance(RETRIEVAL_METHODS, frozenset)


class TestFilterKwargs:
    def test_contains_core_kwargs(self) -> None:
        assert "filter" in FILTER_KWARGS
        assert "where" in FILTER_KWARGS
        assert "where_document" in FILTER_KWARGS

    def test_is_frozenset(self) -> None:
        assert isinstance(FILTER_KWARGS, frozenset)


class TestSinkMethods:
    def test_maps_methods_to_filter_params(self) -> None:
        assert SINK_METHODS["similarity_search"] == "filter"
        assert SINK_METHODS["as_retriever"] == "search_kwargs"

    def test_is_dict(self) -> None:
        assert isinstance(SINK_METHODS, dict)


class TestSanitizeNames:
    def test_contains_core_names(self) -> None:
        assert "sanitize" in SANITIZE_NAMES
        assert "escape" in SANITIZE_NAMES
        assert "strip_tags" in SANITIZE_NAMES

    def test_is_frozenset(self) -> None:
        assert isinstance(SANITIZE_NAMES, frozenset)


class TestTenantKeys:
    def test_contains_identity_keys(self) -> None:
        assert "user_id" in TENANT_KEYS
        assert "tenant_id" in TENANT_KEYS
        assert "org_id" in TENANT_KEYS
        assert "owner_id" in TENANT_KEYS
