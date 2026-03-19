# AgentWall — Enhanced Memory Leak Detection

## Analysis Methodology Specification

**Version:** 1.0
**Date:** 2026-03-17
**Author:** SoH Engineering
**Status:** Draft
**Parent:** AgentWall PRD v2 (Solo-Engineer Edition)
**Scope:** Extends FR-101 (Memory Leakage Detection) with multi-layer analysis beyond regex + AST

---

## 1. Problem Statement

AgentWall v0.1 detects memory leaks using two layers: regex-based framework detection (L0) and single-file AST walking with kwarg inspection (L1). Field testing against Langchain-Chatchat (37K stars) and Long-Trainer confirmed true positives, but also revealed structural limitations:

- **Cross-file blind spots.** When a filter is applied in a wrapper function 3 files away from the retrieval call, L1 misses it. Every cross-check we performed required manual `grep` across files.
- **No data flow tracking.** L1 checks "is there a `filter` kwarg?" but cannot answer "does the user's identity actually reach the query?"
- **Config-layer gaps.** Vector store misconfiguration (e.g. `allow_reset=True`, missing partition isolation) lives in config files, not Python code. L1 doesn't touch configs.
- **False positive cost.** A `kb_name`-based collection scoping pattern looks like missing isolation to L1, requiring manual triage to determine if it's per-user or shared.

This document specifies the analysis layers that close these gaps.

---

## 2. Analysis Layer Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    DETECTION PIPELINE                        │
│                                                             │
│  L0  Regex / Import Matching         (framework detection)  │
│   │                                                         │
│  L1  Single-File AST Visitor         (kwarg inspection)     │
│   │                                                         │
│  L2  Inter-Procedural Call Graph     (cross-file resolution)│
│   │                                                         │
│  L3  Taint Analysis                  (source → sink flow)   │
│   │                                                         │
│  L4  Config Auditing                 (infra misconfiguration│
│   │                                                         │
│  L5  Semgrep Rules                   (declarative patterns) │
│   │                                                         │
│  L6  Symbolic / Abstract Interp.     (path-sensitive)       │
│   │                                                         │
│  L7  Runtime Instrumentation         (dynamic, opt-in)      │
│   │                                                         │
│  L8  LLM-Assisted Confidence        (ambiguity resolver)   │
│                                                             │
│  Each layer feeds findings into the same PolicyEngine.      │
│  Layers are additive — higher layers refine, not replace.   │
└─────────────────────────────────────────────────────────────┘
```

**Design principle:** Each layer is independently deployable. Users on CI with strict time budgets can run L0–L2 only. Full audit runs L0–L5. L6–L8 are opt-in.

---

## 3. Layer Specifications

### 3.1 L0 — Regex / Import Matching (Exists)

**Status:** Implemented
**Purpose:** Framework detection
**Method:** Frequency-scored import counting across source files, with `_SKIP_DIRS` filtering
**Output:** `FrameworkType` enum → selects adapter

No changes needed. Functions as gate for all subsequent layers.

---

### 3.2 L1 — Single-File AST Visitor (Exists)

**Status:** Implemented
**Purpose:** Detect missing filter kwargs on retrieval calls within a single file
**Method:** `ast.NodeVisitor` walks each `.py` file independently. Tracks vector store instantiation, marks retrieval calls as filtered or unfiltered.
**Bugs fixed:**
- `search_kwargs={"k": 5}` no longer counts as a filter (must contain `"filter"` key)
- Sticky-state accumulation (`False or True`) eliminated — any unfiltered call marks config as missing filter

**Limitation:** Cannot follow function calls that cross file boundaries. If `do_search()` is defined in `base.py` and calls `self.vectorstore.similarity_search()` in `chroma_service.py`, L1 treats them as independent files with no connection.

---

### 3.3 L2 — Inter-Procedural Call Graph

**Status:** Planned (W3)
**Purpose:** Resolve method calls across files to trace the full retrieval chain
**Priority:** HIGH — biggest detection gap today

#### 3.3.1 Problem

The Langchain-Chatchat cross-check illustrates the gap:

```
kb_api.py                          base.py                        chromadb_kb_service.py
─────────                          ───────                        ──────────────────────
search_docs()                      KBService.do_search()          ChromaKBService._load_chroma()
  └─ kb.do_search(query, top_k)      └─ retriever = get_Retriever()   └─ Chroma(collection_name=kb_name)
                                        └─ retriever.get_relevant_documents(query)
```

L1 sees each file in isolation. It flags `Chroma(collection_name=...)` but cannot determine if a filter is applied somewhere upstream or downstream in the call chain.

#### 3.3.2 Approach

Build a lightweight call graph using one of:

| Option | Library | Pros | Cons |
|---|---|---|---|
| A | `jedi` | Mature, handles dynamic dispatch | Slow on large codebases, heavy dependency |
| B | `pyright` programmatic API | Fast, type-aware resolution | Requires Node.js runtime, complex API |
| C | Custom AST import resolver | Zero deps, we control it | Won't resolve dynamic dispatch, inheritance |

**Recommended: Option C (custom) for MVP, Option A (jedi) post-launch.**

MVP call graph builder:

1. Parse all source files → collect class definitions, method definitions, function definitions
2. Build import map: `from foo.bar import Baz` → resolve to file path
3. For each method call `x.method()`, resolve `x` to its class via assignment tracking
4. Produce edges: `(caller_file:caller_func) → (callee_file:callee_func)`
5. Walk edges from retrieval calls backward to find if any node applies a filter

#### 3.3.3 Data Model

```python
@dataclass
class CallEdge:
    caller: FunctionRef  # file + function/method name
    callee: FunctionRef
    call_site: Location  # file:line:col
    resolved: bool       # True if statically resolved, False if heuristic

@dataclass
class CallGraph:
    edges: list[CallEdge]
    unresolved: list[Location]  # calls we couldn't resolve

    def callers_of(self, func: FunctionRef) -> list[CallEdge]: ...
    def callees_of(self, func: FunctionRef) -> list[CallEdge]: ...
    def paths_between(self, source: FunctionRef, sink: FunctionRef) -> list[list[CallEdge]]: ...
```

#### 3.3.4 Integration with L1

L1 produces `MemoryConfig` objects with `has_metadata_filter_on_retrieval: bool`. L2 post-processes these:

1. For each `MemoryConfig` where `has_metadata_filter_on_retrieval = False`:
2. Find all callers of the retrieval function via call graph
3. Check if any caller in the chain applies a filter (wraps the call with filter injection)
4. If filter found upstream → downgrade to INFO ("filter applied via wrapper")
5. If no filter in entire chain → confirm as CRITICAL (AW-MEM-001)

This eliminates false positives from wrapper patterns.

#### 3.3.5 Acceptance Criteria

- Resolves direct imports (`from x import Y`) and relative imports
- Resolves class method calls where the class is statically determinable
- Handles inheritance (checks parent class methods)
- Produces `unresolved` list for calls it cannot trace (transparency)
- Scan time increase: < 2x over L1-only for projects under 50K LOC

---

### 3.4 L3 — Taint Analysis

**Status:** Planned (post-launch, v0.2)
**Purpose:** Track whether user identity flows from request entry point to retrieval filter
**Priority:** HIGH — the definitive answer to "is this actually isolated?"

#### 3.4.1 Problem

L1 and L2 check *presence* of a filter kwarg. They don't check *what's in it*. Consider:

```python
# This passes L1 — filter kwarg exists
docs = vectorstore.similarity_search(query, filter={"source": "web"})

# This is what we actually want
docs = vectorstore.similarity_search(query, filter={"user_id": request.user.id})
```

Both have a `filter` kwarg. Only the second provides tenant isolation. Taint analysis answers: "does data from `request.user` (source) reach the `filter` parameter (sink)?"

#### 3.4.2 Approach

| Option | Tool | Effort | Accuracy |
|---|---|---|---|
| A | `pysa` (Meta's taint analyzer) | Low (config-only) | High for supported patterns |
| B | Custom def-use chain builder | Medium | Medium — misses dynamic dispatch |
| C | `CodeQL` Python taint queries | Medium | High — best cross-function tracking |

**Recommended: Option A (pysa) if target has type annotations, Option C (CodeQL) otherwise.**

#### 3.4.3 Taint Model

```
Sources (user identity enters the system):
  - request.user, request.user_id, request.headers["X-User-ID"]
  - session.user_id, g.user, current_user
  - Function parameters named: user_id, tenant_id, org_id, owner_id

Sinks (data reaches vector store query):
  - vectorstore.similarity_search(..., filter=TAINTED)
  - retriever.get_relevant_documents(..., search_kwargs={"filter": TAINTED})
  - collection.query(..., where=TAINTED)

Sanitizers (none — user identity should flow through unchanged):
  - N/A for this check

Verdict:
  - Source reaches sink → ISOLATED (no finding)
  - Source never reaches sink → AW-MEM-001 CRITICAL
  - Source reaches sink but through unsafe transform → AW-MEM-002 HIGH
```

#### 3.4.4 Acceptance Criteria

- Detects when `user_id` from request context flows into vector store filter
- Detects when filter exists but contains only static values (no user scoping)
- Works across 3+ files in a call chain
- Configurable source/sink definitions via `agentwall.yaml`
- False positive rate: < 10% on benchmarked repos

---

### 3.5 L4 — Configuration Auditing

**Status:** Planned (W2 — aligns with AW-MEM-004/005)
**Purpose:** Detect insecure vector store and infrastructure configuration
**Priority:** MEDIUM — different signal from code analysis, cheap to implement

#### 3.5.1 What It Checks

| Config Target | Check | Finding |
|---|---|---|
| ChromaDB | `allow_reset=True` in production | AW-MEM-004 (unsafe default) |
| ChromaDB | No authentication configured | AW-MEM-005 (no access control) |
| Milvus | Single partition for multi-tenant data | AW-MEM-001 variant |
| Milvus | `auto_id=True` without namespace isolation | AW-MEM-003 |
| PGVector | Missing RLS (Row-Level Security) policy | AW-MEM-001 variant |
| PGVector | `collection_name` is static (not per-user) | AW-MEM-001 |
| Pinecone | Single namespace, no metadata filtering | AW-MEM-001 |
| Qdrant | No payload-based access filtering | AW-MEM-001 |
| Weaviate | Multi-tenancy disabled | AW-MEM-003 |
| `.env` / `settings.py` | `DEBUG=True`, `ALLOW_RESET=True` | AW-MEM-004 |
| `docker-compose.yml` | Vector DB port exposed to `0.0.0.0` | AW-MEM-005 |
| Connection strings | No TLS/SSL (`?sslmode=disable`) | AW-MEM-005 |

#### 3.5.2 Implementation

Pure file parsing — no AST needed:

```python
class ConfigAuditor:
    """Scans configuration files for insecure vector store settings."""

    PARSERS: dict[str, Callable] = {
        ".yaml": yaml.safe_load,
        ".yml": yaml.safe_load,
        ".toml": tomllib.loads,
        ".json": json.loads,
        ".env": dotenv_values,
        ".py": _extract_python_config,  # regex on UPPER_CASE assignments
    }

    def audit(self, target: Path) -> list[Finding]:
        findings = []
        for config_file in self._find_config_files(target):
            parsed = self._parse(config_file)
            findings.extend(self._check_vector_db_config(parsed, config_file))
            findings.extend(self._check_network_exposure(parsed, config_file))
            findings.extend(self._check_unsafe_defaults(parsed, config_file))
        return findings
```

#### 3.5.3 Acceptance Criteria

- Parses YAML, TOML, JSON, `.env`, and Python config files
- Detects at least 5 distinct insecure configuration patterns
- Each finding includes file path, line number, and remediation
- No false positives on single-tenant self-hosted configurations (context-aware: if `agentwall.yaml` declares `deployment: single-tenant`, suppress multi-tenancy findings)

---

### 3.6 L5 — Semgrep Rules

**Status:** Planned (W2 — task list item)
**Purpose:** Declarative, community-maintainable detection rules
**Priority:** MEDIUM — replaces/supplements L1 AST visitor for most checks

#### 3.6.1 Why Semgrep

| Property | Custom AST Visitor (L1) | Semgrep Rules (L5) |
|---|---|---|
| Authoring | Python code, requires dev | YAML, community-writable |
| Cross-file | No (single-file) | Limited (Semgrep Pro has cross-file taint) |
| Maintenance | Code changes = PRs | Rule changes = YAML edits |
| Distribution | Bundled in package | Separate rule registry, hot-loadable |
| Performance | Fast (stdlib ast) | Fast (Rust-based engine) |

L5 doesn't replace L1 — it provides an alternative rule format for community contributions and for patterns better expressed declaratively.

#### 3.6.2 Rule Examples

**AW-MEM-001: No Tenant Filter on Retrieval**

```yaml
rules:
  - id: aw-mem-001-similarity-search
    languages: [python]
    severity: ERROR
    message: >
      similarity_search called without metadata filter.
      Cross-user data leakage possible if vector store is multi-tenant.
    patterns:
      - pattern: $VS.similarity_search($QUERY, ...)
      - pattern-not: $VS.similarity_search($QUERY, ..., filter=$FILTER, ...)
      - pattern-not: $VS.similarity_search($QUERY, ..., where=$WHERE, ...)
    metadata:
      category: memory
      agentwall-id: AW-MEM-001
      confidence: HIGH
      cwe: CWE-200
```

**AW-MEM-003: Vector Store Without Access Control**

```yaml
rules:
  - id: aw-mem-003-chroma-no-auth
    languages: [python]
    severity: WARNING
    message: >
      Chroma client created without authentication.
      Any process with network access can read/write the collection.
    patterns:
      - pattern: chromadb.Client(...)
      - pattern-not: chromadb.Client(..., settings=Settings(chroma_client_auth_provider=...), ...)
    metadata:
      category: memory
      agentwall-id: AW-MEM-003
      confidence: MEDIUM
```

**AW-MEM-004: Unsafe Reset Enabled**

```yaml
rules:
  - id: aw-mem-004-allow-reset
    languages: [python]
    severity: WARNING
    message: >
      allow_reset=True permits full collection deletion.
      Disable in production.
    pattern: Settings(..., allow_reset=True, ...)
    metadata:
      category: memory
      agentwall-id: AW-MEM-004
      confidence: HIGH
```

#### 3.6.3 Integration

```python
class SemgrepLayer:
    """Runs Semgrep rules and converts output to AgentWall findings."""

    RULES_DIR = Path(__file__).parent / "rules" / "semgrep"

    def scan(self, target: Path) -> list[Finding]:
        result = subprocess.run(
            ["semgrep", "--config", str(self.RULES_DIR),
             "--json", "--quiet", str(target)],
            capture_output=True, text=True,
        )
        return self._parse_sarif_to_findings(json.loads(result.stdout))
```

Semgrep is an **optional dependency** (`pip install agentwall[semgrep]`). If not installed, L5 is skipped with a warning.

#### 3.6.4 Acceptance Criteria

- Ships with >= 10 Semgrep rules covering AW-MEM-001 through AW-MEM-005
- Rules are in `rules/semgrep/` directory, YAML format
- Users can add custom rules via `agentwall.yaml` → `semgrep_rules_dir`
- Graceful degradation if `semgrep` binary not installed
- Output mapped to AgentWall `Finding` model with correct severity

---

### 3.7 L6 — Symbolic / Abstract Interpretation

**Status:** Future (v0.3+)
**Purpose:** Path-sensitive analysis — determine if a filter is *always* applied, not just *sometimes*
**Priority:** LOW for MVP — high engineering cost, diminishing returns

#### 3.7.1 Problem

```python
def search(query, user, is_admin=False):
    if is_admin:
        docs = vs.similarity_search(query, filter={"user_id": user.id})
    else:
        docs = vs.similarity_search(query)  # no filter on non-admin path
    return docs
```

L1 sees both calls. It flags the second. But it cannot determine that *both* paths exist from a single entry point. L6 would analyze all branches and report: "filter present on admin path, missing on default path."

#### 3.7.2 Approach

Abstract interpretation with a simple lattice:

```
       TOP (unknown)
      /           \
  FILTERED    UNFILTERED
      \           /
      BOTTOM (unreachable)
```

At each branch point, propagate the abstract state. If any path to a `return` or `response` is `UNFILTERED`, emit finding.

#### 3.7.3 When to Build

Only if false positive rate from L1+L2+L3 exceeds 15% (NFR-11) on the benchmark suite. This is academic-grade complexity — Z3 constraint solving, SSA form conversion. Not justified until we have data showing simpler layers are insufficient.

---

### 3.8 L7 — Runtime Instrumentation (Dynamic)

**Status:** Future (v0.3+)
**Purpose:** Observe actual retrieval calls at runtime to catch what static analysis misses
**Priority:** LOW for MVP — breaks "offline static scanner" promise, requires runnable target

#### 3.8.1 Concept

Monkey-patch `similarity_search`, `get_relevant_documents`, and other retrieval methods at import time. Run the target app's test suite. Log every retrieval call with arguments. Check if any call lacks a filter.

```python
# agentwall/runtime/patcher.py
original_search = Chroma.similarity_search

def patched_search(self, query, **kwargs):
    if "filter" not in kwargs:
        logger.warning(f"AW-MEM-001: similarity_search without filter at {caller_location()}")
    return original_search(self, query, **kwargs)

Chroma.similarity_search = patched_search
```

#### 3.8.2 CLI Interface

```bash
agentwall scan ./project --dynamic          # run with instrumentation
agentwall scan ./project --dynamic --test   # run project's test suite with instrumentation
```

#### 3.8.3 When to Build

Post-launch. Requires:
- Target app must be runnable (has dependencies installed)
- Test suite must exercise retrieval paths
- Introduces runtime dependency on vector store SDKs

Positioned as premium feature: `agentwall scan --dynamic` for users who want confirmed (not theoretical) findings.

---

### 3.9 L8 — LLM-Assisted Confidence Scoring

**Status:** Future (v0.2)
**Purpose:** Reduce false positives by using LLM to judge ambiguous patterns
**Priority:** MEDIUM — high value, but requires careful capital routing

#### 3.9.1 Problem

The Langchain-Chatchat cross-check had a specific ambiguity: "Is `kb_name` a per-user identifier or a shared knowledge base name?" This requires semantic understanding of the application's domain model. Static analysis cannot resolve this — it's a naming convention question.

#### 3.9.2 Approach

For each finding at MEDIUM confidence or below, extract a context window (the flagged code + surrounding 50 lines + class definition + any comments) and ask:

```
Given this code, is `{variable_name}` a per-user identifier or a shared/global identifier?
Consider: variable name, how it's set, class context, comments.
Answer: PER_USER | SHARED | AMBIGUOUS
```

Capital-aware routing:
1. Regex heuristic first: if variable is named `user_id`, `tenant_id`, `owner_id` → PER_USER (skip LLM)
2. Local model (Ollama, e.g. `codellama:7b`) for ambiguous cases
3. API call (Claude Haiku) only if local model returns AMBIGUOUS

#### 3.9.3 Integration

```python
class ConfidenceScorer:
    def score(self, finding: Finding, code_context: str) -> ConfidenceLevel:
        # L8a: regex heuristic
        if self._regex_resolve(finding):
            return self._regex_resolve(finding)

        # L8b: local model
        if ollama_available():
            verdict = self._ask_local(finding, code_context)
            if verdict != "AMBIGUOUS":
                return verdict

        # L8c: API (last resort, requires opt-in)
        if self.config.allow_api_calls:
            return self._ask_api(finding, code_context)

        return ConfidenceLevel.MEDIUM  # default if no LLM available
```

#### 3.9.4 Acceptance Criteria

- Reduces false positive rate by >= 30% on benchmark suite
- Regex heuristic resolves >= 60% of ambiguous cases (no LLM needed)
- Local model latency: < 5s per finding
- API calls: opt-in only (`agentwall.yaml` → `llm_assist: true`)
- Zero API calls in default offline mode

---

## 4. Implementation Roadmap

```
v0.1 (Current — W1-W3)
├── L0  Regex framework detection          ✅ Implemented
├── L1  Single-file AST visitor            ✅ Implemented
├── L4  Config auditing (partial)          ⬜ W2 (AW-MEM-004/005)
└── L5  Semgrep rules (initial set)        ⬜ W2

v0.2 (Post-launch — W4-W8)
├── L2  Inter-procedural call graph        ⬜ Biggest gap closer
├── L8  LLM confidence scoring             ⬜ False positive reducer
└── L4  Config auditing (full)             ⬜ All vector DB backends

v0.3 (If traction — W9-W16)
├── L3  Taint analysis (pysa/CodeQL)       ⬜ Definitive isolation proof
├── L6  Symbolic interpretation            ⬜ Only if FP rate > 15%
└── L7  Runtime instrumentation            ⬜ --dynamic mode
```

---

## 5. Detection Matrix

How each layer contributes to each rule:

| Rule | L0 | L1 | L2 | L3 | L4 | L5 | L6 | L7 | L8 |
|---|---|---|---|---|---|---|---|---|---|
| AW-MEM-001 (no tenant isolation) | — | Detect | Confirm | Prove | — | Detect | Path-split | Runtime-confirm | Score confidence |
| AW-MEM-002 (weak isolation) | — | — | — | Detect | — | — | Detect | Runtime-confirm | Score confidence |
| AW-MEM-003 (no access control) | — | Detect | — | — | Detect | Detect | — | Runtime-confirm | — |
| AW-MEM-004 (unsafe defaults) | — | — | — | — | Detect | Detect | — | — | — |
| AW-MEM-005 (no encryption) | — | — | — | — | Detect | Detect | — | — | — |

**Legend:**
- **Detect** = can find the issue
- **Confirm** = can verify L1's finding by tracing cross-file
- **Prove** = provides definitive evidence (data flow from source to sink)
- **Score confidence** = reduces false positives by semantic judgment

---

## 6. Benchmark Suite

To measure each layer's impact, maintain a benchmark of known-vulnerable and known-safe repos:

| Repo | Stars | Framework | Expected Findings | Use |
|---|---|---|---|---|
| Langchain-Chatchat | 37K | LangChain | 6 (3 CRITICAL, 3 HIGH) | True positive validation |
| Long-Trainer | — | LangChain | 5 (2 CRITICAL, 3 HIGH) | True positive validation |
| vulnerable-rag-app (fixture) | — | LangChain | 2 (1 CRITICAL, 1 HIGH) | Regression test |
| LangChain official templates | — | LangChain | 0 (properly filtered) | False positive test |
| Private-GPT | 55K | LangChain | TBD | Real-world calibration |
| Quivr | 36K | LangChain | TBD | Real-world calibration |

**Metrics per layer:**
- True Positive Rate (TPR): findings that are real bugs
- False Positive Rate (FPR): findings that are not bugs
- Scan time delta: overhead added by the layer
- Unique findings: bugs found *only* by this layer

---

## 7. Non-Functional Requirements (Layer-Specific)

| NFR | Target |
|---|---|
| L2 call graph build time (50K LOC) | < 10 seconds |
| L3 taint analysis time (50K LOC) | < 60 seconds |
| L4 config scan time | < 2 seconds |
| L5 Semgrep scan time (50K LOC) | < 30 seconds |
| L8 LLM scoring per finding (local) | < 5 seconds |
| L8 LLM scoring per finding (API) | < 3 seconds |
| Total scan time (L0-L5, 50K LOC) | < 90 seconds |
| Memory overhead per layer | < 100 MB additional |

---

## 8. Dependencies

| Layer | Required Dependency | Optional | Install |
|---|---|---|---|
| L0–L1 | Python stdlib (`ast`, `re`) | — | Built-in |
| L2 | — | `jedi` (post-MVP) | `pip install agentwall[callgraph]` |
| L3 | — | `pysa` or `codeql` | External install |
| L4 | `pyyaml`, `tomllib` (stdlib 3.11+) | `python-dotenv` | `pip install agentwall[config]` |
| L5 | — | `semgrep` | `pip install agentwall[semgrep]` |
| L6 | — | `z3-solver` | `pip install agentwall[symbolic]` |
| L7 | Target app's deps | — | N/A (runtime) |
| L8 | — | `ollama`, `anthropic` | `pip install agentwall[llm]` |

**Core package (`pip install agentwall`) includes L0, L1, L2 (custom resolver), L4 (YAML/TOML only). Everything else is optional extras.**

---

*End of document.*
