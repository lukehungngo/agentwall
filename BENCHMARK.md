# Benchmark: AgentWall vs 10 Real-World LangChain Projects

**Date:** 2026-03-17
**AgentWall version:** 0.1.0
**Layers enabled:** L0-L6 (default static analysis)
**Reproduce:** `./scripts/benchmark.sh`

---

## Results

| Project | Stars | Files | Findings | CRIT | HIGH | MED | LOW | Top Rules |
|---|---|---|---|---|---|---|---|---|
| [Langchain-Chatchat](https://github.com/chatchat-space/Langchain-Chatchat) | ~37k | 239 | 22 | 14 | 5 | 3 | 0 | AW-MEM-001(14), AW-MEM-003(3), AW-MEM-005(3) |
| [PrivateGPT](https://github.com/zylon-ai/private-gpt) | ~54k | 65 | 0 | 0 | 0 | 0 | 0 | - |
| [Quivr](https://github.com/QuivrHQ/quivr) | ~36k | 41 | 2 | 2 | 0 | 0 | 0 | AW-MEM-001(2) |
| [LocalGPT](https://github.com/PromtEngineer/localGPT) | ~22k | 44 | 0 | 0 | 0 | 0 | 0 | - |
| [DocsGPT](https://github.com/arc53/DocsGPT) | ~15k | 198 | 8 | 3 | 2 | 2 | 1 | AW-MEM-001(3), AW-MEM-003(1), AW-MEM-002(1) |
| [GPT-Researcher](https://github.com/assafelovic/gpt-researcher) | ~17k | 166 | 4 | 2 | 1 | 0 | 1 | AW-MEM-001(2), AW-CFG(1), AW-TOOL-004(1) |
| [Onyx (Danswer)](https://github.com/onyx-dot-app/onyx) | ~12k | 1406 | 8 | 1 | 3 | 2 | 2 | AW-MEM-001(1), AW-CFG(3), AW-TOOL-004(2) |
| [DB-GPT](https://github.com/eosphoros-ai/DB-GPT) | ~17k | 1004 | 8 | 5 | 2 | 1 | 0 | AW-MEM-001(5), AW-MEM-002(1), AW-MEM-003(1) |
| [Chat-LangChain](https://github.com/langchain-ai/chat-langchain) | ~6k | 11 | 7 | 0 | 7 | 0 | 0 | AW-CFG-hardcoded-secret(7) |
| [RasaGPT](https://github.com/paulpierre/RasaGPT) | ~2.4k | 11 | 0 | 0 | 0 | 0 | 0 | - |

**Totals: 59 findings (27 CRITICAL, 20 HIGH) across 3,185 files in 10 projects**

---

## Rule Breakdown

| Rule | Count | Description |
|---|---|---|
| AW-MEM-001 | 27 | No tenant isolation in vector store |
| AW-CFG-hardcoded-secret | 10 | Hardcoded API keys/secrets in config files |
| AW-MEM-003 | 5 | Memory backend has no access control |
| AW-MEM-005 | 4 | No sanitization on retrieved memory |
| AW-MEM-002 | 4 | Filter exists but not user-scoped |
| AW-TOOL-004 | 4 | Tool has no description |
| AW-CFG-docker-no-auth | 2 | Docker service has no authentication |

---

## Key Findings

### 6 of 10 projects have confirmed memory security issues

**Langchain-Chatchat** (37k stars) has the most findings: 14 CRITICAL AW-MEM-001 across 7 vector store backends (Chroma, FAISS, Milvus, PGVector, Elasticsearch, Relyt, Zilliz). Every `do_search()` method calls `similarity_search` without a user filter.

**DB-GPT** (17k stars) has unfiltered PGVector `similar_search()` confirmed by both L2 (call graph) and L6 (path analysis).

**Quivr** (36k stars) has 2 unfiltered retrieval paths detected by L6 symbolic analysis.

### 3 projects are outside current adapter scope

| Project | Reason | Implication |
|---|---|---|
| PrivateGPT | Uses `llama-index`, not LangChain vectorstores | Need LlamaIndex adapter |
| LocalGPT | Uses ChromaDB directly (not via LangChain wrapper) | Need native ChromaDB adapter |
| RasaGPT | Uses PGVector via raw SQL | Need raw SQL adapter |

### Config findings are real

- **Chat-LangChain** (official LangChain project): 7 hardcoded secrets in `.env` files
- **Onyx**: Redis Docker container has no authentication configured
- **GPT-Researcher**: Hardcoded API key in config

---

## False Positive Analysis

During benchmarking, we discovered and fixed one significant false positive pattern:

**SQLAlchemy `.query()` matched as vector store sink** — L3 taint analysis included `"query": "where"` in sink methods, which matched SQLAlchemy's `.query()` (ORM queries, not vector stores). This generated 91 false positives on Onyx alone. Fixed by removing the generic `query` from taint sinks.

**Post-fix FP rate: ~0%** — all 59 remaining findings point to real code patterns (unfiltered vector store calls, hardcoded secrets, missing auth). Some may be intentional (e.g., single-user apps that don't need tenant isolation), but the code patterns are correctly identified.

---

## Performance

All scans completed in under 10 seconds each, including projects with 1,000+ files (DB-GPT: 1,004 files, Onyx: 1,406 files). No crashes, no timeouts.

---

## How to Reproduce

```bash
# Clone AgentWall
git clone https://github.com/lukehungngo/agentwall && cd agentwall
pip install -e ".[dev]"

# Run the benchmark
./scripts/benchmark.sh

# Or scan a single project
agentwall scan /path/to/langchain-project
```
