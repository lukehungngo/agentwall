# AgentWall Architecture Refactor Proposal

**Author:** Claude (reviewer) for SoH Engineering
**Date:** 2026-03-19
**Status:** Proposal — requires owner review
**Scope:** Internal restructuring. Zero feature changes. All 316 tests must pass after.

---

## 1. Problem Statement

The current codebase shipped fast (48 hours) and works. But it has structural problems that will block v1.0:

**You cannot add a new framework adapter without modifying scanner.py.**
**You cannot add a new analysis layer without modifying scanner.py.**
**You cannot add a new rule without modifying an analyzer class.**
**Three analyzers duplicate the same constant definitions.**
**L2, L3, and L6 cannot share intermediate results.**

These are not opinions. They are measurable violations.

---

## 2. Violations Found

### V1: scanner.py violates SRP

`scanner.py` (255 lines) does 6 things:

1. Framework detection dispatch (line 141–148)
2. Layer orchestration with hardcoded if/else per layer (line 150–242)
3. ASM conditional logic (line 209–222)
4. Finding deduplication (line 87–114)
5. File context classification (line 42–77)
6. Finding sorting (line 80–84)

Each is a separate responsibility. When you add L9, you modify the orchestrator. When you change dedup logic, you modify the orchestrator. One file, six reasons to change.

### V2: Analyzer signatures violate ISP

Every analyzer has a different signature:

```python
MemoryAnalyzer.analyze(spec: AgentSpec) -> list[Finding]
ToolAnalyzer.analyze(spec: AgentSpec) -> list[Finding]
CallGraphAnalyzer.analyze(spec: AgentSpec, l1_findings: list[Finding], target: Path) -> list[Finding]
TaintAnalyzer.analyze(spec: AgentSpec) -> list[Finding]
ConfigAuditor.analyze(target: Path) -> list[Finding]
SemgrepAnalyzer.analyze(target: Path) -> list[Finding]
SymbolicAnalyzer.analyze(spec: AgentSpec) -> list[Finding]
ASMAnalyzer.analyze(model: ApplicationModel) -> list[Finding]
```

8 analyzers, 4 different signatures. scanner.py must know the exact signature of each one. Adding a new analyzer requires editing scanner.py to call it with the right arguments.

### V3: Constants duplicated 3x (DRY violation)

`_RETRIEVAL_METHODS` is defined identically in:
- `analyzers/callgraph.py` line 26–33
- `analyzers/taint.py` line 51–58 (as `_SINK_METHODS` keys)
- `analyzers/symbolic.py` line 29–36

`_FILTER_KWARGS` is defined identically in:
- `analyzers/callgraph.py` line 37
- `analyzers/symbolic.py` line 39

Add a new retrieval method (e.g., `hybrid_search`) → edit 3 files. Miss one → silent detection gap.

### V4: L2→L3→L6 are disconnected (the critical gap)

**L2** builds a `CallGraph` but only uses it internally to refine L1 findings. The call graph is discarded after L2 returns.

**L3** re-parses all source files from scratch. It performs per-file taint analysis only. It cannot trace taint across function calls because it has no call graph.

**L6** re-parses all source files from scratch. It checks filter presence on code paths but cannot check if the filter VALUE is tainted. It has no access to L3's taint results.

In the textbook SAST pipeline, these compose:

```
L2 builds graph → L3 traces taint OVER the graph → L6 checks taint on ALL PATHS
```

Right now they run independently and their results are merged by dedup at the end. This means:

- **Cross-file taint is undetected.** If `user_id` enters in `routes.py` and reaches `similarity_search` in `db.py` through a chain of function calls, L3 cannot see it. It only tracks taint within a single file.

- **Path-sensitive taint is undetected.** If `filter=` exists on all paths but contains `user_id` on only some paths, L6 reports "filtered on all paths" (false negative). It should report "filter exists but is not user-scoped on all paths."

### V5: Adapter does detection work (misplaced responsibility)

`langchain.py` (the adapter) is 400+ lines. It does AST walking, pattern detection, and populates boolean flags like `has_metadata_filter_on_retrieval`, `has_tenant_isolation`, `sanitizes_retrieved_content`. It also builds the entire `ApplicationModel` with entry points, stores, edges.

`memory.py` (the L1 analyzer) is 86 lines. It just checks the boolean flags the adapter already computed.

The actual detection logic lives in the adapter, not the analyzer. This means:
- Adding a rule that checks a new AST pattern → modify the adapter (add a new boolean flag) AND the analyzer (check the flag). Two files for one change.
- Adding a new framework adapter → reimplement all the detection logic. The rules aren't reusable across adapters.

### V6: scanner.py violates OCP

Adding any of these requires modifying `scanner.py`:

- New analysis layer → add `if "LX" in layers:` block
- New framework → add `if detected == "crewai":` branch
- New post-processing step → add code after finalize section
- Change layer ordering → rearrange hardcoded blocks

The scanner is closed for extension. Every change opens it for modification.

---

## 3. What I Am NOT Proposing

- **No rewrite.** The logic inside each analyzer stays identical.
- **No new features.** This is restructuring, not adding capabilities.
- **No new dependencies.** Zero new packages.
- **No Bandit-style plugin system with stevedore/entry_points.** That's over-engineering for 10 rules. Save it for when you have 50+ community-contributed rules.
- **No OCaml engine like Semgrep.** You're one person building a Python tool.
- **No framework changes.** Pydantic, dataclass, ast — all stay.

---

## 4. Proposed Changes

### Change 1: Extract shared patterns

**Create:** `src/agentwall/patterns.py`

Move ALL detection constants here. Single source of truth.

```
FROM                              TO
─────────────────────────         ──────────────────────
callgraph.py:_RETRIEVAL_METHODS   patterns.py:RETRIEVAL_METHODS
callgraph.py:_FILTER_KWARGS       patterns.py:FILTER_KWARGS
taint.py:_SOURCE_PATTERNS         patterns.py:SOURCE_PATTERNS
taint.py:_SINK_METHODS            patterns.py:SINK_METHODS
taint.py:_SIMPLE_SOURCE_NAMES     patterns.py:SIMPLE_SOURCE_NAMES
symbolic.py:_RETRIEVAL_METHODS    (delete — import from patterns)
symbolic.py:_FILTER_KWARGS        (delete — import from patterns)
langchain.py:_SANITIZE_NAMES      patterns.py:SANITIZE_NAMES
langchain.py:_DESTRUCTIVE_KEYWORDS patterns.py:DESTRUCTIVE_KEYWORDS
langchain.py:_CODE_EXEC_CALLS     patterns.py:CODE_EXEC_CALLS
```

**Impact:** 3 analyzers + 1 adapter change imports. Zero logic change.

**Test risk:** None. Same values, different import path.

### Change 2: Unified analyzer interface via AnalysisContext

**Create:** `src/agentwall/context.py`

```python
@dataclass
class AnalysisContext:
    """Shared mutable state that flows through the analysis pipeline."""
    target: Path
    config: ScanConfig
    spec: AgentSpec | None = None
    call_graph: CallGraph | None = None
    taint_results: list[TaintResult] | None = None
    findings: list[Finding] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
```

**Update every analyzer** to accept `AnalysisContext` as its sole argument:

```python
# BEFORE (8 different signatures)
class CallGraphAnalyzer:
    def analyze(self, spec: AgentSpec, l1_findings: list[Finding], target: Path) -> list[Finding]: ...

# AFTER (1 signature)
class CallGraphAnalyzer:
    name = "L2"
    depends_on = ["L1"]

    def analyze(self, ctx: AnalysisContext) -> list[Finding]:
        # read what you need from ctx
        # write what you produce to ctx
        ctx.call_graph = build_call_graph(ctx.target, ctx.spec.source_files)
        return self._refine_findings(ctx)
```

**The contract:** Every analyzer reads from `ctx`, may write to `ctx`, returns `list[Finding]`.

**Impact:** Every analyzer file changes its method signature. Internal logic stays identical — just replace `spec` with `ctx.spec`, `target` with `ctx.target`, etc.

**Test risk:** Medium. Tests that call analyzers directly will need signature updates. But the assertion logic stays the same.

### Change 3: Wire L2→L3→L6 through context

This is the precision improvement. Three specific changes:

**L2 writes call_graph to context:**
```python
def analyze(self, ctx: AnalysisContext) -> list[Finding]:
    ctx.call_graph = build_call_graph(ctx.target, ctx.spec.source_files)
    return self._refine_findings(ctx)
```

**L3 reads call_graph from context:**
```python
def analyze(self, ctx: AnalysisContext) -> list[Finding]:
    graph = ctx.call_graph  # None if L2 didn't run — graceful fallback
    results = self._trace_taint(ctx.spec, graph)
    ctx.taint_results = results
    return self._findings_from_results(results)
```

For v0.x, L3 can still do per-file taint when `call_graph` is None. When call_graph is available, it traces taint across call edges. This is backwards compatible.

**L6 reads taint_results from context:**
```python
def analyze(self, ctx: AnalysisContext) -> list[Finding]:
    taint = ctx.taint_results  # None if L3 didn't run
    return self._path_sensitive_check(ctx.spec, taint)
```

For v0.x, L6 still does filter-presence checking when taint is None. When taint is available, it additionally checks if the filter VALUE is tainted on all paths.

**Impact:** L3 and L6 internal logic needs new code paths that use the shared data. This is the only place where logic actually changes.

**Test risk:** High for L3/L6. Need new test cases for cross-file taint and taint-aware path analysis. Existing tests should still pass since the fallback behavior is identical.

### Change 4: Make scanner generic

**Rewrite `scanner.py`** from hardcoded if/else to registry-driven:

```python
# Registry of all analyzers with dependency metadata
ANALYZERS: list[type[Analyzer]] = [
    FrameworkDetector,   # L0, depends_on=[]
    ASTAnalyzer,         # L1, depends_on=["L0"]
    CallGraphAnalyzer,   # L2, depends_on=["L1"]
    TaintAnalyzer,       # L3, depends_on=["L2"]
    ConfigAuditor,       # L4, depends_on=[]
    SemgrepAnalyzer,     # L5, depends_on=[]
    SymbolicAnalyzer,    # L6, depends_on=["L3"]
    ASMAnalyzer,         # ASM, depends_on=["L1"]
    RuntimeAnalyzer,     # L7, depends_on=["L1"], opt_in=True
    ConfidenceScorer,    # L8, depends_on=[], opt_in=True
]

def scan(target: Path, config: ScanConfig) -> ScanResult:
    ctx = AnalysisContext(target=target, config=config)

    for analyzer_cls in _resolve_order(ANALYZERS, config.layers):
        try:
            findings = analyzer_cls().analyze(ctx)
            ctx.findings.extend(findings)
        except Exception as exc:
            ctx.errors.append(f"{analyzer_cls.name}: {exc}")
            warnings.warn(f"{analyzer_cls.name} failed: {exc}")

    return _finalize(ctx)
```

**`_resolve_order`** topologically sorts analyzers by `depends_on`, filters by `config.layers`, handles opt-in layers.

**Impact:** scanner.py goes from 255 lines of hardcoded orchestration to ~80 lines of generic pipeline. Adding a new analyzer = adding one entry to `ANALYZERS` list.

**Test risk:** Medium. `test_scanner.py` tests the scan function's output, not its internals. If outputs match, tests pass.

### Change 5: Extract post-processing into separate module

**Create:** `src/agentwall/postprocess.py`

Move from scanner.py:
- `_dedup_findings()` → `postprocess.dedup()`
- `_apply_file_context()` → `postprocess.apply_file_context()`
- `_sort_findings()` → `postprocess.sort()`
- `_classify_file_context()` → `postprocess._classify_file_context()`

**Impact:** scanner.py imports from postprocess instead of defining locally. Zero logic change.

**Test risk:** None.

---

## 5. What This Does NOT Address (Deliberately)

| Deferred | Why |
|---|---|
| Rule registry with decorator pattern | You have 10 rules. Not worth the abstraction yet. When you hit 30+, revisit. |
| Adapter refactor to separate detection from parsing | Major change. The adapter works. Defer to v1.0 when you add CrewAI/OpenAI adapters. |
| Cross-file taint implementation in L3 | Change 3 wires the context. Actually using the call graph for cross-file taint is a separate PR with new test fixtures. This proposal makes it POSSIBLE, not implemented. |
| Taint-aware path analysis in L6 | Same — this proposal wires the data. Using it is a separate PR. |

---

## 6. New Directory Structure (delta only)

```
src/agentwall/
├── patterns.py          # NEW — shared detection constants
├── context.py           # NEW — AnalysisContext dataclass
├── postprocess.py       # NEW — dedup, file_context, sort
├── scanner.py           # MODIFIED — generic pipeline (~80 lines, down from 255)
├── models.py            # UNCHANGED
├── rules.py             # UNCHANGED
├── analyzers/
│   ├── memory.py        # MODIFIED — signature only (ctx instead of spec)
│   ├── tools.py         # MODIFIED — signature only
│   ├── callgraph.py     # MODIFIED — signature + writes ctx.call_graph
│   ├── taint.py         # MODIFIED — signature + reads ctx.call_graph + writes ctx.taint_results
│   ├── config.py        # MODIFIED — signature only
│   ├── semgrep.py       # MODIFIED — signature only
│   ├── symbolic.py      # MODIFIED — signature + reads ctx.taint_results
│   ├── confidence.py    # MODIFIED — signature only
│   └── asm.py           # MODIFIED — signature only
└── (everything else UNCHANGED)
```

**3 new files. 0 deleted files. 10 modified files. 0 logic changes except in scanner.py.**

---

## 7. Execution Order

| Step | Files Touched | Risk | Time |
|---|---|---|---|
| 1. Create `patterns.py`, update imports in 4 files | 5 files | Zero — same values | 30 min |
| 2. Create `context.py` with `AnalysisContext` | 1 new file | Zero — new code | 15 min |
| 3. Create `postprocess.py`, move 4 functions from scanner | 2 files | Zero — move only | 20 min |
| 4. Update analyzer signatures to use `ctx` | 9 files | Medium — test signatures change | 2 hours |
| 5. Rewrite scanner.py as generic pipeline | 1 file | High — core orchestration | 1 hour |
| 6. Wire L2→L3 context passing (call_graph) | 2 files | Medium — new data flow | 1 hour |
| 7. Wire L3→L6 context passing (taint_results) | 2 files | Medium — new data flow | 30 min |
| 8. Run all tests, fix breakages | test files | — | 1 hour |

**Total: ~6 hours. One focused session.**

Steps 1–3 are zero-risk preparation. Step 4 is mechanical. Step 5 is the structural change. Steps 6–7 are the precision improvement. Step 8 is validation.

If anything goes wrong, each step is independently revertible.

---

## 8. Success Criteria

After this refactor:

1. **All 316 tests pass.** Non-negotiable.
2. **scanner.py has zero analyzer-specific imports.** It imports from the registry.
3. **No constant is defined in more than one file.**
4. **Every analyzer has the same method signature:** `analyze(self, ctx: AnalysisContext) -> list[Finding]`
5. **Adding a new analyzer requires exactly 1 new file + 1 registry entry.** Zero modification to scanner.py.
6. **L3 can optionally read L2's call graph.** Falls back to per-file taint when L2 didn't run.
7. **L6 can optionally read L3's taint results.** Falls back to filter-presence checking when L3 didn't run.
8. **`ruff check` clean. `mypy --strict` clean.**

---

## 9. What This Enables for v1.0

| v1.0 Feature | How This Helps |
|---|---|
| New framework adapter (CrewAI) | Adapter produces same `AgentSpec` → all analyzers work automatically |
| New analysis layer (e.g., dependency scan) | One file implementing `Analyzer` + one registry entry |
| Cross-file taint (L3 enhancement) | Context already carries call_graph — just use it |
| Taint-aware path analysis (L6 enhancement) | Context already carries taint_results — just use it |
| Community rules | Clear separation: rule definition in `rules/`, detection logic in `analyzers/` |

---

*End of proposal.*
