# Analysis Layers

AgentWall uses 9 analysis layers that form a progressive refinement funnel — each layer adds precision and catches what the previous layer structurally cannot. Early layers are cheap and fast; later layers are expensive but powerful.

| Layer | Technique | What it does |
|---|---|---|
| **L0** | Regex / Import Matching | Framework detection |
| **L1** | Single-File AST | Kwarg inspection for filters, tools, permissions |
| **L2** | Inter-Procedural Call Graph | Cross-file filter resolution via call chains |
| **L3** | Taint Analysis | Tracks user identity from request entry to filter sink |
| **L4** | Config Auditing | Scans .env, docker-compose, settings.py for insecure defaults |
| **L5** | Semgrep Rules | Declarative pattern matching (requires `semgrep` binary) |
| **L6** | Symbolic Analysis | Path-sensitive: detects filters missing on some branches |
| **L7** | Runtime Instrumentation | Monkey-patches vector stores during test runs (`--dynamic`) |
| **L8** | LLM Confidence Scoring | Reduces false positives via regex/Ollama/API (`--llm-assist`) |

---

## Layer-by-Layer Breakdown

### L0 — Regex / Import Matching (Framework detection)

The cheapest possible pass. Before doing any real analysis, AgentWall identifies what it's looking at by scanning `pyproject.toml`, `requirements.txt`, and top-level imports. This gates which adapter, rules, and downstream layers are activated. No point running LangChain-specific rules against a CrewAI codebase.

```python
# Detects framework from imports or dependencies
import langchain  →  activate langchain adapter + ruleset
```

---

### L1 — Single-File AST (Kwarg inspection)

The core workhorse. Uses Python's `ast` module to parse each file and inspect function call arguments — specifically looking for the dangerous *absence* of kwargs. Operates per-file with no cross-file awareness, which means it has the highest raw false-positive rate in the pipeline. Subsequent layers are designed to prune it.

```python
# L1 flags this — no `filter=` kwarg present
vectorstore.similarity_search(query)

# L1 passes this — filter kwarg exists
vectorstore.similarity_search(query, filter={"user_id": user_id})
```

---

### L2 — Inter-Procedural Call Graph (Cross-file resolution)

L1 misses cases where the filter is passed through a helper function defined in another file. L2 builds a call graph across the entire project to trace whether a filter eventually reaches the vector store sink, dramatically reducing false positives without deeper analysis.

```python
# retriever.py
def search(query, user_id):
    return vectorstore.similarity_search(query, filter={"user_id": user_id})

# agent.py — L1 flags this, L2 resolves it as safe ✅
results = search(user_query, current_user.id)
```

---

### L3 — Taint Analysis (User identity tracking)

Classic taint analysis. Marks `user_id` / `tenant_id` variables as tainted sources at the request boundary (FastAPI path params, JWT claims, headers) and traces whether that value flows into every vector store filter call. This catches cases where a filter exists but doesn't actually scope by the real authenticated user — which L1 and L2 both miss.

```python
user_id = request.headers.get("X-User-Id")  # taint source

# ✅ tainted value flows into filter — safe
vectorstore.similarity_search(query, filter={"user_id": user_id})

# ❌ hardcoded string — not user-scoped, L3 flags this
vectorstore.similarity_search(query, filter={"user_id": "admin"})
```

---

### L4 — Config Auditing (Infrastructure misconfigs)

Orthogonal to code analysis. You can have perfectly filtered queries in code but a misconfigured Chroma instance with no authentication. L4 scans `.env`, `docker-compose.yml`, and `settings.py` for insecure defaults: missing API keys, empty passwords, debug flags in production, and missing TLS configuration.

```bash
# L4 flags these
CHROMA_API_KEY=          # empty auth
POSTGRES_PASSWORD=       # empty password
DEBUG=true               # debug mode on
ALLOW_ANONYMOUS=true     # open access
```

---

### L5 — Semgrep Rules (Declarative pattern matching)

AgentWall ships YAML Semgrep rules as a maintainable, community-contributable layer on top of the Python AST analysis. Rules are readable and auditable without touching Python source. Requires the `semgrep` binary (opt-in).

```yaml
rules:
  - id: AW-MEM-001
    patterns:
      - pattern: $VS.similarity_search($QUERY, ...)
      - pattern-not: $VS.similarity_search($QUERY, ..., filter=..., ...)
    message: Unfiltered vector store query — cross-tenant leakage risk
    languages: [python]
    severity: ERROR
```

---

### L6 — Symbolic Analysis (Branch-conditional gaps)

L1–L5 are largely path-insensitive — they treat all code paths as equivalent. L6 models control flow and detects cases where a filter is applied only on some branches. The most common pattern: filter present in the happy path, absent in the fallback or error branch.

```python
def retrieve(query, user_id=None):
    if user_id:
        # ✅ safe branch
        return vs.similarity_search(query, filter={"user_id": user_id})
    else:
        # ❌ L6 catches this — unfiltered fallback
        return vs.similarity_search(query)
```

---

### L7 — Runtime Instrumentation (opt-in: `--dynamic`)

Shifts from static to dynamic. When you run your test suite with `--dynamic`, AgentWall monkey-patches vector store clients to intercept every actual call at runtime and assert that a filter is present. This catches what static analysis structurally cannot: dynamically constructed kwargs, metaprogramming, conditional imports, and framework-generated retriever chains.

```python
# AgentWall wraps at runtime:
original = Chroma.similarity_search
def patched(self, query, **kwargs):
    if "filter" not in kwargs:
        agentwall.report("AW-MEM-001", caller=inspect.stack())
    return original(self, query, **kwargs)
Chroma.similarity_search = patched
```

---

### L8 — LLM Confidence Scoring (opt-in: `--llm-assist`)

The false-positive reduction layer. Uses a local Ollama model or remote API to re-evaluate borderline findings from L1–L7 and assign a confidence score. Instead of binary flag/no-flag, the model reasons about full context: is this filter semantically equivalent to a user-scoped query? Is the hardcoded value a known-safe system filter? Most expensive layer — one LLM call per borderline finding.

---

## Pipeline Flow

```
Source Code
    │
    ▼
L0  ── Framework detected? ──────────────────────► Activate adapter + ruleset
    │
    ▼
L1  ── Per-file AST ─────────────────────────────► Raw findings (high FP rate)
    │
    ▼
L2  ── Inter-procedural call graph ──────────────► Prune cross-file FPs
    │
    ▼
L3  ── Taint analysis ───────────────────────────► Prune hardcoded-filter FPs
    │
    ▼
L4  ── Config file audit ────────────────────────► New infra-level findings
    │
    ▼
L5  ── Semgrep declarative rules ────────────────► Validate + new pattern hits
    │
    ▼
L6  ── Symbolic / path-sensitive ────────────────► Catch branch-conditional gaps
    │
    ▼
L7* ── Runtime instrumentation ──────────────────► Dynamic validation (--dynamic)
    │
    ▼
L8* ── LLM confidence scoring ───────────────────► Prune remaining FPs (--llm-assist)
    │
    ▼
Final Report  ──────────────────────────────────► Terminal / JSON / SARIF
```

---

## Layer Cost vs. Precision

```
Cost       L0   L1   L2   L3   L4   L5   L6   L7   L8
─────      ──   ──   ──   ──   ──   ──   ──   ──   ──
High                                          ███  ███
Medium                         ██   ██   ███
Low        █    ██   ███  ███

Precision  L0   L1   L2   L3   L4   L5   L6   L7   L8
─────      ──   ──   ──   ──   ──   ──   ──   ──   ──
High                      ███            ███  ███  ███
Medium          ██   ███       ███  ███
Low        █
```

---

## Detection Matrix

Each layer contributes differently to each rule:

| Rule | L1 | L2 | L3 | L4 | L5 | L6 | L7 | L8 |
|---|---|---|---|---|---|---|---|---|
| **AW-MEM-001** (no tenant isolation) | Detect | Confirm | Prove | — | Detect | Path-split | Runtime | Score |
| **AW-MEM-002** (weak isolation) | — | — | Detect | — | — | Detect | Runtime | Score |
| **AW-MEM-003** (no access control) | Detect | — | — | Detect | Detect | — | Runtime | — |
| **AW-MEM-004** (unsafe defaults) | — | — | — | Detect | Detect | — | — | — |
| **AW-MEM-005** (no encryption) | — | — | — | Detect | Detect | — | — | — |

**Legend:** _Detect_ = finds the issue · _Confirm_ = verifies cross-file · _Prove_ = definitive data-flow evidence · _Score_ = reduces false positives via semantic judgment

---

## CLI Usage

```bash
# Default: L0-L6 (all static layers)
agentwall scan .

# Fast mode: L0-L2 only
agentwall scan . --fast

# Pick specific layers
agentwall scan . --layers L1,L3,L6

# Enable runtime instrumentation
agentwall scan . --dynamic

# Enable LLM-assisted confidence scoring
agentwall scan . --llm-assist
```

---

## How It Works

```
agentwall scan ./project/
  │
  ├─ 1. Detect framework    (pyproject.toml, imports)
  ├─ 2. AST parse            (ast.parse — never imports or runs your code)
  ├─ 3. Extract AgentSpec    (tools, vector stores, memory configs)
  ├─ 4. Run analysis layers  (L1-L8, configurable)
  └─ 5. Report               (terminal, JSON, or SARIF)
```

**Key design principles:**

- **Static only** — all analysis via Python `ast` module. Your code is never imported, executed, or modified
- **Zero network calls** — fully offline by default. L7/L8 are opt-in
- **Fail safe** — parse errors on individual files produce a warning and skip. The scan never crashes
- **Conservative** — prefers false negatives over false positives. Findings you see are real
