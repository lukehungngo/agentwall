"""Base schema for framework models.

A framework model declares the patterns an engine should look for
when analyzing code that uses a specific AI framework. Adding a new
framework = writing a new model file using these schemas.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class StoreModel:
    """Describes a vector/memory store backend and its isolation contract.

    Not frozen because list fields (isolation_params, auth_params,
    persistence_params) are mutable; frozen dataclasses cannot hold
    plain list fields.
    """

    backend: str
    """Canonical backend name, e.g. 'chromadb', 'pgvector', 'faiss'."""

    isolation_params: list[str]
    """Constructor/init params that isolate tenants, e.g. ['collection_name']."""

    write_methods: dict[str, str]
    """method name → metadata kwarg, e.g. {'add_texts': 'metadata'}."""

    read_methods: dict[str, str]
    """method name → filter kwarg, e.g. {'similarity_search': 'filter'}."""

    retriever_factory: str | None = None
    """Method that returns a retriever object, e.g. 'as_retriever'."""

    retriever_filter_path: str | None = None
    """Dotted path to the filter kwarg on the retriever, e.g. 'search_kwargs.filter'."""

    auth_params: list[str] = field(default_factory=list)
    """Constructor params that carry credentials, e.g. ['api_key', 'connection_string']."""

    persistence_params: list[str] = field(default_factory=list)
    """Params that indicate local persistence, e.g. ['persist_directory']."""

    has_builtin_acl: bool = False
    """True when the backend enforces access control natively (e.g. managed cloud stores)."""


@dataclass(frozen=True)
class PipePattern:
    """Marks a binary operator used for pipeline composition (e.g. LCEL '|')."""

    operator: str
    """The operator token, e.g. '|'."""


@dataclass(frozen=True)
class FactoryPattern:
    """Describes a class-method factory that wires components together."""

    method: str
    """Factory method name, e.g. 'from_llm'."""

    kwarg: str
    """Keyword argument that accepts the retriever/store, e.g. 'retriever'."""

    role: str
    """Semantic role of the component wired in, e.g. 'retriever'."""


@dataclass(frozen=True)
class DecoratorPattern:
    """Describes a decorator that registers a function as an agent component."""

    decorator: str
    """Decorator name as it appears in source, e.g. 'tool'."""

    registers_as: str
    """Semantic role the decorated function takes on, e.g. 'tool'."""


@dataclass
class FrameworkModel:
    """Top-level declarative model for a single AI framework.

    Mutable (not frozen) because it holds list and dict fields that may be
    populated incrementally when constructing composite models.
    """

    name: str
    """Framework identifier, e.g. 'langchain', 'crewai'."""

    stores: dict[str, StoreModel]
    """Map from class name (as imported) to its StoreModel, e.g. {'Chroma': ...}."""

    pipe_patterns: list[PipePattern] = field(default_factory=list)
    """Pipeline composition operators used by this framework."""

    factory_patterns: list[FactoryPattern] = field(default_factory=list)
    """Factory methods that wire retrievers/stores into chains."""

    decorator_patterns: list[DecoratorPattern] = field(default_factory=list)
    """Decorators that register functions as agent tools or components."""

    auth_sources: list[str] = field(
        default_factory=lambda: [
            "request.user",
            "request.user_id",
            "session.user_id",
            "g.user",
            "current_user",
            "jwt.sub",
        ]
    )
    """Attribute/variable patterns where user identity enters the system."""

    tenant_param_names: list[str] = field(
        default_factory=lambda: ["user_id", "tenant_id", "org_id", "owner_id"]
    )
    """Parameter names that carry tenant identity."""

    memory_classes: list[str] = field(default_factory=list)
    """Class names that represent conversational memory buffers."""
