# AgentWall — Architecture V4

## From Pattern Matching to Application-Level Security Analysis

**Version:** 4.0
**Date:** 2026-03-18
**Author:** SoH Engineering
**Status:** Proposal
**Previous:** Architecture V3 (implicit in PRD v3, Section 14–20)

---

## 1. Where We Are (V3 Architecture)

The current system is a **layered checker pipeline**. Each layer inspects code patterns at increasing depth and emits findings independently.

```
Target Path
    │
    ▼
L0  detector.auto_detect_framework()     → framework: str
    │
    ▼
L1  LangChainAdapter.parse()             → AgentSpec (tools[], memory_configs[])
    MemoryAnalyzer.analyze(spec)          → Finding[] (AW-MEM-001–005)
    ToolAnalyzer.analyze(spec)            → Finding[] (AW-TOOL-001–005)
    │
    ▼
L2  CallGraphAnalyzer.analyze(spec, l1)  → Finding[] (refined — downgrades if filter found upstream)
    │
    ▼
L3  TaintAnalyzer.analyze(spec)          → Finding[] (new — tracks user_id flow to filter sinks)
    │
    ▼
L4  ConfigAuditor.analyze(target)        → Finding[] (new — infra misconfigs)
    │
    ▼
L5  SemgrepAnalyzer.analyze(target)      → Finding[] (new — declarative patterns)
    │
    ▼
L6  SymbolicAnalyzer.analyze(spec)       → Finding[] (new — branch-conditional gaps)
    │
    ▼
L7  patcher.run_with_instrumentation()   → Finding[] (opt-in — runtime confirmed)
    │
    ▼
L8  ConfidenceScorer.apply_scores()      → Finding[] (adjusted confidence)
    │
    ▼
    _dedup → _apply_file_context → _sort → ScanResult
```

### What This Architecture Does Well

- **L1 (AST per-file)** catches the obvious case: `similarity_search()` with no `filter=` kwarg. Reliable on 20 real-world repos (57 CRITICAL findings).
- **L2 (call graph)** reduces false positives: if a wrapper function in another file applies the filter, L2 downgrades the finding from CRITICAL to LOW.
- **L3 (taint)** proves data flow: confirms that `user_id` from `request.user` actually reaches the filter sink, or flags static filters like `filter={"source": "web"}`.
- **L4 (config)** covers infrastructure: `allow_reset=True`, exposed ports, empty passwords, missing TLS. 45 hardcoded key hits across 8 projects.
- **L6 (symbolic)** catches branch gaps: filter present in the `if` branch but missing in the `else` fallback.
- **L8 (confidence)** reduces noise: regex heuristics resolve 60%+ of ambiguous variable names without LLM calls.

### Where This Architecture Hits Its Ceiling

Every layer asks questions about **individual code sites**. No layer asks questions about **the application**.

| Question We Can't Answer | Why |
|---|---|
| "Does the ingestion metadata schema match the retrieval filter schema?" | L1 checks retrieval. Never connects to the write path in another module. |
| "Is the `/ingest` endpoint behind authentication?" | L3 tracks `user_id` within a request. Doesn't map which entry points have auth middleware. |
| "Is `collection_name='faq'` per-tenant or shared?" | L1 sees scoping but can't judge string semantics across multiple callers. |
| "Does the nightly re-indexer preserve metadata?" | L2 call graph doesn't connect cron jobs to API handlers — different entry points. |
| "Can user A's data reach user B's LLM context through any path?" | Requires tracing across ingestion → storage → retrieval → context assembly. No layer does this. |

**Root cause:** The current `AgentSpec` is flat — `tools[]` and `memory_configs[]` with boolean flags. It captures **what exists** but not **how components relate**. There's no model of the application's data lifecycle, trust boundaries, or component topology.

---

## 2. The Core Insight

The upgrade is not a new system. It's a richer intermediate representation.

```
V3:  AST  →  flat AgentSpec (booleans)  →  pattern checkers  →  findings
V4:  AST  →  rich AgentSpec (graph)     →  graph queries     →  findings
```

Same pipeline. Same rules. Same layers. But the data model that flows through the pipeline carries enough structural information to answer application-level questions.

The key change: **`AgentSpec` evolves from a flat list of flags into a graph of typed nodes and edges.** The existing analyzers become extractors that populate the graph. The existing rules become queries against the graph. No new dimensions — just longer reach on the same dimension.

---

## 3. V4 Architecture

### 3.1 Data Model Changes

**Current `AgentSpec` (V3):**

```python
@dataclass
class AgentSpec:
    framework: str
    source_files: list[Path]
    tools: list[ToolSpec]           # flat list of tool registrations
    memory_configs: list[MemoryConfig]  # flat list of vector store configs
    metadata: dict
```

**Proposed `AgentSpec` (V4):**

```python
@dataclass
class AgentSpec:
    framework: str
    source_files: list[Path]
    tools: list[ToolSpec]               # unchanged — tool rules stay L1
    memory_configs: list[MemoryConfig]  # unchanged — backward compat
    metadata: dict

    # NEW: Application Security Model (ASM)
    asm: ApplicationModel | None        # None when --fast or extraction fails
```

ASM is **additive**. Stored in `AgentSpec.asm`. Existing analyzers that consume `spec.tools` and `spec.memory_configs` continue to work unchanged. ASM-aware analyzers additionally consume `spec.asm`.

### 3.2 Application Model (the new IR)

```python
class Confidence(Enum):
    CONFIRMED = "confirmed"   # Statically proven
    INFERRED  = "inferred"    # Structural pattern, high probability
    UNKNOWN   = "unknown"     # Dynamic value, can't resolve

@dataclass
class Provenance:
    file: Path
    line: int
    col: int
    symbol: str               # "ChromaKBService.do_search", "upload_doc"

@dataclass
class EntryPoint:
    id: str
    kind: str                 # "http_route", "background_job", "cli_command", "cron"
    provenance: Provenance
    auth: str                 # "authenticated", "unauthenticated", "unknown"
    auth_mechanism: str | None
    user_id_source: str | None
    confidence: Confidence

@dataclass
class WriteOp:
    id: str
    provenance: Provenance
    store_id: str             # links to Store
    method: str               # "add_documents", "add_texts"
    metadata_keys: set[str]   # {"user_id", "source"} — keys written
    confidence: Confidence

@dataclass
class ReadOp:
    id: str
    provenance: Provenance
    store_id: str             # links to Store
    method: str               # "similarity_search", "as_retriever"
    filter_keys: set[str]     # {"user_id"} — keys filtered on
    has_filter: bool
    confidence: Confidence

@dataclass
class Store:
    id: str
    provenance: Provenance
    backend: str              # "chroma", "pgvector", "faiss"
    collection_name: str | None
    collection_name_is_static: bool  # True if string literal, False if dynamic
    confidence: Confidence

@dataclass
class ContextSink:
    id: str
    provenance: Provenance
    kind: str                 # "llm_context", "api_response", "tool_input"
    sanitized: bool
    confidence: Confidence

@dataclass
class Edge:
    source_id: str
    target_id: str
    kind: str                 # "triggers", "writes_to", "reads_from",
                              # "guarded_by", "assembles_into"
    confidence: Confidence
    provenance: Provenance

@dataclass
class ApplicationModel:
    entry_points: list[EntryPoint]
    write_ops: list[WriteOp]
    stores: list[Store]
    read_ops: list[ReadOp]
    sinks: list[ContextSink]
    edges: list[Edge]
    unresolved: list[Provenance]  # things we couldn't resolve — transparency
```

### 3.3 Pipeline Changes

```
Target Path
    │
    ▼
L0  detector.auto_detect_framework()
    │
    ▼
L1  LangChainAdapter.parse()                → AgentSpec
    │                                            ├── tools[], memory_configs[]  (V3, unchanged)
    │                                            └── asm: ApplicationModel      (V4, NEW)
    │
    ├── MemoryAnalyzer.analyze(spec)         → Finding[] (unchanged)
    ├── ToolAnalyzer.analyze(spec)           → Finding[] (unchanged)
    │
    ▼
L2  CallGraphAnalyzer.analyze(spec, l1)     → Finding[] (unchanged)
    │
    ▼
L3  TaintAnalyzer.analyze(spec)             → Finding[] (unchanged)
    │
    ▼
L4  ConfigAuditor.analyze(target)           → Finding[] (unchanged)
    │
    ▼
L5  SemgrepAnalyzer.analyze(target)         → Finding[] (unchanged)
    │
    ▼
L6  SymbolicAnalyzer.analyze(spec)          → Finding[] (unchanged)
    │
    ▼
ASM ASMAnalyzer.analyze(spec.asm)           → Finding[] (NEW — graph queries)
    │
    ▼
L7  patcher.run_with_instrumentation()      → Finding[] (opt-in, unchanged)
    │
    ▼
L8  ConfidenceScorer.apply_scores()         → Finding[] (unchanged)
    │
    ▼
    _dedup → _apply_file_context → _sort → ScanResult
```

**What changes:**
1. `LangChainAdapter.parse()` produces a richer `AgentSpec` — existing fields unchanged, new `asm` field added.
2. New `ASMAnalyzer` runs graph queries after L6, before L7/L8.
3. `scanner.py` calls `ASMAnalyzer.analyze(spec.asm)` if `spec.asm` is not None.
4. ASM findings use existing rule IDs (AW-MEM-001, AW-MEM-002, AW-MEM-003) with enhanced evidence.

**What doesn't change:**
- All existing analyzers (memory, tools, callgraph, taint, config, semgrep, symbolic, confidence).
- All existing reporters (terminal, json, sarif, agent-json, patch).
- All existing CLI flags (--fast, --layers, --dynamic, --llm-assist).
- All existing rules (AW-MEM-001–005, AW-TOOL-001–005).
- All existing tests.

---

## 4. ASM Extraction — How the Graph Gets Built

The extraction happens inside `LangChainAdapter.parse()`. The existing `_FileVisitor` already walks every AST node and collects vector store calls, tool registrations, etc. We extend it to also emit ASM nodes.

### 4.1 What the Existing Adapter Already Extracts (V3)

The `_FileVisitor` in `langchain.py` already detects:

| Pattern | What it extracts today | What ASM needs additionally |
|---|---|---|
| `Chroma(collection_name=...)` | `MemoryConfig(backend="chroma")` | `Store` node with `collection_name`, `collection_name_is_static` |
| `vs.add_documents(docs, metadata={...})` | `has_metadata_on_write = True` | `WriteOp` node with `metadata_keys` extracted from dict literal |
| `vs.similarity_search(q, filter={...})` | `has_metadata_filter_on_retrieval = True` | `ReadOp` node with `filter_keys` extracted from dict literal |
| `@app.post("/upload")` | Not extracted | `EntryPoint` node with route, method |
| `Depends(get_current_user)` | Not extracted | `EntryPoint.auth = "authenticated"` |
| `"\n".join(docs)` into prompt | `sanitizes_retrieved_content = False` | `ContextSink` node with `sanitized = False` |

**Key insight:** ~60% of what ASM needs is already being detected by the adapter. The adapter currently collapses rich structural information into boolean flags (`has_metadata_filter_on_retrieval: bool`). V4 preserves the original structure.

### 4.2 New Extraction Steps

Added to `LangChainAdapter.parse()` after the existing `_FileVisitor` pass:

**Step 1: Entry Point Extraction**

Detect FastAPI/Flask route decorators and auth dependencies:

```python
# FastAPI
@app.post("/upload")
async def upload(file: UploadFile, user: User = Depends(get_current_user)):
    → EntryPoint(kind="http_route", auth="authenticated", user_id_source="user")

# Background worker
@celery.task
def nightly_reindex():
    → EntryPoint(kind="background_job", auth="unauthenticated")
```

Pattern matching via AST decorator inspection. Confidence: `CONFIRMED` for explicit decorators, `INFERRED` for functions called from routes without direct decorators.

**Step 2: Write/Read Op Enrichment**

The existing visitor already flags `add_documents` and `similarity_search`. V4 additionally extracts the metadata dict keys:

```python
# Existing: has_metadata_on_write = True
# V4 adds:  metadata_keys = {"source", "filename"}
vs.add_documents(docs, metadata={"source": f.name, "filename": f.filename})

# Existing: has_metadata_filter_on_retrieval = True
# V4 adds:  filter_keys = {"user_id"}
vs.similarity_search(q, filter={"user_id": user.id})
```

Extraction: `ast.Dict` key inspection on the `metadata=` and `filter=` kwargs that the adapter already parses.

**Step 3: Store Enrichment**

The existing visitor already detects `Chroma(collection_name=...)`. V4 additionally classifies the collection name:

```python
# Static literal → collection_name_is_static = True
Chroma(collection_name="faq")

# f-string or variable → collection_name_is_static = False
Chroma(collection_name=f"user_{uid}")
```

**Step 4: Context Sink Extraction**

New. Track where retrieval results flow:

```python
# Pattern: results from similarity_search → string join → prompt template
docs = vs.similarity_search(q)
context = "\n".join([d.page_content for d in docs])
response = llm.invoke(f"Context: {context}\nQuestion: {q}")
→ ContextSink(kind="llm_context", sanitized=False)
```

This requires tracking the return value of `similarity_search` through assignments — using the same variable tracking the adapter already does for `vectorstore` aliasing.

**Step 5: Edge Linking**

After all nodes are extracted, link them:

```python
class EdgeLinker:
    def link(self, nodes, call_graph) -> list[Edge]:
        # 1. Variable aliasing: vs = Chroma(...) → vs.add_documents(...)
        #    Links WriteOp/ReadOp to Store via variable name matching
        # 2. Call graph edges: route handler → helper → vs.similarity_search
        #    Links EntryPoint to WriteOp/ReadOp via L2 call graph
        # 3. Decorator scoping: Depends(get_current_user)
        #    Links EntryPoint to auth with "guarded_by" edge
        # 4. Return value flow: similarity_search result → join → llm.invoke
        #    Links ReadOp to ContextSink with "assembles_into" edge
```

**Risk:** Edge linking is the most error-prone step. Mitigation: every edge carries confidence. Variable aliasing within a function → `CONFIRMED`. Cross-function linking via call graph → `INFERRED`. Unresolvable (dynamic dispatch, third-party) → `UNKNOWN`.

### 4.3 Extraction Cost

| Step | What's New | Estimated Overhead |
|---|---|---|
| Entry point extraction | Decorator inspection (one pass per file) | ~1s for 50K LOC |
| Write/Read enrichment | Dict key extraction (extends existing visitor) | ~0.5s (already in hot path) |
| Store enrichment | Collection name classification | Negligible (extends constructor parsing) |
| Context sink extraction | Return value tracking | ~1s for 50K LOC |
| Edge linking | Variable aliasing + call graph integration | ~2s for 50K LOC |
| **Total ASM extraction** | | **< 5s on top of L1 for 50K LOC** |

---

## 5. ASM Queries — The New Analyzer

```python
# analyzers/asm.py — new file
class ASMAnalyzer:
    def analyze(self, model: ApplicationModel) -> list[Finding]:
        findings = []
        findings.extend(self._q1_unauthenticated_write(model))
        findings.extend(self._q2_write_read_key_mismatch(model))
        findings.extend(self._q3_static_shared_collection(model))
        findings.extend(self._q4_cross_tenant_reachable(model))
        findings.extend(self._q5_unsanitized_context(model))
        return findings
```

### Q1: Unauthenticated Write Path

**Rule:** AW-MEM-003 (enhanced)

**Logic:** For every `WriteOp`, trace back through edges to find the `EntryPoint`. If that entry point has `auth = "unauthenticated"`, emit finding.

```python
def _q1_unauthenticated_write(self, model):
    for write in model.write_ops:
        entry = self._find_entry_point(model, write.id)
        if entry and entry.auth == "unauthenticated":
            yield Finding(
                rule_id="AW-MEM-003",
                title="Unauthenticated entry point writes to vector store",
                severity=Severity.HIGH,
                layer="ASM",
                evidence_path=[entry, write, self._find_store(model, write.store_id)],
                proof_strength=self._proof_strength([entry, write]),
            )
```

**What it catches that L1–L3 can't:** Background workers, cron jobs, and public endpoints that write to the same store as authenticated endpoints. L4 checks config-level auth. This checks code-level auth topology.

### Q2: Write-Read Metadata Key Mismatch

**Rule:** AW-MEM-002 (enhanced)

**Logic:** For every `Store`, collect all `WriteOp.metadata_keys` and all `ReadOp.filter_keys`. If any filter key is not present in any write op's metadata keys, the filter is checking a field that was never written.

```python
def _q2_write_read_key_mismatch(self, model):
    for store in model.stores:
        write_keys = set()
        for w in model.write_ops:
            if w.store_id == store.id:
                write_keys |= w.metadata_keys
        for r in model.read_ops:
            if r.store_id == store.id and r.filter_keys:
                missing = r.filter_keys - write_keys
                if missing:
                    yield Finding(
                        rule_id="AW-MEM-002",
                        title=f"Filter key(s) {missing} never written at ingestion",
                        severity=Severity.HIGH,
                        layer="ASM",
                        evidence_path=[write_ops_for_store, store, r],
                        proof_strength=...,
                    )
```

**What it catches that L1–L3 can't:** L1 checks "is there a filter kwarg?" and passes. But the filter checks `user_id` while ingestion only writes `source`. The filter is useless. Only comparing write and read across the full codebase reveals this.

### Q3: Static Shared Collection

**Rule:** AW-MEM-001 (enhanced)

**Logic:** If a `Store` has a static `collection_name` AND is written to by multiple `EntryPoint` nodes AND any `ReadOp` on that store has no filter — the collection is shared and unfiltered.

```python
def _q3_static_shared_collection(self, model):
    for store in model.stores:
        if not store.collection_name_is_static:
            continue
        writers = self._entry_points_that_write_to(model, store.id)
        if len(writers) <= 1:
            continue  # single writer, possibly single-tenant
        unfiltered_reads = [r for r in model.read_ops
                           if r.store_id == store.id and not r.has_filter]
        if unfiltered_reads:
            yield Finding(
                rule_id="AW-MEM-001",
                title=f"Static collection '{store.collection_name}' shared across {len(writers)} entry points without filter",
                severity=Severity.CRITICAL,
                layer="ASM",
                evidence_path=[writers, store, unfiltered_reads],
                proof_strength=...,
            )
```

**What it catches that L1–L3 can't:** `collection_name="faq"` — L1 sees the collection scoping and might consider it isolation. ASM sees that 3 different authenticated endpoints write to the same static collection and 2 read without a filter.

### Q4: Cross-Tenant Reachable Path

**Rule:** AW-MEM-001 (enhanced)

**Logic:** Full path trace — entry point A writes to store S without user metadata, entry point B reads from store S without filter, result flows to an LLM context sink. This is the complete cross-tenant leakage proof.

```python
def _q4_cross_tenant_reachable(self, model):
    for store in model.stores:
        writes = [w for w in model.write_ops if w.store_id == store.id]
        reads = [r for r in model.read_ops if r.store_id == store.id]
        for w in writes:
            if "user_id" not in w.metadata_keys and "tenant_id" not in w.metadata_keys:
                for r in reads:
                    if not r.has_filter:
                        sink = self._find_sink(model, r.id)
                        entry_w = self._find_entry_point(model, w.id)
                        entry_r = self._find_entry_point(model, r.id)
                        yield Finding(
                            rule_id="AW-MEM-001",
                            title="Cross-tenant data reachable: no user scope at write or read",
                            severity=Severity.CRITICAL,
                            layer="ASM",
                            evidence_path=[entry_w, w, store, r, entry_r, sink],
                            proof_strength=...,
                        )
```

### Q5: Unsanitized Context Assembly

**Rule:** AW-MEM-005 (enhanced)

**Logic:** For every `ReadOp` → `ContextSink` edge where `sink.sanitized = False`, emit finding.

```python
def _q5_unsanitized_context(self, model):
    for edge in model.edges:
        if edge.kind == "assembles_into":
            read = self._find_node(model, edge.source_id)
            sink = self._find_node(model, edge.target_id)
            if isinstance(sink, ContextSink) and not sink.sanitized:
                yield Finding(
                    rule_id="AW-MEM-005",
                    title="Retrieved memory injected into LLM context without sanitization",
                    severity=Severity.MEDIUM,
                    layer="ASM",
                    evidence_path=[read, sink],
                    proof_strength=...,
                )
```

### Proof Strength and Severity Discipline

Every ASM finding computes proof strength from the weakest confidence in its path:

```python
def _proof_strength(self, path_nodes: list) -> str:
    confidences = [n.confidence for n in path_nodes]
    if Confidence.UNKNOWN in confidences:
        return "uncertain"    # max severity: MEDIUM
    if Confidence.INFERRED in confidences:
        return "possible"     # max severity: HIGH
    return "confirmed"        # max severity: CRITICAL
```

**CRITICAL only for confirmed cross-tenant paths with all nodes at `CONFIRMED` confidence.** This preserves the severity discipline invariant.

---

## 6. Finding Output — Path Witnesses

ASM findings include a **path witness** — the complete chain from entry point to violation, attached to the finding's evidence field.

```python
@dataclass
class Finding:
    # ... existing fields unchanged ...

    # V4 addition: optional path witness
    evidence_path: list[dict] | None = None   # serialized ASM node chain
    proof_strength: str | None = None         # "confirmed" | "possible" | "uncertain"
```

Serialized in `--format agent-json`:

```json
{
  "rule_id": "AW-MEM-002",
  "title": "Filter key(s) {'user_id'} never written at ingestion",
  "severity": "HIGH",
  "layer": "ASM",
  "proof_strength": "confirmed",
  "evidence_path": [
    {"type": "WriteOp", "file": "ingest.py", "line": 15, "detail": "metadata_keys: {\"source\"}"},
    {"type": "Store", "file": "config.py", "line": 8, "detail": "chroma, collection='docs'"},
    {"type": "ReadOp", "file": "query.py", "line": 20, "detail": "filter_keys: {\"user_id\"}"}
  ]
}
```

Existing reporters (terminal, json, sarif) ignore these new fields gracefully — they're optional. `agent-json` and `sarif` reporters gain richer output.

---

## 7. Integration with Existing Layers

### What Stays Exactly The Same

| Component | Change? | Why |
|---|---|---|
| `MemoryAnalyzer` (L1) | No | Still catches the basic case (no filter kwarg). ASM catches the complex case. Both emit AW-MEM-001 — dedup handles overlap. |
| `ToolAnalyzer` (L1) | No | Tool rules don't benefit from application-level modeling. |
| `CallGraphAnalyzer` (L2) | No | Still refines L1 findings. ASM reuses the call graph for edge linking. |
| `TaintAnalyzer` (L3) | No | Still tracks user_id flow. ASM reuses taint data for confidence. |
| `ConfigAuditor` (L4) | No | Config checks are orthogonal. ASM Store nodes absorb L4 findings as attributes. |
| `SemgrepAnalyzer` (L5) | No | Pattern validation layer. |
| `SymbolicAnalyzer` (L6) | No | Branch-conditional gaps. |
| `ConfidenceScorer` (L8) | No | Scores all findings including ASM findings. |
| All reporters | Minimal | Add optional `evidence_path` and `proof_strength` fields. |
| CLI | Minimal | No new flags needed. ASM runs by default when extraction succeeds. |

### What Changes

| Component | Change | Risk |
|---|---|---|
| `LangChainAdapter.parse()` | Extended to produce `AgentSpec.asm` in addition to existing fields | Low — additive output, existing fields unchanged |
| `scanner.py` | New call: `ASMAnalyzer.analyze(spec.asm)` after L6 | Low — one new analyzer in the sequence |
| `models.py` | New ASM dataclasses + optional `evidence_path` on `Finding` | Low — additive fields |
| `_dedup_findings()` | Must handle ASM findings overlapping with L1 findings on same rule | Medium — dedup logic needs testing |
| New file: `analyzers/asm.py` | ASM query analyzer (Q1–Q5) | New code — needs thorough testing |
| New file: `extractors/entry_points.py` | Entry point detection (FastAPI/Flask/Celery) | New code — framework-specific |
| New file: `extractors/edge_linker.py` | Node-to-node edge inference | High — most error-prone component |

### Dedup Strategy

When ASM and L1 both fire AW-MEM-001 on the same code site:

1. If ASM has a `confirmed` path witness and L1 has no path → keep ASM finding, drop L1 finding.
2. If ASM has an `uncertain` path and L1 has a clean detection → keep L1 finding, drop ASM finding.
3. If both fire on different code sites → keep both (different locations).

---

## 8. Rollout Plan

### Phase A: Shadow Mode

- Build ASM extraction and queries.
- Run ASM alongside existing pipeline but **don't include ASM findings in the output**.
- Log ASM findings internally. Compare against L1–L3 findings on the benchmark suite.
- Metric: "How many true positives does ASM find that L1–L3 miss?"
- CLI: `agentwall scan . --asm-shadow` (internal/debug flag)

### Phase B: Additive Mode

- ASM findings included in output alongside L1–L3 findings.
- Dedup logic active — ASM findings with stronger proof replace L1 findings.
- Existing test suite must pass unchanged.
- New test fixtures validate ASM-specific detections (write-read mismatch, auth gap, lifecycle).
- CLI: ASM runs by default. `--fast` skips ASM (L0–L2 only).

### Phase C: Primary Mode

- For memory isolation rules (AW-MEM-001/002/003), ASM becomes the primary detector.
- L1 memory checks become the fallback — only fire if ASM extraction fails (parse error, unsupported framework).
- Tool rules (AW-TOOL-*) unchanged — L1 remains primary.
- Config rules (AW-CFG-*) unchanged — L4 remains primary.

---

## 9. New Files Summary

```
src/agentwall/
├── models.py                    # + ApplicationModel, EntryPoint, WriteOp, ReadOp,
│                                #   Store, ContextSink, Edge, Confidence, Provenance
├── scanner.py                   # + ASMAnalyzer call after L6
├── adapters/
│   └── langchain.py             # + ASM extraction in parse()
├── extractors/                  # NEW directory
│   ├── __init__.py
│   ├── entry_points.py          # FastAPI/Flask/Celery entry point detection
│   ├── context_sinks.py         # Return value tracking to LLM prompt assembly
│   └── edge_linker.py           # Variable aliasing + call graph → edges
├── analyzers/
│   └── asm.py                   # NEW: Q1–Q5 graph queries
tests/
├── test_asm.py                  # NEW: ASM query tests
├── test_extractors.py           # NEW: extraction tests
└── fixtures/
    ├── asm_write_read_mismatch/ # NEW: Q2 fixture
    ├── asm_unauth_write/        # NEW: Q1 fixture
    ├── asm_shared_collection/   # NEW: Q3 fixture
    └── asm_lifecycle/           # NEW: Q4 fixture
```

---

## 10. Success Criteria

| Metric | Target |
|---|---|
| ASM finds ≥ 3 true positives across real-world repos that L1–L3 cannot | Required |
| Zero false positives on `langchain_safe` fixture | Required |
| Zero regressions on existing 216 tests | Required |
| ASM extraction overhead on 50K LOC | < 5 seconds |
| ASM query execution (5 queries) | < 1 second |
| Path witness included in ≥ 80% of ASM findings | Required |
| `UNCERTAIN` findings never emit CRITICAL | Required (severity discipline) |

---

## 11. What This Does NOT Include

Being explicit about scope:

| Not in V4 | Why | When |
|---|---|---|
| Multi-framework extractors (CrewAI, AutoGen) | FastAPI + LangChain first. Validate ASM on one stack before expanding. | v1.0 |
| User-extensible query language | Hardcoded Q1–Q5 for now. Extensibility is over-engineering at this stage. | v1.2+ |
| Graph visualization export | Nice-to-have but not needed for detection. | v1.3 |
| Temporal lifecycle queries | "Does the nightly job preserve metadata?" requires modeling job schedules. | v1.4 |
| Agent topology for multi-agent systems | Requires CrewAI/AutoGen adapters first. | v1.2 |

---

*End of document.*
