---
paths:
  - "src/agentwall/analyzers/**"
  - "src/agentwall/probes/**"
  - "tests/test_memory_analyzer.py"
  - "tests/test_taint.py"
---

# Memory Leakage Detection Patterns

The core bug: a vector similarity search is called without a user/tenant filter.
The vector store returns the closest vectors globally — including other users' data.

## Three failure modes to detect

1. **Missing filter entirely** — `collection.query(embedding)` with no `where` clause
2. **Metadata mismatch** — `add_texts(metadata={"user_id": x})` but `similarity_search(query)` with no filter. This is the most common false sense of security.
3. **FAISS** — no native access control. `FaissProbe.detect_static()` always returns HIGH. Only check for wrapper existence.

## Neo4j special handling

Neo4j is graph-aware, not vector-store-like:
- Isolation = `BELONGS_TO` relationship scoping on Cypher queries
- Cypher parsing is string-based (regex + AST)
- Unscoped graph traversal can expose entire connected subgraphs across user boundaries

## Rules reference

| Rule ID | Severity | What It Checks |
|---|---|---|
| AW-MEM-001 | CRITICAL | No tenant isolation in vector store |
| AW-MEM-002 | HIGH | Shared collection, no metadata filter |
| AW-MEM-003 | HIGH | Memory backend has no access control config |
| AW-MEM-004 | HIGH | Known injection patterns in memory retrieval path |
| AW-MEM-005 | MEDIUM | No sanitization on retrieved memory before context injection |
| AW-TOOL-001 | HIGH | Destructive tools accessible without approval gate |
| AW-TOOL-002 | MEDIUM | Tool accepts arbitrary code/SQL/shell execution |
| AW-TOOL-003 | MEDIUM | High-risk tool lacks user-scope access check |
| AW-TOOL-004 | LOW | Tool has no description (blocks risk classification) |
| AW-TOOL-005 | INFO | Agent has >15 tools (exceeds recommended limit) |
