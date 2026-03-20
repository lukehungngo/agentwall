"""Verify shared detection constants are complete and consistent."""

from agentwall import patterns
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


class TestNewPatterns:
    """Tests for pattern constants added in Task 3."""

    def test_secret_prefixes_exist(self) -> None:
        assert "sk-" in patterns.SECRET_PREFIXES
        assert "AKIA" in patterns.SECRET_PREFIXES
        assert "ghp_" in patterns.SECRET_PREFIXES

    def test_secret_prefixes_is_list(self) -> None:
        assert isinstance(patterns.SECRET_PREFIXES, list)

    def test_secret_kwarg_names_exist(self) -> None:
        assert "api_key" in patterns.SECRET_KWARG_NAMES
        assert "token" in patterns.SECRET_KWARG_NAMES
        assert "password" in patterns.SECRET_KWARG_NAMES

    def test_secret_kwarg_names_is_frozenset(self) -> None:
        assert isinstance(patterns.SECRET_KWARG_NAMES, frozenset)

    def test_secret_entropy_constants(self) -> None:
        assert patterns.SECRET_ENTROPY_MIN_LEN == 20
        assert patterns.SECRET_ENTROPY_THRESHOLD == 4.5

    def test_unsafe_deser_calls_exist(self) -> None:
        assert "pickle.load" in patterns.UNSAFE_DESER_CALLS
        assert "pickle.loads" in patterns.UNSAFE_DESER_CALLS
        assert "yaml.unsafe_load" in patterns.UNSAFE_DESER_CALLS
        assert "torch.load" in patterns.UNSAFE_DESER_CALLS

    def test_safe_yaml_loaders_exist(self) -> None:
        assert "SafeLoader" in patterns.SAFE_YAML_LOADERS

    def test_mcp_imports_exist(self) -> None:
        assert "mcp" in patterns.MCP_IMPORTS
        assert "mcp.server" in patterns.MCP_IMPORTS

    def test_mcp_shell_calls_exist(self) -> None:
        assert "subprocess.run" in patterns.MCP_SHELL_CALLS
        assert "os.system" in patterns.MCP_SHELL_CALLS

    def test_dynamic_import_calls_exist(self) -> None:
        assert "importlib.import_module" in patterns.DYNAMIC_IMPORT_CALLS
        assert "__import__" in patterns.DYNAMIC_IMPORT_CALLS

    def test_context_var_names_exist(self) -> None:
        assert "chat_history" in patterns.CONTEXT_VAR_NAMES
        assert "memory" in patterns.CONTEXT_VAR_NAMES
        assert "messages" in patterns.CONTEXT_VAR_NAMES

    def test_agent_framework_packages_exist(self) -> None:
        assert "langchain" in patterns.AGENT_FRAMEWORK_PACKAGES
        assert "crewai" in patterns.AGENT_FRAMEWORK_PACKAGES
        assert "mcp" in patterns.AGENT_FRAMEWORK_PACKAGES

    def test_delimiter_patterns_exist(self) -> None:
        assert len(patterns.RAG_DELIMITER_PATTERNS) > 0
        assert "<context>" in patterns.RAG_DELIMITER_PATTERNS
        assert "</context>" in patterns.RAG_DELIMITER_PATTERNS

    def test_untrusted_source_calls_exist(self) -> None:
        assert "requests.get" in patterns.UNTRUSTED_SOURCE_CALLS
        assert "BeautifulSoup" in patterns.UNTRUSTED_SOURCE_CALLS

    def test_vector_store_network_clients_exist(self) -> None:
        assert "QdrantClient" in patterns.VECTOR_STORE_NETWORK_CLIENTS
        assert "HttpClient" in patterns.VECTOR_STORE_NETWORK_CLIENTS

    def test_vector_store_auth_kwargs_exist(self) -> None:
        assert "api_key" in patterns.VECTOR_STORE_AUTH_KWARGS
        assert "token" in patterns.VECTOR_STORE_AUTH_KWARGS

    def test_existing_patterns_unchanged(self) -> None:
        assert len(patterns.RETRIEVAL_METHODS) == 5
        assert len(patterns.FILTER_KWARGS) == 3
