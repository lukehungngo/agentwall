# AgentWall Benchmark 3000

**Date:** 2026-03-22
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

## 2. Tier 2 — LangChain Extended

| # | Project | Stars | Files | Findings | CRIT | HIGH | MED | LOW | Top Rules |
|---|---|---|---|---|---|---|---|---|---|
| 1 | LangChain Streamlit Agent | ~1.6k | 13 | 8 | 0 | 6 | 0 | 2 | AW-MEM-004(3), AW-SER-001(1), AW-RAG-001(1) |
| 2 | LangChain RAG Tutorial | ~926 | 3 | 4 | 0 | 2 | 2 | 0 | AW-RAG-003(2), AW-RAG-001(1), AW-MEM-003(1) |
| 3 | LangChain Examples Collection | ~544 | 17 | 7 | 0 | 5 | 0 | 2 | AW-RAG-001(5), AW-TOOL-004(2) |
| 4 | Multi-Agentic RAG LangGraph | ~207 | 10 | 8 | 0 | 2 | 4 | 2 | AW-RAG-003(3), AW-RAG-001(2), AW-MEM-001(2) |
| 5 | RAG with LangChain ChromaDB | ~209 | 2 | 14 | 2 | 6 | 6 | 0 | AW-MEM-001(4), AW-RAG-003(4), AW-RAG-001(2) |
| 6 | Production-ready FastAPI + LangGraph | ~2k | 34 | 0 | 0 | 0 | 0 | 0 | — |
| 7 | LangChain RAG Tutorial v2 | ~937 | 4 | 11 | 0 | 4 | 5 | 2 | AW-MEM-001(3), AW-MEM-003(2), AW-RAG-003(2) |
| 8 | LangGraph agents with MCP tools | ~810 | 9 | 0 | 0 | 0 | 0 | 0 | — |
| 9 | AI Chatbot with LangChain | ~436 | 7 | 2 | 1 | 1 | 0 | 0 | AW-MEM-001(1), AW-RAG-001(1) |
| 10 | Smart Speaker with LangChain agents | ~311 | 7 | 1 | 0 | 0 | 1 | 0 | AW-SER-002(1) |
| 11 | AWS Bedrock LangChain agent | ~261 | 5 | 1 | 0 | 1 | 0 | 0 | AW-MEM-004(1) |
| 12 | AI Coding Agent with LangGraph | ~242 | 93 | 16 | 0 | 6 | 10 | 0 | AW-TOOL-001(6), AW-TOOL-003(6), AW-AGT-003(2) |
| 13 | LangChain agents for Bitcoin | ~143 | 17 | 3 | 0 | 2 | 1 | 0 | AW-TOOL-001(1), AW-AGT-001(1), AW-TOOL-003(1) |
| 14 | Multi-agent LangGraph template | ~95 | 12 | 0 | 0 | 0 | 0 | 0 | — |
| 15 | Chat with docs using LangChain+Ollama | ~83 | 4 | 9 | 0 | 4 | 4 | 1 | AW-RAG-001(2), AW-RAG-003(2), AW-MEM-004(1) |
| 16 | Agentic incident management LangGraph | ~76 | 400 | 9 | 0 | 6 | 3 | 0 | AW-RAG-004(4), AW-SEC-003(3), AW-SEC-001(1) |
| 17 | GPT4 LangChain research agent | ~74 | 3 | 13 | 0 | 7 | 5 | 1 | AW-MEM-004(4), AW-RAG-003(4), AW-MEM-003(2) |
| 18 | Math chatbot LangChain agents | ~70 | 1 | 1 | 0 | 0 | 1 | 0 | AW-SER-002(1) |
| 19 | AI Agent framework LangChain+LangGraph | ~67 | 94 | 10 | 3 | 3 | 4 | 0 | AW-MEM-001(3), AW-TOOL-001(2), AW-TOOL-003(2) |
| 20 | UiPath LangGraph agents | ~67 | 191 | 6 | 2 | 3 | 1 | 0 | AW-MEM-001(2), AW-SEC-001(1), AW-RAG-001(1) |
| 21 | LangChain Weaviate integration | ~63 | 4 | 0 | 0 | 0 | 0 | 0 | — |
| 22 | LangChain stock screening agent | ~44 | 8 | 5 | 0 | 3 | 1 | 1 | AW-SER-001(2), AW-MEM-003(1), AW-SER-002(1) |
| 23 | LangChain agent for Git commands | ~44 | 8 | 6 | 0 | 0 | 3 | 3 | AW-TOOL-002(3), AW-TOOL-004(3) |
| 24 | LangChain agent + Neo4j memory | ~18 | 11 | 1 | 0 | 0 | 1 | 0 | AW-CFG-docker-no-auth(1) |

**Totals: 135 findings (8 CRITICAL, 61 HIGH) across 957 files. 20/24 have findings.**

---

## 3. Tier 3 — LlamaIndex Core

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

## 4. Tier 4 — LlamaIndex Extended

| # | Project | Stars | Files | Findings | CRIT | HIGH | MED | LOW | Top Rules |
|---|---|---|---|---|---|---|---|---|---|
| 1 | LazyLLM | ~3.7k | 399 | 21 | 0 | 17 | 4 | 0 | AW-SER-001(9), AW-CFG-hardcoded-secret(7), AW-SER-003(3) |
| 2 | ThinkRAG | ~322 | 38 | 6 | 0 | 6 | 0 | 0 | AW-MEM-003(4), AW-MEM-004(2) |
| 3 | Delphic | ~318 | 40 | 0 | 0 | 0 | 0 | 0 | — |
| 4 | local_llama | ~297 | 3 | 0 | 0 | 0 | 0 | 0 | — |
| 5 | Awesome-RAG (lucifertrj) | ~278 | 10 | 11 | 0 | 3 | 6 | 2 | AW-RAG-003(4), AW-MEM-003(2), AW-MEM-005(2) |
| 6 | VeritasGraph | ~254 | 6 | 1 | 0 | 1 | 0 | 0 | AW-CFG-hardcoded-secret(1) |
| 7 | CorpusOS | ~174 | 54 | 7 | 0 | 6 | 0 | 1 | AW-RAG-001(4), AW-MEM-002(2), AW-MEM-001(1) |
| 8 | Hello Wordsmith | ~167 | 4 | 3 | 0 | 2 | 0 | 1 | AW-MEM-003(2), AW-MEM-001(1) |
| 9 | PapersChat | ~153 | 4 | 4 | 0 | 4 | 0 | 0 | AW-MEM-003(3), AW-RAG-004(1) |
| 10 | LlamaIndex Omakase RAG | ~147 | 56 | 2 | 0 | 1 | 1 | 0 | AW-SEC-001(1), AW-CFG-docker-no-auth(1) |
| 11 | local-rag-llamaindex | ~132 | 3 | 7 | 0 | 6 | 1 | 0 | AW-RAG-004(3), AW-MEM-003(3), AW-CFG-docker-no-auth(1) |
| 12 | XRAG | ~118 | 58 | 17 | 2 | 13 | 2 | 0 | AW-MEM-003(8), AW-MEM-001(4), AW-SER-001(2) |
| 13 | flexible-graphrag | ~114 | 60 | 10 | 1 | 7 | 2 | 0 | AW-MEM-001(3), AW-RAG-004(2), AW-MEM-003(2) |
| 14 | Vector Cookbook (Timescale) | ~125 | 10 | 5 | 0 | 4 | 0 | 1 | AW-RAG-001(4), AW-TOOL-004(1) |
| 15 | DocMind AI | ~102 | 126 | 16 | 0 | 14 | 1 | 1 | AW-RAG-004(10), AW-SEC-001(3), AW-RAG-001(1) |
| 16 | RAGArch | ~87 | 1 | 5 | 0 | 4 | 1 | 0 | AW-MEM-003(3), AW-RAG-004(1), AW-SER-002(1) |
| 17 | RAG-LlamaIndex (Pinecone) | ~81 | 15 | 10 | 0 | 10 | 0 | 0 | AW-MEM-003(10) |
| 18 | RAG Job Search Assistant | ~86 | 5 | 1 | 0 | 1 | 0 | 0 | AW-MEM-003(1) |
| 19 | ingest-anything | ~89 | 8 | 4 | 0 | 3 | 1 | 0 | AW-MEM-003(3), AW-TOOL-002(1) |
| 20 | OpenInference (Arize) | ~891 | 205 | 2 | 0 | 1 | 1 | 0 | AW-RAG-001(1), AW-SER-003(1) |
| 21 | MCPAdapt | ~420 | 9 | 2 | 0 | 0 | 1 | 1 | AW-SER-002(1), AW-TOOL-004(1) |
| 22 | PlanExe | ~361 | 242 | 18 | 0 | 18 | 0 | 0 | AW-CFG-hardcoded-secret(14), AW-MCP-001(3), AW-SEC-001(1) |
| 23 | LlamaIndex Docs Agent | ~156 | 18 | 5 | 0 | 3 | 1 | 1 | AW-RAG-001(1), AW-MEM-001(1), AW-MEM-003(1) |
| 24 | LlamaIndex Trip Planner | ~49 | 7 | 0 | 0 | 0 | 0 | 0 | — |
| 25 | User-Centric RAG (LlamaIndex+Qdrant) | ~55 | 7 | 5 | 0 | 4 | 1 | 0 | AW-MEM-004(2), AW-MEM-003(2), AW-SER-002(1) |
| 26 | AgentServe | ~40 | 13 | 0 | 0 | 0 | 0 | 0 | — |
| 27 | Agentic RAG (LlamaIndex) | ~8 | 18 | 15 | 0 | 7 | 0 | 8 | AW-TOOL-004(6), AW-MEM-003(5), AW-RAG-001(2) |
| 28 | Agent-as-a-Service | ~24 | 15 | 2 | 0 | 1 | 0 | 1 | AW-MEM-003(1), AW-TOOL-004(1) |
| 29 | Workflows ACP | ~45 | 37 | 0 | 0 | 0 | 0 | 0 | — |
| 30 | Agentic AI Chatbot (LlamaIndex) | ~15 | 7 | 14 | 0 | 0 | 0 | 14 | AW-TOOL-004(14) |
| 31 | Llama-4 Researcher | ~192 | 5 | 0 | 0 | 0 | 0 | 0 | — |
| 32 | e-Library Agent | ~48 | 4 | 2 | 0 | 2 | 0 | 0 | AW-RAG-004(1), AW-MEM-003(1) |
| 33 | ragcoon | ~56 | 4 | 8 | 0 | 4 | 4 | 0 | AW-TOOL-002(4), AW-MEM-003(3), AW-RAG-004(1) |
| 34 | diRAGnosis | ~42 | 4 | 28 | 2 | 18 | 8 | 0 | AW-MEM-001(10), AW-MEM-003(8), AW-MEM-005(8) |
| 35 | Agentic PRD Generation | ~11 | 26 | 1 | 0 | 0 | 1 | 0 | AW-CFG-docker-no-auth(1) |
| 36 | LlamaIndexChat | ~45 | 2 | 1 | 0 | 1 | 0 | 0 | AW-MEM-003(1) |
| 37 | LlamaIndex Ollama Chainlit | ~20 | 2 | 3 | 0 | 3 | 0 | 0 | AW-MEM-003(3) |
| 38 | RAGIndex | ~12 | 16 | 1 | 0 | 0 | 1 | 0 | AW-CFG-docker-no-auth(1) |
| 39 | LlamaIndex Agent (Swastik) | ~10 | 2 | 3 | 0 | 1 | 2 | 0 | AW-TOOL-002(2), AW-MEM-003(1) |
| 40 | Azure LlamaIndex Sample | ~20 | 17 | 1 | 0 | 1 | 0 | 0 | AW-MEM-003(1) |
| 41 | Brainiac | ~45 | 10 | 1 | 0 | 1 | 0 | 0 | AW-SER-001(1) |
| 42 | RAG-TUI | ~21 | 20 | 0 | 0 | 0 | 0 | 0 | — |
| 43 | Chat-RAG | ~23 | 7 | 3 | 0 | 3 | 0 | 0 | AW-MEM-003(3) |
| 44 | ToK | ~28 | 2 | 16 | 0 | 16 | 0 | 0 | AW-MEM-004(8), AW-MEM-003(8) |
| 45 | Multimodal Semantic RAG | ~26 | 2 | 5 | 0 | 2 | 1 | 2 | AW-MEM-001(2), AW-RAG-001(1), AW-MEM-003(1) |
| 46 | M2M Vector Search | ~24 | 47 | 1 | 0 | 1 | 0 | 0 | AW-SER-001(1) |
| 47 | RAG Performance | ~20 | 2 | 2 | 0 | 2 | 0 | 0 | AW-RAG-002(1), AW-MEM-003(1) |
| 48 | RAG Firewall | ~19 | 26 | 5 | 0 | 4 | 0 | 1 | AW-SEC-001(3), AW-RAG-001(1), AW-MEM-001(1) |
| 49 | RAG Framework Evaluation | ~14 | 5 | 7 | 0 | 5 | 1 | 1 | AW-RAG-001(3), AW-AGT-004(1), AW-MEM-003(1) |
| 50 | RAG Ingest | ~13 | 3 | 4 | 0 | 3 | 1 | 0 | AW-MEM-003(3), AW-SER-002(1) |
| 51 | GPTStonks | ~57 | 42 | 4 | 0 | 4 | 0 | 0 | AW-MEM-003(3), AW-AGT-001(1) |
| 52 | Quackling | ~57 | 20 | 0 | 0 | 0 | 0 | 0 | — |
| 53 | GUT | ~62 | 11 | 0 | 0 | 0 | 0 | 0 | — |
| 54 | AI Equity Research Analyst | ~36 | 1 | 1 | 0 | 0 | 1 | 0 | AW-SER-002(1) |
| 55 | Opik (Comet) | ~18k | 96 | 1 | 0 | 1 | 0 | 0 | AW-MEM-003(1) |
| 56 | GPTCache | ~8k | 102 | 7 | 0 | 4 | 3 | 0 | AW-SER-001(2), AW-RAG-003(2), AW-RAG-004(1) |
| 57 | All-in-RAG | ~5k | 77 | 28 | 0 | 17 | 7 | 4 | AW-RAG-001(10), AW-RAG-003(4), AW-MEM-001(4) |
| 58 | Gerev | ~2.8k | 65 | 1 | 0 | 1 | 0 | 0 | AW-SER-001(1) |
| 59 | PyGPT (LlamaIndex) | ~1.7k | 1190 | 31 | 0 | 6 | 4 | 21 | AW-TOOL-004(18), AW-SEC-001(5), AW-MEM-001(3) |
| 60 | Judgeval | ~1k | 139 | 0 | 0 | 0 | 0 | 0 | — |
| 61 | AutoLLM | ~1k | 29 | 3 | 0 | 3 | 0 | 0 | AW-MEM-003(3) |
| 62 | RepoAgent | ~923 | 26 | 2 | 0 | 2 | 0 | 0 | AW-MEM-003(2) |
| 63 | RAG Chatbot (datvodinh) | ~638 | 29 | 4 | 0 | 3 | 1 | 0 | AW-MEM-003(3), AW-CFG-docker-no-auth(1) |
| 64 | GraphRAG Toolkit (AWS) | ~367 | 250 | 0 | 0 | 0 | 0 | 0 | — |
| 65 | Agent-Wiz | ~369 | 29 | 0 | 0 | 0 | 0 | 0 | — |
| 66 | Agentic AI Systems | ~261 | 155 | 83 | 14 | 53 | 16 | 0 | AW-MEM-001(15), AW-RAG-001(14), AW-SEC-001(13) |
| 67 | RESTai | ~200 | 95 | 15 | 0 | 7 | 7 | 1 | AW-SER-003(7), AW-SER-001(4), AW-MEM-003(2) |
| 68 | SlideSpeak | ~92 | 6 | 2 | 0 | 2 | 0 | 0 | AW-MEM-003(2) |
| 69 | Whisk | ~88 | 31 | 2 | 0 | 0 | 2 | 0 | AW-SER-003(2) |
| 70 | Airgapped Offline RAG | ~81 | 6 | 5 | 0 | 1 | 3 | 1 | AW-SEC-003(2), AW-RAG-001(1), AW-RAG-003(1) |
| 71 | FastAPI Agents | ~47 | 14 | 2 | 0 | 0 | 2 | 0 | AW-SER-003(2) |
| 72 | BentoML RAG Tutorials | ~49 | 16 | 8 | 0 | 8 | 0 | 0 | AW-MEM-003(6), AW-SEC-001(2) |
| 73 | Reliable RAG | ~41 | 4 | 1 | 0 | 1 | 0 | 0 | AW-RAG-004(1) |
| 74 | LLM Ollama LlamaIndex Bootstrap | ~47 | 4 | 1 | 0 | 1 | 0 | 0 | AW-MEM-003(1) |
| 75 | AI Playground (rokbenko) | ~321 | 42 | 6 | 0 | 3 | 1 | 2 | AW-RAG-001(2), AW-TOOL-004(2), AW-SEC-001(1) |
| 76 | Applied AI RAG Assistant | ~26 | 21 | 19 | 0 | 10 | 3 | 6 | AW-MEM-001(6), AW-RAG-001(4), AW-AGT-001(3) |
| 77 | DSPy RAG + LlamaIndex | ~27 | 1 | 2 | 0 | 2 | 0 | 0 | AW-SEC-001(2) |
| 78 | ATO Chatbot | ~21 | 7 | 11 | 0 | 7 | 2 | 2 | AW-MEM-003(5), AW-RAG-004(2), AW-MEM-001(2) |
| 79 | Ragtag Tiger | ~21 | 8 | 2 | 0 | 1 | 1 | 0 | AW-MEM-003(1), AW-SER-002(1) |
| 80 | LlamaIndex Zoom Assistant | ~15 | 2 | 1 | 0 | 0 | 1 | 0 | AW-SER-002(1) |
| 81 | LlamaIndex Retrieval API | ~14 | 7 | 3 | 0 | 2 | 1 | 0 | AW-MEM-003(2), AW-SER-002(1) |
| 82 | ChatGPT Custom Knowledge | ~136 | 3 | 1 | 0 | 0 | 1 | 0 | AW-SER-003(1) |
| 83 | Smart LLM Loader | ~75 | 6 | 0 | 0 | 0 | 0 | 0 | — |
| 84 | ChatGPT Long-Term Memory | ~62 | 18 | 1 | 0 | 1 | 0 | 0 | AW-MEM-003(1) |
| 85 | LlamaIndex Examples (alphasecio) | ~55 | 2 | 1 | 0 | 1 | 0 | 0 | AW-MEM-003(1) |
| 86 | Agentic Playground | ~53 | 44 | 2 | 0 | 1 | 1 | 0 | AW-AGT-001(1), AW-SEC-003(1) |
| 87 | IntelliWeb GPT | ~36 | 15 | 5 | 0 | 3 | 2 | 0 | AW-CFG-hardcoded-secret(2), AW-MEM-003(1), AW-SER-002(1) |
| 88 | LlamaIndex Supervisor | ~33 | 5 | 0 | 0 | 0 | 0 | 0 | — |
| 89 | Contextual Retrieval (Anthropic) | ~27 | 9 | 6 | 1 | 4 | 1 | 0 | AW-MEM-003(3), AW-MEM-001(2), AW-MEM-005(1) |
| 90 | Streaming LLM Chat | ~25 | 1 | 3 | 0 | 3 | 0 | 0 | AW-MEM-003(2), AW-MEM-004(1) |
| 91 | Docs-n-Data Knowledge App | ~24 | 11 | 0 | 0 | 0 | 0 | 0 | — |
| 92 | AgenticAI Coach | ~22 | 116 | 1 | 0 | 0 | 1 | 0 | AW-RAG-003(1) |
| 93 | GemInsights | ~20 | 23 | 2 | 0 | 1 | 1 | 0 | AW-SER-001(1), AW-SER-002(1) |
| 94 | LLM RAG | ~20 | 5 | 3 | 0 | 3 | 0 | 0 | AW-MEM-003(2), AW-MEM-004(1) |
| 95 | QuickDigest | ~44 | 1 | 1 | 0 | 1 | 0 | 0 | AW-MEM-003(1) |
| 96 | AItrika | ~36 | 32 | 7 | 0 | 7 | 0 | 0 | AW-MEM-003(7) |
| 97 | LangChain RAG DevKit | ~49 | 17 | 19 | 0 | 11 | 5 | 3 | AW-RAG-001(4), AW-RAG-003(4), AW-MEM-004(3) |
| 98 | RAG AI Voice Assistant | ~46 | 3 | 5 | 0 | 5 | 0 | 0 | AW-MEM-003(3), AW-MEM-004(1), AW-RAG-004(1) |
| 99 | Translation Agent WebUI | ~30 | 3 | 1 | 0 | 0 | 1 | 0 | AW-SER-002(1) |
| 100 | Hiflylabs Agent Demo | ~10 | 7 | 1 | 0 | 0 | 0 | 1 | AW-MEM-001(1) |
| 101 | RAG KnowledgeLLM Bot | ~13 | 4 | 1 | 0 | 1 | 0 | 0 | AW-MEM-003(1) |
| 102 | PyQt LlamaIndex | ~8 | 5 | 2 | 0 | 1 | 1 | 0 | AW-MEM-003(1), AW-SER-002(1) |
| 103 | Doppalf | ~9 | 10 | 4 | 0 | 4 | 0 | 0 | AW-CFG-hardcoded-secret(2), AW-MEM-003(2) |
| 104 | Bot-the-Defect | ~6 | 23 | 4 | 0 | 4 | 0 | 0 | AW-MEM-004(2), AW-MEM-003(2) |
| 105 | EduRAG Network Assistant | ~15 | 10 | 11 | 3 | 7 | 1 | 0 | AW-MEM-001(4), AW-RAG-001(3), AW-MEM-003(3) |
| 106 | LlamaIndex Agent Workflow Browse | ~15 | 1 | 1 | 0 | 0 | 1 | 0 | AW-SER-002(1) |
| 107 | LlamaIndex Chatbot Advanced | ~20 | 13 | 5 | 0 | 3 | 0 | 2 | AW-MEM-003(3), AW-TOOL-004(2) |
| 108 | LEANN | ~10k | 78 | 6 | 0 | 6 | 0 | 0 | AW-SER-001(6) |
| 109 | LlamaIndex RAG (romilandc) | ~15 | 1 | 4 | 0 | 3 | 1 | 0 | AW-MEM-003(2), AW-RAG-004(1), AW-SER-002(1) |
| 110 | MCP Toolbox SDK (Google) | ~167 | 38 | 0 | 0 | 0 | 0 | 0 | — |
| 111 | PromptPilot | ~71 | 20 | 0 | 0 | 0 | 0 | 0 | — |
| 112 | Jetson Orin Nano RAG Kit | ~149 | 29 | 7 | 0 | 2 | 5 | 0 | AW-TOOL-002(5), AW-SEC-001(2) |

**Totals: 634 findings (23 CRITICAL, 414 HIGH) across 4762 files. 95/112 have findings.**

---

## 5. Tier 5 — CrewAI Ecosystem

| # | Project | Stars | Files | Findings | CRIT | HIGH | MED | LOW | Top Rules |
|---|---|---|---|---|---|---|---|---|---|
| 1 | CrewAI Examples | ~3k | 116 | 0 | 0 | 0 | 0 | 0 | — |
| 2 | CrewAI Tools | ~1.4k | 163 | 4 | 0 | 1 | 3 | 0 | AW-SEC-001(1), AW-SER-002(1), AW-SER-003(1) |
| 3 | AutoGroq | ~1.5k | 40 | 2 | 0 | 0 | 2 | 0 | AW-SER-003(2) |
| 4 | MCP Memory Service | ~1.5k | 144 | 12 | 0 | 8 | 4 | 0 | AW-SEC-001(5), AW-SEC-003(4), AW-MCP-001(3) |
| 5 | CrewAI Studio | ~1.2k | 26 | 0 | 0 | 0 | 0 | 0 | — |
| 6 | Full Stack AI Agent Template | ~808 | 22 | 8 | 0 | 0 | 8 | 0 | AW-CFG-debug-mode(7), AW-CFG-docker-no-auth(1) |
| 7 | Viral Clips Crew | ~749 | 9 | 0 | 0 | 0 | 0 | 0 | — |
| 8 | AIWriteX | ~700 | 40 | 0 | 0 | 0 | 0 | 0 | — |
| 9 | Tiger (Upsonic) | ~465 | 26 | 0 | 0 | 0 | 0 | 0 | — |
| 10 | Easy Investment Agent | ~383 | 22 | 0 | 0 | 0 | 0 | 0 | — |
| 11 | Devyan | ~290 | 5 | 1 | 0 | 0 | 1 | 0 | AW-SER-002(1) |
| 12 | OpenPlexity Pages | ~253 | 17 | 0 | 0 | 0 | 0 | 0 | — |
| 13 | CrewAI Test (NanGePlus) | ~226 | 48 | 24 | 0 | 24 | 0 | 0 | AW-SEC-001(24) |
| 14 | CrewAI GUI Qt | ~206 | 18 | 0 | 0 | 0 | 0 | 0 | — |
| 15 | Wavefront | ~200 | 513 | 9 | 0 | 7 | 2 | 0 | AW-SEC-001(5), AW-SER-001(2), AW-CFG-docker-no-auth(1) |
| 16 | CrewAI UI Business Launch | ~188 | 1 | 2 | 0 | 1 | 1 | 0 | AW-SEC-001(1), AW-SER-002(1) |
| 17 | Open Extract | ~184 | 35 | 1 | 0 | 0 | 1 | 0 | AW-CFG-docker-no-auth(1) |
| 18 | CrewAI Gmail Automation | ~182 | 8 | 1 | 0 | 0 | 1 | 0 | AW-SER-002(1) |
| 19 | Value | ~169 | 8 | 3 | 0 | 2 | 1 | 0 | AW-CFG-hardcoded-secret(2), AW-CFG-docker-no-auth(1) |
| 20 | Resume Optimization Crew | ~146 | 6 | 1 | 0 | 0 | 1 | 0 | AW-SER-002(1) |
| 21 | CrewAI Stock Analysis | ~147 | 23 | 0 | 0 | 0 | 0 | 0 | — |
| 22 | Geo AI Agent | ~145 | 6 | 1 | 0 | 0 | 1 | 0 | AW-SER-002(1) |
| 23 | Trip Planner Agent | ~139 | 7 | 1 | 0 | 0 | 1 | 0 | AW-SER-002(1) |
| 24 | Paper Summarizer | ~126 | 2 | 1 | 0 | 1 | 0 | 0 | AW-SEC-001(1) |
| 25 | CrewAI Flows FullStack | ~119 | 8 | 4 | 0 | 4 | 0 | 0 | AW-SEC-001(4) |
| 26 | Agent Audit | ~117 | 58 | 26 | 0 | 26 | 0 | 0 | AW-SEC-001(26) |
| 27 | Mengram | ~112 | 40 | 4 | 0 | 4 | 0 | 0 | AW-MCP-001(2), AW-RAG-001(2) |
| 28 | FenixAI Trading Bot | ~99 | 153 | 4 | 0 | 1 | 3 | 0 | AW-SEC-003(2), AW-SER-001(1), AW-CFG-docker-no-auth(1) |
| 29 | Aitino | ~91 | 122 | 1 | 0 | 0 | 1 | 0 | AW-SEC-003(1) |
| 30 | Awesome AI Agents HUB | ~90 | 33 | 0 | 0 | 0 | 0 | 0 | — |
| 31 | Workshop AI Agent | ~88 | 37 | 27 | 0 | 12 | 12 | 3 | AW-RAG-003(5), AW-MEM-002(4), AW-TOOL-001(3) |
| 32 | Spotify Playlist (CrewAI) | ~81 | 7 | 0 | 0 | 0 | 0 | 0 | — |
| 33 | CrewAI Sheets UI | ~76 | 26 | 1 | 0 | 0 | 1 | 0 | AW-SER-002(1) |
| 34 | AI Agents with CrewAI | ~73 | 5 | 0 | 0 | 0 | 0 | 0 | — |
| 35 | AI Agents (whyash) | ~69 | - | - | - | - | - | - | not scanned |
| 36 | CrewAI Streamlit Demo | ~69 | 6 | 1 | 0 | 0 | 1 | 0 | AW-SER-002(1) |
| 37 | Agent OS | ~68 | 277 | 14 | 0 | 4 | 10 | 0 | AW-SEC-001(4), AW-CFG-docker-no-auth(4), AW-SER-003(3) |
| 38 | Eval View | ~68 | 167 | 8 | 0 | 5 | 3 | 0 | AW-SEC-001(4), AW-SEC-003(2), AW-TOOL-001(1) |
| 39 | Multi-Agents System from Scratch | ~67 | 13 | 0 | 0 | 0 | 0 | 0 | — |
| 40 | RAG Boilerplate | ~66 | 114 | 4 | 3 | 1 | 0 | 0 | AW-MEM-001(3), AW-RAG-004(1) |
| 41 | YouTube Yapper Trapper | ~66 | 5 | 1 | 0 | 1 | 0 | 0 | AW-SEC-001(1) |
| 42 | RoboCrew | ~63 | 27 | 6 | 0 | 2 | 4 | 0 | AW-TOOL-001(2), AW-TOOL-003(2), AW-AGT-003(2) |
| 43 | AISquare Studio QA | ~63 | 37 | 1 | 0 | 0 | 1 | 0 | AW-SER-002(1) |
| 44 | VN Stock Advisor | ~62 | 5 | 1 | 0 | 0 | 1 | 0 | AW-SER-002(1) |
| 45 | ComfyUI-CrewAI | ~60 | 12 | 1 | 0 | 0 | 1 | 0 | AW-SER-002(1) |
| 46 | TravelPlanner CrewAI | ~54 | 11 | 1 | 0 | 0 | 1 | 0 | AW-SER-002(1) |
| 47 | Multi-Agent RAG Template | ~53 | 7 | 1 | 0 | 0 | 1 | 0 | AW-SER-002(1) |
| 48 | Investment Agent (LangGraph+CrewAI) | ~51 | 86 | 8 | 0 | 0 | 8 | 0 | AW-SEC-003(8) |
| 49 | AI Agent Crew (Bitcoin) | ~47 | 36 | 6 | 0 | 1 | 4 | 1 | AW-AGT-003(3), AW-RAG-001(1), AW-SER-002(1) |
| 50 | AI Trading Crew | ~47 | 18 | 3 | 0 | 2 | 1 | 0 | AW-SER-001(2), AW-SER-002(1) |
| 51 | CrewAI MCP | ~40 | 5 | 0 | 0 | 0 | 0 | 0 | — |
| 52 | Email Agent | ~43 | 54 | 1 | 0 | 0 | 1 | 0 | AW-SEC-003(1) |
| 53 | Jira Tiger | ~43 | 15 | 0 | 0 | 0 | 0 | 0 | — |
| 54 | KAI | ~42 | - | - | - | - | - | - | not scanned |
| 55 | CrewAI Essay Writer | ~40 | 5 | 3 | 0 | 3 | 0 | 0 | AW-AGT-004(3) |
| 56 | LLM Agents Example | ~40 | 7 | 5 | 0 | 3 | 2 | 0 | AW-TOOL-001(2), AW-TOOL-003(2), AW-SEC-001(1) |
| 57 | Crew Llamafile | ~39 | 6 | 0 | 0 | 0 | 0 | 0 | — |
| 58 | Crew News | ~39 | 6 | 0 | 0 | 0 | 0 | 0 | — |
| 59 | CrewAI Multi-Agent (Financial) | ~37 | 3 | 2 | 0 | 1 | 0 | 1 | AW-RAG-001(1), AW-MEM-001(1) |
| 60 | AI News Researcher & Blog Writer | ~36 | 5 | 1 | 0 | 0 | 1 | 0 | AW-SER-002(1) |
| 61 | Multiagent Debugger | ~35 | 21 | 1 | 0 | 0 | 1 | 0 | AW-AGT-003(1) |
| 62 | Personal Brand Team | ~37 | 1 | 1 | 0 | 0 | 0 | 1 | AW-TOOL-004(1) |
| 63 | AgentFacts | ~33 | 55 | 1 | 0 | 0 | 1 | 0 | AW-SER-003(1) |
| 64 | AI Book Writer | ~33 | 21 | 2 | 0 | 2 | 0 | 0 | AW-CFG-hardcoded-secret(2) |
| 65 | Smart Marketing Assistant | ~32 | 9 | 2 | 0 | 0 | 2 | 0 | AW-SER-002(1), AW-TOOL-002(1) |
| 66 | Operagents | ~31 | 40 | 1 | 0 | 0 | 1 | 0 | AW-SER-003(1) |
| 67 | ContextLoom | ~31 | 11 | 1 | 0 | 1 | 0 | 0 | AW-AGT-004(1) |
| 68 | Multi-Agent Travel Advisor | ~30 | 14 | 16 | 0 | 2 | 4 | 10 | AW-TOOL-004(8), AW-RAG-003(2), AW-MEM-001(2) |
| 69 | CrewAI Qdrant Obsidian | ~29 | 18 | 0 | 0 | 0 | 0 | 0 | — |
| 70 | Multi-Agent AI Newsletter | ~28 | 5 | 0 | 0 | 0 | 0 | 0 | — |
| 71 | CV Agents | ~27 | 9 | 1 | 0 | 0 | 1 | 0 | AW-SER-002(1) |
| 72 | Smart Nutritional App | ~26 | 7 | 0 | 0 | 0 | 0 | 0 | — |
| 73 | Crewlit | ~26 | 38 | 0 | 0 | 0 | 0 | 0 | — |
| 74 | Healthcare Assistant | ~25 | 8 | 2 | 0 | 1 | 1 | 0 | AW-RAG-001(1), AW-SER-002(1) |
| 75 | Agent Kernel | ~25 | 114 | 4 | 0 | 3 | 1 | 0 | AW-SER-001(2), AW-SEC-001(1), AW-SER-003(1) |
| 76 | CrewAI Stock Trader | ~25 | 7 | 0 | 0 | 0 | 0 | 0 | — |
| 77 | Compliance Assistant (AWS) | ~24 | 3 | 2 | 0 | 1 | 1 | 0 | AW-CFG-hardcoded-secret(1), AW-SER-002(1) |
| 78 | Kalibr SDK | ~24 | 56 | 0 | 0 | 0 | 0 | 0 | — |
| 79 | Coral AI | ~23 | 25 | 1 | 0 | 0 | 0 | 1 | AW-TOOL-004(1) |
| 80 | Agentic Stock Analysis Crew | ~23 | 3 | 0 | 0 | 0 | 0 | 0 | — |
| 81 | Newsletter Agent | ~23 | 5 | 0 | 0 | 0 | 0 | 0 | — |
| 82 | Yaitec Hub Templates | ~23 | 10 | 3 | 0 | 2 | 1 | 0 | AW-RAG-001(2), AW-TOOL-002(1) |
| 83 | Agentic AI Projects | ~22 | 49 | 0 | 0 | 0 | 0 | 0 | — |
| 84 | BentoCrewAI | ~22 | 6 | 0 | 0 | 0 | 0 | 0 | — |
| 85 | CrewAI Agentic Jira | ~22 | 20 | 0 | 0 | 0 | 0 | 0 | — |
| 86 | News AI Agents (Gemini) | ~22 | 4 | 0 | 0 | 0 | 0 | 0 | — |
| 87 | Python Coding Agent | ~22 | 3 | 3 | 0 | 0 | 3 | 0 | AW-TOOL-002(2), AW-SER-002(1) |
| 88 | Market Research Agent | ~21 | 4 | 1 | 0 | 0 | 1 | 0 | AW-SER-002(1) |
| 89 | Mistral Backlinker | ~21 | 12 | 0 | 0 | 0 | 0 | 0 | — |
| 90 | TaskForce | ~21 | 45 | 4 | 0 | 1 | 2 | 1 | AW-RAG-001(1), AW-TOOL-002(1), AW-SER-003(1) |
| 91 | Graphlit Tools | ~20 | 45 | 0 | 0 | 0 | 0 | 0 | — |
| 92 | InsAIts | ~20 | 50 | 6 | 0 | 6 | 0 | 0 | AW-SEC-001(5), AW-MCP-001(1) |
| 93 | LangCrew | ~113 | 106 | 2 | 0 | 1 | 1 | 0 | AW-SEC-001(1), AW-SEC-003(1) |
| 94 | PagePod | ~19 | 4 | 1 | 0 | 0 | 1 | 0 | AW-SER-002(1) |
| 95 | Doctor Assist (CrewAI) | ~14 | 2 | 1 | 0 | 0 | 1 | 0 | AW-SER-002(1) |
| 96 | CrewAI Projects (hmnajam) | ~10 | 116 | 2 | 0 | 1 | 1 | 0 | AW-CFG-hardcoded-secret(1), AW-TOOL-002(1) |
| 97 | CrewAI Projects (lakshya) | ~10 | - | - | - | - | - | - | not scanned |
| 98 | CrewAI Multi-Agent Debate | ~5 | 2 | 1 | 0 | 0 | 1 | 0 | AW-SER-002(1) |
| 99 | MultiAgent CrewAI (Indicium) | ~5 | 5 | 0 | 0 | 0 | 0 | 0 | — |
| 100 | Investor Crew | ~10 | 4 | 0 | 0 | 0 | 0 | 0 | — |
| 101 | AIForge | ~48 | 202 | 7 | 0 | 2 | 5 | 0 | AW-SER-003(5), AW-SER-001(2) |
| 102 | Prompt Maker | ~46 | 16 | 0 | 0 | 0 | 0 | 0 | — |
| 103 | CrewAI Research Assistant | ~8 | 4 | 1 | 0 | 0 | 1 | 0 | AW-SER-002(1) |
| 104 | CrewAI experiments with local models | ~1k | 3 | 3 | 0 | 1 | 0 | 2 | AW-TOOL-004(2), AW-SEC-001(1) |
| 105 | CrewAI hierarchical tutorial | ~176 | 6 | 0 | 0 | 0 | 0 | 0 | — |
| 106 | Automate YouTube with CrewAI | ~171 | 6 | 0 | 0 | 0 | 0 | 0 | — |
| 107 | CrewAI RAG deep dive | ~152 | 6 | 2 | 0 | 0 | 0 | 2 | AW-TOOL-004(2) |
| 108 | Agency Swarm tutorial | ~72 | 4 | 0 | 0 | 0 | 0 | 0 | — |

**Totals: 278 findings (3 CRITICAL, 138 HIGH) across 3925 files. 68/108 have findings.**

---

## 6. Tier 6 — Multi-Agent Frameworks

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
| 10 | AutoGen + GraphRAG + Ollama | ~835 | 5 | 1 | 0 | 0 | 1 | 0 | AW-SER-002(1) |
| 11 | Dynamic AI agent automation platform | ~3.2k | 165 | 65 | 0 | 4 | 53 | 8 | AW-TOOL-002(51), AW-TOOL-004(8), AW-SEC-001(3) |
| 12 | Open source autonomous AI agent framework | ~17.3k | 272 | 53 | 0 | 15 | 25 | 13 | AW-TOOL-002(18), AW-TOOL-004(13), AW-MEM-003(7) |
| 13 | Fully local autonomous agent | ~25.6k | 41 | 8 | 0 | 0 | 8 | 0 | AW-TOOL-002(8) |
| 14 | GPT autonomous agent creating newspapers | ~1.5k | 12 | 3 | 0 | 2 | 1 | 0 | AW-CFG-hardcoded-secret(2), AW-SER-002(1) |
| 15 | Hierarchical Autonomous Agent Swarm | ~3.1k | 37 | 1 | 0 | 0 | 1 | 0 | AW-SER-003(1) |
| 16 | LLM agent controlling RESTful APIs | ~1.4k | 13 | 4 | 0 | 4 | 0 | 0 | AW-SER-001(4) |
| 17 | Terminal agent with local tools | ~4.2k | 229 | 2 | 0 | 0 | 2 | 0 | AW-SER-003(2) |
| 18 | Multi-Agent LLM Trading | ~35k | 58 | 0 | 0 | 0 | 0 | 0 | — |
| 19 | Zero-Code LLM Agent Framework | ~8.7k | 98 | 32 | 0 | 5 | 20 | 7 | AW-TOOL-002(11), AW-TOOL-004(7), AW-SER-003(5) |
| 20 | Low-code multi-agent with memory | ~5.7k | 1190 | 49 | 0 | 22 | 27 | 0 | AW-SER-003(21), AW-SEC-001(17), AW-SEC-003(6) |
| 21 | Multi-Agent Orchestration | ~4.1k | 90 | 3 | 0 | 1 | 2 | 0 | AW-SEC-001(1), AW-TOOL-002(1), AW-SER-003(1) |
| 22 | Multi-Agent Programming LLMs | ~3.9k | 136 | 18 | 0 | 8 | 8 | 2 | AW-MEM-003(6), AW-TOOL-002(5), AW-RAG-004(2) |
| 23 | Multi-agent poster generation | ~3.5k | 799 | 107 | 0 | 35 | 61 | 11 | AW-TOOL-002(39), AW-TOOL-001(13), AW-TOOL-003(13) |
| 24 | Multi-agent deep research | ~3.3k | 572 | 18 | 0 | 11 | 7 | 0 | AW-SER-001(7), AW-SEC-003(5), AW-SEC-001(2) |
| 25 | No-code multi-agent framework | ~2.3k | 384 | 10 | 1 | 5 | 4 | 0 | AW-MEM-003(3), AW-SER-003(3), AW-SEC-001(2) |
| 26 | LLM multi-agent framework | ~2.2k | 469 | 28 | 0 | 13 | 15 | 0 | AW-SER-003(12), AW-SER-001(4), AW-AGT-004(4) |
| 27 | LLM Agent Framework ComfyUI | ~2.1k | 129 | 29 | 7 | 12 | 10 | 0 | AW-MEM-001(7), AW-SEC-001(7), AW-RAG-003(7) |
| 28 | Agentic Memory for LLM Agents | ~926 | 4 | 4 | 0 | 4 | 0 | 0 | AW-MEM-003(4) |
| 29 | General memory for agents | ~832 | 100 | 0 | 0 | 0 | 0 | 0 | — |
| 30 | MCP long-term agent memory | ~663 | 2 | 1 | 0 | 0 | 1 | 0 | AW-SER-002(1) |
| 31 | Agency Swarm experiments | ~629 | 127 | 6 | 0 | 1 | 3 | 2 | AW-TOOL-002(3), AW-TOOL-004(2), AW-SEC-001(1) |
| 32 | Agent memory with Redis | ~207 | 52 | 10 | 0 | 3 | 7 | 0 | AW-CFG-docker-no-auth(4), AW-SEC-003(3), AW-MCP-001(2) |
| 33 | Smolagents framework examples | ~165 | 10 | 1 | 0 | 1 | 0 | 0 | AW-SEC-001(1) |
| 34 | Langroid multi-agent examples | ~148 | 5 | 0 | 0 | 0 | 0 | 0 | — |
| 35 | 7-layer memory for AI Agents | ~137 | 48 | 3 | 0 | 2 | 1 | 0 | AW-MEM-003(2), AW-TOOL-002(1) |
| 36 | DeepSearch with smolagents | ~136 | 113 | 1 | 0 | 0 | 1 | 0 | AW-SER-002(1) |
| 37 | Hallucination eval agent memory | ~115 | 10 | 0 | 0 | 0 | 0 | 0 | — |
| 38 | Autonomous agent LLM | ~91 | 1 | 0 | 0 | 0 | 0 | 0 | — |
| 39 | LLM with vector DB memory | ~53 | 7 | 1 | 0 | 1 | 0 | 0 | AW-MEM-003(1) |

**Totals: 702 findings (8 CRITICAL, 217 HIGH) across 7906 files. 33/39 have findings.**

---

## 7. Tier 7 — OpenAI Agents SDK

| # | Project | Stars | Files | Findings | CRIT | HIGH | MED | LOW | Top Rules |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Customer service Agents SDK demo | ~5.9k | 10 | 0 | 0 | 0 | 0 | 0 | — |
| 2 | Deep research with Agents SDK | ~745 | 26 | 1 | 0 | 0 | 1 | 0 | AW-SER-002(1) |
| 3 | OpenAI function calling + Deep Lake | ~357 | - | - | - | - | - | - | not scanned |
| 4 | MCP server multi-framework | ~154 | 2 | 1 | 0 | 0 | 1 | 0 | AW-SER-002(1) |
| 5 | OpenAI function calling helpers | ~82 | 7 | 0 | 0 | 0 | 0 | 0 | — |
| 6 | OpenAI Functions JSON metadata | ~70 | 7 | 0 | 0 | 0 | 0 | 0 | — |
| 7 | Financial agent OpenAI SDK | ~35 | 84 | 1 | 0 | 0 | 1 | 0 | AW-SER-002(1) |
| 8 | Multi-agent investment research | ~27 | 18 | 3 | 0 | 1 | 2 | 0 | AW-TOOL-001(1), AW-SER-002(1), AW-TOOL-003(1) |

**Totals: 6 findings (0 CRITICAL, 1 HIGH) across 154 files. 4/8 have findings.**

---

## 8. Tier 8 — Pydantic AI

| # | Project | Stars | Files | Findings | CRIT | HIGH | MED | LOW | Top Rules |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Pydantic AI agents tutorial | ~146 | 14 | 4 | 0 | 0 | 4 | 0 | AW-TOOL-002(4) |
| 2 | Agentic RAG with Pydantic AI | ~498 | 102 | 0 | 0 | 0 | 0 | 0 | — |
| 3 | AI observability for agents | ~4.1k | 118 | 4 | 0 | 2 | 2 | 0 | AW-SEC-001(2), AW-SEC-003(1), AW-SER-003(1) |
| 4 | AI web framework FastAPI+Pydantic | ~840 | 27 | 1 | 0 | 0 | 1 | 0 | AW-SER-003(1) |
| 5 | Airflow + Pydantic AI agents | ~523 | 12 | 0 | 0 | 0 | 0 | 0 | — |
| 6 | Deep Agent on Pydantic-AI | ~507 | 61 | 0 | 0 | 0 | 0 | 0 | — |
| 7 | PydanticAI research agent | ~130 | 21 | 2 | 0 | 2 | 0 | 0 | AW-SER-001(2) |
| 8 | MongoDB RAG with Pydantic AI | ~102 | 21 | 0 | 0 | 0 | 0 | 0 | — |

**Totals: 11 findings (0 CRITICAL, 4 HIGH) across 376 files. 4/8 have findings.**

---

## 9. Tier 9 — GraphRAG

| # | Project | Stars | Files | Findings | CRIT | HIGH | MED | LOW | Top Rules |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Graph-based RAG retrieval | ~3.7k | 30 | 6 | 0 | 6 | 0 | 0 | AW-SER-001(6) |
| 2 | GraphRAG with local LLMs | ~2.3k | 399 | 15 | 0 | 6 | 5 | 4 | AW-TOOL-002(4), AW-TOOL-004(4), AW-CFG-hardcoded-secret(3) |
| 3 | GraphRAG + Ollama local models | ~1.1k | 391 | 3 | 0 | 3 | 0 | 0 | AW-RAG-001(3) |
| 4 | Neo4j GraphRAG Python | ~1.1k | 102 | 1 | 0 | 0 | 1 | 0 | AW-SER-003(1) |
| 5 | Production GraphRAG + AI agents | ~1.1k | 289 | 6 | 0 | 4 | 2 | 0 | AW-RAG-004(2), AW-MEM-003(2), AW-SEC-003(1) |
| 6 | GraphRAG + LightRAG + Neo4j | ~2k | 222 | 9 | 0 | 6 | 3 | 0 | AW-SER-001(4), AW-TOOL-002(2), AW-RAG-001(1) |
| 7 | Graph Retriever for QA | ~538 | 26 | 12 | 0 | 12 | 0 | 0 | AW-SER-001(12) |

**Totals: 52 findings (0 CRITICAL, 37 HIGH) across 1459 files. 7/7 have findings.**

---

## 10. Tier 10 — DSPy

| # | Project | Stars | Files | Findings | CRIT | HIGH | MED | LOW | Top Rules |
|---|---|---|---|---|---|---|---|---|---|
| 1 | DSPy+Weaviate retrieval | ~94 | 61 | 0 | 0 | 0 | 0 | 0 | — |

**Totals: 0 findings (0 CRITICAL, 0 HIGH) across 61 files. 0/1 have findings.**

---

## 11. Tier 11 — RAG Applications

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
| 15 | Enterprise RAG pipeline framework | ~14.9k | 40 | 10 | 0 | 3 | 7 | 0 | AW-SER-003(5), AW-RAG-004(2), AW-TOOL-002(2) |
| 16 | ColBERT late-interaction for RAG | ~3.9k | 19 | 1 | 0 | 0 | 1 | 0 | AW-SER-002(1) |
| 17 | Multi-query + Reciprocal Rank Fusion | ~908 | 7 | 2 | 0 | 2 | 0 | 0 | AW-MEM-003(2) |
| 18 | Advanced RAG pipeline from scratch | ~860 | 4 | 1 | 0 | 1 | 0 | 0 | AW-MEM-003(1) |
| 19 | Super performant RAG pipelines | ~389 | 33 | 0 | 0 | 0 | 0 | 0 | — |
| 20 | Educational production RAG | ~548 | 69 | 11 | 0 | 10 | 1 | 0 | AW-CFG-hardcoded-secret(8), AW-CFG-no-tls(1), AW-RAG-004(1) |
| 21 | Python RAG toolkit with DuckDB | ~1.1k | 25 | 6 | 0 | 3 | 1 | 2 | AW-MEM-001(2), AW-SER-001(1), AW-RAG-001(1) |
| 22 | Azure OpenAI RAG at scale | ~1.1k | 9 | 4 | 0 | 0 | 3 | 1 | AW-SEC-003(2), AW-TOOL-002(1), AW-TOOL-004(1) |
| 23 | Azure RAG sample app | ~7.6k | 49 | 1 | 0 | 1 | 0 | 0 | AW-SEC-001(1) |
| 24 | RAG hallucination detection | ~534 | 34 | 0 | 0 | 0 | 0 | 0 | — |
| 25 | Rule-based retrieval with Pinecone | ~249 | 7 | 2 | 0 | 1 | 1 | 0 | AW-MEM-003(1), AW-SER-002(1) |
| 26 | Production RAG with 6 vector DB swaps | ~115 | 279 | 15 | 0 | 12 | 3 | 0 | AW-RAG-004(5), AW-SEC-001(3), AW-RAG-003(2) |
| 27 | RAG with Docling + ChromaDB | ~125 | 185 | 30 | 4 | 21 | 5 | 0 | AW-MEM-001(9), AW-MEM-003(7), AW-RAG-001(4) |
| 28 | Vectara agentic RAG Python | ~114 | 27 | 9 | 0 | 5 | 2 | 2 | AW-SER-001(3), AW-SER-003(2), AW-TOOL-004(2) |
| 29 | RAG chatbot from documents | ~393 | 59 | 16 | 1 | 5 | 8 | 2 | AW-RAG-003(4), AW-MEM-001(3), AW-RAG-001(3) |
| 30 | Local RAG with open-source LLMs | ~735 | 17 | 3 | 0 | 3 | 0 | 0 | AW-SEC-001(2), AW-MEM-003(1) |
| 31 | Production agentic RAG course | ~4.3k | 97 | 2 | 0 | 2 | 0 | 0 | AW-SEC-001(1), AW-MEM-003(1) |
| 32 | Production LLM+RAG with LLMOps | ~4.3k | 150 | 2 | 0 | 1 | 1 | 0 | AW-RAG-004(1), AW-CFG-docker-no-auth(1) |
| 33 | NVIDIA RAG chatbots Windows | ~3.1k | 44 | 8 | 0 | 5 | 1 | 2 | AW-MEM-003(2), AW-MEM-001(2), AW-SEC-001(1) |
| 34 | YouTube Full Text Search CLI | ~1.8k | 14 | 0 | 0 | 0 | 0 | 0 | — |
| 35 | On-premises conversational RAG | ~1k | 22 | 8 | 0 | 7 | 1 | 0 | AW-RAG-004(4), AW-RAG-001(2), AW-MCP-001(1) |
| 36 | MCP knowledge graph RAG | ~758 | 9 | 1 | 0 | 1 | 0 | 0 | AW-MEM-003(1) |
| 37 | Forward-Looking Active REtrieval | ~666 | 8 | 3 | 0 | 0 | 2 | 1 | AW-TOOL-002(1), AW-SEC-003(1), AW-TOOL-004(1) |
| 38 | Visual Document RAG agents | ~645 | 15 | 9 | 0 | 3 | 2 | 4 | AW-MEM-001(4), AW-MEM-003(2), AW-MEM-005(2) |
| 39 | RAG retrieval + re-ranking toolkit | ~600 | 317 | 37 | 0 | 37 | 0 | 0 | AW-SER-001(36), AW-RAG-001(1) |
| 40 | Hierarchical knowledge RAG | ~525 | 35 | 0 | 0 | 0 | 0 | 0 | — |
| 41 | Multimodal RAG Framework | ~486 | 221 | 12 | 0 | 7 | 5 | 0 | AW-SER-001(7), AW-SER-003(5) |
| 42 | Corrective RAG | ~448 | 0 | 0 | 0 | 0 | 0 | 0 | — |
| 43 | RAG with txtai | ~445 | 1 | 0 | 0 | 0 | 0 | 0 | — |
| 44 | Text-to-SQL RAG with ChromaDB+FAISS | ~438 | 28 | 6 | 0 | 4 | 2 | 0 | AW-MEM-003(2), AW-TOOL-001(1), AW-RAG-004(1) |
| 45 | Personal knowledge base RAG | ~437 | 2 | 2 | 0 | 2 | 0 | 0 | AW-SER-001(2) |
| 46 | MultiHop RAG evaluation | ~427 | 16 | 5 | 0 | 3 | 1 | 1 | AW-SER-001(1), AW-RAG-001(1), AW-MEM-003(1) |
| 47 | Agentic RAG via RL | ~397 | 40 | 5 | 0 | 5 | 0 | 0 | AW-SER-001(5) |
| 48 | Agentic RAG from GitHub repos | ~318 | 21 | 3 | 0 | 1 | 2 | 0 | AW-SEC-001(1), AW-SER-002(1), AW-SEC-003(1) |
| 49 | RAG on codebases with LanceDB | ~283 | 8 | 0 | 0 | 0 | 0 | 0 | — |
| 50 | Local LLM with RAG | ~272 | 6 | 0 | 0 | 0 | 0 | 0 | — |
| 51 | Complex reasoning agentic RAG | ~252 | 14 | 2 | 0 | 2 | 0 | 0 | AW-SER-001(2) |
| 52 | AI-powered local chatbot | ~250 | 22 | 9 | 0 | 8 | 1 | 0 | AW-RAG-004(4), AW-SEC-001(2), AW-CFG-hardcoded-secret(1) |
| 53 | Air-gapped LLMs toolkit | ~224 | 10 | 9 | 0 | 5 | 1 | 3 | AW-MEM-001(3), AW-RAG-004(2), AW-RAG-001(2) |
| 54 | Hybrid RAG vector+graph | ~205 | 43 | 3 | 0 | 2 | 1 | 0 | AW-RAG-004(1), AW-MEM-003(1), AW-CFG-docker-no-auth(1) |
| 55 | Naive to Agentic to GraphRAG | ~170 | 49 | 26 | 1 | 8 | 5 | 12 | AW-MEM-001(13), AW-RAG-001(6), AW-TOOL-002(2) |
| 56 | GPT with web browsing | ~169 | 7 | 1 | 0 | 0 | 0 | 1 | AW-MEM-001(1) |
| 57 | ChromaDB-based memory | ~147 | 32 | 21 | 6 | 7 | 5 | 3 | AW-MEM-001(6), AW-MEM-003(4), AW-TOOL-004(3) |
| 58 | Multimodal RAG with Milvus | ~135 | 3 | 0 | 0 | 0 | 0 | 0 | — |
| 59 | Local RAG with Qdrant | ~122 | 9 | 1 | 0 | 0 | 0 | 1 | AW-MEM-001(1) |
| 60 | Privacy-first multimodal RAG | ~109 | 16 | 11 | 0 | 6 | 3 | 2 | AW-RAG-001(4), AW-MEM-001(2), AW-SER-001(1) |
| 61 | Agentic RAG for drug intelligence | ~97 | 436 | 6 | 0 | 2 | 4 | 0 | AW-SER-001(2), AW-SER-003(2), AW-RAG-003(2) |
| 62 | Agentic RAG for small LMs | ~92 | 46 | 2 | 0 | 0 | 2 | 0 | AW-SER-003(2) |
| 63 | Multi-agent RAG with Qdrant | ~85 | 31 | 15 | 1 | 12 | 2 | 0 | AW-RAG-002(5), AW-AGT-004(5), AW-CFG-docker-no-auth(2) |
| 64 | Local RAG Ollama+ChromaDB | ~78 | 6 | 13 | 1 | 6 | 4 | 2 | AW-MEM-001(3), AW-MEM-003(3), AW-RAG-003(3) |
| 65 | Containerized RAG with Qdrant | ~76 | 10 | 2 | 0 | 2 | 0 | 0 | AW-CFG-hardcoded-secret(2) |
| 66 | Chat PDF LangChain+ChromaDB | ~71 | 2 | 6 | 0 | 2 | 3 | 1 | AW-RAG-003(2), AW-RAG-001(1), AW-MEM-003(1) |
| 67 | RAG ops with cache layers | ~70 | 41 | 15 | 0 | 9 | 6 | 0 | AW-SER-001(2), AW-RAG-001(2), AW-MEM-003(2) |
| 68 | Semantic search for Gmail | ~69 | 24 | 1 | 0 | 1 | 0 | 0 | AW-MEM-003(1) |
| 69 | LLMs + vector stores framework | ~66 | 50 | 4 | 0 | 4 | 0 | 0 | AW-RAG-004(2), AW-MEM-003(2) |
| 70 | Agentic RAG FAISS+BM25 | ~65 | 39 | 6 | 0 | 4 | 2 | 0 | AW-MEM-003(2), AW-SER-001(1), AW-RAG-004(1) |
| 71 | Search PDF LangChain+ChromaDB | ~62 | 3 | 7 | 0 | 1 | 4 | 2 | AW-RAG-003(2), AW-MEM-001(2), AW-MEM-003(1) |
| 72 | Chat with docs multi-LLM | ~48 | 36 | 15 | 0 | 6 | 6 | 3 | AW-RAG-003(4), AW-RAG-004(3), AW-MEM-001(3) |
| 73 | LangChain Pinecone RAG | ~47 | 5 | 14 | 1 | 7 | 3 | 3 | AW-MEM-003(5), AW-MEM-001(4), AW-MEM-005(3) |
| 74 | Multimodal RAG semantic search | ~41 | 32 | 0 | 0 | 0 | 0 | 0 | — |

**Totals: 536 findings (25 CRITICAL, 312 HIGH) across 5054 files. 63/74 have findings.**

---

## 12. Tier 12 — Vector Store Ecosystems

| # | Project | Stars | Files | Findings | CRIT | HIGH | MED | LOW | Top Rules |
|---|---|---|---|---|---|---|---|---|---|
| 1 | ChromaDB | ~17k | 148 | 5 | 0 | 3 | 2 | 0 | AW-SER-003(2), AW-SEC-001(1), AW-SER-001(1) |
| 2 | Milvus Bootcamp | ~2k | 78 | 10 | 1 | 6 | 3 | 0 | AW-SER-001(5), AW-CFG-docker-no-auth(3), AW-MEM-001(1) |
| 3 | Qdrant Examples | ~500 | 4 | 4 | 0 | 4 | 0 | 0 | AW-MEM-003(4) |
| 4 | LanceDB | ~5k | 71 | 4 | 0 | 0 | 3 | 1 | AW-TOOL-002(2), AW-CFG-debug-mode(1), AW-TOOL-004(1) |
| 5 | Agent memory with ChromaDB | ~233 | 12 | 1 | 0 | 1 | 0 | 0 | AW-MEM-003(1) |
| 6 | Chat with PDF using embeddings | ~841 | 14 | 1 | 0 | 1 | 0 | 0 | AW-SER-001(1) |
| 7 | Multimodal data representation | ~3.1k | 146 | 5 | 0 | 5 | 0 | 0 | AW-MEM-003(3), AW-SER-001(2) |
| 8 | Prompt testing for LLMs+vector DBs | ~3k | 80 | 7 | 0 | 6 | 1 | 0 | AW-SER-001(4), AW-MEM-003(2), AW-TOOL-002(1) |
| 9 | Qdrant MCP server | ~1.3k | 15 | 0 | 0 | 0 | 0 | 0 | — |
| 10 | Python Qdrant client | ~1.2k | 118 | 2 | 0 | 2 | 0 | 0 | AW-SER-001(2) |
| 11 | AI spreadsheet with LLM pipelines | ~1.1k | 93 | 8 | 0 | 7 | 1 | 0 | AW-SEC-001(5), AW-SER-001(2), AW-SEC-003(1) |
| 12 | Graph-vector memory service | ~668 | 64 | 1 | 0 | 0 | 1 | 0 | AW-SEC-003(1) |
| 13 | OSINT analysis with embeddings | ~498 | 18 | 4 | 0 | 4 | 0 | 0 | AW-MEM-003(2), AW-RAG-004(1), AW-RAG-001(1) |
| 14 | AI Assistant with Qdrant | ~314 | 63 | 142 | 0 | 136 | 3 | 3 | AW-MEM-003(82), AW-RAG-004(54), AW-TOOL-002(3) |
| 15 | Conversational agent Qdrant | ~247 | 25 | 2 | 1 | 0 | 1 | 0 | AW-MEM-001(1), AW-CFG-docker-no-auth(1) |
| 16 | Weaviate Python client | ~217 | 431 | 15 | 0 | 12 | 2 | 1 | AW-MEM-003(8), AW-RAG-004(4), AW-TOOL-002(1) |
| 17 | Reverse image search CLIP+Qdrant | ~185 | 46 | 1 | 0 | 0 | 1 | 0 | AW-CFG-docker-no-auth(1) |
| 18 | Document app Qdrant+BGE | ~151 | 3 | 7 | 0 | 3 | 2 | 2 | AW-MEM-001(2), AW-RAG-004(1), AW-RAG-001(1) |
| 19 | ChromaDB chatbot | ~145 | 2 | 4 | 0 | 2 | 2 | 0 | AW-MEM-003(2), AW-RAG-003(2) |
| 20 | ETL for vector databases | ~108 | 36 | 4 | 0 | 4 | 0 | 0 | AW-MEM-003(4) |
| 21 | Weaviate Agent Skills | ~69 | 0 | 0 | 0 | 0 | 0 | 0 | — |

**Totals: 227 findings (2 CRITICAL, 196 HIGH) across 1467 files. 19/21 have findings.**

---

## 13. Tier 13 — Memory & Knowledge Systems

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

## 14. Tier 14 — Chatbot / Assistant Frameworks

| # | Project | Stars | Files | Findings | CRIT | HIGH | MED | LOW | Top Rules |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Open WebUI | ~124k | 163 | 8 | 0 | 7 | 0 | 1 | AW-RAG-004(5), AW-RAG-001(1), AW-MEM-003(1) |
| 2 | Khoj | ~33k | 110 | 5 | 0 | 3 | 2 | 0 | AW-SER-001(2), AW-SEC-003(2), AW-SEC-001(1) |
| 3 | PyGPT | ~3k | 1190 | 31 | 0 | 6 | 4 | 21 | AW-TOOL-004(18), AW-SEC-001(5), AW-MEM-001(3) |
| 4 | Jan | ~25k | 5 | 5 | 0 | 0 | 5 | 0 | AW-TOOL-002(5) |

**Totals: 49 findings (0 CRITICAL, 16 HIGH) across 1468 files. 4/4 have findings.**

---

## 15. Tier 15 — Code / Dev Agents

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

## 16. Tier 16 — Production Agent Platforms

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

## 17. Tier 17 — Small / Niche Projects

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

## 18. Grand Summary

| Metric | Value |
|---|---|
| Total projects | 486 |
| Projects scanned | 480 |
| Projects with findings | 380 (79%) |
| Total files scanned | 48,618 |
| Total findings | 3679 |
| CRITICAL | 139 |
| HIGH | 1900 |
| Findings per file | 0.076 |

### Category Comparison

| Category | Projects | Scanned | With Findings | Findings | CRIT | HIGH | Files |
|---|---|---|---|---|---|---|---|
| LangChain Ecosystem (>2k stars) | 26 | 26 | 21 | 517 | 50 | 214 | 8,881 |
| LangChain Extended | 24 | 24 | 20 | 135 | 8 | 61 | 957 |
| LlamaIndex Core | 12 | 11 | 9 | 147 | 14 | 103 | 1,020 |
| LlamaIndex Extended | 112 | 112 | 95 | 634 | 23 | 414 | 4,762 |
| CrewAI Ecosystem | 108 | 105 | 68 | 278 | 3 | 138 | 3,925 |
| Multi-Agent Frameworks | 39 | 39 | 33 | 702 | 8 | 217 | 7,906 |
| OpenAI Agents SDK | 8 | 7 | 4 | 6 | 0 | 1 | 154 |
| Pydantic AI | 8 | 8 | 4 | 11 | 0 | 4 | 376 |
| GraphRAG | 7 | 7 | 7 | 52 | 0 | 37 | 1,459 |
| DSPy | 1 | 1 | 0 | 0 | 0 | 0 | 61 |
| RAG Applications | 74 | 74 | 63 | 536 | 25 | 312 | 5,054 |
| Vector Store Ecosystems | 21 | 21 | 19 | 227 | 2 | 196 | 1,467 |
| Memory & Knowledge Systems | 6 | 6 | 5 | 41 | 0 | 25 | 2,302 |
| Chatbot / Assistant Frameworks | 4 | 4 | 4 | 49 | 0 | 16 | 1,468 |
| Code / Dev Agents | 6 | 6 | 6 | 48 | 0 | 13 | 1,075 |
| Production Agent Platforms | 11 | 11 | 9 | 208 | 4 | 113 | 7,318 |
| Small / Niche Projects | 19 | 18 | 13 | 88 | 2 | 36 | 433 |

---

## 19. Rule Distribution

| Rule | Count | % | Description |
|---|---|---|---|
| AW-MEM-003 | 539 | 15% | Memory backend has no access control |
| AW-TOOL-002 | 396 | 11% | Tool accepts arbitrary code execution |
| AW-MEM-001 | 323 | 9% | No tenant isolation in vector store |
| AW-TOOL-004 | 287 | 8% | Tool has no description |
| AW-SEC-001 | 272 | 7% | Hardcoded API key/secret in agent config |
| AW-SER-001 | 267 | 7% | Unsafe deserialization |
| AW-RAG-001 | 241 | 7% | Retrieved context without delimiters |
| AW-SER-003 | 227 | 6% | Dynamic import with variable argument |
| AW-RAG-004 | 177 | 5% | Vector store exposed without auth |
| AW-RAG-003 | 151 | 4% | Unencrypted local vector store |
| AW-SEC-003 | 124 | 3% | Agent context logged at DEBUG level |
| AW-MEM-005 | 95 | 3% | No sanitization on retrieved memory |
| AW-TOOL-001 | 85 | 2% | Destructive tool without approval gate |
| AW-TOOL-003 | 85 | 2% | High-risk tool lacks scope check |
| AW-SER-002 | 71 | 2% | Unpinned agent framework dependency |
| AW-CFG-hardcoded-secret | 70 | 2% | AW-CFG-hardcoded-secret |
| AW-AGT-004 | 48 | 1% | LLM output stored to memory without validation |
| AW-CFG-docker-no-auth | 47 | 1% | AW-CFG-docker-no-auth |
| AW-MEM-004 | 47 | 1% | Injection patterns in retrieval path |
| AW-MEM-002 | 41 | 1% | Shared collection without retrieval filter |
| AW-AGT-001 | 21 | 1% | Sub-agent inherits full parent tool set |
| AW-MCP-001 | 20 | 1% | MCP server without authentication |
| AW-RAG-002 | 18 | 0% | Ingestion from untrusted source |
| AW-AGT-003 | 14 | 0% | Agent has read+write+delete without approval |
| AW-CFG-debug-mode | 9 | 0% | AW-CFG-debug-mode |
| AW-MCP-002 | 2 | 0% | Static token in MCP config |
| AW-CFG-no-tls | 2 | 0% | AW-CFG-no-tls |

---

## 20. False Positive Estimation

Based on manual triage of 98 findings against real source code (2026-03-20).

| Rule | Count | Sampled | TP | FP | FP Rate | Est. FP in Benchmark | Mitigation |
|---|---|---|---|---|---|---|---|
| AW-MEM-003 | 539 | — | — | — | ~15% (est.) | ~80 | Not triaged |
| AW-TOOL-002 | 396 | — | — | — | ~15% (est.) | ~59 | Not triaged |
| AW-MEM-001 | 323 | 13 | 0 | 13 | 100% | ~323 | Skip library code, require multi-tenant evidence |
| AW-TOOL-004 | 287 | — | — | — | ~15% (est.) | ~43 | Not triaged |
| AW-SEC-001 | 272 | — | — | — | ~15% (est.) | ~40 | Not triaged |
| AW-SER-001 | 267 | — | — | — | ~15% (est.) | ~40 | Not triaged |
| AW-RAG-001 | 241 | — | — | — | ~15% (est.) | ~36 | Not triaged |
| AW-SER-003 | 227 | 30 | 16 | 14 | 47% | ~105 | Suppress dict-lookup imports, variable indirection |
| AW-RAG-004 | 177 | — | — | — | ~15% (est.) | ~26 | Not triaged |
| AW-RAG-003 | 151 | — | — | — | ~15% (est.) | ~22 | Not triaged |
| AW-SEC-003 | 124 | 30 | 14 | 16 | 53% | ~66 | Require content reference, not metadata access |
| AW-MEM-005 | 95 | 9 | 2 | 7 | 78% | ~73 | Require retrieval-to-sink path |
| AW-TOOL-001 | 85 | — | — | — | ~15% (est.) | ~12 | Not triaged |
| AW-TOOL-003 | 85 | — | — | — | ~15% (est.) | ~12 | Not triaged |
| AW-SER-002 | 71 | — | — | — | ~15% (est.) | ~10 | Not triaged |
| AW-CFG-hardcoded-secret | 70 | 16 | 4 | 12 | 75% | ~52 | Skip templates, placeholders, non-secret keys |
| AW-AGT-004 | 48 | — | — | — | ~15% (est.) | ~7 | Not triaged |
| AW-CFG-docker-no-auth | 47 | — | — | — | ~15% (est.) | ~7 | Not triaged |
| AW-MEM-004 | 47 | — | — | — | ~15% (est.) | ~7 | Not triaged |
| AW-MEM-002 | 41 | — | — | — | ~15% (est.) | ~6 | Not triaged |
| AW-AGT-001 | 21 | — | — | — | ~15% (est.) | ~3 | Not triaged |
| AW-MCP-001 | 20 | — | — | — | ~15% (est.) | ~3 | Not triaged |
| AW-RAG-002 | 18 | — | — | — | ~15% (est.) | ~2 | Not triaged |
| AW-AGT-003 | 14 | — | — | — | ~15% (est.) | ~2 | Not triaged |
| AW-CFG-debug-mode | 9 | — | — | — | ~15% (est.) | ~1 | Not triaged |
| AW-MCP-002 | 2 | — | — | — | ~15% (est.) | ~0 | Not triaged |
| AW-CFG-no-tls | 2 | — | — | — | ~15% (est.) | ~0 | Not triaged |

**Estimated totals:** 3679 findings → ~2642 true positives, ~1037 false positives (28% est. FP rate)

*FP rates for triaged rules are based on manual verification of real source code.
Untriaged rules use 15% conservative estimate. Actual FP rate may vary.*

---

## 21. Attack Vector Coverage (9 / 35 Detectable)

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
| **AW-ATK-AGT-001** | Tool Poisoning / Unsafe Tool Access | 7-layer memory for AI Agents, AI Agent Crew (Bitcoin), AI Agent framework LangChain+LangGraph, AI Assistant with Qdrant, AI Coding Agent with LangGraph, Agency Swarm experiments, Agent OS, Agentic AI Systems, Agentic Playground, Agentic RAG FAISS+BM25 (+71 more) | 601 | `agents_registry.py:140` (AW-AGT-001) |
| **AW-ATK-AGT-004** | Cross-Agent Memory Contamination | AdalFlow, Agentic AI Systems, All-in-RAG, Awesome LLM Apps, ChromaDB-based memory, ContextLoom, CrewAI Essay Writer, LLM multi-agent framework, LangChain (mono), Multi-agent RAG with Qdrant (+5 more) | 48 | `vectorstore.py:107` (AW-AGT-004) |
| **AW-ATK-CFG-001** | Unsafe Reset Enabled | Full Stack AI Agent Template, LanceDB, Production RAG with 6 vector DB swaps | 9 | `docker-compose.yml:19` (AW-CFG-debug-mode) |
| **AW-ATK-CFG-003** | No TLS / No Auth / Exposed Ports | AI Assistant with Qdrant, AI Playground (rokbenko), AI-powered local chatbot, ATO Chatbot, Agent OS, Agent memory with Redis, AgentOps, Agentic PRD Generation, Agentic RAG FAISS+BM25, Agentic incident management LangGraph (+82 more) | 246 | `vector_store_component.py:112` (AW-RAG-004) |
| **AW-ATK-CFG-004** | Hardcoded API Keys | AI Book Writer, AI Playground (rokbenko), AI observability for agents, AI spreadsheet with LLM pipelines, AI-powered local chatbot, AdalFlow, Agency Swarm experiments, Agent Audit, Agent Kernel, Agent OS (+87 more) | 344 | `settings.py:452` (AW-SEC-001) |
| **AW-ATK-INJ-001** | Stored Prompt Injection | AI Agent Crew (Bitcoin), AI Agent framework LangChain+LangGraph, AI Chatbot with LangChain, AI Playground (rokbenko), AI-powered local chatbot, ATO Chatbot, Agentic AI Systems, Agentic RAG (LlamaIndex), Agno (Phidata), Aider (+95 more) | 336 | `file_chat.py:66` (AW-RAG-001) |
| **AW-ATK-MEM-001** | Cross-Tenant Retrieval (No Filter) | AI Agent Crew (Bitcoin), AI Agent framework LangChain+LangGraph, AI Chatbot with LangChain, ATO Chatbot, Agentic AI Systems, Agentic RAG (LlamaIndex), Agno (Phidata), Aider, Air-gapped LLMs toolkit, Airgapped Offline RAG (+79 more) | 323 | `milvus_kb_service.py:100` (AW-MEM-001) |
| **AW-ATK-MEM-002** | Weak Tenant Isolation (Static Filter) | Agentic AI Systems, Agno (Phidata), All-in-RAG, Awesome LLM Apps, CorpusOS, DocsGPT, LangChain (mono), Langchain-Chatchat, Langflow, Low-code multi-agent with memory (+5 more) | 41 | `ensemble.py:27` (AW-MEM-002) |
| **AW-ATK-MEM-003** | Namespace/Collection Confusion | 7-layer memory for AI Agents, AI Assistant with Qdrant, AItrika, ATO Chatbot, Advanced RAG pipeline from scratch, Agent memory with ChromaDB, Agent memory with Redis, Agent-as-a-Service, Agentic AI Systems, Agentic Memory for LLM Agents (+143 more) | 539 | `chromadb_kb_service.py:67` (AW-MEM-003) |
| **AW-ATK-MEM-004** | Partition Bypass via Direct API | AWS Bedrock LangChain agent, Agentic AI Systems, Applied AI RAG Assistant, Bot-the-Defect, Chat with docs using LangChain+Ollama, GPT4 LangChain research agent, LLM RAG, LangChain (mono), LangChain RAG DevKit, LangChain Streamlit Agent (+10 more) | 47 | `vectorstore_token_buffer_memory.py:120` (AW-MEM-004) |
| **AW-ATK-POI-005** | Document Loader Exploitation | Agno (Phidata), Awesome LLM Apps, Dify, Multi-agent RAG with Qdrant, RAG Performance, SEC Insights | 18 | `qwen_local_rag_agent.py:234` (AW-RAG-002) |

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

## 22. Attack Vector Heatmap (Per Project)

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

## 23. How to Reproduce

```bash
pip install -e ".[dev]"
./scripts/benchmark3000.sh
```

### Environment Variables

| Variable | Default | Description |
|---|---|---|
| `MAX_PARALLEL` | 4 | Parallel git clone jobs |
| `SCAN_TIMEOUT` | 300 | Per-project scan timeout (seconds) |
