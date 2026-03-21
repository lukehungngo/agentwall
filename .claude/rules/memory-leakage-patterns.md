---
paths:
  - "src/agentwall/analyzers/memory.py"
  - "src/agentwall/analyzers/tools.py"
  - "src/agentwall/analyzers/rag.py"
  - "src/agentwall/analyzers/agent_arch.py"
  - "src/agentwall/engine/isolation_evidence.py"
  - "src/agentwall/probes/**"
  - "tests/test_memory_analyzer.py"
  - "tests/test_tool_analyzer.py"
  - "tests/test_rag_analyzer.py"
  - "tests/test_taint.py"
---

# Memory Leakage Detection Patterns

The core bug: a vector similarity search is called without a user/tenant filter.
The vector store returns the closest vectors globally — including other users' data.

## Three failure modes to detect

1. **Missing filter entirely** — `collection.query(embedding)` with no `where` clause
2. **Metadata mismatch** — `add_texts(metadata={"user_id": x})` but `similarity_search(query)` with no filter. This is the most common false sense of security.
3. **FAISS** — no native access control. Always flag as HIGH. Only check for wrapper existence.

## Framework-agnostic AST fallback

When no adapter matches (`spec is None`), MemoryAnalyzer and ToolAnalyzer run AST fallback:

- **MemoryAnalyzer** scans for vectorstore imports (chromadb/faiss/pinecone/qdrant/milvus/weaviate), builds synthetic `MemoryConfig` objects
- **ToolAnalyzer** scans for `@tool` decorators and dangerous calls (`exec()`/`eval()`/`subprocess.run()`), builds synthetic `ToolSpec` objects
- **RAGAnalyzer** and **AgentArchAnalyzer** are fully framework-agnostic — they only use `ctx.source_files`

### Critical P0 lesson: subprocess qualification

`_SUBPROCESS_ATTRS` must check the receiver is `subprocess`, not just any `.run()` call. Without this, `model.run()`, `app.run()` etc. all false-match as TOOL-002.

```python
# CORRECT — qualifies the receiver
isinstance(child.func.value, ast.Name) and child.func.value.id == "subprocess"
```

## Neo4j special handling

Neo4j is graph-aware, not vector-store-like:
- Isolation = `BELONGS_TO` relationship scoping on Cypher queries
- Unscoped graph traversal can expose entire connected subgraphs across user boundaries

## Full rules reference

| Rule ID | Severity | Category | What It Checks |
|---|---|---|---|
| AW-MEM-001 | CRITICAL | memory | No tenant isolation in vector store |
| AW-MEM-002 | HIGH | memory | Shared collection, no metadata filter |
| AW-MEM-003 | HIGH | memory | Memory backend has no access control config |
| AW-MEM-004 | HIGH | memory | Known injection patterns in memory retrieval path |
| AW-MEM-005 | MEDIUM | memory | No sanitization on retrieved memory before context injection |
| AW-TOOL-001 | HIGH | tool | Destructive tools accessible without approval gate |
| AW-TOOL-002 | MEDIUM | tool | Tool accepts arbitrary code/SQL/shell execution |
| AW-TOOL-003 | MEDIUM | tool | High-risk tool lacks user-scope access check |
| AW-TOOL-004 | LOW | tool | Tool has no description (blocks risk classification) |
| AW-TOOL-005 | INFO | tool | Agent has >15 tools (exceeds recommended limit) |
| AW-SEC-001 | HIGH | secrets | Hardcoded API key/secret in agent config |
| AW-SEC-002 | MEDIUM | secrets | Env var injected into prompt template |
| AW-SEC-003 | MEDIUM | secrets | Agent context logged at DEBUG level |
| AW-RAG-001 | HIGH | rag | Retrieved context injected without delimiters |
| AW-RAG-002 | HIGH | rag | Ingestion from untrusted source without validation |
| AW-RAG-003 | MEDIUM | rag | Unencrypted local vector store persistence |
| AW-RAG-004 | HIGH | rag | Vector store exposed on network without auth |
| AW-MCP-001 | HIGH | mcp | MCP server over HTTP without auth |
| AW-MCP-002 | HIGH | mcp | Static long-lived token in MCP config |
| AW-MCP-003 | MEDIUM | mcp | MCP tool with shell/filesystem access |
| AW-SER-001 | HIGH | serialization | Unsafe deserialization (pickle, yaml.unsafe_load) |
| AW-SER-002 | MEDIUM | serialization | Unpinned agent framework dependency |
| AW-SER-003 | MEDIUM | serialization | Dynamic import of external tool/plugin |
| AW-AGT-001 | HIGH | agent | Sub-agent inherits full parent tool set |
| AW-AGT-002 | MEDIUM | agent | Agent-to-agent communication without auth |
| AW-AGT-003 | MEDIUM | agent | Agent has RWD on same resource without approval |
| AW-AGT-004 | HIGH | agent | LLM output stored to memory without validation |
| AW-CFG-* | MEDIUM–HIGH | config | Config file issues (hardcoded secrets, no auth, debug mode, no TLS) |

## Known FP hotspots (v1.0)

- **AW-RAG-002** (~55% FP) — triggers on any file read/HTTP fetch near vectorstore code
- **AW-MEM-002** (~27% FP) — metadata write without matching filter, but sometimes isolation exists elsewhere
- **AW-AGT-004** (~25% FP) — LLM output → memory, but validation may happen in a different module
