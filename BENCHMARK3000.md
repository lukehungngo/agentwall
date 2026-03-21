# AgentWall Benchmark 3000

**Date:** 2026-03-21
**Version:** AgentWall v0.1.0
**Layers enabled:** L0–L6 (default static analysis) + V5 engine
**Projects:** 486
**Reproduce:** `./scripts/benchmark3000.sh`

---

## 1. Tier 1 — LangChain Ecosystem (>2k stars)

| # | Project | Stars | Files | Findings | CRIT | HIGH | MED | LOW | Top Rules |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Langchain-Chatchat | ~37k | 239 | 50 | 12 | 28 | 9 | 1 | AW-MEM-001(15), AW-RAG-001(10), AW-SEC-001(6) |
| 2 | PrivateGPT | ~54k | 65 | 4 | 0 | 3 | 1 | 0 | AW-RAG-004(2), AW-SEC-001(1), AW-SEC-003(1) |
| 3 | Quivr | ~36k | 41 | 7 | 0 | 2 | 3 | 2 | AW-RAG-001(2), AW-RAG-003(2), AW-MEM-001(2) |
| 4 | LocalGPT | ~22k | 44 | 2 | 0 | 0 | 2 | 0 | AW-SEC-003(2) |
| 5 | DocsGPT | ~15k | 208 | 22 | 3 | 11 | 7 | 1 | AW-RAG-003(5), AW-MEM-001(4), AW-SEC-001(3) |
| 6 | GPT-Researcher | ~17k | 167 | 7 | 2 | 3 | 1 | 1 | AW-MEM-001(2), AW-RAG-001(2), AW-SER-001(1) |
| 7 | Onyx/Danswer | ~12k | 1420 | 19 | 0 | 12 | 5 | 2 | AW-SER-001(9), AW-SER-003(3), AW-TOOL-004(2) |
| 8 | DB-GPT | ~17k | 1004 | 80 | 1 | 16 | 50 | 13 | AW-TOOL-002(27), AW-TOOL-004(13), AW-SEC-003(11) |
| 9 | Chat-LangChain | ~6k | 11 | 0 | 0 | 0 | 0 | 0 | — |
| 10 | RasaGPT | ~2.4k | 11 | 0 | 0 | 0 | 0 | 0 | — |
| 11 | Langflow | ~48k | 1274 | 87 | 19 | 36 | 28 | 4 | AW-MEM-001(21), AW-SER-003(15), AW-RAG-001(11) |
| 12 | Open Interpreter | ~58k | 136 | 41 | 0 | 1 | 22 | 18 | AW-TOOL-002(22), AW-TOOL-004(18), AW-SER-001(1) |
| 13 | Chainlit | ~8k | 121 | 3 | 0 | 2 | 1 | 0 | AW-SEC-001(1), AW-SER-001(1), AW-SER-003(1) |
| 14 | Mem0/Embedchain | ~48k | 374 | 15 | 2 | 8 | 4 | 1 | AW-RAG-001(3), AW-MEM-001(2), AW-RAG-004(2) |
| 15 | LLM App (Pathway) | ~4k | 17 | 0 | 0 | 0 | 0 | 0 | — |
| 16 | Haystack | ~18k | 296 | 3 | 0 | 1 | 2 | 0 | AW-SER-003(2), AW-SER-001(1) |
| 17 | SuperAgent | ~5k | 22 | 0 | 0 | 0 | 0 | 0 | — |
| 18 | AgentGPT | ~32k | 85 | 1 | 0 | 0 | 1 | 0 | AW-SER-003(1) |
| 19 | AutoGPT | ~172k | 918 | 39 | 0 | 13 | 23 | 3 | AW-TOOL-002(15), AW-TOOL-001(5), AW-TOOL-003(5) |
| 20 | LangGraph | ~45k | 173 | 10 | 0 | 3 | 7 | 0 | AW-SER-003(7), AW-SEC-001(1), AW-SER-001(1) |
| 21 | LangSmith SDK | ~1k | 81 | 1 | 0 | 1 | 0 | 0 | AW-SEC-001(1) |
| 22 | LangChain (mono) | ~100k | 1669 | 38 | 0 | 16 | 5 | 17 | AW-MEM-001(17), AW-AGT-004(4), AW-RAG-001(3) |
| 23 | OpenGPTs | ~6k | 28 | 16 | 0 | 3 | 0 | 13 | AW-TOOL-004(13), AW-CFG-no-tls(1), AW-SER-001(1) |
| 24 | LangServe | ~2k | 13 | 0 | 0 | 0 | 0 | 0 | — |
| 25 | LangChain Extract | ~1k | 20 | 1 | 1 | 0 | 0 | 0 | AW-MEM-001(1) |
| 26 | Awesome LLM Apps | ~60k | 444 | 71 | 10 | 55 | 6 | 0 | AW-MEM-001(12), AW-AGT-004(12), AW-MEM-002(10) |

**Totals: 517 findings (50 CRITICAL, 214 HIGH) across 8881 files. 21/26 have findings.**

---

## 2. Tier 2 — LlamaIndex Ecosystem

| # | Project | Stars | Files | Findings | CRIT | HIGH | MED | LOW | Top Rules |
|---|---|---|---|---|---|---|---|---|---|
| 1 | LlamaIndex | ~47k | - | - | - | - | - | - | not scanned |
| 2 | RAGS (LlamaIndex) | ~6k | 15 | 2 | 0 | 1 | 0 | 1 | AW-RAG-001(1), AW-MEM-001(1) |
| 3 | LlamaParse | ~3k | 41 | 1 | 0 | 0 | 0 | 1 | AW-MEM-001(1) |
| 4 | create-llama | ~2k | 172 | 26 | 0 | 21 | 0 | 5 | AW-MEM-003(11), AW-MEM-004(6), AW-RAG-001(3) |
| 5 | SEC Insights | ~2k | 36 | 3 | 0 | 2 | 1 | 0 | AW-RAG-002(1), AW-MEM-003(1), AW-SEC-003(1) |
| 6 | LlamaDeploy | ~2k | 60 | 2 | 0 | 1 | 1 | 0 | AW-CFG-hardcoded-secret(1), AW-SER-003(1) |
| 7 | LlamaIndex.TS | ~3k | 0 | 1 | 0 | 1 | 0 | 0 | AW-CFG-hardcoded-secret(1) |
| 8 | LlamaAgents | ~1k | 60 | 2 | 0 | 1 | 1 | 0 | AW-CFG-hardcoded-secret(1), AW-SER-003(1) |
| 9 | LlamaHub | ~3k | 593 | 108 | 14 | 74 | 19 | 1 | AW-MEM-003(50), AW-MEM-001(30), AW-MEM-005(17) |
| 10 | LlamaLab | ~1k | 26 | 0 | 0 | 0 | 0 | 0 | — |
| 11 | Multi-Agent Concierge | ~500 | 3 | 2 | 0 | 2 | 0 | 0 | AW-MEM-004(1), AW-MEM-003(1) |
| 12 | PR Manager (LlamaIndex) | ~11 | 14 | 0 | 0 | 0 | 0 | 0 | — |

**Totals: 147 findings (14 CRITICAL, 103 HIGH) across 1020 files. 9/12 have findings.**

---

## 3. Tier 3 — Multi-Agent Frameworks

| # | Project | Stars | Files | Findings | CRIT | HIGH | MED | LOW | Top Rules |
|---|---|---|---|---|---|---|---|---|---|
| 1 | CrewAI | ~46k | 752 | 90 | 0 | 14 | 39 | 37 | AW-TOOL-004(37), AW-TOOL-002(25), AW-TOOL-001(7) |
| 2 | AutoGen | ~48k | 406 | 11 | 0 | 6 | 5 | 0 | AW-SER-003(4), AW-SEC-001(3), AW-SER-001(2) |
| 3 | MetaGPT | ~58k | 494 | 39 | 0 | 17 | 15 | 7 | AW-SER-003(9), AW-MEM-003(8), AW-MEM-001(7) |
| 4 | ChatDev | ~25k | 186 | 17 | 0 | 4 | 8 | 5 | AW-TOOL-002(7), AW-TOOL-004(5), AW-SER-001(2) |
| 5 | CAMEL | ~10k | 498 | 74 | 0 | 25 | 48 | 1 | AW-TOOL-002(31), AW-TOOL-001(8), AW-MEM-003(8) |
| 6 | BabyAGI | ~20k | 35 | 6 | 0 | 0 | 3 | 3 | AW-TOOL-002(3), AW-TOOL-004(3) |
| 7 | OpenAI Swarm | ~18k | 6 | 0 | 0 | 0 | 0 | 0 | — |
| 8 | Swarms | ~4k | 215 | 2 | 0 | 1 | 1 | 0 | AW-SER-001(1), AW-SER-002(1) |
| 9 | TaskWeaver | ~5k | 136 | 5 | 0 | 1 | 2 | 2 | AW-MEM-001(2), AW-SER-001(1), AW-SER-003(1) |

**Totals: 244 findings (0 CRITICAL, 68 HIGH) across 2728 files. 8/9 have findings.**

---

## 4. Tier 4 — RAG Applications

| # | Project | Stars | Files | Findings | CRIT | HIGH | MED | LOW | Top Rules |
|---|---|---|---|---|---|---|---|---|---|
| 1 | RAGFlow | ~70k | 463 | 36 | 0 | 22 | 11 | 3 | AW-CFG-hardcoded-secret(10), AW-SEC-001(8), AW-TOOL-002(6) |
| 2 | Kotaemon | ~25k | 232 | 20 | 0 | 15 | 0 | 5 | AW-SER-001(15), AW-TOOL-004(5) |
| 3 | LightRAG | ~30k | 77 | 3 | 0 | 1 | 2 | 0 | AW-RAG-004(1), AW-SEC-003(1), AW-SER-003(1) |
| 4 | FastGPT | ~27k | 16 | 3 | 0 | 1 | 1 | 1 | AW-CFG-hardcoded-secret(1), AW-TOOL-002(1), AW-TOOL-004(1) |
| 5 | QAnything | ~12k | 148 | 11 | 0 | 7 | 4 | 0 | AW-SER-001(5), AW-RAG-003(3), AW-RAG-001(2) |
| 6 | R2R | ~4k | 224 | 5 | 0 | 0 | 5 | 0 | AW-TOOL-002(2), AW-SER-003(2), AW-SEC-003(1) |
| 7 | FlashRAG | ~2k | 75 | 12 | 0 | 5 | 5 | 2 | AW-TOOL-002(4), AW-MEM-003(3), AW-SER-001(2) |
| 8 | AutoRAG | ~3k | 177 | 4 | 0 | 3 | 1 | 0 | AW-SER-001(2), AW-RAG-004(1), AW-SER-003(1) |
| 9 | Canopy (Pinecone) | ~3k | 80 | 0 | 0 | 0 | 0 | 0 | — |
| 10 | Verba (Weaviate) | ~6k | 53 | 2 | 0 | 1 | 1 | 0 | AW-RAG-004(1), AW-SER-003(1) |
| 11 | Vanna | ~13k | 262 | 23 | 10 | 9 | 4 | 0 | AW-MEM-001(10), AW-MEM-003(5), AW-MEM-005(3) |
| 12 | Cognita | ~8k | 73 | 5 | 0 | 4 | 1 | 0 | AW-RAG-004(3), AW-RAG-001(1), AW-CFG-docker-no-auth(1) |
| 13 | ChatGPT Retrieval Plugin | ~21k | 30 | 1 | 0 | 0 | 1 | 0 | AW-RAG-003(1) |
| 14 | txtai | ~10k | 261 | 8 | 0 | 5 | 3 | 0 | AW-MEM-003(3), AW-SER-001(2), AW-SER-003(2) |

**Totals: 133 findings (10 CRITICAL, 73 HIGH) across 2171 files. 13/14 have findings.**

---

## 5. Tier 5 — Vector Store Ecosystems

| # | Project | Stars | Files | Findings | CRIT | HIGH | MED | LOW | Top Rules |
|---|---|---|---|---|---|---|---|---|---|
| 1 | ChromaDB | ~17k | 148 | 5 | 0 | 3 | 2 | 0 | AW-SER-003(2), AW-SEC-001(1), AW-SER-001(1) |
| 2 | Milvus Bootcamp | ~2k | 78 | 10 | 1 | 6 | 3 | 0 | AW-SER-001(5), AW-CFG-docker-no-auth(3), AW-MEM-001(1) |
| 3 | Qdrant Examples | ~500 | 4 | 4 | 0 | 4 | 0 | 0 | AW-MEM-003(4) |
| 4 | LanceDB | ~5k | 71 | 4 | 0 | 0 | 3 | 1 | AW-TOOL-002(2), AW-CFG-debug-mode(1), AW-TOOL-004(1) |

**Totals: 23 findings (1 CRITICAL, 13 HIGH) across 301 files. 4/4 have findings.**

---

## 6. Tier 6 — Memory & Knowledge Systems

| # | Project | Stars | Files | Findings | CRIT | HIGH | MED | LOW | Top Rules |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Cognee | ~12k | 950 | 6 | 0 | 4 | 2 | 0 | AW-MCP-001(2), AW-MEM-003(2), AW-CFG-docker-no-auth(2) |
| 2 | Graphiti (Zep) | ~14k | 178 | 6 | 0 | 6 | 0 | 0 | AW-RAG-001(6) |
| 3 | Letta (MemGPT) | ~22k | 692 | 21 | 0 | 7 | 9 | 5 | AW-SEC-003(6), AW-SER-001(5), AW-TOOL-004(5) |
| 4 | GraphRAG (Microsoft) | ~22k | 444 | 5 | 0 | 5 | 0 | 0 | AW-RAG-001(5) |
| 5 | nano-graphrag | ~5k | 19 | 3 | 0 | 3 | 0 | 0 | AW-CFG-hardcoded-secret(2), AW-SER-001(1) |
| 6 | Zep | ~3k | 19 | 0 | 0 | 0 | 0 | 0 | — |

**Totals: 41 findings (0 CRITICAL, 25 HIGH) across 2302 files. 5/6 have findings.**

---

## 7. Tier 7 — Chatbot / Assistant Frameworks

| # | Project | Stars | Files | Findings | CRIT | HIGH | MED | LOW | Top Rules |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Open WebUI | ~124k | 163 | 8 | 0 | 7 | 0 | 1 | AW-RAG-004(5), AW-RAG-001(1), AW-MEM-003(1) |
| 2 | Khoj | ~33k | 110 | 5 | 0 | 3 | 2 | 0 | AW-SER-001(2), AW-SEC-003(2), AW-SEC-001(1) |
| 3 | PyGPT | ~3k | 1190 | 31 | 0 | 6 | 4 | 21 | AW-TOOL-004(18), AW-SEC-001(5), AW-MEM-001(3) |
| 4 | Jan | ~25k | 5 | 5 | 0 | 0 | 5 | 0 | AW-TOOL-002(5) |

**Totals: 49 findings (0 CRITICAL, 16 HIGH) across 1468 files. 4/4 have findings.**

---

## 8. Tier 8 — Code / Dev Agents

| # | Project | Stars | Files | Findings | CRIT | HIGH | MED | LOW | Top Rules |
|---|---|---|---|---|---|---|---|---|---|
| 1 | OpenHands (OpenDevin) | ~65k | 710 | 30 | 0 | 5 | 19 | 6 | AW-TOOL-002(17), AW-TOOL-004(6), AW-SER-001(5) |
| 2 | SWE-agent | ~15k | 68 | 1 | 0 | 0 | 1 | 0 | AW-SER-003(1) |
| 3 | Aider | ~36k | 90 | 5 | 0 | 2 | 1 | 2 | AW-MEM-001(2), AW-RAG-001(1), AW-MEM-003(1) |
| 4 | Devika | ~18k | 70 | 3 | 0 | 1 | 1 | 1 | AW-SEC-001(1), AW-TOOL-002(1), AW-TOOL-004(1) |
| 5 | GPT-Engineer | ~52k | 43 | 4 | 0 | 0 | 4 | 0 | AW-SEC-003(3), AW-SER-003(1) |
| 6 | GPT-Pilot | ~32k | 94 | 5 | 0 | 5 | 0 | 0 | AW-CFG-hardcoded-secret(5) |

**Totals: 48 findings (0 CRITICAL, 13 HIGH) across 1075 files. 6/6 have findings.**

---

## 9. Tier 9 — Production Agent Platforms

| # | Project | Stars | Files | Findings | CRIT | HIGH | MED | LOW | Top Rules |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Dify | ~129k | 1577 | 24 | 0 | 16 | 7 | 1 | AW-MEM-003(7), AW-RAG-004(4), AW-TOOL-002(3) |
| 2 | Agno (Phidata) | ~19k | 2626 | 81 | 2 | 41 | 37 | 1 | AW-TOOL-002(18), AW-MEM-003(13), AW-TOOL-001(11) |
| 3 | Pydantic AI | ~15k | 236 | 0 | 0 | 0 | 0 | 0 | — |
| 4 | smolagents (HF) | ~26k | 18 | 4 | 0 | 3 | 1 | 0 | AW-SER-001(3), AW-SER-003(1) |
| 5 | Semantic Kernel | ~22k | 923 | 28 | 0 | 26 | 2 | 0 | AW-MEM-003(12), AW-SEC-001(9), AW-RAG-004(3) |
| 6 | OpenAI Agents SDK | ~7k | 165 | 0 | 0 | 0 | 0 | 0 | — |
| 7 | DSPy | ~20k | 140 | 4 | 0 | 0 | 2 | 2 | AW-SEC-003(2), AW-TOOL-004(2) |
| 8 | Google Agent Dev Kit | ~18k | 835 | 28 | 1 | 13 | 11 | 3 | AW-SER-003(9), AW-SEC-001(5), AW-RAG-001(3) |
| 9 | UFO (Microsoft) | ~5k | 291 | 14 | 1 | 2 | 11 | 0 | AW-RAG-003(9), AW-MEM-001(1), AW-RAG-001(1) |
| 10 | AgentOps | ~3k | 303 | 16 | 0 | 9 | 7 | 0 | AW-SEC-001(7), AW-SEC-003(4), AW-SER-003(3) |
| 11 | ModelScope Agent | ~3k | 204 | 9 | 0 | 3 | 6 | 0 | AW-SEC-003(3), AW-SER-003(3), AW-MEM-003(2) |

**Totals: 208 findings (4 CRITICAL, 113 HIGH) across 7318 files. 9/11 have findings.**

---

## 10. Tier 10 — Small / Niche Projects

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
| 11 | AdalFlow | ~3k | 231 | 11 | 0 | 8 | 3 | 0 | AW-SER-001(6), AW-SEC-003(2), AW-SEC-001(1) |
| 12 | Hindsight | ~4k | - | - | - | - | - | - | not scanned |
| 13 | Vector Admin | ~2k | 2 | 0 | 0 | 0 | 0 | 0 | — |
| 14 | HF Agents Course | ~5k | 1 | 0 | 0 | 0 | 0 | 0 | — |
| 15 | Libre Chat | ~500 | 9 | 5 | 0 | 1 | 4 | 0 | AW-RAG-003(2), AW-RAG-001(1), AW-SER-002(1) |
| 16 | LangGraph BigTool | ~500 | 4 | 0 | 0 | 0 | 0 | 0 | — |
| 17 | RAG-Anything | ~1k | 15 | 7 | 0 | 0 | 7 | 0 | AW-TOOL-002(7) |
| 18 | OASIS (CAMEL) | ~2k | 45 | 8 | 0 | 5 | 2 | 1 | AW-SER-001(2), AW-SEC-001(1), AW-RAG-001(1) |
| 19 | SWE-bench | ~4k | 84 | 19 | 0 | 2 | 13 | 4 | AW-TOOL-002(11), AW-TOOL-004(4), AW-TOOL-001(2) |

**Totals: 88 findings (2 CRITICAL, 36 HIGH) across 433 files. 13/19 have findings.**

---

## 11. Grand Summary

| Metric | Value |
|---|---|
| Total projects | 486 |
| Projects scanned | 480 |
| Projects with findings | 380 (79%) |
| Zero-finding projects | 100 (21%) |
| Total findings | 3,679 |
| CRITICAL | 140 |
| HIGH | 1,899 |
| MEDIUM | 1,219 |
| LOW | 290 |
| INFO | 131 |
| Estimated FP rate | **6.4%** (path-based) |
| Estimated real FP | **~8-9%** (incl. source-path FP) |
| Scan timeouts | 1 (llama-index) |

### Category Comparison

| Category | Projects | Scanned | With Findings | Findings | CRIT | HIGH | Files |
|---|---|---|---|---|---|---|---|
| LangChain Ecosystem (>2k stars) | 26 | 26 | 21 | 517 | 50 | 214 | 8,881 |
| LlamaIndex Ecosystem | 12 | 11 | 9 | 147 | 14 | 103 | 1,020 |
| Multi-Agent Frameworks | 9 | 9 | 8 | 244 | 0 | 68 | 2,728 |
| RAG Applications | 14 | 14 | 13 | 133 | 10 | 73 | 2,171 |
| Vector Store Ecosystems | 4 | 4 | 4 | 23 | 1 | 13 | 301 |
| Memory & Knowledge Systems | 6 | 6 | 5 | 41 | 0 | 25 | 2,302 |
| Chatbot / Assistant Frameworks | 4 | 4 | 4 | 49 | 0 | 16 | 1,468 |
| Code / Dev Agents | 6 | 6 | 6 | 48 | 0 | 13 | 1,075 |
| Production Agent Platforms | 11 | 11 | 9 | 208 | 4 | 113 | 7,318 |
| Small / Niche Projects | 19 | 18 | 13 | 88 | 2 | 36 | 433 |

---

## 12. Rule Distribution

| Rule | Count | % | Description |
|---|---|---|---|
| AW-TOOL-002 | 211 | 14% | Tool accepts arbitrary code execution |
| AW-MEM-003 | 171 | 11% | Memory backend has no access control |
| AW-TOOL-004 | 161 | 11% | Tool has no description |
| AW-MEM-001 | 152 | 10% | No tenant isolation in vector store |
| AW-SER-003 | 114 | 8% | Dynamic import with variable argument |
| AW-SER-001 | 102 | 7% | Unsafe deserialization |
| AW-RAG-001 | 98 | 7% | Retrieved context without delimiters |
| AW-SEC-001 | 85 | 6% | Hardcoded API key/secret in agent config |
| AW-RAG-003 | 56 | 4% | Unencrypted local vector store |
| AW-SEC-003 | 54 | 4% | Agent context logged at DEBUG level |
| AW-TOOL-001 | 45 | 3% | Destructive tool without approval gate |
| AW-TOOL-003 | 45 | 3% | High-risk tool lacks scope check |
| AW-RAG-004 | 41 | 3% | Vector store exposed without auth |
| AW-MEM-005 | 40 | 3% | No sanitization on retrieved memory |
| AW-CFG-hardcoded-secret | 21 | 1% | AW-CFG-hardcoded-secret |
| AW-MEM-002 | 20 | 1% | Shared collection without retrieval filter |
| AW-AGT-004 | 19 | 1% | LLM output stored to memory without validation |
| AW-MEM-004 | 15 | 1% | Injection patterns in retrieval path |
| AW-RAG-002 | 12 | 1% | Ingestion from untrusted source |
| AW-CFG-docker-no-auth | 10 | 1% | AW-CFG-docker-no-auth |
| AW-AGT-001 | 8 | 1% | Sub-agent inherits full parent tool set |
| AW-MCP-001 | 8 | 1% | MCP server without authentication |
| AW-SER-002 | 5 | 0% | Unpinned agent framework dependency |
| AW-MCP-002 | 2 | 0% | Static token in MCP config |
| AW-CFG-no-tls | 1 | 0% | AW-CFG-no-tls |
| AW-CFG-debug-mode | 1 | 0% | AW-CFG-debug-mode |
| AW-AGT-003 | 1 | 0% | Agent has read+write+delete without approval |

---

## 13. False Positive Estimation

Automated path-based FP estimation on 3,679 findings across 480 scanned projects (2026-03-21).

**Methodology:** Findings in test/example/tutorial/docs/fixture/mock directories are counted as likely false positives. This is a lower bound — some FPs exist in production source paths but are not detectable by path heuristics.

| Rule | Count | Est FP | FP% | Status |
|---|---|---|---|---|
| AW-MEM-003 | 539 | 31 | 5.8% | Good |
| AW-TOOL-002 | 396 | 33 | 8.3% | Moderate — subprocess-qualified after P0 fix |
| AW-MEM-001 | 323 | 20 | 6.2% | Good — engine-driven severity |
| AW-TOOL-004 | 287 | 14 | 4.9% | Good |
| AW-SEC-001 | 272 | 31 | 11.4% | Moderate — test API keys |
| AW-SER-001 | 267 | 5 | 1.9% | Good |
| AW-RAG-001 | 241 | 14 | 5.8% | Good |
| AW-SER-003 | 227 | 5 | 2.2% | Good — 4 heuristics applied |
| AW-RAG-004 | 177 | 9 | 5.1% | Good |
| AW-RAG-003 | 151 | 7 | 4.6% | Good |
| AW-SEC-003 | 124 | 4 | 3.2% | Good |
| AW-MEM-005 | 95 | 6 | 6.3% | Good |
| AW-TOOL-001 | 85 | 10 | 11.8% | Moderate |
| AW-TOOL-003 | 85 | 10 | 11.8% | Moderate |
| AW-SER-002 | 71 | 0 | 0.0% | Clean |
| AW-CFG-hardcoded-secret | 70 | 0 | 0.0% | Clean |
| AW-AGT-004 | 48 | 12 | 25.0% | Needs work — fires in test code |
| AW-MEM-004 | 47 | 0 | 0.0% | Clean |
| AW-CFG-docker-no-auth | 47 | 1 | 2.1% | Good |
| AW-MEM-002 | 41 | 11 | 26.8% | Needs work — fires in test fixtures |
| AW-AGT-001 | 21 | 0 | 0.0% | Clean |
| AW-MCP-001 | 20 | 3 | 15.0% | Moderate |
| AW-RAG-002 | 18 | 10 | 55.6% | Needs work — fires in example ingestion code |
| AW-AGT-003 | 14 | 1 | 7.1% | Good |
| AW-CFG-debug-mode | 9 | 0 | 0.0% | Clean |
| AW-MCP-002 | 2 | 0 | 0.0% | Clean |
| AW-CFG-no-tls | 2 | 0 | 0.0% | Clean |

**Overall: 3,679 findings → 237 estimated FP (6.4%), 3,442 estimated TP (93.6%)**

### Key Improvements from v1.0 OKR Work

| Rule | Before FP% | After FP% | How Fixed |
|---|---|---|---|
| AW-MEM-001 | 100% | 6.2% | IsolationEvidence engine |
| AW-SER-003 | 47% | 2.2% | 4 AST heuristics (f-string, config attr, try/except, .format) |
| AW-SEC-003 | 53% | 3.2% | Content reference check |
| AW-CFG-hardcoded-secret | 75% | 0.0% | Template/placeholder detection |
| AW-TOOL-002 | ~87% (inflated) | 8.3% | P0 fix: subprocess receiver qualification |
| **Overall** | **~35%** | **6.4%** | **5.5x improvement** |

### Remaining FP Hotspots (for v1.1)

| Rule | FP% | Volume | Priority |
|---|---|---|---|
| AW-RAG-002 | 55.6% | 18 | Low — small volume |
| AW-MEM-002 | 26.8% | 41 | Medium — test fixtures |
| AW-AGT-004 | 25.0% | 48 | Medium — test code paths |

*Note: Path-based estimation is a lower bound. Manual sampling of 50 source-path findings suggests an additional ~2-3% FP in production code, putting the real FP rate at ~8-9%.*

---

## 14. Attack Vector Coverage (9 / 35 Detectable)

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
| **AW-ATK-AGT-001** | Tool Poisoning / Unsafe Tool Access | Agno (Phidata), AutoGPT, Awesome LLM Apps, BabyAGI, CAMEL, ChatDev, CrewAI, DB-GPT, Devika, Dify (+18 more) | 310 | `agents_registry.py:140` (AW-AGT-001) |
| **AW-ATK-AGT-004** | Cross-Agent Memory Contamination | AdalFlow, Awesome LLM Apps, LangChain (mono), create-llama, langchain-RAG-chroma | 19 | `vectorstore.py:107` (AW-AGT-004) |
| **AW-ATK-CFG-001** | Unsafe Reset Enabled | LanceDB | 1 | `docker-compose.yml:9` (AW-CFG-debug-mode) |
| **AW-ATK-CFG-003** | No TLS / No Auth / Exposed Ports | AgentOps, Agno (Phidata), AutoGen, AutoRAG, Awesome LLM Apps, CAMEL, Cognee, Cognita, CrewAI, Dify (+18 more) | 60 | `vector_store_component.py:112` (AW-RAG-004) |
| **AW-ATK-CFG-004** | Hardcoded API Keys | AdalFlow, AgentOps, Agno (Phidata), AutoGPT, AutoGen, Awesome LLM Apps, CAMEL, Chainlit, ChromaDB, CrewAI (+23 more) | 108 | `settings.py:452` (AW-SEC-001) |
| **AW-ATK-INJ-001** | Stored Prompt Injection | Agno (Phidata), Aider, Awesome LLM Apps, Cognita, DB-GPT, Dify, DocsGPT, GPT-Researcher, Google Agent Dev Kit, GraphRAG (Microsoft) (+24 more) | 138 | `file_chat.py:66` (AW-RAG-001) |
| **AW-ATK-MEM-001** | Cross-Tenant Retrieval (No Filter) | Agno (Phidata), Aider, Awesome LLM Apps, DB-GPT, DocsGPT, GPT-Researcher, Google Agent Dev Kit, LangChain (mono), LangChain Extract, Langchain-Chatchat (+20 more) | 152 | `milvus_kb_service.py:100` (AW-MEM-001) |
| **AW-ATK-MEM-002** | Weak Tenant Isolation (Static Filter) | Agno (Phidata), Awesome LLM Apps, DocsGPT, LangChain (mono), Langchain-Chatchat, Langflow, OpenGPTs, UFO (Microsoft) | 20 | `ensemble.py:27` (AW-MEM-002) |
| **AW-ATK-MEM-003** | Namespace/Collection Confusion | Agno (Phidata), Aider, AutoGPT, Awesome LLM Apps, CAMEL, ChatDev, ChromaDB, Cognee, DB-GPT, Dify (+24 more) | 171 | `chromadb_kb_service.py:67` (AW-MEM-003) |
| **AW-ATK-MEM-004** | Partition Bypass via Direct API | LangChain (mono), LlamaHub, Multi-Agent Concierge, RAG-chatbot-langchain, create-llama, langchain-chatbot | 15 | `vectorstore_token_buffer_memory.py:120` (AW-MEM-004) |
| **AW-ATK-POI-005** | Document Loader Exploitation | Agno (Phidata), Awesome LLM Apps, Dify, SEC Insights | 12 | `qwen_local_rag_agent.py:234` (AW-RAG-002) |

### Vectors Not Detected (26 / 35)

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

## 15. Attack Vector Heatmap (Per Project)

| Project | AGT-001 | CFG-001 | CFG-003 | CFG-004 | INJ-001 | MEM-001 | MEM-002 | MEM-003 | MEM-004 | Total |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Langchain-Chatchat | **3** | · | · | **6** | **13** | **15** | **2** | **3** | · | 42 |
| PrivateGPT | · | · | **2** | **1** | · | · | · | · | · | 3 |
| Quivr | · | · | · | · | **2** | **2** | · | · | · | 4 |
| LocalGPT | · | · | · | · | · | · | · | · | · | 0 |
| DocsGPT | · | · | **1** | **5** | **4** | **4** | **1** | **1** | · | 16 |
| GPT-Researcher | · | · | · | · | **2** | **2** | · | · | · | 4 |
| Onyx/Danswer | · | · | **1** | **1** | **1** | · | · | **1** | · | 4 |
| DB-GPT | **37** | · | · | · | **8** | **1** | · | **3** | · | 49 |
| Chat-LangChain | · | · | · | · | · | · | · | · | · | 0 |
| RasaGPT | · | · | · | · | · | · | · | · | · | 0 |
| Langflow | **2** | · | **4** | **2** | **13** | **21** | **1** | **11** | · | 54 |
| Open Interpreter | **22** | · | · | · | · | · | · | · | · | 22 |
| Chainlit | · | · | · | **1** | · | · | · | · | · | 1 |
| Mem0/Embedchain | · | · | **2** | · | **3** | **2** | · | **2** | · | 9 |
| LLM App (Pathway) | · | · | · | · | · | · | · | · | · | 0 |
| Haystack | · | · | · | · | · | · | · | · | · | 0 |
| SuperAgent | · | · | · | · | · | · | · | · | · | 0 |
| AgentGPT | · | · | · | · | · | · | · | · | · | 0 |
| AutoGPT | **25** | · | · | **4** | · | · | · | **3** | · | 32 |
| LangGraph | · | · | **1** | **1** | · | · | · | · | · | 2 |
| LangSmith SDK | · | · | · | **1** | · | · | · | · | · | 1 |
| LangChain (mono) | **3** | · | **2** | · | **3** | **17** | **3** | **1** | **1** | 30 |
| OpenGPTs | · | · | **1** | · | · | · | **1** | · | · | 2 |
| LangServe | · | · | · | · | · | · | · | · | · | 0 |
| LangChain Extract | · | · | · | · | · | **1** | · | · | · | 1 |
| Awesome LLM Apps | **4** | · | **3** | **3** | **12** | **12** | **10** | **5** | · | 49 |
| LlamaIndex | — | — | — | — | — | — | — | — | — | — |
| RAGS (LlamaIndex) | · | · | · | · | **1** | **1** | · | · | · | 2 |
| LlamaParse | · | · | · | · | · | **1** | · | · | · | 1 |
| create-llama | · | · | · | · | **3** | **2** | · | **11** | **6** | 22 |
| SEC Insights | · | · | · | · | · | · | · | **1** | · | 1 |
| CrewAI | **40** | · | **1** | **4** | · | · | · | · | · | 45 |
| AutoGen | · | · | **1** | **3** | · | · | · | · | · | 4 |
| MetaGPT | · | · | **1** | · | **9** | **7** | · | **8** | · | 25 |
| ChatDev | **7** | · | · | · | · | · | · | **2** | · | 9 |
| CAMEL | **47** | · | **3** | **5** | · | · | · | **8** | · | 63 |
| BabyAGI | **3** | · | · | · | · | · | · | · | · | 3 |
| OpenAI Swarm | · | · | · | · | · | · | · | · | · | 0 |
| Swarms | · | · | · | · | · | · | · | · | · | 0 |
| TaskWeaver | · | · | · | · | · | **2** | · | · | · | 2 |
| RAGFlow | **6** | · | **2** | **18** | · | · | · | · | · | 26 |
| Kotaemon | · | · | · | · | · | · | · | · | · | 0 |
| LightRAG | · | · | **1** | · | · | · | · | · | · | 1 |
| FastGPT | **1** | · | · | **1** | · | · | · | · | · | 2 |
| QAnything | · | · | · | · | **2** | · | · | · | · | 2 |
| R2R | **2** | · | · | · | · | · | · | · | · | 2 |
| FlashRAG | **4** | · | · | · | · | · | · | **3** | · | 7 |
| AutoRAG | · | · | **1** | · | · | · | · | · | · | 1 |
| Canopy (Pinecone) | · | · | · | · | · | · | · | · | · | 0 |
| Verba (Weaviate) | · | · | **1** | · | · | · | · | · | · | 1 |
| Vanna | · | · | **1** | · | **5** | **10** | · | **5** | · | 21 |
| Cognita | · | · | **4** | · | **1** | · | · | · | · | 5 |
| ChatGPT Retrieval Plugin | · | · | · | · | · | · | · | · | · | 0 |
| txtai | **1** | · | · | · | · | · | · | **3** | · | 4 |
| ChromaDB | · | · | · | **1** | · | · | · | **1** | · | 2 |
| Milvus Bootcamp | · | · | **3** | · | · | **1** | · | **1** | · | 5 |
| Qdrant Examples | · | · | · | · | · | · | · | **4** | · | 4 |
| LanceDB | **2** | **1** | · | · | · | · | · | · | · | 3 |
| Cognee | · | · | **4** | · | · | · | · | **2** | · | 6 |
| Graphiti (Zep) | · | · | · | · | **6** | · | · | · | · | 6 |
| Letta (MemGPT) | · | · | · | **1** | · | · | · | **1** | · | 2 |
| GraphRAG (Microsoft) | · | · | · | · | **5** | · | · | · | · | 5 |
| nano-graphrag | · | · | · | **2** | · | · | · | · | · | 2 |
| Zep | · | · | · | · | · | · | · | · | · | 0 |
| Open WebUI | · | · | **5** | · | **1** | · | · | **1** | · | 7 |
| Khoj | · | · | · | **1** | · | · | · | · | · | 1 |
| PyGPT | **2** | · | · | **5** | **1** | **3** | · | · | · | 11 |
| Jan | **5** | · | · | · | · | · | · | · | · | 5 |
| OpenHands (OpenDevin) | **17** | · | · | · | · | · | · | · | · | 17 |
| SWE-agent | · | · | · | · | · | · | · | · | · | 0 |
| Aider | · | · | · | · | **2** | **2** | · | **1** | · | 5 |
| Devika | **1** | · | · | **1** | · | · | · | · | · | 2 |
| GPT-Engineer | · | · | · | · | · | · | · | · | · | 0 |
| GPT-Pilot | · | · | · | **5** | · | · | · | · | · | 5 |
| Dify | **5** | · | **4** | **1** | **1** | · | · | **7** | · | 18 |
| Agno (Phidata) | **41** | · | **3** | **8** | **3** | **3** | **1** | **13** | · | 72 |
| Pydantic AI | · | · | · | · | · | · | · | · | · | 0 |
| smolagents (HF) | · | · | · | · | · | · | · | · | · | 0 |
| Semantic Kernel | · | · | **5** | **9** | · | · | · | **12** | · | 26 |
| OpenAI Agents SDK | · | · | · | · | · | · | · | · | · | 0 |
| DSPy | · | · | · | · | · | · | · | · | · | 0 |
| Google Agent Dev Kit | **4** | · | **1** | **5** | **3** | **1** | · | · | · | 14 |
| UFO (Microsoft) | · | · | · | · | **1** | **1** | **1** | · | · | 3 |
| AgentOps | · | · | **1** | **7** | · | · | · | · | · | 8 |
| ModelScope Agent | · | · | · | **1** | · | · | · | **2** | · | 3 |
| memory-agent | · | · | · | · | · | · | · | · | · | 0 |
| rag-research-agent-template | · | · | · | · | **1** | · | · | · | · | 1 |
| langchain-chatbot | **1** | · | · | · | **2** | **2** | · | · | **4** | 9 |
| chat-with-websites | · | · | · | · | · | **1** | · | · | · | 1 |
| cohere-qdrant-doc-retrieval | · | · | · | · | **2** | **2** | · | **1** | · | 5 |
| RAG-chatbot-langchain | · | · | · | · | **1** | **2** | · | **1** | **2** | 6 |
| langchain-RAG-chroma | · | · | · | · | **2** | **2** | · | **1** | · | 5 |
| chat-with-pdf | · | · | · | · | · | · | · | · | · | 0 |
| langchain-multi-agent | **3** | · | · | · | **1** | **1** | · | · | · | 5 |
| objectbox-rag | · | · | · | · | · | · | · | · | · | 0 |
| AdalFlow | · | · | · | **1** | · | · | · | · | · | 1 |
| Hindsight | — | — | — | — | — | — | — | — | — | — |
| Vector Admin | · | · | · | · | · | · | · | · | · | 0 |
| HF Agents Course | · | · | · | · | · | · | · | · | · | 0 |
| Libre Chat | · | · | **1** | · | **1** | · | · | · | · | 2 |
| LangGraph BigTool | · | · | · | · | · | · | · | · | · | 0 |
| RAG-Anything | **7** | · | · | · | · | · | · | · | · | 7 |
| OASIS (CAMEL) | · | · | · | **1** | **2** | **1** | · | **1** | · | 5 |
| SWE-bench | **15** | · | · | · | · | · | · | · | · | 15 |
| LlamaDeploy | · | · | · | **1** | · | · | · | · | · | 1 |
| LlamaIndex.TS | · | · | · | **1** | · | · | · | · | · | 1 |
| LlamaAgents | · | · | · | **1** | · | · | · | · | · | 1 |
| LlamaHub | · | · | · | · | **21** | **30** | · | **50** | **1** | 102 |
| LlamaLab | · | · | · | · | · | · | · | · | · | 0 |
| Multi-Agent Concierge | · | · | · | · | · | · | · | **1** | **1** | 2 |
| PR Manager (LlamaIndex) | · | · | · | · | · | · | · | · | · | 0 |
| LazyLLM | · | · | **1** | **7** | · | · | · | · | · | 8 |
| ThinkRAG | · | · | · | · | · | · | · | **4** | **2** | 6 |
| Delphic | · | · | · | · | · | · | · | · | · | 0 |
| local_llama | · | · | · | · | · | · | · | · | · | 0 |
| Awesome-RAG (lucifertrj) | · | · | · | **1** | **2** | **2** | · | **2** | · | 7 |
| VeritasGraph | · | · | · | **1** | · | · | · | · | · | 1 |
| CorpusOS | · | · | · | · | **4** | **1** | **2** | · | · | 7 |
| Hello Wordsmith | · | · | · | · | · | **1** | · | **2** | · | 3 |
| PapersChat | · | · | **1** | · | · | · | · | **3** | · | 4 |
| LlamaIndex Omakase RAG | · | · | **1** | **1** | · | · | · | · | · | 2 |
| local-rag-llamaindex | · | · | **4** | · | · | · | · | **3** | · | 7 |
| XRAG | · | · | · | · | **3** | **4** | · | **8** | · | 15 |
| flexible-graphrag | · | · | **2** | · | **3** | **3** | · | **2** | · | 10 |
| Vector Cookbook (Timescale) | · | · | · | · | **4** | · | · | · | · | 4 |
| DocMind AI | · | · | **11** | **3** | **1** | **1** | · | · | · | 16 |
| RAGArch | · | · | **1** | · | · | · | · | **3** | · | 4 |
| RAG-LlamaIndex (Pinecone) | · | · | · | · | · | · | · | **10** | · | 10 |
| RAG Job Search Assistant | · | · | · | · | · | · | · | **1** | · | 1 |
| ingest-anything | **1** | · | · | · | · | · | · | **3** | · | 4 |
| OpenInference (Arize) | · | · | · | · | **1** | · | · | · | · | 1 |
| MCPAdapt | · | · | · | · | · | · | · | · | · | 0 |
| PlanExe | · | · | **3** | **15** | · | · | · | · | · | 18 |
| LlamaIndex Docs Agent | · | · | · | · | **2** | **1** | · | **1** | · | 4 |
| LlamaIndex Trip Planner | · | · | · | · | · | · | · | · | · | 0 |
| User-Centric RAG (LlamaIndex+Qdrant) | · | · | · | · | · | · | · | **2** | **2** | 4 |
| AgentServe | · | · | · | · | · | · | · | · | · | 0 |
| Agentic RAG (LlamaIndex) | · | · | · | · | **2** | **2** | · | **5** | · | 9 |
| Agent-as-a-Service | · | · | · | · | · | · | · | **1** | · | 1 |
| Workflows ACP | · | · | · | · | · | · | · | · | · | 0 |
| Agentic AI Chatbot (LlamaIndex) | · | · | · | · | · | · | · | · | · | 0 |
| Llama-4 Researcher | · | · | · | · | · | · | · | · | · | 0 |
| e-Library Agent | · | · | **1** | · | · | · | · | **1** | · | 2 |
| ragcoon | **4** | · | **1** | · | · | · | · | **3** | · | 8 |
| diRAGnosis | · | · | **1** | · | **9** | **10** | · | **8** | · | 28 |
| Agentic PRD Generation | · | · | **1** | · | · | · | · | · | · | 1 |
| LlamaIndexChat | · | · | · | · | · | · | · | **1** | · | 1 |
| LlamaIndex Ollama Chainlit | · | · | · | · | · | · | · | **3** | · | 3 |
| RAGIndex | · | · | **1** | · | · | · | · | · | · | 1 |
| LlamaIndex Agent (Swastik) | **2** | · | · | · | · | · | · | **1** | · | 3 |
| Azure LlamaIndex Sample | · | · | · | · | · | · | · | **1** | · | 1 |
| Brainiac | · | · | · | · | · | · | · | · | · | 0 |
| RAG-TUI | · | · | · | · | · | · | · | · | · | 0 |
| Chat-RAG | · | · | · | · | · | · | · | **3** | · | 3 |
| ToK | · | · | · | · | · | · | · | **8** | **8** | 16 |
| Multimodal Semantic RAG | · | · | · | · | **2** | **2** | · | **1** | · | 5 |
| M2M Vector Search | · | · | · | · | · | · | · | · | · | 0 |
| RAG Performance | · | · | · | · | · | · | · | **1** | · | 1 |
| RAG Firewall | · | · | · | **3** | **1** | **1** | · | · | · | 5 |
| RAG Framework Evaluation | · | · | · | · | **3** | **1** | · | **1** | · | 5 |
| RAG Ingest | · | · | · | · | · | · | · | **3** | · | 3 |
| GPTStonks | **1** | · | · | · | · | · | · | **3** | · | 4 |
| Quackling | · | · | · | · | · | · | · | · | · | 0 |
| GUT | · | · | · | · | · | · | · | · | · | 0 |
| AI Equity Research Analyst | · | · | · | · | · | · | · | · | · | 0 |
| Opik (Comet) | · | · | · | · | · | · | · | **1** | · | 1 |
| GPTCache | · | · | **1** | · | · | · | · | **1** | · | 2 |
| All-in-RAG | · | · | **2** | · | **10** | **4** | **3** | · | · | 19 |
| Gerev | · | · | · | · | · | · | · | · | · | 0 |
| PyGPT (LlamaIndex) | **2** | · | · | **5** | **1** | **3** | · | · | · | 11 |
| Judgeval | · | · | · | · | · | · | · | · | · | 0 |
| AutoLLM | · | · | · | · | · | · | · | **3** | · | 3 |
| RepoAgent | · | · | · | · | · | · | · | **2** | · | 2 |
| RAG Chatbot (datvodinh) | · | · | **1** | · | · | · | · | **3** | · | 4 |
| GraphRAG Toolkit (AWS) | · | · | · | · | · | · | · | · | · | 0 |
| Agent-Wiz | · | · | · | · | · | · | · | · | · | 0 |
| Agentic AI Systems | **3** | · | · | **13** | **17** | **15** | **8** | **4** | **1** | 61 |
| RESTai | · | · | **1** | · | · | · | · | **2** | · | 3 |
| SlideSpeak | · | · | · | · | · | · | · | **2** | · | 2 |
| Whisk | · | · | · | · | · | · | · | · | · | 0 |
| Airgapped Offline RAG | · | · | · | · | **1** | **1** | · | · | · | 2 |
| FastAPI Agents | · | · | · | · | · | · | · | · | · | 0 |
| BentoML RAG Tutorials | · | · | · | **2** | · | · | · | **6** | · | 8 |
| Reliable RAG | · | · | **1** | · | · | · | · | · | · | 1 |
| LLM Ollama LlamaIndex Bootstrap | · | · | · | · | · | · | · | **1** | · | 1 |
| AI Playground (rokbenko) | · | · | **1** | **1** | **2** | · | · | · | · | 4 |
| Applied AI RAG Assistant | **3** | · | · | · | **4** | **6** | · | **1** | **2** | 16 |
| DSPy RAG + LlamaIndex | · | · | · | **2** | · | · | · | · | · | 2 |
| ATO Chatbot | · | · | **2** | · | **1** | **2** | · | **5** | · | 10 |
| Ragtag Tiger | · | · | · | · | · | · | · | **1** | · | 1 |
| LlamaIndex Zoom Assistant | · | · | · | · | · | · | · | · | · | 0 |
| LlamaIndex Retrieval API | · | · | · | · | · | · | · | **2** | · | 2 |
| ChatGPT Custom Knowledge | · | · | · | · | · | · | · | · | · | 0 |
| Smart LLM Loader | · | · | · | · | · | · | · | · | · | 0 |
| ChatGPT Long-Term Memory | · | · | · | · | · | · | · | **1** | · | 1 |
| LlamaIndex Examples (alphasecio) | · | · | · | · | · | · | · | **1** | · | 1 |
| Agentic Playground | **1** | · | · | · | · | · | · | · | · | 1 |
| IntelliWeb GPT | · | · | · | **2** | · | · | · | **1** | · | 3 |
| LlamaIndex Supervisor | · | · | · | · | · | · | · | · | · | 0 |
| Contextual Retrieval (Anthropic) | · | · | · | · | **1** | **2** | · | **3** | · | 6 |
| Streaming LLM Chat | · | · | · | · | · | · | · | **2** | **1** | 3 |
| Docs-n-Data Knowledge App | · | · | · | · | · | · | · | · | · | 0 |
| AgenticAI Coach | · | · | · | · | · | · | · | · | · | 0 |
| GemInsights | · | · | · | · | · | · | · | · | · | 0 |
| LLM RAG | · | · | · | · | · | · | · | **2** | **1** | 3 |
| QuickDigest | · | · | · | · | · | · | · | **1** | · | 1 |
| AItrika | · | · | · | · | · | · | · | **7** | · | 7 |
| LangChain RAG DevKit | **2** | · | · | · | **4** | **3** | · | **2** | **3** | 14 |
| RAG AI Voice Assistant | · | · | **1** | · | · | · | · | **3** | **1** | 5 |
| Translation Agent WebUI | · | · | · | · | · | · | · | · | · | 0 |
| Hiflylabs Agent Demo | · | · | · | · | · | **1** | · | · | · | 1 |
| RAG KnowledgeLLM Bot | · | · | · | · | · | · | · | **1** | · | 1 |
| PyQt LlamaIndex | · | · | · | · | · | · | · | **1** | · | 1 |
| Doppalf | · | · | · | **2** | · | · | · | **2** | · | 4 |
| Bot-the-Defect | · | · | · | · | · | · | · | **2** | **2** | 4 |
| EduRAG Network Assistant | · | · | · | · | **4** | **4** | · | **3** | · | 11 |
| LlamaIndex Agent Workflow Browse | · | · | · | · | · | · | · | · | · | 0 |
| LlamaIndex Chatbot Advanced | · | · | · | · | · | · | · | **3** | · | 3 |
| LEANN | · | · | · | · | · | · | · | · | · | 0 |
| LlamaIndex RAG (romilandc) | · | · | **1** | · | · | · | · | **2** | · | 3 |
| MCP Toolbox SDK (Google) | · | · | · | · | · | · | · | · | · | 0 |
| PromptPilot | · | · | · | · | · | · | · | · | · | 0 |
| Jetson Orin Nano RAG Kit | **5** | · | · | **2** | · | · | · | · | · | 7 |
| CrewAI Examples | · | · | · | · | · | · | · | · | · | 0 |
| CrewAI Tools | · | · | · | **1** | · | · | · | · | · | 1 |
| AutoGroq | · | · | · | · | · | · | · | · | · | 0 |
| MCP Memory Service | · | · | **3** | **5** | · | · | · | · | · | 8 |
| CrewAI Studio | · | · | · | · | · | · | · | · | · | 0 |
| Full Stack AI Agent Template | · | **7** | **1** | · | · | · | · | · | · | 8 |
| Viral Clips Crew | · | · | · | · | · | · | · | · | · | 0 |
| AIWriteX | · | · | · | · | · | · | · | · | · | 0 |
| Tiger (Upsonic) | · | · | · | · | · | · | · | · | · | 0 |
| Easy Investment Agent | · | · | · | · | · | · | · | · | · | 0 |
| Devyan | · | · | · | · | · | · | · | · | · | 0 |
| OpenPlexity Pages | · | · | · | · | · | · | · | · | · | 0 |
| CrewAI Test (NanGePlus) | · | · | · | **24** | · | · | · | · | · | 24 |
| CrewAI GUI Qt | · | · | · | · | · | · | · | · | · | 0 |
| Wavefront | · | · | **1** | **5** | · | · | · | · | · | 6 |
| CrewAI UI Business Launch | · | · | · | **1** | · | · | · | · | · | 1 |
| Open Extract | · | · | **1** | · | · | · | · | · | · | 1 |
| CrewAI Gmail Automation | · | · | · | · | · | · | · | · | · | 0 |
| Value | · | · | **1** | **2** | · | · | · | · | · | 3 |
| Resume Optimization Crew | · | · | · | · | · | · | · | · | · | 0 |
| CrewAI Stock Analysis | · | · | · | · | · | · | · | · | · | 0 |
| Geo AI Agent | · | · | · | · | · | · | · | · | · | 0 |
| Trip Planner Agent | · | · | · | · | · | · | · | · | · | 0 |
| Paper Summarizer | · | · | · | **1** | · | · | · | · | · | 1 |
| CrewAI Flows FullStack | · | · | · | **4** | · | · | · | · | · | 4 |
| Agent Audit | · | · | · | **26** | · | · | · | · | · | 26 |
| Mengram | · | · | **2** | · | **2** | · | · | · | · | 4 |
| FenixAI Trading Bot | · | · | **1** | · | · | · | · | · | · | 1 |
| Aitino | · | · | · | · | · | · | · | · | · | 0 |
| Awesome AI Agents HUB | · | · | · | · | · | · | · | · | · | 0 |
| Workshop AI Agent | **7** | · | · | · | **5** | **3** | **4** | **2** | · | 21 |
| Spotify Playlist (CrewAI) | · | · | · | · | · | · | · | · | · | 0 |
| CrewAI Sheets UI | · | · | · | · | · | · | · | · | · | 0 |
| AI Agents with CrewAI | · | · | · | · | · | · | · | · | · | 0 |
| AI Agents (whyash) | — | — | — | — | — | — | — | — | — | — |
| CrewAI Streamlit Demo | · | · | · | · | · | · | · | · | · | 0 |
| Agent OS | **2** | · | **4** | **4** | · | · | · | · | · | 10 |
| Eval View | **2** | · | · | **4** | · | · | · | · | · | 6 |
| Multi-Agents System from Scratch | · | · | · | · | · | · | · | · | · | 0 |
| RAG Boilerplate | · | · | **1** | · | · | **3** | · | · | · | 4 |
| YouTube Yapper Trapper | · | · | · | **1** | · | · | · | · | · | 1 |
| RoboCrew | **6** | · | · | · | · | · | · | · | · | 6 |
| AISquare Studio QA | · | · | · | · | · | · | · | · | · | 0 |
| VN Stock Advisor | · | · | · | · | · | · | · | · | · | 0 |
| ComfyUI-CrewAI | · | · | · | · | · | · | · | · | · | 0 |
| TravelPlanner CrewAI | · | · | · | · | · | · | · | · | · | 0 |
| Multi-Agent RAG Template | · | · | · | · | · | · | · | · | · | 0 |
| Investment Agent (LangGraph+CrewAI) | · | · | · | · | · | · | · | · | · | 0 |
| AI Agent Crew (Bitcoin) | **3** | · | · | · | **1** | **1** | · | · | · | 5 |
| AI Trading Crew | · | · | · | · | · | · | · | · | · | 0 |
| CrewAI MCP | · | · | · | · | · | · | · | · | · | 0 |
| Email Agent | · | · | · | · | · | · | · | · | · | 0 |
| Jira Tiger | · | · | · | · | · | · | · | · | · | 0 |
| KAI | — | — | — | — | — | — | — | — | — | — |
| CrewAI Essay Writer | · | · | · | · | · | · | · | · | · | 0 |
| LLM Agents Example | **4** | · | · | **1** | · | · | · | · | · | 5 |
| Crew Llamafile | · | · | · | · | · | · | · | · | · | 0 |
| Crew News | · | · | · | · | · | · | · | · | · | 0 |
| CrewAI Multi-Agent (Financial) | · | · | · | · | **1** | **1** | · | · | · | 2 |
| AI News Researcher & Blog Writer | · | · | · | · | · | · | · | · | · | 0 |
| Multiagent Debugger | **1** | · | · | · | · | · | · | · | · | 1 |
| Personal Brand Team | · | · | · | · | · | · | · | · | · | 0 |
| AgentFacts | · | · | · | · | · | · | · | · | · | 0 |
| AI Book Writer | · | · | · | **2** | · | · | · | · | · | 2 |
| Smart Marketing Assistant | **1** | · | · | · | · | · | · | · | · | 1 |
| Operagents | · | · | · | · | · | · | · | · | · | 0 |
| ContextLoom | · | · | · | · | · | · | · | · | · | 0 |
| Multi-Agent Travel Advisor | · | · | · | · | **2** | **2** | · | **1** | · | 5 |
| CrewAI Qdrant Obsidian | · | · | · | · | · | · | · | · | · | 0 |
| Multi-Agent AI Newsletter | · | · | · | · | · | · | · | · | · | 0 |
| CV Agents | · | · | · | · | · | · | · | · | · | 0 |
| Smart Nutritional App | · | · | · | · | · | · | · | · | · | 0 |
| Crewlit | · | · | · | · | · | · | · | · | · | 0 |
| Healthcare Assistant | · | · | · | · | **1** | · | · | · | · | 1 |
| Agent Kernel | · | · | · | **1** | · | · | · | · | · | 1 |
| CrewAI Stock Trader | · | · | · | · | · | · | · | · | · | 0 |
| Compliance Assistant (AWS) | · | · | · | **1** | · | · | · | · | · | 1 |
| Kalibr SDK | · | · | · | · | · | · | · | · | · | 0 |
| Coral AI | · | · | · | · | · | · | · | · | · | 0 |
| Agentic Stock Analysis Crew | · | · | · | · | · | · | · | · | · | 0 |
| Newsletter Agent | · | · | · | · | · | · | · | · | · | 0 |
| Yaitec Hub Templates | **1** | · | · | · | **2** | · | · | · | · | 3 |
| Agentic AI Projects | · | · | · | · | · | · | · | · | · | 0 |
| BentoCrewAI | · | · | · | · | · | · | · | · | · | 0 |
| CrewAI Agentic Jira | · | · | · | · | · | · | · | · | · | 0 |
| News AI Agents (Gemini) | · | · | · | · | · | · | · | · | · | 0 |
| Python Coding Agent | **2** | · | · | · | · | · | · | · | · | 2 |
| Market Research Agent | · | · | · | · | · | · | · | · | · | 0 |
| Mistral Backlinker | · | · | · | · | · | · | · | · | · | 0 |
| TaskForce | **1** | · | · | · | **1** | **1** | · | · | · | 3 |
| Graphlit Tools | · | · | · | · | · | · | · | · | · | 0 |
| InsAIts | · | · | **1** | **5** | · | · | · | · | · | 6 |
| LangCrew | · | · | · | **1** | · | · | · | · | · | 1 |
| PagePod | · | · | · | · | · | · | · | · | · | 0 |
| Doctor Assist (CrewAI) | · | · | · | · | · | · | · | · | · | 0 |
| CrewAI Projects (hmnajam) | **1** | · | · | **1** | · | · | · | · | · | 2 |
| CrewAI Projects (lakshya) | — | — | — | — | — | — | — | — | — | — |
| CrewAI Multi-Agent Debate | · | · | · | · | · | · | · | · | · | 0 |
| MultiAgent CrewAI (Indicium) | · | · | · | · | · | · | · | · | · | 0 |
| Investor Crew | · | · | · | · | · | · | · | · | · | 0 |
| AIForge | · | · | · | · | · | · | · | · | · | 0 |
| Prompt Maker | · | · | · | · | · | · | · | · | · | 0 |
| CrewAI Research Assistant | · | · | · | · | · | · | · | · | · | 0 |
| LangChain Streamlit Agent | **1** | · | · | · | **1** | **1** | · | · | **3** | 6 |
| LangChain RAG Tutorial | · | · | · | · | **1** | · | · | **1** | · | 2 |
| LangChain Examples Collection | · | · | · | · | **5** | · | · | · | · | 5 |
| Multi-Agentic RAG LangGraph | · | · | · | · | **2** | **2** | · | · | · | 4 |
| RAG with LangChain ChromaDB | · | · | · | · | **4** | **4** | · | **2** | · | 10 |
| Enterprise RAG pipeline framework | **2** | · | **2** | **1** | · | · | · | · | · | 5 |
| ColBERT late-interaction for RAG | · | · | · | · | · | · | · | · | · | 0 |
| Multi-query + Reciprocal Rank Fusion | · | · | · | · | · | · | · | **2** | · | 2 |
| Advanced RAG pipeline from scratch | · | · | · | · | · | · | · | **1** | · | 1 |
| Super performant RAG pipelines | · | · | · | · | · | · | · | · | · | 0 |
| Educational production RAG | · | · | **3** | **8** | · | · | · | · | · | 11 |
| Python RAG toolkit with DuckDB | · | · | · | · | **2** | **2** | · | **1** | · | 5 |
| Azure OpenAI RAG at scale | **1** | · | · | · | · | · | · | · | · | 1 |
| Azure RAG sample app | · | · | · | **1** | · | · | · | · | · | 1 |
| RAG hallucination detection | · | · | · | · | · | · | · | · | · | 0 |
| Rule-based retrieval with Pinecone | · | · | · | · | · | · | · | **1** | · | 1 |
| Production RAG with 6 vector DB swaps | · | **1** | **5** | **3** | **1** | · | · | **1** | · | 11 |
| RAG with Docling + ChromaDB | · | · | **3** | · | **8** | **9** | · | **7** | · | 27 |
| Graph-based RAG retrieval | · | · | · | · | · | · | · | · | · | 0 |
| GraphRAG with local LLMs | **4** | · | · | **3** | **3** | · | · | · | · | 10 |
| GraphRAG + Ollama local models | · | · | · | · | **3** | · | · | · | · | 3 |
| Neo4j GraphRAG Python | · | · | · | · | · | · | · | · | · | 0 |
| Production GraphRAG + AI agents | · | · | **2** | · | · | · | · | **2** | · | 4 |
| GraphRAG + LightRAG + Neo4j | **2** | · | · | · | **1** | · | · | **1** | · | 4 |
| AutoGen + GraphRAG + Ollama | · | · | · | · | · | · | · | · | · | 0 |
| Customer service Agents SDK demo | · | · | · | · | · | · | · | · | · | 0 |
| Deep research with Agents SDK | · | · | · | · | · | · | · | · | · | 0 |
| Pydantic AI agents tutorial | **4** | · | · | · | · | · | · | · | · | 4 |
| Agentic RAG with Pydantic AI | · | · | · | · | · | · | · | · | · | 0 |
| Agent memory with ChromaDB | · | · | · | · | · | · | · | **1** | · | 1 |
| Chat with PDF using embeddings | · | · | · | · | · | · | · | · | · | 0 |
| Dynamic AI agent automation platform | **51** | · | · | **3** | · | · | · | · | · | 54 |
| Open source autonomous AI agent framework | **28** | · | **2** | **1** | · | · | · | **7** | · | 38 |
| Fully local autonomous agent | **8** | · | · | · | · | · | · | · | · | 8 |
| GPT autonomous agent creating newspapers | · | · | · | **2** | · | · | · | · | · | 2 |
| Hierarchical Autonomous Agent Swarm | · | · | · | · | · | · | · | · | · | 0 |
| LLM agent controlling RESTful APIs | · | · | · | · | · | · | · | · | · | 0 |
| Terminal agent with local tools | · | · | · | · | · | · | · | · | · | 0 |
| Vectara agentic RAG Python | · | · | · | **1** | **1** | · | · | · | · | 2 |
| RAG chatbot from documents | · | · | · | · | **5** | **3** | · | **2** | · | 10 |
| Local RAG with open-source LLMs | · | · | · | **2** | · | · | · | **1** | · | 3 |
| Production-ready FastAPI + LangGraph | · | · | · | · | · | · | · | · | · | 0 |
| LangChain RAG Tutorial v2 | · | · | · | · | **3** | **3** | · | **2** | · | 8 |
| LangGraph agents with MCP tools | · | · | · | · | · | · | · | · | · | 0 |
| AI Chatbot with LangChain | · | · | · | · | **1** | **1** | · | · | · | 2 |
| Smart Speaker with LangChain agents | · | · | · | · | · | · | · | · | · | 0 |
| AWS Bedrock LangChain agent | · | · | · | · | · | · | · | · | **1** | 1 |
| AI Coding Agent with LangGraph | **14** | · | · | · | · | · | · | · | · | 14 |
| LangChain agents for Bitcoin | **3** | · | · | · | · | · | · | · | · | 3 |
| Multi-agent LangGraph template | · | · | · | · | · | · | · | · | · | 0 |
| Chat with docs using LangChain+Ollama | · | · | · | · | **3** | **1** | · | **1** | **1** | 6 |
| Agentic incident management LangGraph | · | · | **4** | **1** | · | · | · | · | · | 5 |
| GPT4 LangChain research agent | · | · | · | · | **2** | **1** | · | **2** | **4** | 9 |
| Math chatbot LangChain agents | · | · | · | · | · | · | · | · | · | 0 |
| AI Agent framework LangChain+LangGraph | **5** | · | · | · | **2** | **3** | · | · | · | 10 |
| UiPath LangGraph agents | **1** | · | · | **1** | **1** | **2** | **1** | · | · | 6 |
| LangChain Weaviate integration | · | · | · | · | · | · | · | · | · | 0 |
| LangChain stock screening agent | · | · | · | · | · | · | · | **1** | · | 1 |
| LangChain agent for Git commands | **3** | · | · | · | · | · | · | · | · | 3 |
| LangChain agent + Neo4j memory | · | · | **1** | · | · | · | · | · | · | 1 |
| CrewAI experiments with local models | · | · | · | **1** | · | · | · | · | · | 1 |
| CrewAI hierarchical tutorial | · | · | · | · | · | · | · | · | · | 0 |
| Automate YouTube with CrewAI | · | · | · | · | · | · | · | · | · | 0 |
| CrewAI RAG deep dive | · | · | · | · | · | · | · | · | · | 0 |
| Agency Swarm tutorial | · | · | · | · | · | · | · | · | · | 0 |
| OpenAI function calling + Deep Lake | — | — | — | — | — | — | — | — | — | — |
| MCP server multi-framework | · | · | · | · | · | · | · | · | · | 0 |
| OpenAI function calling helpers | · | · | · | · | · | · | · | · | · | 0 |
| OpenAI Functions JSON metadata | · | · | · | · | · | · | · | · | · | 0 |
| Financial agent OpenAI SDK | · | · | · | · | · | · | · | · | · | 0 |
| Multi-agent investment research | **2** | · | · | · | · | · | · | · | · | 2 |
| Production agentic RAG course | · | · | · | **1** | · | · | · | **1** | · | 2 |
| Production LLM+RAG with LLMOps | · | · | **2** | · | · | · | · | · | · | 2 |
| NVIDIA RAG chatbots Windows | · | · | · | **1** | **2** | **2** | · | **2** | · | 7 |
| YouTube Full Text Search CLI | · | · | · | · | · | · | · | · | · | 0 |
| On-premises conversational RAG | · | · | **5** | · | **2** | · | · | · | · | 7 |
| MCP knowledge graph RAG | · | · | · | · | · | · | · | **1** | · | 1 |
| Forward-Looking Active REtrieval | **1** | · | · | · | · | · | · | · | · | 1 |
| Visual Document RAG agents | · | · | · | · | **3** | **4** | · | **2** | · | 9 |
| RAG retrieval + re-ranking toolkit | · | · | · | · | **1** | · | · | · | · | 1 |
| Hierarchical knowledge RAG | · | · | · | · | · | · | · | · | · | 0 |
| Multimodal RAG Framework | · | · | · | · | · | · | · | · | · | 0 |
| Corrective RAG | · | · | · | · | · | · | · | · | · | 0 |
| RAG with txtai | · | · | · | · | · | · | · | · | · | 0 |
| Text-to-SQL RAG with ChromaDB+FAISS | **3** | · | **1** | · | · | · | · | **2** | · | 6 |
| Personal knowledge base RAG | · | · | · | · | · | · | · | · | · | 0 |
| MultiHop RAG evaluation | · | · | · | · | **2** | **1** | · | **1** | · | 4 |
| Agentic RAG via RL | · | · | · | · | · | · | · | · | · | 0 |
| Agentic RAG from GitHub repos | · | · | · | **1** | · | · | · | · | · | 1 |
| RAG on codebases with LanceDB | · | · | · | · | · | · | · | · | · | 0 |
| Local LLM with RAG | · | · | · | · | · | · | · | · | · | 0 |
| Complex reasoning agentic RAG | · | · | · | · | · | · | · | · | · | 0 |
| AI-powered local chatbot | · | · | **4** | **3** | **1** | · | · | · | · | 8 |
| Air-gapped LLMs toolkit | · | · | **2** | · | **3** | **3** | · | **1** | · | 9 |
| Hybrid RAG vector+graph | · | · | **2** | · | · | · | · | **1** | · | 3 |
| Naive to Agentic to GraphRAG | **2** | · | · | · | **7** | **13** | · | **1** | · | 23 |
| GPT with web browsing | · | · | · | · | · | **1** | · | · | · | 1 |
| ChromaDB-based memory | · | · | · | · | **4** | **6** | · | **4** | · | 14 |
| Multimodal RAG with Milvus | · | · | · | · | · | · | · | · | · | 0 |
| Local RAG with Qdrant | · | · | · | · | · | **1** | · | · | · | 1 |
| Privacy-first multimodal RAG | **1** | · | **1** | · | **4** | **2** | · | **1** | · | 9 |
| Agentic RAG for drug intelligence | · | · | · | · | · | · | · | · | · | 0 |
| Agentic RAG for small LMs | · | · | · | · | · | · | · | · | · | 0 |
| Multi-agent RAG with Qdrant | · | · | **2** | · | **1** | **1** | · | · | · | 4 |
| Local RAG Ollama+ChromaDB | **1** | · | · | · | **3** | **3** | · | **3** | · | 10 |
| Containerized RAG with Qdrant | · | · | · | **2** | · | · | · | · | · | 2 |
| Chat PDF LangChain+ChromaDB | · | · | · | · | **2** | **1** | · | **1** | · | 4 |
| RAG ops with cache layers | · | · | **2** | **1** | **3** | · | **2** | **2** | · | 10 |
| Semantic search for Gmail | · | · | · | · | · | · | · | **1** | · | 1 |
| LLMs + vector stores framework | · | · | **2** | · | · | · | · | **2** | · | 4 |
| Agentic RAG FAISS+BM25 | **1** | · | **2** | · | · | · | · | **2** | · | 5 |
| Search PDF LangChain+ChromaDB | · | · | · | · | **1** | **2** | · | **1** | · | 4 |
| Chat with docs multi-LLM | · | · | **5** | · | **2** | **3** | · | **1** | · | 11 |
| LangChain Pinecone RAG | · | · | · | · | **5** | **4** | · | **5** | · | 14 |
| Multimodal RAG semantic search | · | · | · | · | · | · | · | · | · | 0 |
| Multimodal data representation | · | · | · | · | · | · | · | **3** | · | 3 |
| Prompt testing for LLMs+vector DBs | **1** | · | · | · | · | · | · | **2** | · | 3 |
| Qdrant MCP server | · | · | · | · | · | · | · | · | · | 0 |
| Python Qdrant client | · | · | · | · | · | · | · | · | · | 0 |
| AI spreadsheet with LLM pipelines | · | · | · | **5** | · | · | · | · | · | 5 |
| Graph-vector memory service | · | · | · | · | · | · | · | · | · | 0 |
| OSINT analysis with embeddings | · | · | **1** | · | **1** | · | · | **2** | · | 4 |
| AI Assistant with Qdrant | **3** | · | **54** | · | · | · | · | **82** | · | 139 |
| Conversational agent Qdrant | · | · | **1** | · | · | **1** | · | · | · | 2 |
| Weaviate Python client | **1** | · | **4** | · | · | · | · | **8** | · | 13 |
| Reverse image search CLIP+Qdrant | · | · | **1** | · | · | · | · | · | · | 1 |
| Document app Qdrant+BGE | · | · | **1** | · | **2** | **2** | · | **1** | · | 6 |
| ChromaDB chatbot | · | · | · | · | · | · | · | **2** | · | 2 |
| ETL for vector databases | · | · | · | · | · | · | · | **4** | · | 4 |
| Weaviate Agent Skills | · | · | · | · | · | · | · | · | · | 0 |
| Multi-Agent LLM Trading | · | · | · | · | · | · | · | · | · | 0 |
| Zero-Code LLM Agent Framework | **15** | · | · | **1** | · | · | · | **1** | · | 17 |
| Low-code multi-agent with memory | · | · | **1** | **17** | **1** | · | **1** | **2** | · | 22 |
| Multi-Agent Orchestration | **1** | · | · | **1** | · | · | · | · | · | 2 |
| Multi-Agent Programming LLMs | **5** | · | **2** | · | · | · | · | **6** | · | 13 |
| Multi-agent poster generation | **65** | · | **4** | **10** | · | · | · | **8** | · | 87 |
| Multi-agent deep research | · | · | **1** | **2** | · | · | · | **1** | · | 4 |
| No-code multi-agent framework | · | · | · | **2** | · | **1** | · | **3** | · | 6 |
| LLM multi-agent framework | **3** | · | **2** | · | · | · | · | · | · | 5 |
| LLM Agent Framework ComfyUI | · | · | · | **7** | **2** | **7** | · | **2** | · | 18 |
| Agentic Memory for LLM Agents | · | · | · | · | · | · | · | **4** | · | 4 |
| General memory for agents | · | · | · | · | · | · | · | · | · | 0 |
| MCP long-term agent memory | · | · | · | · | · | · | · | · | · | 0 |
| Agency Swarm experiments | **3** | · | · | **1** | · | · | · | · | · | 4 |
| AI observability for agents | · | · | · | **2** | · | · | · | · | · | 2 |
| AI web framework FastAPI+Pydantic | · | · | · | · | · | · | · | · | · | 0 |
| Airflow + Pydantic AI agents | · | · | · | · | · | · | · | · | · | 0 |
| Deep Agent on Pydantic-AI | · | · | · | · | · | · | · | · | · | 0 |
| PydanticAI research agent | · | · | · | · | · | · | · | · | · | 0 |
| MongoDB RAG with Pydantic AI | · | · | · | · | · | · | · | · | · | 0 |
| Agent memory with Redis | · | · | **6** | · | · | · | · | **1** | · | 7 |
| Smolagents framework examples | · | · | · | **1** | · | · | · | · | · | 1 |
| Langroid multi-agent examples | · | · | · | · | · | · | · | · | · | 0 |
| 7-layer memory for AI Agents | **1** | · | · | · | · | · | · | **2** | · | 3 |
| DeepSearch with smolagents | · | · | · | · | · | · | · | · | · | 0 |
| Hallucination eval agent memory | · | · | · | · | · | · | · | · | · | 0 |
| Autonomous agent LLM | · | · | · | · | · | · | · | · | · | 0 |
| LLM with vector DB memory | · | · | · | · | · | · | · | **1** | · | 1 |
| Graph Retriever for QA | · | · | · | · | · | · | · | · | · | 0 |
| DSPy+Weaviate retrieval | · | · | · | · | · | · | · | · | · | 0 |

*Legend: number = findings count, · = not detected, — = not scanned*

---

## 16. How to Reproduce

```bash
pip install -e ".[dev]"
./scripts/benchmark3000.sh
```

### Environment Variables

| Variable | Default | Description |
|---|---|---|
| `MAX_PARALLEL` | 4 | Parallel git clone jobs |
| `SCAN_TIMEOUT` | 300 | Per-project scan timeout (seconds) |
