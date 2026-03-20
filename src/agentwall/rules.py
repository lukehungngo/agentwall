"""All rule definitions: AW-MEM, AW-TOOL, AW-SEC, AW-RAG, AW-MCP, AW-SER, AW-AGT."""

from dataclasses import dataclass

from agentwall.models import Category, Severity


@dataclass(frozen=True)
class RuleDef:
    rule_id: str
    title: str
    severity: Severity
    category: Category
    description: str
    fix: str


# ── Memory rules ─────────────────────────────────────────────────────────────

AW_MEM_001 = RuleDef(
    rule_id="AW-MEM-001",
    title="No tenant isolation in vector store",
    severity=Severity.CRITICAL,
    category=Category.MEMORY,
    description=(
        "Vector store queries are executed without any user/tenant filter. "
        "A similarity search returns the globally closest vectors — including other users' data."
    ),
    fix="Add a metadata filter on every retrieval call: similarity_search(query, filter={'user_id': user_id})",
)

AW_MEM_002 = RuleDef(
    rule_id="AW-MEM-002",
    title="Shared collection without metadata filter on retrieval",
    severity=Severity.HIGH,
    category=Category.MEMORY,
    description=(
        "Documents are written with user-scoped metadata (e.g. user_id) but retrieved "
        "without a matching filter. The write-time metadata provides false security."
    ),
    fix="Ensure every retrieval call includes the same metadata filter used at write time.",
)

AW_MEM_003 = RuleDef(
    rule_id="AW-MEM-003",
    title="Memory backend has no access control configuration",
    severity=Severity.HIGH,
    category=Category.MEMORY,
    description=(
        "The configured memory backend has no observable access control setup. "
        "Without explicit isolation, all agents share the same memory namespace."
    ),
    fix="Configure per-user collections or namespaces, or add metadata-based filtering.",
)

AW_MEM_004 = RuleDef(
    rule_id="AW-MEM-004",
    title="Known injection patterns in memory retrieval path",
    severity=Severity.HIGH,
    category=Category.MEMORY,
    description=(
        "The memory retrieval path uses unsanitized external input. "
        "This is a vector for memory poisoning attacks (MINJA, MemoryGraft patterns)."
    ),
    fix="Sanitize all content before storing it to memory. Validate retrieved content before injecting into context.",
)

AW_MEM_005 = RuleDef(
    rule_id="AW-MEM-005",
    title="No sanitization on retrieved memory before context injection",
    severity=Severity.MEDIUM,
    category=Category.MEMORY,
    description=(
        "Retrieved memory content is injected directly into the agent context without sanitization. "
        "Poisoned memories can influence agent behavior across sessions."
    ),
    fix="Pass retrieved memories through a sanitization step before adding to context.",
)

# ── Tool rules ────────────────────────────────────────────────────────────────

AW_TOOL_001 = RuleDef(
    rule_id="AW-TOOL-001",
    title="Destructive tool accessible without approval gate",
    severity=Severity.HIGH,
    category=Category.TOOL,
    description=(
        "A tool classified as destructive (deletes data, modifies files, sends messages) "
        "is registered without a human-in-the-loop approval gate."
    ),
    fix="Wrap destructive tools with an approval gate (e.g. HumanApprovalCallbackHandler).",
)

AW_TOOL_002 = RuleDef(
    rule_id="AW-TOOL-002",
    title="Tool accepts arbitrary code/SQL/shell execution",
    severity=Severity.MEDIUM,
    category=Category.TOOL,
    description=(
        "A tool can execute arbitrary code, SQL queries, or shell commands. "
        "Without input validation this enables prompt-injection-to-RCE escalation."
    ),
    fix="Restrict tool inputs with an allowlist schema. Avoid eval/exec patterns.",
)

AW_TOOL_003 = RuleDef(
    rule_id="AW-TOOL-003",
    title="High-risk tool lacks user-scope access check",
    severity=Severity.MEDIUM,
    category=Category.TOOL,
    description=(
        "A high-risk tool (file access, database query, API call) does not verify "
        "that the requesting user has permission to perform the requested action."
    ),
    fix="Add a user-scope check at the start of the tool function.",
)

AW_TOOL_004 = RuleDef(
    rule_id="AW-TOOL-004",
    title="Tool has no description",
    severity=Severity.LOW,
    category=Category.TOOL,
    description=(
        "A registered tool has no description. This blocks risk classification and "
        "degrades the LLM's ability to select tools correctly."
    ),
    fix="Add a docstring or description= argument to every tool.",
)

AW_TOOL_005 = RuleDef(
    rule_id="AW-TOOL-005",
    title="Agent has >15 tools (exceeds recommended limit)",
    severity=Severity.INFO,
    category=Category.TOOL,
    description=(
        "The agent has more than 15 registered tools. Large tool sets increase "
        "token usage and reduce tool-selection accuracy."
    ),
    fix="Split the agent into specialized sub-agents with focused tool sets.",
)

# ── Secrets rules ────────────────────────────────────────────────────────────

AW_SEC_001 = RuleDef(
    rule_id="AW-SEC-001",
    title="Hardcoded API key/secret in agent config",
    severity=Severity.HIGH,
    category=Category.SECRETS,
    description=(
        "A string literal matching known API key patterns (sk-, AKIA, ghp_, xoxb-) "
        "was found in agent or tool configuration code."
    ),
    fix="Move secrets to environment variables or a secrets manager.",
)

AW_SEC_002 = RuleDef(
    rule_id="AW-SEC-002",
    title="Env var injected into prompt template",
    severity=Severity.MEDIUM,
    category=Category.SECRETS,
    description=(
        "An environment variable value flows into a prompt template. "
        "If the env var contains sensitive data, it will be sent to the LLM."
    ),
    fix="Redact sensitive env vars before injecting into prompts.",
)

AW_SEC_003 = RuleDef(
    rule_id="AW-SEC-003",
    title="Agent context logged at DEBUG level",
    severity=Severity.MEDIUM,
    category=Category.SECRETS,
    description=(
        "Agent memory, chat history, or conversation context is passed to "
        "a logging or print call. This may expose sensitive user data in logs."
    ),
    fix="Redact or summarize context before logging. Never log full conversation state.",
)

# ── RAG rules ────────────────────────────────────────────────────────────────

AW_RAG_001 = RuleDef(
    rule_id="AW-RAG-001",
    title="Retrieved context injected into prompt without delimiters",
    severity=Severity.HIGH,
    category=Category.RAG,
    description=(
        "Retrieved documents are concatenated directly into a prompt without structural "
        "delimiters (XML tags, fenced blocks). This increases indirect prompt injection risk."
    ),
    fix="Wrap retrieved content in explicit delimiters: <context>...</context> or similar.",
)

AW_RAG_002 = RuleDef(
    rule_id="AW-RAG-002",
    title="Ingestion from untrusted source without validation",
    severity=Severity.HIGH,
    category=Category.RAG,
    description=(
        "Documents from an external source (HTTP, file upload, web scraper) are ingested "
        "into the vector store without content validation or sanitization."
    ),
    fix="Validate and sanitize document content before calling add_documents/add_texts.",
)

AW_RAG_003 = RuleDef(
    rule_id="AW-RAG-003",
    title="Unencrypted local vector store persistence",
    severity=Severity.MEDIUM,
    category=Category.RAG,
    description=(
        "A local vector store (FAISS, Chroma) persists data to disk without encryption. "
        "Stored embeddings and documents are readable by any process with file access."
    ),
    fix="Encrypt the persistence directory or use a vector store with built-in encryption.",
)

AW_RAG_004 = RuleDef(
    rule_id="AW-RAG-004",
    title="Vector store exposed on network without auth",
    severity=Severity.HIGH,
    category=Category.RAG,
    description=(
        "A vector store client connects to a remote server without authentication parameters. "
        "The store may be accessible to anyone on the network."
    ),
    fix="Add api_key, auth_credentials, or equivalent auth parameters to the client.",
)

# ── MCP rules ────────────────────────────────────────────────────────────────

AW_MCP_001 = RuleDef(
    rule_id="AW-MCP-001",
    title="MCP server over HTTP without authentication",
    severity=Severity.HIGH,
    category=Category.MCP,
    description=(
        "An MCP server is exposed over HTTP/SSE without authentication middleware. "
        "Any client on the network can invoke its tools."
    ),
    fix="Add authentication middleware to the MCP server handler chain.",
)

AW_MCP_002 = RuleDef(
    rule_id="AW-MCP-002",
    title="Static long-lived token in MCP config",
    severity=Severity.HIGH,
    category=Category.MCP,
    description=(
        "A hardcoded token or API key was found in MCP server/client initialization. "
        "Static credentials cannot be rotated without redeployment."
    ),
    fix="Load MCP credentials from environment variables or a secrets manager.",
)

AW_MCP_003 = RuleDef(
    rule_id="AW-MCP-003",
    title="MCP tool with shell/filesystem access",
    severity=Severity.MEDIUM,
    category=Category.MCP,
    description=(
        "An MCP tool handler contains subprocess, os.system, or open() calls with "
        "variable arguments. This enables arbitrary command/file execution via the tool."
    ),
    fix="Restrict tool inputs with an allowlist. Avoid shell=True and variable file paths.",
)

# ── Serialization rules ─────────────────────────────────────────────────────

AW_SER_001 = RuleDef(
    rule_id="AW-SER-001",
    title="Unsafe deserialization of agent state",
    severity=Severity.HIGH,
    category=Category.SERIALIZATION,
    description=(
        "Unsafe deserialization (pickle.load, yaml.unsafe_load, torch.load) is used "
        "in an agent or memory code path. This enables remote code execution if the "
        "serialized data is attacker-controlled."
    ),
    fix="Use safe alternatives: json, yaml.safe_load, torch.load(weights_only=True).",
)

AW_SER_002 = RuleDef(
    rule_id="AW-SER-002",
    title="Unpinned agent framework dependency",
    severity=Severity.MEDIUM,
    category=Category.SERIALIZATION,
    description=(
        "An agent framework library is listed as a dependency without a version pin. "
        "Unpinned dependencies can introduce breaking changes or vulnerabilities silently."
    ),
    fix="Pin agent framework dependencies to a specific version or bounded range.",
)

AW_SER_003 = RuleDef(
    rule_id="AW-SER-003",
    title="Dynamic import of external tool/plugin",
    severity=Severity.MEDIUM,
    category=Category.SERIALIZATION,
    description=(
        "importlib.import_module() or __import__() is called with a variable argument "
        "in a tool registration path. This enables loading arbitrary code as a tool."
    ),
    fix="Use a static tool registry with explicit imports. Avoid dynamic plugin loading.",
)

# ── Agent architecture rules ────────────────────────────────────────────────

AW_AGT_001 = RuleDef(
    rule_id="AW-AGT-001",
    title="Sub-agent inherits full parent tool set",
    severity=Severity.HIGH,
    category=Category.AGENT,
    description=(
        "A sub-agent receives the full tool set of its parent agent without filtering. "
        "This violates the principle of least privilege."
    ),
    fix="Filter the tool list to only tools the sub-agent needs.",
)

AW_AGT_002 = RuleDef(
    rule_id="AW-AGT-002",
    title="Agent-to-agent communication without authentication",
    severity=Severity.MEDIUM,
    category=Category.AGENT,
    description=(
        "An agent delegation call passes no authentication-related parameters. "
        "The receiving agent cannot verify the caller's identity."
    ),
    fix="Pass auth tokens or session credentials in agent delegation calls.",
)

AW_AGT_003 = RuleDef(
    rule_id="AW-AGT-003",
    title="Agent has read+write+delete on same resource without separate approval",
    severity=Severity.MEDIUM,
    category=Category.AGENT,
    description=(
        "An agent has tools for reading, writing, and deleting the same resource type "
        "but the destructive tools lack a separate approval gate."
    ),
    fix="Add a separate approval gate for destructive tools on shared resources.",
)

AW_AGT_004 = RuleDef(
    rule_id="AW-AGT-004",
    title="LLM output stored to memory without validation",
    severity=Severity.HIGH,
    category=Category.AGENT,
    description=(
        "LLM output is stored directly into agent memory or a vector store without "
        "validation. This enables memory poisoning (MemoryGraft) attacks."
    ),
    fix="Validate or sanitize LLM output before persisting to memory.",
)

# ── Registry ──────────────────────────────────────────────────────────────────

ALL_RULES: dict[str, RuleDef] = {
    r.rule_id: r
    for r in [
        AW_MEM_001,
        AW_MEM_002,
        AW_MEM_003,
        AW_MEM_004,
        AW_MEM_005,
        AW_TOOL_001,
        AW_TOOL_002,
        AW_TOOL_003,
        AW_TOOL_004,
        AW_TOOL_005,
        AW_SEC_001,
        AW_SEC_002,
        AW_SEC_003,
        AW_RAG_001,
        AW_RAG_002,
        AW_RAG_003,
        AW_RAG_004,
        AW_MCP_001,
        AW_MCP_002,
        AW_MCP_003,
        AW_SER_001,
        AW_SER_002,
        AW_SER_003,
        AW_AGT_001,
        AW_AGT_002,
        AW_AGT_003,
        AW_AGT_004,
    ]
}
