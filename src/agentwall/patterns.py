"""Shared detection constants used across analyzers, adapters, and probes.

Single source of truth for method names, keyword sets, and filter parameters
that multiple modules need to agree on. Import from here — never redefine.
"""

from __future__ import annotations

# ── Retrieval methods that indicate a vector store query ─────────────────────

RETRIEVAL_METHODS: frozenset[str] = frozenset(
    [
        "similarity_search",
        "similarity_search_with_score",
        "max_marginal_relevance_search",
        "as_retriever",
        "get_relevant_documents",
    ]
)

# ── Filter kwargs that indicate tenant scoping ───────────────────────────────

FILTER_KWARGS: frozenset[str] = frozenset(["filter", "where", "where_document"])

# ── Taint sources: where user identity enters the system ─────────────────────

SOURCE_PATTERNS: list[str] = [
    # Attribute access patterns
    "request.user",
    "request.user_id",
    "request.headers",
    "session.user_id",
    "session.user",
    "g.user",
    "current_user",
    "auth.user",
    # Common parameter names
    "user_id",
    "tenant_id",
    "org_id",
    "owner_id",
    "user",
    "tenant",
    "owner",
]

SIMPLE_SOURCE_NAMES: frozenset[str] = frozenset(
    s for s in SOURCE_PATTERNS if "." not in s
)

# ── Taint sinks: retrieval method → expected filter parameter ────────────────

SINK_METHODS: dict[str, str] = {
    "similarity_search": "filter",
    "similarity_search_with_score": "filter",
    "max_marginal_relevance_search": "filter",
    "as_retriever": "search_kwargs",
    "get_relevant_documents": "filter",
}

# ── Sanitization heuristics ──────────────────────────────────────────────────

SANITIZE_NAMES: frozenset[str] = frozenset(
    [
        "sanitize",
        "sanitise",
        "clean",
        "strip_tags",
        "escape",
        "filter_content",
        "scrub",
        "bleach",
        "clean_text",
        "sanitize_output",
        "sanitize_content",
    ]
)

# ── Destructive tool keywords ────────────────────────────────────────────────

DESTRUCTIVE_KEYWORDS: frozenset[str] = frozenset(
    ["delete", "remove", "drop", "rm", "write", "send", "post", "execute", "run"]
)

# ── Code execution detection ─────────────────────────────────────────────────

CODE_EXEC_CALLS: frozenset[str] = frozenset(["subprocess", "eval", "exec"])
CODE_EXEC_KEYWORDS: frozenset[str] = frozenset(
    ["shell", "exec", "eval", "subprocess", "code", "script", "sql"]
)

# ── Tenant identity keys ─────────────────────────────────────────────────────

TENANT_KEYS: frozenset[str] = frozenset(
    {"user_id", "tenant_id", "org_id", "owner_id"}
)
