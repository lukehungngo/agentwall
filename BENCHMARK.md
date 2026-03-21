# AgentWall Benchmark Report

**Date:** 2026-03-21
**Version:** 0.1.0 (Phase 1 complete)
**Layers enabled:** L0–L6 (default static analysis)
**Reproduce:** `./scripts/benchmark.sh`

---

## 1. Tier 1 — Established Projects (>2k stars)

| # | Project | Stars | Files | Findings | CRIT | HIGH | MED | LOW | Top Rules |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Langchain-Chatchat | ~37k | 239 | 50 | 12 | 28 | 9 | 1 | AW-MEM-001(15), AW-RAG-001(10), AW-SEC-001(6) |
| 2 | PrivateGPT | ~54k | 65 | 4 | 0 | 3 | 1 | 0 | AW-RAG-004(2), AW-SEC-001(1), AW-SEC-003(1) |
| 3 | Quivr | ~36k | 41 | 7 | 0 | 2 | 3 | 2 | AW-RAG-001(2), AW-RAG-003(2), AW-MEM-001(2) |
| 4 | LocalGPT | ~22k | 44 | 2 | 0 | 0 | 2 | 0 | AW-SEC-003(2) |
| 5 | DocsGPT | ~15k | 208 | 24 | 3 | 11 | 9 | 1 | AW-RAG-003(5), AW-MEM-001(4), AW-SEC-001(3) |
| 6 | GPT-Researcher | ~17k | 167 | 7 | 2 | 3 | 1 | 1 | AW-MEM-001(2), AW-RAG-001(2), AW-SER-001(1) |
| 7 | Onyx/Danswer | ~12k | 1420 | 23 | 0 | 12 | 9 | 2 | AW-SER-001(9), AW-SER-003(7), AW-TOOL-004(2) |
| 8 | DB-GPT | ~17k | 1004 | 18 | 0 | 0 | 18 | 0 | AW-SEC-003(11), AW-SER-003(7) |
| 9 | Chat-LangChain | ~6k | 11 | 0 | 0 | 0 | 0 | 0 | — |
| 10 | RasaGPT | ~2.4k | 11 | 0 | 0 | 0 | 0 | 0 | — |
| 11 | Langflow | ~48k | 1274 | 97 | 19 | 36 | 38 | 4 | AW-SER-003(25), AW-MEM-001(21), AW-RAG-001(11) |
| 12 | Flowise | ~35k | 0 | 0 | 0 | 0 | 0 | 0 | — |
| 13 | Open Interpreter | ~58k | 136 | 6 | 0 | 1 | 5 | 0 | AW-SER-003(5), AW-SER-001(1) |
| 14 | Chainlit | ~8k | 121 | 4 | 0 | 2 | 2 | 0 | AW-SER-003(2), AW-SEC-001(1), AW-SER-001(1) |
| 15 | Mem0/Embedchain | ~25k | 374 | 16 | 2 | 8 | 5 | 1 | AW-RAG-001(3), AW-SER-003(3), AW-MEM-001(2) |
| 16 | LLM App (Pathway) | ~4k | 17 | 0 | 0 | 0 | 0 | 0 | — |
| 17 | Haystack | ~18k | 296 | 3 | 0 | 1 | 2 | 0 | AW-SER-003(2), AW-SER-001(1) |
| 18 | SuperAgent | ~5k | 22 | 0 | 0 | 0 | 0 | 0 | — |
| 19 | AgentGPT | ~32k | 85 | 1 | 0 | 0 | 1 | 0 | AW-SER-003(1) |
| 20 | AutoGPT | ~172k | 918 | 8 | 0 | 5 | 3 | 0 | AW-SEC-001(4), AW-SER-003(3), AW-SER-001(1) |

**Totals: 270 findings (38 CRITICAL, 112 HIGH) across 6453 files. 15/20 have findings.**

---

## 2. Tier 2 — Small Projects (<500 stars)

| # | Project | Stars | Files | Findings | CRIT | HIGH | MED | LOW | Top Rules |
|---|---|---|---|---|---|---|---|---|---|
| 1 | memory-agent | 416 | 7 | 0 | 0 | 0 | 0 | 0 | — |
| 2 | rag-research-agent-template | 295 | 17 | 1 | 0 | 1 | 0 | 0 | AW-RAG-001(1) |
| 3 | langchain-chatbot | 273 | 9 | 9 | 0 | 7 | 0 | 2 | AW-MEM-004(4), AW-RAG-001(2), AW-MEM-001(2) |
| 4 | chat-with-websites | 260 | 1 | 1 | 0 | 0 | 0 | 1 | AW-MEM-001(1) |
| 5 | cohere-qdrant-doc-retrieval | 152 | 1 | 5 | 1 | 3 | 1 | 0 | AW-MEM-001(2), AW-RAG-001(1), AW-MEM-003(1) |
| 6 | RAG-chatbot-langchain | 133 | 1 | 8 | 0 | 3 | 3 | 2 | AW-MEM-004(2), AW-RAG-003(2), AW-MEM-001(2) |
| 7 | langchain-RAG-chroma | 8 | 1 | 7 | 1 | 3 | 2 | 1 | AW-MEM-001(2), AW-RAG-001(1), AW-AGT-004(1) |
| 8 | chat-with-pdf | 2 | 1 | 2 | 0 | 0 | 2 | 0 | AW-RAG-003(2) |
| 9 | langchain-multi-agent | 10 | 1 | 5 | 0 | 3 | 1 | 1 | AW-AGT-001(2), AW-RAG-001(1), AW-TOOL-002(1) |
| 10 | objectbox-rag | 10 | 3 | 0 | 0 | 0 | 0 | 0 | — |

**Totals: 38 findings (2 CRITICAL, 20 HIGH) across 42 files. 8/10 have findings.**

### Tier Comparison

| Metric | Tier 1 (>2k stars) | Tier 2 (<500 stars) |
|---|---|---|
| Projects with findings | 15/20 (75%) | 8/10 (80%) |
| Findings per file | 270 / 6453 = **0.042** | 38 / 42 = **0.905** |
| CRITICAL rate | 38/270 = **14%** | 2/38 = **5%** |

---

## 3. Rule Distribution

| Rule | Count | % | Description |
|---|---|---|---|
| AW-SER-003 | 59 | 19% | AW-SER-003 |
| AW-MEM-001 | 56 | 18% | No tenant isolation in vector store |
| AW-RAG-001 | 38 | 12% | AW-RAG-001 |
| AW-RAG-003 | 25 | 8% | AW-RAG-003 |
| AW-SER-001 | 21 | 7% | AW-SER-001 |
| AW-MEM-003 | 21 | 7% | Memory backend has no access control |
| AW-SEC-001 | 18 | 6% | AW-SEC-001 |
| AW-SEC-003 | 18 | 6% | AW-SEC-003 |
| AW-TOOL-004 | 10 | 3% | Tool has no description |
| AW-MEM-005 | 9 | 3% | No sanitization on retrieved memory |
| AW-AGT-001 | 6 | 2% | AW-AGT-001 |
| AW-MEM-004 | 6 | 2% | Injection patterns in retrieval path |
| AW-RAG-004 | 5 | 2% | AW-RAG-004 |
| AW-MEM-002 | 4 | 1% | Shared collection without retrieval filter |
| AW-CFG-docker-no-auth | 3 | 1% | AW-CFG-docker-no-auth |
| AW-MCP-002 | 2 | 1% | AW-MCP-002 |
| AW-MCP-001 | 2 | 1% | AW-MCP-001 |
| AW-TOOL-001 | 1 | 0% | Destructive tool without approval gate |
| AW-TOOL-003 | 1 | 0% | High-risk tool lacks scope check |
| AW-AGT-004 | 1 | 0% | AW-AGT-004 |
| AW-SER-002 | 1 | 0% | AW-SER-002 |
| AW-TOOL-002 | 1 | 0% | Tool accepts arbitrary code execution |

---

## 4. Attack Vector Coverage (10 / 32 Detectable)

| Category | Detected | Total | Coverage |
|---|---|---|---|
| **MEM** — Memory Isolation | 4 | 4 | 100% |
| **POI** — Data Poisoning | 0 | 6 | 0% |
| **EMB** — Embedding Attacks | 0 | 5 | 0% |
| **INJ** — Prompt Injection | 1 | 3 | 33% |
| **EXF** — Exfiltration | 0 | 3 | 0% |
| **CFG** — Configuration | 3 | 6 | 50% |
| **DOS** — Denial of Service | 0 | 3 | 0% |
| **AGT** — Agentic Attacks | 1 | 5 | 20% |

### Attack Vectors Confirmed in Real-World Projects

| Attack Vector | Description | Projects Affected | Hits | Example Evidence |
|---|---|---|---|---|
| **AW-ATK-AGT-001** | Tool Poisoning / Unsafe Tool Access | Langflow, langchain-multi-agent | 3 | `apify_actor.py:139` (AW-TOOL-001) |
| **AW-ATK-CFG-003** | No TLS / No Auth / Exposed Ports | DocsGPT, Langflow, Onyx/Danswer | 3 | `docker-compose.yaml:59` (AW-CFG-docker-no-auth) |
| **AW-ATK-INJ-001** | Stored Prompt Injection | DocsGPT, Langchain-Chatchat, Langflow, RAG-chatbot-langchain, cohere-qdrant-doc-retrieval, langchain-RAG-chroma | 9 | `chromadb_kb_service.py:67` (AW-MEM-005) |
| **AW-ATK-MEM-001** | Cross-Tenant Retrieval (No Filter) | DocsGPT, GPT-Researcher, Langchain-Chatchat, Langflow, Mem0/Embedchain, Quivr, RAG-chatbot-langchain, chat-with-websites, cohere-qdrant-doc-retrieval, langchain-RAG-chroma, langchain-chatbot, langchain-multi-agent | 56 | `milvus_kb_service.py:100` (AW-MEM-001) |
| **AW-ATK-MEM-002** | Weak Tenant Isolation (Static Filter) | DocsGPT, Langchain-Chatchat, Langflow | 4 | `ensemble.py:27` (AW-MEM-002) |
| **AW-ATK-MEM-003** | Namespace/Collection Confusion | DocsGPT, Langchain-Chatchat, Langflow, Mem0/Embedchain, Onyx/Danswer, RAG-chatbot-langchain, cohere-qdrant-doc-retrieval, langchain-RAG-chroma | 21 | `chromadb_kb_service.py:67` (AW-MEM-003) |
| **AW-ATK-MEM-004** | Partition Bypass via Direct API | RAG-chatbot-langchain, langchain-chatbot | 6 | `2_⭐_context_aware_chatbot.py:21` (AW-MEM-004) |

### Vectors Not Detected (22 / 32)

| Vector | Description | Reason |
|---|---|---|
| AW-ATK-AGT-002 | Delegation Chain Escalation | Requires multi-agent delegation graph |
| AW-ATK-AGT-003 | Memory-Mediated Identity Hijacking | Requires agent identity redefinition detection |
| AW-ATK-AGT-004 | Cross-Agent Memory Contamination | Requires multi-agent shared memory provenance |
| AW-ATK-AGT-005 | Conversation History Replay | Requires session management analysis |
| AW-ATK-CFG-002 | No Encryption at Rest | Requires vector DB config schema inspection |
| AW-ATK-CFG-005 | Missing RBAC | Requires vector DB RBAC/ACL audit |
| AW-ATK-CFG-006 | No Row-Level Security | Requires PostgreSQL RLS policy inspection |
| AW-ATK-DOS-001 | Embedding Flood | Requires rate-limit config audit |
| AW-ATK-DOS-002 | Query Amplification | Requires parameter bounds checking |
| AW-ATK-DOS-003 | Collection Deletion via Admin | Requires admin endpoint auth audit |
| AW-ATK-EMB-001 | Vector Collision Attack | Requires embedding model invocation |
| AW-ATK-EMB-002 | Semantic Cache Poisoning | Requires semantic cache identification |
| AW-ATK-EMB-003 | Embedding Inversion | Requires embedding model + inversion validation |
| AW-ATK-EMB-004 | Adversarial Multi-Modal Embedding | Requires multi-modal model analysis |
| AW-ATK-EMB-005 | Vector Drift | Requires embedding lifecycle tracking |
| AW-ATK-EXF-001 | Membership Inference | Requires runtime: membership inference |
| AW-ATK-EXF-002 | Embedding Exfiltration via API | Requires runtime: embedding extraction |
| AW-ATK-EXF-003 | Timing Side-Channel | Requires runtime: timing measurement |
| AW-ATK-INJ-002 | Cross-Session Context Hijacking | Requires session identity tracking |
| AW-ATK-INJ-003 | EchoLeak | Requires action execution tracing |
| AW-ATK-POI-001 | PoisonedRAG | Requires runtime: inject docs, measure ranking |
| AW-ATK-POI-002 | CorruptRAG | Requires runtime: single-doc injection |
| AW-ATK-POI-003 | MINJA | Requires runtime: query-only memory injection |
| AW-ATK-POI-004 | Persistent Memory Poisoning | Requires runtime: time-delayed session analysis |
| AW-ATK-POI-005 | Document Loader Exploitation | Requires binary analysis: PDF/DOCX hidden content |
| AW-ATK-POI-006 | Training Data Backdoor | Requires tracking memory→fine-tuning pipeline |

---

## 5. Attack Vector Heatmap (Per Project)

| Project | AGT-001 | CFG-001 | CFG-003 | CFG-004 | INJ-001 | MEM-001 | MEM-002 | MEM-003 | MEM-004 | Total |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Langchain-Chatchat | · | · | · | · | **3** | **15** | **2** | **3** | · | 23 |
| PrivateGPT | · | · | · | · | · | · | · | · | · | 0 |
| Quivr | · | · | · | · | · | **2** | · | · | · | 2 |
| LocalGPT | · | · | · | · | · | · | · | · | · | 0 |
| DocsGPT | · | · | **1** | · | **1** | **4** | **1** | **1** | · | 8 |
| GPT-Researcher | · | · | · | · | · | **2** | · | · | · | 2 |
| Onyx/Danswer | · | · | **1** | · | · | · | · | **1** | · | 2 |
| DB-GPT | · | · | · | · | · | · | · | · | · | 0 |
| Chat-LangChain | · | · | · | · | · | · | · | · | · | 0 |
| RasaGPT | · | · | · | · | · | · | · | · | · | 0 |
| Langflow | **2** | · | **1** | · | **2** | **21** | **1** | **11** | · | 38 |
| Flowise | · | · | · | · | · | · | · | · | · | 0 |
| Open Interpreter | · | · | · | · | · | · | · | · | · | 0 |
| Chainlit | · | · | · | · | · | · | · | · | · | 0 |
| Mem0/Embedchain | · | · | · | · | · | **2** | · | **2** | · | 4 |
| LLM App (Pathway) | · | · | · | · | · | · | · | · | · | 0 |
| Haystack | · | · | · | · | · | · | · | · | · | 0 |
| SuperAgent | · | · | · | · | · | · | · | · | · | 0 |
| AgentGPT | · | · | · | · | · | · | · | · | · | 0 |
| AutoGPT | · | · | · | · | · | · | · | · | · | 0 |
| memory-agent | · | · | · | · | · | · | · | · | · | 0 |
| rag-research-agent-template | · | · | · | · | · | · | · | · | · | 0 |
| langchain-chatbot | · | · | · | · | · | **2** | · | · | **4** | 6 |
| chat-with-websites | · | · | · | · | · | **1** | · | · | · | 1 |
| cohere-qdrant-doc-retrieval | · | · | · | · | **1** | **2** | · | **1** | · | 4 |
| RAG-chatbot-langchain | · | · | · | · | **1** | **2** | · | **1** | **2** | 6 |
| langchain-RAG-chroma | · | · | · | · | **1** | **2** | · | **1** | · | 4 |
| chat-with-pdf | · | · | · | · | · | · | · | · | · | 0 |
| langchain-multi-agent | **1** | · | · | · | · | **1** | · | · | · | 2 |
| objectbox-rag | · | · | · | · | · | · | · | · | · | 0 |

*Legend: number = findings count, · = not detected, — = not scanned*

---

## 6. How to Reproduce

```bash
pip install -e ".[dev]"
./scripts/benchmark.sh
```
