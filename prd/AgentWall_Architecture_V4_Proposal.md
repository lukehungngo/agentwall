# AgentWall

## Architecture V4 Proposal

**From Pattern Matching to Application-Level Security Analysis**

SoH Engineering — March 2026

**CONFIDENTIAL**

---

# 1. Executive Summary

This proposal describes an architectural enhancement to AgentWall that extends the current pattern-matching pipeline (L0–L8) with application-level semantic analysis. The enhancement is called the Application Security Model (ASM).

ASM is not a new system. It is a richer intermediate representation flowing through the same pipeline. The existing AgentSpec evolves from a flat list of boolean flags into a graph of typed nodes with relationships. Same layers, same rules, longer reach.

**Key outcome:** 6 new detection capabilities that L0–L8 structurally cannot produce, using the same rule IDs (AW-MEM-001/002/003/005), mapped to the same attack vectors, with no breaking changes to the existing codebase.

---

# 2. Current Architecture (V3)

## 2.1 What We Have

AgentWall v0.x is a layered checker pipeline. Each layer inspects code patterns at increasing depth and emits findings independently. 216 tests passing, 72% coverage, benchmark across 20 real-world projects (12/20 with confirmed issues, 57 CRITICAL findings).

### Pipeline Flow

```
L0 detector.auto_detect_framework()     → framework: str
L1 LangChainAdapter.parse()             → AgentSpec (tools[], memory_configs[])
   MemoryAnalyzer.analyze(spec)          → Finding[] (AW-MEM-001–005)
   ToolAnalyzer.analyze(spec)            → Finding[] (AW-TOOL-001–005)
L2 CallGraphAnalyzer.analyze(spec, l1)   → Finding[] (refined)
L3 TaintAnalyzer.analyze(spec)           → Finding[] (new)
L4 ConfigAuditor.analyze(target)         → Finding[] (new)
L5 SemgrepAnalyzer.analyze(target)       → Finding[] (new)
L6 SymbolicAnalyzer.analyze(spec)        → Finding[] (new)
L7 patcher.run_with_instrumentation()    → Finding[] (opt-in)
L8 ConfidenceScorer.apply_scores()       → Finding[] (adjusted)
```

### Core Data Model

AgentSpec is the central intermediate representation. Today it is flat:

| Field | Type | What It Captures |
|---|---|---|
| tools | `list[ToolSpec]` | Tool registrations with boolean flags |
| memory_configs | `list[MemoryConfig]` | Vector store configs with boolean flags |
| source_files | `list[Path]` | Scanned file paths |
| metadata | `dict` | Framework metadata |

MemoryConfig carries boolean flags: `has_tenant_isolation`, `has_metadata_filter_on_retrieval`, `has_metadata_on_write`, `sanitizes_retrieved_content`, `has_injection_risk`. These capture what exists but not how components relate.

## 2.2 What Works Well

- **L1 (AST per-file)** reliably catches missing filter kwargs. 57 CRITICAL findings across 8 real-world projects.
- **L2 (call graph)** reduces false positives when wrapper functions apply filters cross-file.
- **L3 (taint)** proves whether user_id actually flows from request to filter sink.
- **L4 (config)** catches infrastructure misconfigs: exposed ports, allow_reset=True, hardcoded keys. 45 hits across 8 projects.
- **L6 (symbolic)** detects branch-conditional gaps where filter exists on some paths but not all.
- **L8 (confidence)** regex heuristics resolve 60%+ of ambiguous variable names without LLM calls.

## 2.3 Where It Hits the Ceiling

Every layer asks questions about individual code sites. No layer asks questions about the application as a whole.

| Question We Cannot Answer | Why |
|---|---|
| Does ingestion metadata schema match retrieval filter schema? | L1 checks retrieval only. Never connects to write path in another module. |
| Is the /ingest endpoint behind authentication? | L3 tracks user_id flow within a request, not auth middleware topology. |
| Is collection_name='faq' per-tenant or shared? | L1 sees scoping but cannot judge string semantics across multiple callers. |
| Does the nightly re-indexer preserve metadata? | L2 call graph does not connect cron jobs to API handlers. |
| Can user A's data reach user B's LLM context? | Requires tracing ingestion → storage → retrieval → context assembly across the full app. |

**Root cause:** AgentSpec is flat. It captures what exists (boolean flags) but not how components relate. There is no model of the application's data lifecycle, trust boundaries, or component topology.

---

# 3. Why We Need to Change

## 3.1 The Gap: Rules vs. Detection Capability

We mapped every rule (AW-MEM-001–005, AW-TOOL-001–005) and every attack vector (35 cataloged) against what each analysis layer can actually detect. The result:

| Rule | L1–L3 Catches | What L1–L3 Misses |
|---|---|---|
| **AW-MEM-001** | Missing filter kwarg (the obvious case) | Filter exists but checks wrong key. Static shared collection. |
| **AW-MEM-002** | Write metadata + no read filter (same file only) | Write and read in different modules. Metadata keys mismatch. |
| **AW-MEM-003** | No access control on constructor | Store has auth config but unauthenticated cron job writes to it. |
| **AW-MEM-005** | Raw concatenation patterns | Full retrieval-to-LLM-context path across multiple modules. |

## 3.2 The 6 Blind Spots

These are real bugs in real codebases that our current pipeline structurally cannot find:

| Blind Spot | Attack Vector | Why Current Layers Miss It |
|---|---|---|
| Write-read metadata key mismatch | ATK-MEM-002 | L1 checks read side only. Never compares to write path. |
| Static shared collection used as isolation | ATK-MEM-003 | L1 sees collection_name='faq' and cannot judge it is shared. |
| Unauthenticated background worker writes to store | ATK-MEM-004 | L4 checks config. No layer maps code-level auth topology. |
| Cross-session memory hijacking | ATK-INJ-002 | Nothing detects shared conversation memory without session scoping. |
| Metadata loss in re-indexing lifecycle | ATK-MEM-002 variant | L2 call graph does not link cron/worker entry points to API handlers. |
| Unsanitized retrieval-to-LLM-context assembly | ATK-INJ-001 | L1 pattern-matches but does not trace the full data flow path. |

**Evidence:** The write-read mismatch in Langchain-Chatchat (37K stars) is confirmed. `kb_name` is used as collection scoping but `user_id` is never written as metadata — the filter on retrieval checks a field that does not exist at ingestion time. L1 passes this because the filter kwarg exists.

## 3.3 Why Not Just Improve L1–L3?

Because the limitation is structural, not implementational. L1 operates per-file. L2 connects functions. L3 tracks single variables. None of them build a model of the application. The questions in Section 2.3 require comparing components that are architecturally related but have no direct code-level connection (ingestion endpoint vs. retrieval endpoint, API handler vs. cron job).

No amount of improvement to per-file pattern matching or single-variable taint tracking will answer "does the write path metadata schema match the read path filter schema across the entire codebase." That requires a different kind of analysis: build the model first, then query it.

---

# 4. The Proposal: Application Security Model (ASM)

## 4.1 Core Idea

Replace the flat boolean AgentSpec with a graph of typed nodes and edges that represents the application's data lifecycle. Then express security properties as graph queries instead of pattern matches.

```
V3:  AST  →  flat AgentSpec (booleans)  →  pattern checkers  →  findings
V4:  AST  →  rich AgentSpec (graph)     →  graph queries     →  findings
```

Same pipeline. Same rules. Same layers. The data model that flows through the pipeline carries enough structural information to answer application-level questions.

## 4.2 New Data Model

AgentSpec gains an optional `asm` field. Existing fields are unchanged for backward compatibility:

```python
class AgentSpec(BaseModel):
    framework: str                          # unchanged
    source_files: list[Path]                # unchanged
    tools: list[ToolSpec]                   # unchanged
    memory_configs: list[MemoryConfig]      # unchanged
    metadata: dict                          # unchanged
    asm: ApplicationModel | None = None     # NEW
```

The ApplicationModel is a directed graph with 6 node types:

| Node Type | What It Represents | Key Attributes |
|---|---|---|
| EntryPoint | HTTP route, cron job, CLI command, background worker | kind, auth state, user_id_source |
| WriteOp | Call to add_documents, add_texts, upsert | store_id, metadata_keys written |
| Store | Vector store instance (Chroma, FAISS, PGVector...) | backend, collection_name, is_static |
| ReadOp | Call to similarity_search, as_retriever | store_id, filter_keys, has_filter |
| ContextSink | Where retrieved data ends up (LLM prompt, API response) | kind, sanitized |
| AuthBoundary | Authentication enforcement point (Depends, middleware) | mechanism, extracts_user_id |

Every node carries provenance (file:line:col), confidence (CONFIRMED / INFERRED / UNKNOWN), and domain-specific attributes. Edges connect nodes: `triggers`, `writes_to`, `reads_from`, `guarded_by`, `assembles_into`.

## 4.3 Confidence and Severity Discipline

Every node and edge has a three-valued confidence level. This is the single most important design decision — it prevents severity inflation.

| Confidence | Meaning | Example |
|---|---|---|
| CONFIRMED | Statically proven. Value is known. | `filter={'user_id': uid}` → filter key is 'user_id' |
| INFERRED | Derived from structure. High probability. | Function called from a route with `Depends()` |
| UNKNOWN | Dynamic value, third-party code, metaprogramming. | `collection_name = os.getenv('COLL')` |

| Proof Strength | When | Max Severity Allowed |
|---|---|---|
| Confirmed | All path nodes/edges are CONFIRMED | CRITICAL |
| Possible | At least one INFERRED node/edge | HIGH |
| Uncertain | At least one UNKNOWN node/edge | MEDIUM (flagged for L7/L8) |

**CRITICAL only for confirmed cross-tenant paths.** UNCERTAIN findings cap at MEDIUM and are flagged as candidates for runtime (L7) or LLM (L8) confirmation. This preserves the severity discipline invariant.

## 4.4 The 5 Graph Queries

Security properties expressed as graph traversals. Each query maps to an existing rule ID:

| Query | What It Detects | Rule ID | Proof |
|---|---|---|---|
| Q1 | Unauthenticated entry point writes to vector store | AW-MEM-003 | EntryPoint(auth=unauth) → WriteOp → Store |
| Q2 | Write metadata keys do not match read filter keys | AW-MEM-002 | WriteOp(keys={source}) vs ReadOp(keys={user_id}) |
| Q3 | Static shared collection with no per-query filter | AW-MEM-001 | Store(static name) ← multiple writers, unfiltered reads |
| Q4 | Cross-tenant reachable path (full lifecycle proof) | AW-MEM-001 | EntryPoint → Write(no uid) → Store → Read(no filter) → Sink |
| Q5 | Unsanitized retrieval assembled into LLM context | AW-MEM-005 | ReadOp → ContextSink(sanitized=false) |

Every finding includes a path witness — the complete node chain from entry point to violation, with per-hop confidence and source location.

---

# 5. Concrete Changes to the Codebase

## 5.1 Files That Change (Additive Only)

| File | Change | Risk |
|---|---|---|
| `models.py` | Add ASM dataclasses (EntryPoint, WriteOp, Store, ReadOp, ContextSink, Edge, ApplicationModel). Add optional evidence_path + proof_strength to Finding. | Low — additive fields |
| `scanner.py` | Add one call: `ASMAnalyzer.analyze(spec.asm)` after L6, before L7. ~10 lines. | Low — one new analyzer in sequence |
| `adapters/langchain.py` | Extend _FileVisitor to emit ASM nodes alongside existing boolean flags. Extend `parse()` to run EdgeLinker and build ApplicationModel. | Medium — extends hot path |
| `_dedup_findings()` in `scanner.py` | Handle ASM findings overlapping with L1 findings on same rule + location. | Medium — dedup logic needs testing |

## 5.2 New Files

| New File | Purpose | Effort |
|---|---|---|
| `analyzers/asm.py` | ASM query analyzer: Q1–Q5 graph traversals | Medium |
| `extractors/__init__.py` | New directory for ASM extraction modules | Trivial |
| `extractors/entry_points.py` | FastAPI/Flask/Celery route + decorator detection | Medium |
| `extractors/context_sinks.py` | Return value tracking from retrieval to LLM prompt assembly | Medium |
| `extractors/edge_linker.py` | Variable aliasing + call graph integration → graph edges | High (most error-prone) |
| `tests/test_asm.py` | ASM query tests | Medium |
| `tests/test_extractors.py` | Extraction unit tests | Medium |
| `tests/fixtures/asm_*/` | 4 new fixture directories (write-read mismatch, unauth write, shared collection, lifecycle) | Medium |

## 5.3 What Does NOT Change

- **MemoryAnalyzer (L1)** — still catches the basic case (no filter kwarg)
- **ToolAnalyzer (L1)** — tool rules do not benefit from application modeling
- **CallGraphAnalyzer (L2)** — still refines L1. ASM reuses its call graph for edge linking.
- **TaintAnalyzer (L3)** — still tracks user_id flow. ASM reuses taint data for confidence.
- **ConfigAuditor (L4)** — config checks are orthogonal to code-level analysis.
- **SemgrepAnalyzer (L5), SymbolicAnalyzer (L6)** — unchanged.
- **ConfidenceScorer (L8)** — scores all findings including ASM findings.
- All reporters (terminal, json, sarif, agent-json, patch) — minimal change: add optional evidence_path field.
- All CLI flags (`--fast`, `--layers`, `--dynamic`, `--llm-assist`) — unchanged.
- All 216 existing tests — must pass with zero regressions.

## 5.4 Extraction: What the Adapter Already Detects

~60% of what ASM needs is already being detected by the LangChain adapter and collapsed into boolean flags. V4 preserves the original structure instead of discarding it:

| Pattern Already Detected | V3 Output (boolean) | V4 Adds (structured) |
|---|---|---|
| `Chroma(collection_name=...)` | `MemoryConfig(backend='chroma')` | Store node + collection_name + is_static |
| `vs.add_documents(metadata={...})` | `has_metadata_on_write = True` | WriteOp node + metadata_keys extracted |
| `vs.similarity_search(filter={...})` | `has_metadata_filter_on_retrieval = True` | ReadOp node + filter_keys extracted |
| `@app.post('/upload')` | Not extracted | EntryPoint node + route + method |
| `Depends(get_current_user)` | Not extracted | EntryPoint.auth = 'authenticated' |
| `'\n'.join(docs)` into prompt | `sanitizes_retrieved_content = False` | ContextSink node + sanitized = False |

---

# 6. Rollout Plan

## Phase A: Shadow Mode

- Build ASM extraction and queries.
- Run ASM alongside existing pipeline but do not include ASM findings in output.
- Log ASM findings internally. Compare against L1–L3 on benchmark suite.
- Metric: How many true positives does ASM find that L1–L3 miss?
- CLI flag: `--asm-shadow` (internal debug flag).

## Phase B: Additive Mode

- ASM findings included in output alongside L1–L3 findings.
- Dedup logic active — ASM findings with stronger proof replace L1 findings.
- Existing 216 tests must pass unchanged. New fixtures validate ASM-specific detections.
- ASM runs by default. `--fast` skips ASM (L0–L2 only).

## Phase C: Primary Mode

- For memory isolation rules (AW-MEM-001/002/003), ASM becomes primary detector.
- L1 memory checks become fallback — only fire if ASM extraction fails.
- Tool rules (AW-TOOL-*) unchanged — L1 remains primary.
- Config rules unchanged — L4 remains primary.

## Dedup Strategy

When ASM and L1 both fire on the same rule + location:

- ASM has confirmed path + L1 has no path → keep ASM, drop L1.
- ASM has uncertain path + L1 has clean detection → keep L1, drop ASM.
- Both fire on different locations → keep both.

---

# 7. Success Criteria

| Metric | Target | Validation Method |
|---|---|---|
| New true positives | ≥ 3 findings on real-world repos that L1–L3 cannot produce | Benchmark suite comparison |
| False positives on safe fixture | 0 | langchain_safe fixture |
| Regressions on existing tests | 0 out of 216 | CI pipeline |
| ASM extraction overhead (50K LOC) | < 5 seconds | Benchmark timing |
| ASM query execution (5 queries) | < 1 second | Benchmark timing |
| Path witness coverage | ≥ 80% of ASM findings include evidence path | Report inspection |
| Severity discipline | UNCERTAIN findings never emit CRITICAL | Unit test assertion |

---

# 8. Risks and Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Incorrect entity linking | High-confidence wrong findings | Confidence propagation: every edge carries confidence. Wrong links get INFERRED or UNKNOWN, capping severity. |
| Graph construction too slow | Scan time exceeds 90s budget | Incremental caching keyed by file content hashes. `--fast` skips ASM entirely. |
| Framework API drift | Extractors break on new LangChain versions | Same adapter pattern as V3. Version-aware normalization. Fail-safe: if extraction fails, fall back to L1–L3. |
| Noise from UNKNOWN nodes | Too many MEDIUM findings that are not actionable | UNKNOWN nodes produce suggestions, not findings. Only emit if there is a confirmed partial path. |
| Scope creep during implementation | ASM absorbs more than planned | Strict MVP: FastAPI + LangChain, 5 node types, 5 queries. Ship and validate before expanding. |

---

# 9. Explicit Non-Goals

- Multi-framework extractors (CrewAI, AutoGen) — validate ASM on one stack first.
- User-extensible query language — hardcoded Q1–Q5 for now.
- Graph visualization export — nice-to-have, not needed for detection.
- Agent topology for multi-agent systems — requires multi-framework support.
- Runtime behavior confirmation — that is L7's job, not ASM's.

---

# 10. Implementation Sequence

| Step | What | Depends On | Effort |
|---|---|---|---|
| 1 | Define IR data model in `models.py` | Nothing | Low |
| 2 | FastAPI EntryPoint extractor | Step 1 | Medium |
| 3 | LangChain Write/Read extractors (extend adapter) | Step 1 | Medium |
| 4 | Chroma/FAISS Store extractor (extend adapter) | Step 1 | Low |
| 5 | Context Sink extractor | Step 1 | Medium |
| 6 | Auth boundary extractor | Step 1 | Medium |
| 7 | Edge linker (variable aliasing + call graph) | Steps 2–6 + L2 | High |
| 8 | ASM query engine (Q1–Q5) | Step 7 | Medium |
| 9 | Path witness formatter + Finding integration | Step 8 | Low |
| 10 | `scanner.py` integration + dedup | Step 9 | Low |
| 11 | Test fixtures + validation suite | Steps 8–10 | Medium |

---

*End of Proposal*
