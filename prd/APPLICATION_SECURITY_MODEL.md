# Application Security Model (ASM)

## Design Specification for Semantic-Level Agent Security Analysis

**Version:** 0.1 — Draft
**Date:** 2026-03-18
**Author:** SoH Engineering
**Status:** Design phase
**Parent:** [PRD v4](../prd/AgentWall_PRD_v4.md)
**Scope:** Defines a new analysis architecture that builds a semantic model of the target application, then queries that model for security violations — replacing pattern-matching with model-querying.

---

## 1. Problem Statement

### What L0–L8 Actually Do

AgentWall's current 9-layer pipeline is a **pattern-matching** system operating at increasing granularity:

```
L0  "Is this a LangChain project?"              → regex on imports
L1  "Does this call have a filter kwarg?"        → AST kwarg inspection
L2  "Does any caller in the chain add a filter?" → call graph traversal
L3  "Does user_id flow from request to filter?"  → taint tracking
L4  "Is the config insecure?"                    → config file parsing
L5  "Does this match a known-bad pattern?"       → Semgrep rules
L6  "Is the filter present on ALL branches?"     → symbolic execution
L7  "Is the filter present at runtime?"          → monkey-patching
L8  "Is this finding real or a false positive?"  → LLM judgment
```

Every layer asks a question about **individual code sites** or **individual data flows**. None of them asks a question about the **application as a whole**.

### What L0–L8 Cannot Answer

Questions that require application-level understanding:

| Question | Why L0–L8 Can't Answer It |
|---|---|
| "Does the metadata schema at ingestion match the filter schema at retrieval?" | L1 checks retrieval only. Never sees the write path. |
| "Is the `/ingest` endpoint behind authentication?" | L3 tracks `user_id` flow, not auth middleware topology. |
| "Is `collection_name='faq'` a per-tenant scope or a shared scope?" | L1 sees scoping exists but can't infer intent from a string literal. |
| "Does the nightly re-indexing job preserve `user_id` metadata?" | L2 call graph doesn't connect background workers to API handlers. |
| "Can data written by user A be retrieved in user B's LLM context?" | Requires tracing across ingestion → storage → retrieval → context assembly. No single layer does this. |
| "Do all entry points that write to the vector store require authentication?" | Requires mapping entry points to auth decorators to write operations. |

### Root Cause

L0–L8 are **checkers** — they scan code and flag patterns. What's missing is a **builder** — something that constructs a model of what the application *is*, then checks that model for violations.

```
Today:     Source code  →  Pattern match  →  Findings
Proposed:  Source code  →  Build model    →  Query model  →  Findings
```

The difference is fundamental. Pattern matching asks "does this line have a filter?" Model querying asks "in this application, can user A's data reach user B's context?"

---

## 2. Levels of Understanding

Static analysis can go significantly further than L0–L8 without an LLM or runtime. But there's a hard ceiling. Being precise about the levels matters because it defines what AgentWall can realistically claim.

```
Level 0: Syntax checking     ← "is the kwarg there?"               (L1 today)
Level 1: Cross-file wiring   ← "is the kwarg applied somewhere     (L2 today)
                                 in the call chain?"
Level 2: Data flow tracking  ← "does the right value flow          (L3 today)
                                 into the kwarg?"
────────── current ceiling ──────────────────────────────────────────────────
Level 3: Component modeling  ← "what does this module DO?           (ASM target)
                                 what are its inputs, outputs,
                                 side effects, auth requirements?"
Level 4: Application model   ← "how do components compose?          (ASM target)
                                 where are trust boundaries?
                                 what's the data lifecycle?"
Level 5: Architectural       ← "does the architecture as a whole    (ASM target)
         verification           satisfy isolation properties?"
────────── static ceiling ──────────────────────────────────────────────────
Level 6: Runtime confirmed   ← "does it ACTUALLY leak at runtime?"  (L7 today)
Level 7: Behavioral          ← "can an attacker exploit this        (needs runtime)
                                 in practice?"
```

**The ASM targets Levels 3–5.** These are achievable with pure static analysis. No LLM. No runtime. The gap between the current ceiling and the static ceiling is where the real power lives.

### What Makes Levels 3–5 Different from L0–L8

L0–L8 operate on **code artifacts** — AST nodes, function calls, variable flows. Levels 3–5 operate on **application concepts** — entry points, data stores, auth boundaries, data lifecycles. The extraction layer must translate from code artifacts to application concepts, and the query layer must reason about relationships between concepts.

This is analogous to how a compiler translates source code to an intermediate representation (IR) before optimizing — you can't do meaningful optimization on raw source text, and you can't do meaningful security reasoning on raw AST nodes.

---

## 3. Architecture Overview

```
┌──────────────────────────────────────────────────────────┐
│                    TARGET CODEBASE                         │
└──────────────┬───────────────────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────────────────┐
│              EXTRACTION LAYER                              │
│                                                            │
│  L0–L8 (existing)          ASM Extractors (new)           │
│  ├─ AST per-file           ├─ EntryPointExtractor         │
│  ├─ Call graph              ├─ WriteOpExtractor            │
│  ├─ Taint tracking          ├─ StoreExtractor             │
│  └─ Config parsing          ├─ ReadOpExtractor            │
│                             ├─ SinkExtractor              │
│                             └─ AuthBoundaryExtractor      │
└──────────────┬───────────────────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────────────────┐
│              APPLICATION SECURITY MODEL (IR)               │
│                                                            │
│  A directed graph of typed nodes and edges:               │
│                                                            │
│  Nodes: EntryPoint, WriteOp, Store, ReadOp, Sink, Auth   │
│  Edges: flows_to, writes_to, reads_from, guarded_by,     │
│         scoped_by, assembles_into                         │
│                                                            │
│  Every node/edge carries:                                 │
│    - provenance (file:line:col)                           │
│    - confidence (Confirmed | Inferred | Unknown)          │
│    - metadata fields (schema, keys, values)               │
└──────────────┬───────────────────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────────────────┐
│              QUERY ENGINE                                   │
│                                                            │
│  Security properties expressed as graph queries:          │
│                                                            │
│  Q1: "Unauthenticated write path"                         │
│  Q2: "Write-read metadata key mismatch"                   │
│  Q3: "Cross-tenant reachable path"                        │
│  Q4: "Static shared collection"                           │
│  Q5: "Unsanitized context assembly"                       │
│                                                            │
│  Each query traverses the graph and returns:              │
│    - Violation paths (witnesses)                          │
│    - Proof strength (Confirmed | Possible | Unknown)      │
│    - Remediation pointers                                 │
└──────────────┬───────────────────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────────────────┐
│              FINDINGS (semantic-level)                      │
│                                                            │
│  Each finding includes a PATH WITNESS:                    │
│  EntryPoint → WriteOp → Store → ReadOp → Sink            │
│  with per-hop confidence and provenance                   │
└──────────────────────────────────────────────────────────┘
```

---

## 4. Intermediate Representation (IR)

The IR is a directed graph. Every element carries provenance (where in the source code it was extracted from), confidence level, and domain-specific attributes.

### 4.1 Confidence Model

Every node and edge in the graph has a confidence level. This is the single most important design decision — it determines whether the system produces trustworthy findings or noise.

```python
class Confidence(Enum):
    CONFIRMED = "confirmed"   # Statically proven. Value is known.
    INFERRED  = "inferred"    # Derived from structural patterns. High probability.
    UNKNOWN   = "unknown"     # Dynamic value, third-party code, or metaprogramming.
```

**Critical rule:** The query engine must reason in three-valued logic. `UNKNOWN` is not `True` and not `False` — it's a distinct state that propagates through queries. A finding with `UNKNOWN` nodes in its path is a `Possible` finding, not a `Confirmed` finding.

**Severity mapping by proof strength:**

| Proof Strength | When | Max Severity |
|---|---|---|
| **Confirmed** | All nodes/edges in violation path are `CONFIRMED` | CRITICAL |
| **Possible** | At least one node/edge is `INFERRED` | HIGH |
| **Uncertain** | At least one node/edge is `UNKNOWN` | MEDIUM (flagged for L7/L8 confirmation) |

This prevents severity inflation. CRITICAL means "we proved it." MEDIUM means "we can't tell — run `--dynamic` or `--llm-assist` to confirm."

### 4.2 Node Types

#### EntryPoint

An entry into the application that can trigger data flow.

```python
@dataclass
class EntryPoint:
    id: str
    kind: EntryPointKind          # HTTP_ROUTE, CLI_COMMAND, BACKGROUND_JOB,
                                  # EVENT_HANDLER, CRON, MCP_TOOL
    location: Location            # file:line:col
    auth: AuthState               # AUTHENTICATED, UNAUTHENTICATED, UNKNOWN
    auth_mechanism: str | None    # "Depends(get_current_user)", "jwt_required", etc.
    user_id_source: str | None    # "request.state.user.id", "g.user.id", etc.
    confidence: Confidence
```

**Extraction:** FastAPI `@app.get`/`@app.post` decorators with `Depends()` inspection. Flask `@app.route` with `@login_required`. Django `urlpatterns` with permission classes. Background workers via Celery `@task`, APScheduler, etc.

#### WriteOp

A call that writes data into a memory store.

```python
@dataclass
class WriteOp:
    id: str
    location: Location
    store_ref: str                # Which Store node this writes to
    method: str                   # "add_documents", "add_texts", "upsert", etc.
    metadata_keys: set[str]       # Keys attached at write time: {"user_id", "source"}
    metadata_values: dict[str, ValueState]  # {"user_id": Dynamic, "source": Static("web")}
    confidence: Confidence
```

**Extraction:** AST inspection of `vectorstore.add_documents()`, `collection.add()`, `add_texts()` calls. Extract the `metadata` or `metadatas` kwarg, parse dict literal keys. If the value is a variable reference, mark as `Dynamic`. If it's a string literal, mark as `Static(value)`.

#### Store

A memory backend (vector store, conversation memory, cache).

```python
@dataclass
class Store:
    id: str
    location: Location
    backend: StoreBackend         # CHROMA, PGVECTOR, PINECONE, FAISS, etc.
    collection_name: ValueState   # Static("faq") | Dynamic("f'user_{uid}'") | Unknown
    scope_strategy: ScopeStrategy # PER_TENANT_COLLECTION, SHARED_WITH_FILTER,
                                  # SHARED_NO_FILTER, UNKNOWN
    access_control: AccessControl # AUTH_REQUIRED, NO_AUTH, UNKNOWN
    config: dict                  # Parsed from constructor kwargs, .env, docker-compose
    confidence: Confidence
```

**Extraction:** Constructor calls (`Chroma(collection_name=...)`, `PGVector(connection_string=...)`). Config auditing (L4) feeds `access_control` and `config`. Collection name analysis determines `scope_strategy`.

#### ReadOp

A call that retrieves data from a memory store.

```python
@dataclass
class ReadOp:
    id: str
    location: Location
    store_ref: str                # Which Store node this reads from
    method: str                   # "similarity_search", "get_relevant_documents", etc.
    filter_keys: set[str]         # Keys used in filter: {"user_id"} or empty
    filter_values: dict[str, ValueState]  # {"user_id": Dynamic} or {"user_id": Static("admin")}
    has_filter: bool
    confidence: Confidence
```

**Extraction:** Same as L1 today but richer — extract not just "is there a filter?" but "what keys does the filter use and are the values dynamic (user-scoped) or static?"

#### Sink

Where retrieved data ends up — the final destination that determines impact.

```python
@dataclass
class Sink:
    id: str
    kind: SinkKind                # LLM_CONTEXT, API_RESPONSE, TOOL_INPUT,
                                  # FILE_WRITE, LOG, DATABASE
    location: Location
    sanitized: bool               # Is the data sanitized/delimited before injection?
    delimiter: str | None         # "---", XML tags, markdown, None
    confidence: Confidence
```

**Extraction:** Track where retrieved documents flow after `similarity_search()` returns. If they're concatenated into an LLM prompt via `format_docs()`, `"\n".join()`, or chain construction — that's an `LLM_CONTEXT` sink. Check for delimiter/tagging patterns.

#### AuthBoundary

An authentication/authorization enforcement point.

```python
@dataclass
class AuthBoundary:
    id: str
    location: Location
    mechanism: str                # "FastAPI Depends", "Django permission_classes",
                                  # "Flask login_required", "custom middleware"
    scope: str                    # What it protects: "router", "view", "endpoint"
    extracts_user_id: bool        # Does it put user_id into request context?
    user_id_attribute: str | None # "request.state.user.id", "g.user", etc.
    confidence: Confidence
```

**Extraction:** Decorator patterns (`@login_required`, `Depends(get_current_user)`), middleware registration, Django `permission_classes`. Parse the auth function body to determine if it extracts `user_id`.

### 4.3 Edge Types

```python
class EdgeKind(Enum):
    FLOWS_TO       = "flows_to"        # Data flows from source to target
    WRITES_TO      = "writes_to"       # WriteOp writes to Store
    READS_FROM     = "reads_from"      # ReadOp reads from Store
    GUARDED_BY     = "guarded_by"      # EntryPoint is protected by AuthBoundary
    ASSEMBLES_INTO = "assembles_into"  # ReadOp result feeds into Sink
    TRIGGERS       = "triggers"        # EntryPoint triggers WriteOp or ReadOp

@dataclass
class Edge:
    source: str           # Node ID
    target: str           # Node ID
    kind: EdgeKind
    confidence: Confidence
    provenance: Location  # Where in source code this relationship was inferred
```

### 4.4 The Graph

```python
@dataclass
class ApplicationSecurityModel:
    entry_points: dict[str, EntryPoint]
    write_ops: dict[str, WriteOp]
    stores: dict[str, Store]
    read_ops: dict[str, ReadOp]
    sinks: dict[str, Sink]
    auth_boundaries: dict[str, AuthBoundary]
    edges: list[Edge]

    # Graph traversal
    def paths(self, source_type: type, sink_type: type) -> list[Path]: ...
    def reachable(self, node_id: str, edge_kinds: set[EdgeKind]) -> set[str]: ...
    def nodes_without_edge(self, node_type: type, edge_kind: EdgeKind) -> list[str]: ...
    def unresolved(self) -> list[Node]: ...  # All nodes with confidence=UNKNOWN
```

### 4.5 Example: A Typical RAG Application

Consider this FastAPI + LangChain + Chroma application:

```python
# auth.py
async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = decode_jwt(token)
    return user

# ingest.py
@app.post("/upload")
async def upload_doc(file: UploadFile, user: User = Depends(get_current_user)):
    docs = PyPDFLoader(file).load()
    vectorstore.add_documents(docs, metadata={"source": file.filename})

# query.py
@app.post("/query")
async def query_docs(q: str, user: User = Depends(get_current_user)):
    results = vectorstore.similarity_search(q, filter={"user_id": user.id})
    context = "\n".join([doc.page_content for doc in results])
    return llm.invoke(f"Context: {context}\nQuestion: {q}")

# reindex.py (cron job)
def nightly_reindex():
    all_docs = load_all_from_disk()
    vectorstore.delete_collection()
    vectorstore.add_documents(all_docs)  # metadata lost!
```

**ASM graph for this application:**

```
EntryPoint("/upload", auth=AUTHENTICATED, user_id="user.id")
  ──triggers──► WriteOp(add_documents, metadata_keys={"source"})  ← MISSING user_id!
                  ──writes_to──► Store(chroma, collection="docs")

EntryPoint("/query", auth=AUTHENTICATED, user_id="user.id")
  ──triggers──► ReadOp(similarity_search, filter_keys={"user_id"})
                  ──reads_from──► Store(chroma, collection="docs")
                  ──assembles_into──► Sink(LLM_CONTEXT, sanitized=false)

EntryPoint("nightly_reindex", auth=UNAUTHENTICATED)  ← NO AUTH!
  ──triggers──► WriteOp(add_documents, metadata_keys={})  ← NO METADATA!
                  ──writes_to──► Store(chroma, collection="docs")
```

**What the query engine finds from this graph:**

1. **Write-read key mismatch (Q2):** `/upload` writes `{"source"}` but `/query` filters on `{"user_id"}`. The filter key doesn't exist at write time. L1 would pass this — the filter kwarg exists on the read side.

2. **Unauthenticated write path (Q1):** `nightly_reindex` writes to the same store without auth. An attacker who can trigger or modify the reindex job can poison the store.

3. **Metadata loss in lifecycle (Q2 variant):** `nightly_reindex` writes with no metadata at all. After reindex runs, every document loses its `user_id` even if `/upload` had attached it.

4. **Unsanitized context assembly (Q5):** Retrieved docs are joined with `\n` and injected directly into the LLM prompt with no delimiter or tagging. Indirect prompt injection via stored content.

**None of these are visible to L1–L3.** They require understanding the application's data lifecycle as a whole.

---

## 5. Extractors

Extractors are framework-specific modules that translate AST artifacts into ASM nodes. Each extractor is responsible for one node type and carries a version-aware adapter pattern.

### 5.1 Extractor Contract

```python
class Extractor(Protocol):
    """Base contract for all ASM extractors."""

    def extract(self, ast_forest: dict[Path, ast.Module],
                call_graph: CallGraph,
                config_findings: list[Finding]) -> list[Node]:
        """
        Given parsed ASTs for the entire project, the L2 call graph,
        and L4 config findings, produce ASM nodes.

        Returns nodes with confidence levels. Extractors MUST set
        confidence=UNKNOWN for anything they cannot statically resolve.
        """
        ...
```

### 5.2 Extractor Registry (MVP)

| Extractor | Produces | Input | Framework-Specific? |
|---|---|---|---|
| `FastAPIEntryPointExtractor` | `EntryPoint` nodes | Route decorators, Depends() | Yes (FastAPI) |
| `FlaskEntryPointExtractor` | `EntryPoint` nodes | @app.route, @login_required | Yes (Flask) |
| `CeleryEntryPointExtractor` | `EntryPoint` nodes | @task, @periodic_task | Yes (Celery) |
| `LangChainWriteExtractor` | `WriteOp` nodes | add_documents, add_texts calls | Yes (LangChain) |
| `LangChainReadExtractor` | `ReadOp` nodes | similarity_search, retriever calls | Yes (LangChain) |
| `VectorStoreExtractor` | `Store` nodes | Chroma(), PGVector(), etc. constructors | Per-backend |
| `ContextSinkExtractor` | `Sink` nodes | Chain construction, prompt formatting | Yes (LangChain) |
| `AuthBoundaryExtractor` | `AuthBoundary` nodes | Depends(), middleware, decorators | Per-framework |

### 5.3 Edge Inference

Edges are inferred by a separate `EdgeLinker` that connects extracted nodes:

```python
class EdgeLinker:
    def link(self, nodes: list[Node], call_graph: CallGraph) -> list[Edge]:
        """
        Infer edges between nodes using:
        1. Variable aliasing: if `vs = Chroma(...)` and later `vs.add_documents(...)`,
           link the WriteOp to the Store.
        2. Call graph: if function A calls function B which calls similarity_search,
           link the EntryPoint to the ReadOp.
        3. Decorator scoping: if an endpoint has Depends(get_current_user),
           add a guarded_by edge to the AuthBoundary.
        4. Return value tracking: if similarity_search result flows into
           string formatting / chain, link ReadOp to Sink.
        """
```

**The most error-prone step.** Incorrect linking produces false findings. Mitigation: every edge carries a confidence level. If the linker can't statically prove the connection (e.g., variable aliasing through dynamic dispatch), the edge is `INFERRED` or `UNKNOWN`.

---

## 6. Query Engine

Security properties are expressed as graph queries. Each query traverses the ASM graph and returns violation paths (witnesses) with proof strength.

### 6.1 Query Contract

```python
@dataclass
class Violation:
    query_id: str
    rule_id: str                  # Maps to existing AW-MEM-*/AW-TOOL-* rules
    path: list[Node]              # The full witness path through the graph
    proof_strength: ProofStrength # CONFIRMED, POSSIBLE, UNCERTAIN
    description: str
    remediation: str
    provenance: list[Location]    # All source locations in the path

class ProofStrength(Enum):
    CONFIRMED = "confirmed"   # All nodes/edges in path are Confidence.CONFIRMED
    POSSIBLE  = "possible"    # At least one INFERRED node/edge
    UNCERTAIN = "uncertain"   # At least one UNKNOWN node/edge
```

**Proof strength is computed from the weakest link in the path.** If every node and edge is `CONFIRMED`, the violation is `CONFIRMED`. If any element is `UNKNOWN`, the violation is `UNCERTAIN`.

### 6.2 MVP Queries

#### Q1: Unauthenticated Write Path

**Property:** Every path from an `EntryPoint` to a `WriteOp` must pass through an `AuthBoundary`.

```
MATCH (ep:EntryPoint)-[:TRIGGERS*]->(w:WriteOp)
WHERE NOT EXISTS (ep)-[:GUARDED_BY]->(:AuthBoundary)
RETURN ep, w AS violation_path
```

**What it catches:**
- Background workers that write to the vector store without auth
- Public API endpoints that accept document uploads without authentication
- Cron jobs that re-ingest data and can be triggered externally

**Maps to:** AW-MEM-003 (no access control), new rule AW-ASM-001

---

#### Q2: Write-Read Metadata Key Mismatch

**Property:** For every `ReadOp` with a filter key K, there must exist a `WriteOp` targeting the same `Store` that includes K in its metadata keys.

```
MATCH (w:WriteOp)-[:WRITES_TO]->(s:Store)<-[:READS_FROM]-(r:ReadOp)
WHERE r.filter_keys IS NOT EMPTY
  AND NOT r.filter_keys ⊆ w.metadata_keys
RETURN w, s, r AS violation_path
```

**What it catches:**
- Retrieval filters on `user_id` but ingestion never attaches `user_id`
- Re-indexing jobs that strip metadata
- Partial metadata — some write paths attach `user_id`, others don't

**Maps to:** AW-MEM-002 (weak isolation), new rule AW-ASM-002

---

#### Q3: Cross-Tenant Reachable Path

**Property:** There must be no path where data written by entry point A (with user scope X) can be retrieved by entry point B (with user scope Y ≠ X) without a filter that enforces scope.

```
MATCH (ep1:EntryPoint)-[:TRIGGERS*]->(w:WriteOp)-[:WRITES_TO]->(s:Store)
      <-[:READS_FROM]-(r:ReadOp)<-[:TRIGGERS*]-(ep2:EntryPoint)
WHERE s.scope_strategy = SHARED_NO_FILTER
   OR (s.scope_strategy = SHARED_WITH_FILTER AND r.has_filter = false)
RETURN ep1, w, s, r, ep2 AS violation_path
```

**What it catches:**
- The core cross-tenant leakage scenario via unfiltered shared collection
- "Filter exists on some paths but not all" when multiple entry points read from the same store
- Static collection names used as false isolation (shared `"faq"` collection)

**Maps to:** AW-MEM-001 (no tenant isolation) — this is the semantic-level version

---

#### Q4: Static Shared Collection

**Property:** If a `Store` has `collection_name` set to a static literal value AND is written to by multiple `EntryPoint` nodes with different user scopes, the collection is shared and requires per-query filtering.

```
MATCH (ep:EntryPoint)-[:TRIGGERS*]->(w:WriteOp)-[:WRITES_TO]->(s:Store)
WHERE s.collection_name.state = STATIC
GROUP BY s
HAVING count(DISTINCT ep.user_id_source) > 1  -- multiple user scopes write here
   AND NOT ALL (r:ReadOp WHERE (r)-[:READS_FROM]->(s) AND r.has_filter = true)
RETURN s AS violation_path
```

**What it catches:**
- `collection_name="faq"` shared across all tenants with no per-query filter
- `collection_name=kb_name` where `kb_name` is a knowledge base ID, not a user ID
- Named collections that look scoped but are actually shared

**Maps to:** AW-MEM-001 variant, new rule AW-ASM-003

---

#### Q5: Unsanitized Context Assembly

**Property:** Every path from a `ReadOp` to a `Sink` of kind `LLM_CONTEXT` must pass through sanitization (delimiter tagging, content wrapping, or explicit filtering).

```
MATCH (r:ReadOp)-[:ASSEMBLES_INTO]->(sink:Sink)
WHERE sink.kind = LLM_CONTEXT
  AND sink.sanitized = false
RETURN r, sink AS violation_path
```

**What it catches:**
- Retrieved documents concatenated directly into the prompt without delimiters
- No source attribution tags that the LLM can use to distinguish retrieval from instruction
- Missing content wrapping that enables indirect prompt injection via stored documents

**Maps to:** AW-MEM-005 (no sanitization), AW-INJ-001

---

### 6.3 Query Execution and Three-Valued Logic

The query engine operates in three-valued logic. When traversing a path, it tracks the minimum confidence across all nodes and edges:

```python
def compute_proof_strength(path: list[Node], edges: list[Edge]) -> ProofStrength:
    min_confidence = min(
        [n.confidence for n in path] + [e.confidence for e in edges]
    )
    match min_confidence:
        case Confidence.CONFIRMED: return ProofStrength.CONFIRMED
        case Confidence.INFERRED:  return ProofStrength.POSSIBLE
        case Confidence.UNKNOWN:   return ProofStrength.UNCERTAIN
```

**Uncertain findings are never CRITICAL.** They're flagged as "needs confirmation" and surfaced as candidates for L7 (runtime) or L8 (LLM) confirmation. This prevents the system from producing high-confidence wrong findings.

---

## 7. Integration with L0–L8

The ASM does not replace L0–L8. It reframes them as **feature providers** to a semantic layer.

```
┌─────────────────────────────────────────────────────┐
│                 EXISTING PIPELINE                     │
│                                                       │
│  L0 (framework detection)  ──► framework type         │
│  L1 (per-file AST)         ──► raw call sites         │
│  L2 (call graph)           ──► cross-file edges       │
│  L3 (taint tracking)       ──► user_id flow paths     │
│  L4 (config audit)         ──► infra misconfigs       │
│  L5 (semgrep)              ──► pattern matches        │
│                                                       │
│  These become INPUTS to ASM, not final outputs.       │
└──────────────┬──────────────────────────────────────┘
               │ raw extraction artifacts
               ▼
┌─────────────────────────────────────────────────────┐
│                 ASM LAYER (NEW)                       │
│                                                       │
│  Extractors  ──► ASM Graph  ──► Query Engine          │
│                                                       │
│  Produces semantic-level findings with path witnesses │
└──────────────┬──────────────────────────────────────┘
               │ semantic findings + uncertain paths
               ▼
┌─────────────────────────────────────────────────────┐
│                 CONFIRMATION LAYERS                    │
│                                                       │
│  L6 (symbolic)   ──► confirm/deny branch conditions   │
│  L7 (runtime)    ──► confirm/deny uncertain paths     │
│  L8 (LLM)        ──► resolve ambiguous semantics      │
│                                                       │
│  These become CONFIRMATION for ASM uncertainties.     │
└──────────────────────────────────────────────────────┘
```

**Backwards compatibility:** Existing L1–L5 findings continue to work as-is. ASM findings are a new category (`AW-ASM-*`) that coexist with pattern-based findings. Users who run `--fast` (L0–L2) get the old behavior. Users who run the full pipeline get ASM findings as well.

---

## 8. Finding Format

ASM findings use a **path witness** format — every finding shows the complete chain from entry point to violation, with per-hop confidence and provenance.

```json
{
  "rule_id": "AW-ASM-002",
  "title": "Write-read metadata key mismatch",
  "proof_strength": "CONFIRMED",
  "severity": "CRITICAL",
  "description": "The /upload endpoint writes documents with metadata keys {\"source\"} but the /query endpoint filters on {\"user_id\"}. The filter key 'user_id' is never set at ingestion time, so the filter will match zero documents — or all documents if the store ignores unknown filter keys.",
  "path_witness": [
    {
      "node": "EntryPoint(/upload)",
      "location": "ingest.py:12",
      "confidence": "CONFIRMED",
      "detail": "POST /upload, auth=Depends(get_current_user)"
    },
    {
      "node": "WriteOp(add_documents)",
      "location": "ingest.py:15",
      "confidence": "CONFIRMED",
      "detail": "metadata_keys={\"source\"}, MISSING: user_id"
    },
    {
      "node": "Store(chroma, collection='docs')",
      "location": "config.py:8",
      "confidence": "CONFIRMED",
      "detail": "Shared collection, scope_strategy=SHARED_WITH_FILTER"
    },
    {
      "node": "ReadOp(similarity_search)",
      "location": "query.py:20",
      "confidence": "CONFIRMED",
      "detail": "filter_keys={\"user_id\"}"
    }
  ],
  "remediation": "Add user_id to document metadata at ingestion: vectorstore.add_documents(docs, metadata={\"user_id\": user.id, \"source\": file.filename})"
}
```

---

## 9. Hard Boundaries — What ASM Cannot Do

Being honest about limits is critical for trust.

| Limitation | Why | Mitigation |
|---|---|---|
| **Dynamically computed values** | `collection_name = os.getenv("COLL")` — can't resolve at static time | Mark as `UNKNOWN`. Flag for L7/L8 confirmation. |
| **Third-party library internals** | `some_lib.get_retriever()` — no source available | Mark edge as `UNKNOWN`. Note the library boundary. |
| **Metaprogramming** | `setattr(vs, method_name, func)` — dynamic dispatch | Mark as `UNKNOWN`. Recommend `--dynamic` mode. |
| **Runtime-only behavior** | Does the Chroma server actually enforce auth? | Out of scope for static analysis. L7 live probing confirms. |
| **Intent** | Is the missing filter a bug or a deliberate single-tenant design? | Provide `agentwall.yaml` override: `deployment: single-tenant` suppresses multi-tenancy findings. |
| **Incorrect entity linking** | Mapping retrieval to the wrong ingestion path | Confidence propagation limits blast radius. Edge linker flags low-confidence links. |

---

## 10. Performance Considerations

| Operation | Target | Scaling Factor |
|---|---|---|
| Full AST extraction (reuses L0–L1) | < 5s for 50K LOC | Number of files |
| ASM node extraction | < 3s for 50K LOC | Number of vector store / auth / route call sites |
| Edge linking | < 2s for 50K LOC | Number of nodes × call graph edges |
| Query execution (5 queries) | < 1s | Number of paths in graph |
| **Total ASM overhead** | **< 10s on top of L0–L5** | |

**Incremental caching:** The ASM graph is deterministic given the same source code. Cache the graph keyed by file content hashes. On subsequent scans, only re-extract changed files and re-link affected edges.

---

## 11. MVP Scope

**One framework slice. Five node types. Five queries. Ship and validate.**

| Dimension | MVP Scope |
|---|---|
| Frameworks | FastAPI + LangChain |
| Vector stores | Chroma, FAISS |
| Node types | EntryPoint, WriteOp, Store, ReadOp, Sink (+ AuthBoundary) |
| Queries | Q1–Q5 (unauthenticated write, key mismatch, cross-tenant, shared collection, unsanitized context) |
| Output | Path witness JSON integrated into existing `--format agent-json` |
| CLI | `agentwall scan . --asm` enables ASM layer |

### Validation Plan

Test against known TP/FP corpora:

| Corpus | Expected | Use |
|---|---|---|
| `fixtures/langchain_unsafe` | ≥ 2 new ASM findings not caught by L1–L3 | True positive validation |
| `fixtures/langchain_safe` | 0 ASM findings | False positive test |
| Langchain-Chatchat (37K stars) | Confirm write-read mismatch on kb_name pattern | Real-world validation |
| Langflow (48K stars) | Confirm cross-tenant paths in shared collections | Real-world validation |
| New fixture: `fixtures/asm_lifecycle` | Purpose-built for lifecycle and auth boundary tests | Regression suite |

**Success criteria:** ≥ 3 true positive findings across real-world repos that L1–L3 cannot produce. Zero false positives on safe fixtures.

---

## 12. Implementation Sequence

| Step | What | Effort | Depends On |
|---|---|---|---|
| 1 | Define IR data model (Python dataclasses) | Low | Nothing |
| 2 | FastAPI EntryPoint extractor | Medium | Step 1 |
| 3 | LangChain Write/Read extractors | Medium | Step 1 |
| 4 | Chroma/FAISS Store extractor | Low | Step 1 |
| 5 | Context Sink extractor | Medium | Step 1 |
| 6 | Auth boundary extractor | Medium | Step 1 |
| 7 | Edge linker (variable aliasing + call graph) | High | Steps 2–6, L2 call graph |
| 8 | Query engine (Q1–Q5) | Medium | Step 7 |
| 9 | Path witness formatter | Low | Step 8 |
| 10 | Integration with `--format agent-json` | Low | Step 9 |
| 11 | Test fixtures + validation suite | Medium | Steps 8–10 |

**Estimated total: 2–3 focused sprints for a solo engineer.**

---

## 13. Future Extensions (Post-MVP)

| Extension | When | What It Enables |
|---|---|---|
| Multi-framework extractors (CrewAI, AutoGen) | v1.0 | Agent topology queries, delegation chain analysis |
| Dependency graph integration | v1.1 | Supply chain queries — "does this PyPI package touch my vector store?" |
| Cross-agent memory scope analysis | v1.2 | Multi-agent trust boundary violations |
| Temporal lifecycle queries | v1.4 | "Does the nightly job preserve metadata?" — requires modeling job schedules |
| Graph visualization export | v1.3 | Mermaid/DOT diagrams of the ASM for architecture review |
| Diff-aware incremental queries | v2.0 | "What changed in the ASM between this PR and main?" |

---

## 14. Open Questions

| # | Question | Impact | Notes |
|---|---|---|---|
| 1 | Should the ASM graph be persisted to disk for cross-run analysis? | Enables drift detection (v2.0) but adds complexity. | Lean toward in-memory for MVP, disk persistence for v2.0. |
| 2 | How to handle Django ORM-style implicit queries? | Django retrievers may not use explicit `similarity_search` calls. | Defer Django until post-MVP. FastAPI + LangChain first. |
| 3 | Should ASM findings replace or supplement L1–L3 findings? | User confusion if both fire on the same code site. | Supplement. ASM findings are `AW-ASM-*`, distinct from `AW-MEM-*`. Dedup in reporter. |
| 4 | How to handle monorepos with multiple apps sharing one vector store? | Multiple ASM graphs? One merged graph? | One graph per scan target. User scopes via `agentwall.yaml`. |
| 5 | Should the query language be user-extensible? | Power users could write custom security properties. | Post-MVP. Start with hardcoded Q1–Q5. |

---

*End of document.*
