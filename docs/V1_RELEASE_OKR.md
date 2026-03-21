# AgentWall v1.0 Release OKRs

**Date:** 2026-03-21
**Status:** In Progress
**Gate:** Do not release until all KRs marked REQUIRED are met

---

## Current State Assessment (2026-03-21, post-BENCHMARK3000 full re-run)

| Dimension          | Reality                                                      | Production Standard            | Gap          |
| ------------------ | ------------------------------------------------------------ | ------------------------------ | ------------ |
| Framework adapters | **6 (LangChain, LlamaIndex, CrewAI, OpenAI Agents, AutoGen, vectorstore_direct)** | 5+ with deep analysis | **Done**     |
| FP rate            | **~28% estimated** (manual triage on 5 rules, 15% est. for rest) | <15%                       | **NOT MET**  |
| Engine integration | IsolationEvidence drives MEM findings                        | Engine drives all findings     | **Done**     |
| Detection coverage | **380/480 projects get findings (79%)**                      | >85%                           | Medium       |
| Zero-finding rate  | **21% overall** (100 zero-finding)                           | <10% for vector-store projects | Medium       |
| CI/CD              | **action.yml created, SARIF upload**                         | GitHub Action + SARIF upload   | **Done**     |
| Documentation      | **README updated, docs/rules.md, CLI explain/rules**         | Full docs                      | **Done**     |
| Test coverage      | **85% (808 tests)**                                          | >85%                           | **Done**     |
| Code quality       | **0 ruff, 0 mypy errors**                                    | ruff clean, mypy strict        | **Done**     |

### BENCHMARK3000 Results (486 projects, 2026-03-21, fresh re-run)

| Metric                 | Value                                            |
| ---------------------- | ------------------------------------------------ |
| Projects registered    | 486                                              |
| Projects scanned       | 480                                              |
| Projects with findings | 380 (79%)                                        |
| Total files scanned    | 48,618                                           |
| Total findings         | 3,679                                            |
| CRITICAL               | 139                                              |
| HIGH                   | 1,900                                            |
| Estimated FP rate      | **~28%** (~1,037 est. FP, manual triage + 15% est.) |

### FP Rate by Rule (manual triage where available)

| Rule                    | Count | Sampled | TP | FP | FP%        | Status                                |
| ----------------------- | ----- | ------- | -- | -- | ---------- | ------------------------------------- |
| AW-MEM-001              | 323   | 13      | 0  | 13 | **100%**   | Scanning library code, not user code  |
| AW-MEM-005              | 95    | 9       | 2  | 7  | **78%**    | Needs retrieval-to-sink path evidence |
| AW-CFG-hardcoded-secret | 70    | 16      | 4  | 12 | **75%**    | Needs template/placeholder filtering  |
| AW-SEC-003              | 124   | 30      | 14 | 16 | **53%**    | Too broad on DEBUG logging detection  |
| AW-SER-003              | 227   | 30      | 16 | 14 | **47%**    | 4 heuristics added, needs re-triage   |
| AW-MEM-003              | 539   | —       | —  | —  | ~15% est.  | Not triaged                           |
| AW-TOOL-002             | 396   | —       | —  | —  | ~15% est.  | Not triaged                           |
| AW-TOOL-004             | 287   | —       | —  | —  | ~15% est.  | Not triaged                           |
| All others              | 1,618 | —       | —  | —  | ~15% est.  | Not triaged                           |

**Note:** Previous OKR version used path-based FP estimation (only flagging findings in test/example/docs paths). That method reported "0.0% FP" for MEM-001 and "3.2% overall" — both misleading. Manual triage is the ground truth.

### Framework Detection & Adapter Coverage (349 projects)

| Framework          | Detected | Has Adapter | Gets Full Analysis       | Zero-Finding |
| ------------------ | -------- | ----------- | ------------------------ | ------------ |
| LangChain          | ~120     | **Yes**     | Yes                      | 15           |
| LlamaIndex         | ~60      | **Yes**     | Yes                      | 22           |
| CrewAI             | ~80      | **Yes**     | Yes                      | 41           |
| OpenAI Agents      | ~15      | No          | No (agnostic rules only) | ~12          |
| AutoGen            | ~5       | No          | No                       | ~3           |
| Pydantic AI        | ~3       | No          | No                       | ~2           |
| vectorstore_direct | ~10      | No          | No                       | ~8           |
| Undetected         | ~56      | No          | No                       | ~30+         |

### Architecture Gap: Why 97 Projects Get Zero Findings

**Root cause:** When no adapter matches, only 5 of 16 analyzers run (framework-agnostic ones).

| Category                 | Agnostic? | Rules                    | Status                                                                   |
| ------------------------ | --------- | ------------------------ | ------------------------------------------------------------------------ |
| VersionsAnalyzer         | Yes       | L0 dependency checks     | Runs always                                                              |
| SecretsAnalyzer          | Yes       | SEC-001, SEC-003         | Runs always                                                              |
| SerializationAnalyzer    | Yes       | SER-001, SER-003         | Runs always                                                              |
| MCPSecurityAnalyzer      | Yes       | MCP-001, MCP-002         | Runs always                                                              |
| ConfigAuditor            | Yes       | CFG-\*                   | Runs always                                                              |
| **RAGAnalyzer**          | **No**    | **RAG-001 to RAG-004**   | **Skipped** — only uses `ctx.source_files`, no `ctx.spec` needed         |
| **AgentArchAnalyzer**    | **No**    | **AGT-001 to AGT-004**   | **Skipped** — only uses `ctx.source_files`, no `ctx.spec` needed         |
| **MemoryAnalyzer**       | **No**    | **MEM-001 to MEM-005**   | **Skipped** — reads `ctx.spec.memory_configs`, needs adapter or fallback |
| **ToolAnalyzer**         | **No**    | **TOOL-001 to TOOL-005** | **Skipped** — reads `ctx.spec.tools`, needs adapter or fallback          |
| CallGraphAnalyzer        | No        | L2 flow                  | Skipped — depends on L1-memory, L1-tools                                 |
| TaintAnalyzer            | No        | L3 taint                 | Skipped — depends on L2                                                  |
| SymbolicAnalyzer         | No        | L6 symbolic              | Skipped — depends on L3                                                  |
| ASMAnalyzer              | No        | ASM engine               | Skipped — depends on L2                                                  |
| ConfidenceScorerAnalyzer | No        | L8 scoring               | Skipped — post-processing                                                |

**97 zero-finding projects break down as:**

| Category                              | Count   | Reason                              | Action                           |
| ------------------------------------- | ------- | ----------------------------------- | -------------------------------- |
| No Python files (JS/TS only)          | 10      | Expected — Python-only scanner      | None                             |
| Tiny (<3 .py files)                   | 12      | Too small                           | None                             |
| Small (3-10 .py)                      | 24      | Minimal code                        | None                             |
| Medium (11-50 .py) — no relevant code | ~20     | Pure orchestration                  | None                             |
| **Medium with relevant code**         | **~14** | **Adapter-dependent rules skipped** | **Make agnostic**                |
| **Large (50+ .py) — missed**          | **17**  | **Scanner blind without adapter**   | **Make agnostic + new adapters** |

---

## Objective 1: Make Findings Trustworthy (FP < 15%) — NOT MET

**Why first:** Nobody adopts a scanner that cries wolf.

| KR    | Metric                       | Before | After (manual triage)      | Target   | Required | Status                                          |
| ----- | ---------------------------- | ------ | -------------------------- | -------- | -------- | ----------------------------------------------- |
| KR1.1 | MEM-001 FP rate              | 100%   | **100%** (13/13 sampled)   | <20%     | Yes      | **NOT MET** — scanning library code, not user code |
| KR1.2 | SEC-003 FP rate              | 53%    | **53%** (16/30 sampled)    | <20%     | Yes      | **NOT MET** — too broad on DEBUG logging        |
| KR1.3 | CFG-hardcoded-secret FP rate | 75%    | **75%** (12/16 sampled)    | <15%     | Yes      | **NOT MET** — needs template/placeholder filter |
| KR1.4 | SER-003 FP rate              | 47%    | **47%** (14/30 sampled)    | <25%     | Yes      | **NOT MET** — 4 heuristics added but not re-triaged |
| KR1.5 | Overall FP rate              | ~35%   | **~28%** (1037/3679 est.)  | <15%     | Yes      | **NOT MET** — MEM-001 alone is 323 FPs          |
| KR1.6 | Engine drives findings       | None   | IsolationEvidence primary  | 100% MEM | Yes      | **Done**                                        |

**Correction note (2026-03-21):** Previous version of this OKR claimed KR1.1–KR1.5 were "Done" using path-based FP estimation (only counting findings in test/example/docs paths as FP). That methodology is misleading — a finding in production code can still be a false positive. Manual triage of actual source code is the ground truth. The real numbers above come from the manual triage in BENCHMARK3000.md Section 20.

### Top FP Offenders (fix priority for O1)

1. **MEM-001** (323 findings, 100% FP) — flagging vectorstore usage in library source code as "no tenant isolation". Need to skip library dirs or require multi-tenant evidence.
2. **MEM-005** (95 findings, 78% FP) — flagging any retrieval without sanitization. Need retrieval-to-sink path evidence.
3. **CFG-hardcoded-secret** (70 findings, 75% FP) — matching templates, placeholders, and non-secret config values.
4. **SEC-003** (124 findings, 53% FP) — too broad on DEBUG-level logging detection.
5. **SER-003** (227 findings, 47% FP) — 4 AST heuristics were added but triage was done before the fix. Needs re-triage.

---

## Objective 2: Scan Everything — Framework-Agnostic Rules + Universal Coverage

**Why:** 97 projects (28%) get zero findings. 17 large projects with 50+ Python files and real vector store / memory / tool patterns are completely invisible. The scanner must produce findings for any Python AI project, not just LangChain/LlamaIndex/CrewAI.

**Strategy:** Two-pronged approach:

1. Make analyzers framework-agnostic where they genuinely don't need `ctx.spec`
2. Add adapters for all detected-but-unsupported frameworks

### Step 2A: Make Analyzers Framework-Agnostic

| KR     | Analyzer          | Rules                | Current                      | Change                                                                                                                                        | Required | Status          |
| ------ | ----------------- | -------------------- | ---------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- | -------- | --------------- |
| KR2A.1 | RAGAnalyzer       | RAG-001 to RAG-004   | `framework_agnostic = True` | Flipped boolean — only uses `ctx.source_files`, zero `ctx.spec` references | Yes      | **Done** — 2 tests added, RAG findings fire on all projects |
| KR2A.2 | AgentArchAnalyzer | AGT-001 to AGT-004   | `framework_agnostic = True` | Flipped boolean — only uses `ctx.source_files`, zero `ctx.spec` references | Yes      | **Done** — 2 tests added, AGT findings fire on all projects |
| KR2A.3 | MemoryAnalyzer    | MEM-001 to MEM-005   | `framework_agnostic = True` | AST fallback: scans imports for chromadb/faiss/pinecone/qdrant/milvus/weaviate, builds synthetic MemoryConfig. Also falls back when adapter returns empty configs. | Yes      | **Done** — 6 tests, MEM-001/003 fire on raw vectorstore projects |
| KR2A.4 | ToolAnalyzer      | TOOL-001 to TOOL-005 | `framework_agnostic = True` | AST fallback: detects @tool decorators, exec/eval/compile/subprocess calls, builds synthetic ToolSpec. Also falls back when adapter returns empty tools. | Yes      | **Done** — 6 tests, TOOL-001/002 fire on projects with dangerous patterns |
| KR2A.5 | CallGraphAnalyzer | L2 flow              | `framework_agnostic = False` | Set `True` — can build call graph from `ctx.source_files` alone when `spec` absent | No       | **Not Started** |

**Impact achieved:** 291/345 projects now get findings (was 247). Zero-finding dropped from 97 → 54 (-43). Total findings: 6,571 (was 2,001). TOOL-002 and TOOL-004 dominate new findings — genuine exec/eval/subprocess patterns detected across all projects.

### Step 2B: New Framework Adapters

| KR     | Framework          | Projects Detected | Stars (top project) | How                                                                                                                                                   | Required | Status          |
| ------ | ------------------ | ----------------- | ------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- | -------- | --------------- |
| KR2B.1 | OpenAI Agents SDK  | ~15               | 7k                  | `adapters/openai_agents.py`: 200 LOC, 13 tests. Detects Agent(), Runner.run(), @function_tool, handoffs. | Yes      | **Done** |
| KR2B.2 | AutoGen            | ~5                | 48k                 | `adapters/autogen.py`: 200 LOC, 14 tests. Detects ConversableAgent, AssistantAgent, register_for_llm/execution. | Yes      | **Done** |
| KR2B.3 | Pydantic AI        | ~3                | 15k                 | Detection added (KR2C.1). Adapter not yet needed — agnostic rules cover it. | No       | **Deferred** |
| KR2B.4 | vectorstore_direct | ~10               | varies              | `adapters/vectorstore_direct.py`: 200 LOC, 13 tests. Detects raw chromadb/faiss/pinecone/qdrant/milvus/weaviate SDK usage. | Yes      | **Done** |

### Step 2C: Expand Framework Detection

| KR     | Target                    | How                                                                   | Required | Status          |
| ------ | ------------------------- | --------------------------------------------------------------------- | -------- | --------------- |
| KR2C.1 | Pydantic AI detection     | Added to `_FRAMEWORK_SIGNATURES` + test | Yes      | **Done** |
| KR2C.2 | GraphRAG detection        | Added to `_FRAMEWORK_SIGNATURES` + test | No       | **Done** |
| KR2C.3 | DSPy detection            | Added to `_FRAMEWORK_SIGNATURES` + test | No       | **Done** |
| KR2C.4 | Semantic Kernel detection | Added to `_FRAMEWORK_SIGNATURES` + test | No       | **Done** |

### Step 2D: Previously Completed

| KR     | Status   | Notes                                                   |
| ------ | -------- | ------------------------------------------------------- |
| KR2D.1 | **Done** | LlamaIndex adapter — 17 tests, fixture gets 12 findings |
| KR2D.2 | **Done** | CrewAI adapter — 14 tests, fixture gets 5 findings      |
| KR2D.3 | **Done** | LlamaIndex + vectorstore_direct detection added         |

### Zero-Finding Rate Targets

| Metric                               | Current      | Target      | How                                                         |
| ------------------------------------ | ------------ | ----------- | ----------------------------------------------------------- |
| Overall zero-finding rate            | **16% (54/345)** (was 28%) | <15%        | KR2A done. Need 2B+2C for last ~9 projects |
| Vector-store project zero-finding    | ~5% (was ~12%) | <5%         | KR2A.3 fallback covers most. Near target. |
| Large project (50+ .py) zero-finding | ~5 projects (was 17) | <5 projects | KR2A + empty-spec fallback covered most |
| Benchmark projects with findings     | **291/345** (was 247/344) | 300+/344    | Need 9 more from STEP 3 adapters |

---

## Objective 3: Ship CI/CD Integration

**Why:** "Run in CI or it doesn't exist" for production teams.

| KR    | Metric           | Current            | Target                      | How                                                                       | Required | Status          |
| ----- | ---------------- | ------------------ | --------------------------- | ------------------------------------------------------------------------- | -------- | --------------- |
| KR3.1 | GitHub Action    | None               | Published to marketplace    | `action.yml`: composite action, install agentwall, run scan, upload SARIF | Yes      | **Done** |
| KR3.2 | PR comment       | None               | Findings diff in PR         | Action posts comment with new/resolved findings vs base branch            | No       | **Not Started** |
| KR3.3 | Quality gate     | `--fail-on` exists | Documented in Action README | Already implemented. Documented in `action.yml` header comment.           | Yes      | **Done** |
| KR3.4 | Incremental scan | None               | <30s on PR diff             | `--changed-files` flag — only scan files in git diff                      | No       | **Not Started** |

### GitHub Action Design

```yaml
# .github/workflows/agentwall.yml
name: AgentWall Security Scan
on: [push, pull_request]
jobs:
  scan:
    runs-on: ubuntu-latest
    permissions:
      security-events: write   # required for SARIF upload
    steps:
      - uses: actions/checkout@v4
      - uses: agentwall/scan-action@v1
        with:
          path: '.'
          format: sarif
          fail-on: high          # critical|high|medium|low|none
          upload-sarif: 'true'   # posts findings to GitHub Security tab
```

---

## Objective 4: Documentation for Adoption

| KR    | Metric              | Current                                                    | Target                             | How                                                                        | Required | Status          |
| ----- | ------------------- | ---------------------------------------------------------- | ---------------------------------- | -------------------------------------------------------------------------- | -------- | --------------- |
| KR4.1 | README              | **Updated: 781+ tests, 85%, 6 frameworks** | Install → scan → fix in <2 minutes | Correct badges, framework table, no "Planned" markers | Yes      | **Done** |
| KR4.2 | Rule reference      | **`docs/rules.md` — 26 rules** | Every rule documented              | Generated from `rules.py` with severity, category, description, fix | Yes      | **Done** |
| KR4.3 | Getting started     | None                                                       | 3 workflows                        | Local dev, CI pipeline, AI agent integration                               | No       | **Not Started** |
| KR4.4 | `agentwall explain` | **CLI command implemented** | CLI command | `agentwall explain AW-MEM-001` prints description, severity, fix guidance | No       | **Done** |
| KR4.5 | `agentwall rules`   | **CLI command implemented** | CLI command | Lists all 26 rules grouped by category with severity | No       | **Done** |

---

## Objective 5: Quality Bar

| KR    | Metric               | Current                      | Target                                                      | How                                                                         | Required | Status                                               |
| ----- | -------------------- | ---------------------------- | ----------------------------------------------------------- | --------------------------------------------------------------------------- | -------- | ---------------------------------------------------- |
| KR5.1 | Test coverage        | **85% (735 tests)**          | >85%                                                        | Added CrewAI framework model tests + coverage from new analyzer tests       | Yes      | **Done** — 84.56% → 85%                             |
| KR5.2 | Code quality         | **0 ruff, 0 mypy**           | ruff clean, mypy strict                                     | Fixed SIM102, I001, F401, installed PyYAML stubs, fixed type annotations    | Yes      | **Done** — all clean                                 |
| KR5.3 | Benchmark regression | **18 labeled regression tests** | Zero TP lost between versions                            | 18 tests covering 12 rules, run on every pytest execution                   | Yes      | **Done** — `test_regression_labeled.py`              |
| KR5.4 | Performance          | ~10s                         | <30s on any project <100k LOC                               | Profile Langflow scan (1274 files, currently 10s)                           | Yes      | **Done** — already meets target                      |
| KR5.5 | Package              | **4 package tests + CI build** | `pip install agentwall && agentwall scan .` works first try | Import, scan, CLI help, fixture scan — all verified                       | Yes      | **Done** — `test_package.py` + CI build step         |
| KR5.6 | CI matrix            | **3.10/3.11/3.12**           | 3.10 / 3.11 / 3.12 matrix                                   | Added strategy.matrix to ci.yml                                             | Yes      | **Done**                                             |
| KR5.7 | Publish workflow     | **`publish.yml` created**    | Tag-triggered PyPI publish                                  | hatch build + pypa/gh-action-pypi-publish on `v*` tags                     | Yes      | **Done**                                             |

---

## Execution Timeline

```
STEP 1: O2A — Framework-Agnostic Rules (HIGHEST IMPACT)
  ├── KR2A.1: RAGAnalyzer → framework_agnostic = True (1 line)
  ├── KR2A.2: AgentArchAnalyzer → framework_agnostic = True (1 line)
  ├── KR2A.3: MemoryAnalyzer AST fallback (~80 LOC)
  ├── KR2A.4: ToolAnalyzer AST fallback (~60 LOC)
  └── Re-run BENCHMARK3000, measure zero-finding reduction

STEP 2: O1 + O5 — SER-003 Fix + Quality
  ├── KR1.4: SER-003 4 heuristics (~40 LOC)
  ├── KR5.1: Coverage 84.36% → 85% (~20 LOC tests)
  ├── KR5.2: Fix ruff + mypy errors
  └── KR5.6: CI matrix 3.10/3.11/3.12

STEP 3: O2B — New Adapters
  ├── KR2B.1: OpenAI Agents adapter (~200 LOC)
  ├── KR2B.2: AutoGen adapter (~200 LOC)
  ├── KR2B.4: vectorstore_direct adapter (~150 LOC)
  ├── KR2C.1-4: Detection expansion
  └── Re-run BENCHMARK3000

STEP 4: O3 + O4 — CI/CD + Docs
  ├── KR3.1: GitHub Action (action.yml)
  ├── KR3.3: Quality gate documentation
  ├── KR4.1: README rewrite
  ├── KR4.2: Rule reference generation
  └── KR4.4-4.5: CLI explain + rules commands

STEP 5: O5 — Package + Launch
  ├── KR5.5: Package verification
  ├── KR5.7: Publish workflow
  ├── KR5.3: Labeled test set
  └── Launch: PyPI + GitHub + blog + HN
```

---

## v1.0 Release Gate

**Do NOT release until ALL of these are true:**

- [ ] FP rate <15% on benchmark — **BLOCKING: currently ~28% (manual triage). MEM-001 alone is 100% FP (323 findings).**
- [x] 3+ frameworks with full analysis (LangChain + LlamaIndex + CrewAI)
- [x] Engine StoreProfile is the primary decision source for MEM rules
- [x] RAG + AGT + MEM + TOOL rules fire on any Python project (framework-agnostic) — 380/480 projects get findings
- [x] 6 frameworks with adapters (LangChain, LlamaIndex, CrewAI, OpenAI Agents, AutoGen, vectorstore_direct)
- [x] 380 of 480 benchmark projects get findings (79%)
- [ ] SER-003 FP rate <25% — **BLOCKING: currently 47% (14/30 sampled FP). Heuristics added but not verified.**
- [x] GitHub Action created (`action.yml`)
- [x] README quickstart updated with correct badges and framework table
- [x] Every rule has description, severity, fix guidance (CLI `explain` + `docs/rules.md`)
- [x] `pip install agentwall && agentwall scan . --format sarif` verified in tests + CI
- [x] 808 tests passing, 85% coverage, ruff clean, mypy strict
- [x] CI runs on Python 3.10 / 3.11 / 3.12
- [ ] No known P0 issues — **BLOCKING: MEM-001 100% FP is a P0 trust issue**

---

## What Success Looks Like

**STEP 1 complete:** A developer scans _any_ Python AI project — Pydantic AI, GraphRAG, OpenAI Agents, custom RAG pipeline — and gets memory isolation, RAG injection, and tool security findings. Zero "framework not supported" messages for Python projects with vector stores.

**STEP 2 complete:** SER-003 drops from 17% to <5% FP. Coverage hits 85%. CI matrix catches Python 3.10 regressions.

**STEP 3 complete:** OpenAI Agents SDK, AutoGen, and raw vectorstore projects get full deep analysis with dedicated adapters. 300+ of 349 benchmark projects produce findings.

**STEP 4 complete:** Developer adds AgentWall to GitHub Actions. Every PR shows a security diff. SARIF findings appear in the Security tab. `agentwall explain AW-MEM-001` prints actionable fix guidance.

**STEP 5 complete:** `pip install agentwall` on a fresh machine. README gets them scanning in 90 seconds. Blog post on Hacker News. First external issue filed.

## Propose Solution

V1 OKR Solution — 5 Steps, Prioritized by Impact

STEP 1: Framework-Agnostic Rules (highest ROI, ~2 hours)

4 changes that unlock findings for 97 zero-finding projects:

┌───────────────────────────────────────────┬────────┬───────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Change │ Effort │ Impact │
├───────────────────────────────────────────┼────────┼───────────────────────────────────────────────────────────────────────────────────────────────────┤
│ rag.py:30 → framework_agnostic = True │ 1 line │ RAG-001–004 fire on all projects │
├───────────────────────────────────────────┼────────┼───────────────────────────────────────────────────────────────────────────────────────────────────┤
│ agent_arch.py:22 → framework_agnostic = │ 1 line │ AGT-001–004 fire on all projects │
│ True │ │ │
├───────────────────────────────────────────┼────────┼───────────────────────────────────────────────────────────────────────────────────────────────────┤
│ memory.py:57 → framework_agnostic = True │ ~80 │ MEM rules fire without adapter — scan source files for similarity_search, Chroma(, FAISS(, │
│ + AST fallback │ LOC │ Pinecone(, build synthetic MemoryConfig objects │
├───────────────────────────────────────────┼────────┼───────────────────────────────────────────────────────────────────────────────────────────────────┤
│ tools.py:54 → framework_agnostic = True + │ ~60 │ TOOL rules fire without adapter — detect @tool decorators, exec()/eval()/subprocess in functions, │
│ AST fallback │ LOC │ build synthetic ToolSpec objects │
└───────────────────────────────────────────┴────────┴───────────────────────────────────────────────────────────────────────────────────────────────────┘

RAG + AGT are trivial — they already iterate ctx.source_files and never touch ctx.spec. Just flip the boolean.

MEM + TOOL need AST fallbacks — when ctx.spec is None, scan source files directly:

- MemoryAnalyzer: Walk AST for Chroma(, FAISS(, Pinecone(, Qdrant(, similarity_search() calls. Build MemoryConfig(backend="chroma", ...) from call-site info.
  Existing \_check() logic runs unchanged.
- ToolAnalyzer: Walk AST for @tool decorated functions, functions containing exec()/eval()/subprocess.run(). Build ToolSpec(name=func_name, ...). Existing
  \_check_tool() runs unchanged.

Expected result: Zero-finding rate drops from 28% to ~10-12%.

---

STEP 2: SER-003 FP Fix + Quality Bar (~2 hours)

KR1.4 — 4 AST heuristics in serialization.py (~40 LOC):

1. \_is_fstring_with_constant_prefix() — suppress f"myapp.backends.{name}"
2. \_is_config_attribute_import() — suppress settings.BACKEND_CLASS
3. \_is_try_except_guarded() — suppress guarded imports
4. \_is_constant_format_call() — suppress "module.{}".format(name)

KR5.1 — Coverage 84.36% → 85%: Add tests for crewai.py (0% covered, 3 lines) + CLI stdout paths.

KR5.2 — Fix 2 ruff errors (SIM102, import sort) + 5 mypy errors (yaml/tomli stubs, type mismatches).

KR5.6 — CI matrix: Add strategy.matrix.python-version: [3.10, 3.11, 3.12] to ci.yml.

---

STEP 3: New Adapters (~4 hours)

KR2B.1 — OpenAI Agents (adapters/openai_agents.py, ~200 LOC):

- Detect Agent(), Runner.run(), tool functions, handoffs
- Extract tools from agent.tools and @function_tool decorators
- Map to AgentSpec with memory configs from any vectorstore usage

KR2B.2 — AutoGen (adapters/autogen.py, ~200 LOC):

- Detect ConversableAgent, AssistantAgent, register_function, initiate_chat
- Extract tools from register_function() calls

KR2B.4 — vectorstore_direct (adapters/vectorstore_direct.py, ~150 LOC):

- Raw chromadb/pinecone/qdrant SDK usage without framework wrapper
- Extract store instances, collection names, query patterns

KR2C.1-4 — Detection expansion in detector.py:

- Add pydantic_ai, graphrag, dspy, semantic_kernel to \_FRAMEWORK_SIGNATURES

Expected result: 300+ of 349 benchmark projects produce findings.

---

STEP 4: CI/CD + Docs (~3 hours)

KR3.1 — GitHub Action (action.yml):

- Composite action: install agentwall, run scan, upload SARIF
- --format sarif output → github/codeql-action/upload-sarif

KR4.1 — README rewrite: Correct badges (708 tests, 84%), framework table, quickstart.

KR4.2 — Rule reference: Generate from rules.py — each rule gets description, severity, example, fix.

KR4.4-4.5 — CLI commands:

- agentwall explain AW-MEM-001 — prints rule description, fix, OWASP mapping
- agentwall rules — lists all rules with severity and category

---

STEP 5: Package + Launch (~2 hours)

KR5.5 — End-to-end package test in CI (pip install . && agentwall scan tests/fixtures/)
KR5.7 — Publish workflow (publish.yml: hatch build + publish on tag push)
KR5.3 — Create 100-finding labeled test set from benchmark data
Launch — PyPI release, update README badges to point to live package

---

Recommendation

Start with STEP 1 — it's the highest-impact change with the least risk. RAG + AGT are literally 2 one-line boolean flips. MEM + TOOL fallbacks are
self-contained ~140 LOC total.

Want me to create a detailed implementation plan and start executing? I'd use the writing-plans skill to produce a full TDD plan, then execute with
subagent-driven-development.
