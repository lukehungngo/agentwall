# AgentWall — Solo-Engineer PRD v2

## Product Requirements Document, Technical Specification & Market Analysis

**Version:** 2.0 — Solo-Engineer Edition
**Date:** 2026-03-17
**Author:** SoH Engineering
**Status:** Draft — Ready for execution
**Classification:** Internal — Confidential

---

## Table of Contents

**Part I — Market Intelligence**
1. [Market Landscape](#1-market-landscape)
2. [Competitive Analysis](#2-competitive-analysis)
3. [Threat Assessment & Attack Research](#3-threat-assessment--attack-research)
4. [Strategic Positioning](#4-strategic-positioning)

**Part II — Scope Decisions**
5. [What We Cut and Why](#5-what-we-cut-and-why)
6. [What We Keep and Why](#6-what-we-keep-and-why)

**Part III — Product Specification**
7. [Executive Summary](#7-executive-summary)
8. [Product Vision (Revised)](#8-product-vision-revised)
9. [Target Persona](#9-target-persona)
10. [Functional Requirements](#10-functional-requirements)
11. [Non-Functional Requirements](#11-non-functional-requirements)
12. [Constraints](#12-constraints)
13. [Potential Technical Blockages](#13-potential-technical-blockages)

**Part IV — Technical Architecture**
14. [High-Level Architecture](#14-high-level-architecture)
15. [Directory Structure](#15-directory-structure)
16. [Technology Stack](#16-technology-stack)
17. [Data Flow](#17-data-flow)
18. [Data Model](#18-data-model)

**Part V — Execution**
19. [3-Week Sprint Plan](#19-3-week-sprint-plan)
20. [Success Metrics](#20-success-metrics)
21. [Risk Matrix](#21-risk-matrix)
22. [Growth Path (If Traction)](#22-growth-path-if-traction)

---

# PART I — MARKET INTELLIGENCE

---

## 1. Market Landscape

### 1.1 Market Size

The agentic AI market is valued at ~$9–11B in 2026, projected to $139–199B by 2034 (40–44% CAGR). The agentic AI **cybersecurity** sub-market is projected at $22.5B → $322B by 2033.

According to UBS Research, 53% of organizations plan to adopt agentic AI by 2026, with 83% by 2028. Every organization deploying agents will need security controls — this is not a niche market.

### 1.2 Market Maturity

The market is in **early growth** stage:

- Enterprise buyers are budgeting for agent security (Microsoft, Palo Alto Networks publishing about it)
- Funded startups are shipping products (not just raising money)
- OpenAI acquired Promptfoo (March 9, 2026) — signal that agent security is core infrastructure
- Galileo launched OSS agent control plane (March 11, 2026) — the OSS playbook is validated
- But: no clear winner yet. No "Datadog for agents" has emerged

### 1.3 Buyer Behavior

Current buying patterns:

- **Developers** adopt bottom-up via CLI/OSS (Promptfoo model: 350K devs, 25% Fortune 500)
- **Security teams** evaluate top-down (Zenity, Noma model: enterprise sales)
- **Platform teams** look for middleware integration (Operant, Galileo model)

The bottom-up developer motion is the **only viable path for a solo engineer**. Enterprise sales requires headcount, compliance certifications, and sales cycles that a solo builder cannot sustain.

---

## 2. Competitive Analysis

### 2.1 Direct Competitors

| Company | Funding | Team | Product | Launched | GTM |
|---|---|---|---|---|---|
| **Galileo (Agent Control)** | Established (pivoted from ML observability) | ~50+ engineers | OSS control plane: portable policies, guardrails, eval framework integration. Apache 2.0 | March 11, 2026 | OSS + enterprise. Partners: CrewAI, Glean, Cisco AI Defense, Strands Agents |
| **Noma Security** | $132M total ($100M Series B, July 2025) | Growing fast (Tel Aviv + US) | Unified AI + agent security platform. Runtime monitoring, policy, vulnerability detection | Nov 2024 (stealth exit) | Enterprise top-down. 1300% ARR growth. Financial services, life sciences, retail |
| **Operant AI** | Series A (Felicis, SineWave) | ~20-30 | AI Gatekeeper, MCP Gateway, Agent Protector. Runtime protection, zero-trust for agents | 2024, major launches Apr/Jun 2025, Feb 2026 | Enterprise + developer. K8s, cloud-native focus |
| **Zenity** | $55.5M ($38M Series B, Oct 2024) | ~65 people | Runtime agent monitoring, permission control. Gartner Cool Vendor | 2021 (originally low-code security, pivoted to agents) | Enterprise. Microsoft M12 strategic investor. Salesforce partnership |
| **Promptfoo** | Acquired by OpenAI (March 9, 2026) | Was ~15-20 | AI security testing/scanning CLI. Red-teaming, evals, jailbreak detection. OSS | 2023 | OSS + enterprise. 350K devs, 25% Fortune 500. Now part of OpenAI Frontier |
| **Lasso Security** | Funded | ~30+ | Enterprise AI visibility + control. Shadow AI detection | 2023 | Enterprise top-down |

### 2.2 What They Cover vs. What's Missing

```
                    Galileo  Noma  Operant  Zenity  Promptfoo
                    ───────  ────  ───────  ──────  ────────
Prompt guardrails      ✅      ✅     ✅       ✅       ✅
I/O filtering          ✅      ✅     ✅       ✅       ✅
Policy enforcement     ✅      ✅     ✅       ✅       ❌
Runtime monitoring     ❌      ✅     ✅       ✅       ❌
MCP security           ❌      ❌     ✅       ❌       ❌
Agent eval/testing     ✅      ❌     ❌       ❌       ✅
────────────────────────────────────────────────────────────
Memory leak detection  ❌      ❌     ❌       ❌       ❌  ← GAP
Memory poisoning       ❌      ❌     ❌       ❌       ❌  ← GAP
Vector store audit     ❌      ❌     ❌       ❌       ❌  ← GAP
Tool permission scan   ❌      partial❌       partial ❌  ← GAP
Pre-deploy scanner     ❌      ❌     ❌       ❌       ✅  (prompt-level only)
```

**The memory security layer is unoccupied.** No funded competitor is building deep memory leakage detection, memory poisoning analysis, or vector store isolation auditing. This is AgentWall's opening.

### 2.3 Competitive Threat Assessment

**CRITICAL THREAT: Galileo Agent Control**
- Launched 6 days ago as OSS (Apache 2.0)
- Positions as "the control plane for AI agents" — identical to AgentWall's Phase 3–5 vision
- Has CrewAI, Glean, Cisco as launch partners
- BUT: focused on policy governance and guardrail orchestration, NOT memory security or pre-deploy scanning
- **Impact on AgentWall:** AgentWall must NOT position as "control plane." That fight is lost. AgentWall must own "memory security scanner."

**HIGH THREAT: OpenAI acquiring Promptfoo**
- Promptfoo was the closest OSS analog to AgentWall's scanner concept
- OpenAI will integrate it into their Frontier platform
- BUT: Promptfoo focuses on prompt-level red-teaming and model evals, NOT stateful agent memory/tool analysis
- **Impact on AgentWall:** The "agent scanner" category now has a giant behind it. AgentWall must differentiate on what Promptfoo never built — memory and state analysis.

**MEDIUM THREAT: Noma / Zenity / Operant**
- All well-funded, all enterprise-focused
- None are building bottom-up developer tools
- None focus on memory security
- **Impact on AgentWall:** These are potential acquirers or integration partners, not direct competitors at the developer layer.

---

## 3. Threat Assessment & Attack Research

### 3.1 Published Attack Research (Why Memory Security Matters)

The academic and security research community has validated the exact attack surface AgentWall targets:

**MINJA — Memory INJection Attack (NeurIPS 2025)**
- Authors: Dong et al.
- Finding: Attackers can inject malicious records into an agent's memory through query-only interaction — without direct access to the memory store
- Impact: >95% injection success rate, >70% attack success rate across tested LLM agents
- Implication: Memory stores are an attack surface even when access-controlled

**MemoryGraft (Srivastava & He, 2025)**
- Finding: Attackers plant fabricated "successful experiences" into long-term memory
- The agent later retrieves these grafted memories via standard similarity search and replicates embedded patterns
- Implication: Memory poisoning doesn't require explicit instruction injection — semantic manipulation is enough

**Palo Alto Unit42 — Persistent Memory Poisoning (2025)**
- Finding: Indirect prompt injection can poison an agent's long-term memory
- The poisoned memories persist across sessions and influence all future interactions
- Implication: A single successful injection has permanent compounding effects

**LangGrinch CVE (CVSS 9.3, December 2025)**
- A critical vulnerability in LangChain core that put agent secrets at risk
- Demonstrates that framework-level security is insufficient — agents need independent security scanning

**Christian Schneider — Persistent Memory Poisoning in AI Agents (2025)**
- Detailed technical analysis of how memory poisoning exploits work across different agent architectures
- Published remediation patterns that align with AgentWall's detection approach

### 3.2 Why This Research Matters for AgentWall

Every published attack targets the exact layer AgentWall scans. No existing tool specifically detects these attacks. The research provides:

1. **Validation** — the problem is real and published at top venues (NeurIPS)
2. **Detection patterns** — published exploits give us concrete test cases to implement
3. **Marketing content** — reproducing these attacks on popular frameworks is the content strategy
4. **Urgency signal** — enterprises reading this research will search for tools to detect it

---

## 4. Strategic Positioning

### 4.1 Revised Positioning (Based on Competitive Reality)

**Original positioning (v1 PRD):**
> "Trust and control layer for production AI agents"

**Problem:** This is now Galileo's exact positioning. Noma, Operant, and Zenity also claim this space with $200M+ combined funding.

**Revised positioning (v2):**
> "Memory security scanner for AI agents"

Specifically: **the tool that finds memory leakage, memory poisoning, and unsafe tool permissions in your agent before you deploy it.**

### 4.2 Why This Narrower Position Wins

1. **No competitor owns it.** Zero funded companies focus on agent memory security scanning.
2. **Research-backed urgency.** MINJA, MemoryGraft, Unit42 research creates immediate demand.
3. **Concrete and scannable.** "Find memory leaks" is clearer than "trust layer."
4. **Composable.** AgentWall scans can feed into Galileo policies, Operant enforcement, Noma dashboards. We're complementary, not competitive.
5. **Solo-viable.** A focused scanner is shippable in 3 weeks. A "trust platform" is not.

### 4.3 Competitive Strategy

```
DO:    Own "memory security for AI agents"
DO:    Be the tool that Galileo/Operant/Noma recommend for memory scanning
DO:    Publish attack research as primary marketing
DO:    Ship in 3 weeks, not 12

DON'T: Call yourself a "control plane" or "trust platform"
DON'T: Build a dashboard before you have 500+ users
DON'T: Try to compete on policy enforcement
DON'T: Support 3 frameworks on day 1
```

---

# PART II — SCOPE DECISIONS

---

## 5. What We Cut and Why

### 5.1 Features Cut from v1 PRD

| v1 Feature | v1 Priority | Decision | Rationale |
|---|---|---|---|
| **Unsafe action path detection (FR-104)** | P0 | **CUT** | Requires building a full graph traversal engine (NetworkX, ActionGraph, PathTracer). High complexity, high false-positive risk, 2+ weeks alone. Galileo Agent Control already covers action-level policy. Not differentiated. |
| **Traceability gap detection (FR-105)** | P1 | **CUT** | Nice-to-have audit check but not scary. Doesn't create "wow/fear moment." Observability tools (LangSmith, Arize) already cover logging gaps. Low differentiation. |
| **OpenAI Agents SDK adapter (FR-201)** | P0 → **deferred** | **DEFER to week 4+** | OpenAI SDK has fewer memory patterns than LangChain. Ship LangChain first (largest ecosystem), add OpenAI based on user demand. Reduces day-1 scope by ~40%. |
| **CrewAI adapter (FR-202)** | P1 → **deferred** | **DEFER to week 5+** | CrewAI delegation chain analysis is complex (TB-06). Galileo already partnered with CrewAI. Come back when there's pull. |
| **HTML reporter (FR-300)** | P0 | **CUT** | Engineering effort with low initial value. Terminal + JSON + SARIF covers all CI/CD and developer use cases. HTML is cosmetic. |
| **Custom policy rules engine (FR-401)** | P0 | **CUT** | Full YAML policy DSL is overengineered for a scanner with <20 rules. Hardcode built-in rules. Add custom rules only if users ask. YAGNI. |
| **YAML config file system (FR-400)** | P0 | **SIMPLIFY** | Replace with CLI flags + optional `agentwall.yaml` (minimal). No config parser needed for MVP — auto-detect everything. |
| **Generic adapter interface (FR-203)** | P0 | **DEFER** | Plugin architecture is premature. Build the LangChain adapter well. Extract the interface when adapter #2 forces it. |
| **7 vector store backends** | P0 | **CUT to 1** | Start with ChromaDB only (most popular for local dev, easiest to test). Add Pinecone in week 3 if time allows. Plugin architecture for rest. |
| **Policy engine (separate layer)** | P0 | **MERGE** | Merge rule evaluation directly into analyzers. No separate PolicyEngine, RuleRegistry, SeverityResolver. Over-abstracted for 10 rules. |
| **MkDocs documentation site** | P1 | **CUT** | README.md is enough. Docs site is busywork. Write a great README with examples instead. |
| **Automated changelog generation** | NFR-63 | **CUT** | Solo engineer. Write changelogs manually. |
| **80% test coverage target** | NFR-60 | **RELAX to 60%** | Cover critical paths (memory detection, tool audit). Skip testing CLI formatting, report templates. |
| **4 CI platform support** | NFR-42 | **CUT to 1** | GitHub Actions only. 90%+ of OSS CI runs on GitHub. Add others on demand. |
| **REST API (Phase 2)** | — | **CUT** | No API before product-market fit. |
| **Python SDK (Phase 1)** | — | **SIMPLIFY** | CLI is the SDK. Expose `Scanner` class for programmatic use but don't build a separate package. |

### 5.2 Architecture Simplifications

| v1 Architecture Component | Decision | Rationale |
|---|---|---|
| **ScanOrchestrator** | **KEEP but simplify** | Single function, not a class hierarchy. ~50 lines. |
| **FrameworkResolver** | **KEEP** | Auto-detect is critical UX. Simple heuristic (check imports/pyproject.toml). |
| **Separate PolicyEngine** | **REMOVE** | Rules live inside analyzers. No indirection. |
| **SeverityResolver** | **REMOVE** | Severity is set per-rule at definition time. No dynamic resolution. |
| **ReportAggregator** | **MERGE into scan()** | The scan function collects findings directly. No separate aggregation layer. |
| **concurrent.futures parallelism** | **REMOVE** | Run 2 analyzers sequentially. Total scan <10 seconds. Parallelism is premature optimization. |
| **ActionGraph data model** | **REMOVE** | No action path analysis = no graph model needed. |
| **memory_backends/ package (6 files)** | **CUT to 1** | Single `chroma_probe.py`. Add backends as needed. |
| **reporters/ package (4 files)** | **CUT to 2** | Terminal reporter + JSON reporter. SARIF in week 3. |

### 5.3 Impact Summary

| Metric | v1 PRD | v2 Solo | Reduction |
|---|---|---|---|
| Estimated files to write | ~45 | ~18 | 60% |
| Framework adapters | 3 + generic | 1 (LangChain) | 75% |
| Analyzers | 4 | 2 (Memory + Tool) | 50% |
| Vector store backends | 7 | 1 (ChromaDB) | 86% |
| Report formats | 4 | 2 (Terminal + JSON) | 50% |
| Time to ship | 12 weeks | 3 weeks | 75% |
| Built-in rules | 20+ | 8–10 | 50% |

---

## 6. What We Keep and Why

| Feature | Why It Stays |
|---|---|
| **Memory leakage detection** | Core differentiator. No competitor has this. Directly maps to MINJA/MemoryGraft research. The reason AgentWall exists. |
| **Memory poisoning detection** | Second core differentiator. Pattern-based detection of known injection techniques in stored memory. High fear factor. |
| **Tool permission audit** | Quick win, high signal. Enumerating tools + classifying risk is straightforward and produces immediately actionable findings. |
| **LangChain adapter** | Largest agent framework ecosystem. Richest memory integration surface. Most templates to scan. |
| **ChromaDB memory probe** | Most popular local vector store. Used in >80% of LangChain tutorials. Easiest to set up for testing. |
| **Terminal reporter (Rich)** | Developer experience. Beautiful colored output = shareability = organic distribution. |
| **JSON reporter** | Machine-readable output for CI/CD integration. Required for `--fail-on` exit codes. |
| **SARIF reporter (week 3)** | GitHub Advanced Security integration. Shows findings directly in PR. High-value CI integration. |
| **CLI with Typer** | Type-safe, auto-generated `--help`, minimal code. Perfect for solo dev. |
| **`pip install agentwall`** | Frictionless distribution. The entire GTM depends on this being dead simple. |
| **CI exit codes** | Core CI/CD integration. Exit 0/1/2 is trivial to implement and enables the "pre-deploy check" use case. |
| **Auto-detect framework** | Critical UX. User should run `agentwall scan .` with zero config and get results. |

---

# PART III — PRODUCT SPECIFICATION

---

## 7. Executive Summary

AgentWall is the **memory security scanner for AI agents**. It detects cross-user memory leakage, memory poisoning vulnerabilities, and unsafe tool permissions in AI agent applications before deployment.

Distributed as an open-source Python CLI (`pip install agentwall`), it gives AI engineers a 10-minute "fear moment" — showing them exactly how their agent can leak user data across tenants, retrieve poisoned memory that overrides instructions, or call tools it should never have access to.

AgentWall targets the one security layer that no funded competitor covers: **the stateful memory and permission surface of production AI agents.**

---

## 8. Product Vision (Revised)

### 8.1 What AgentWall Is

AgentWall is a **pre-deployment security scanner** that answers one question:

> "Can my agent leak memory, retrieve poisoned data, or call tools it shouldn't?"

### 8.2 What AgentWall Is NOT

- NOT a runtime control plane (that's Galileo, Operant)
- NOT an enterprise governance dashboard (that's Noma, Zenity)
- NOT a prompt red-teaming tool (that's Promptfoo/OpenAI)
- NOT an observability platform (that's LangSmith, Arize)

### 8.3 Where AgentWall Sits

```
Development              Pre-Deploy              Runtime               Post-Incident
─────────────          ─────────────          ─────────────          ─────────────
Code → Build    →    ★ AgentWall scan ★   →   Galileo/Operant   →   Noma/Zenity
                     memory + tool audit       policy enforce         audit/forensics
                     "Is it safe to ship?"     "Block bad actions"    "What happened?"
```

AgentWall is the **shift-left** tool. It runs before production, in CI, during development. It is complementary to runtime tools, not competitive.

### 8.4 Future Evolution (If Traction)

```
Month 1–3:  Memory scanner CLI (this PRD)
Month 4–6:  + OpenAI/CrewAI adapters, + Pinecone/pgvector, + MCP audit
Month 7–12: + Team dashboard, + policy templates, + hosted scan history
Year 2:     Evaluate: stay OSS scanner → get acquired, OR raise → build control plane
```

The strategic question at month 6: **stay a scanner (Semgrep/Trivy model) or expand to platform (Snyk model)?** That decision depends entirely on traction data.

---

## 9. Target Persona

### 9.1 Primary Persona: AI Engineer

**One persona only. Laser focus.**

- Builds agents using LangChain/LangGraph
- Uses ChromaDB, Pinecone, or pgvector for memory/RAG
- Ships via GitHub Actions CI
- Python 3.10+ environment
- Knows their agent "works" but has no idea if it's "safe"
- Pain: "I shipped a support agent and I have no clue if it can leak one customer's data to another"

### 9.2 Secondary Persona: Security-Minded AI Builder (deferred)

- Will naturally discover AgentWall via attack research content
- Not worth building features for directly — they'll use the same CLI
- Important for content marketing, not product decisions

---

## 10. Functional Requirements

### 10.1 Core Scanner

**FR-100: Agent Configuration Parsing**
- The system SHALL auto-detect LangChain/LangGraph projects by inspecting `pyproject.toml`, `requirements.txt`, and Python imports
- The system SHALL accept `--framework langchain` CLI flag to force detection
- The system SHALL scan a single project directory

**FR-101: Memory Leakage Detection**
- The system SHALL detect cross-user memory access patterns in ChromaDB configurations
- The system SHALL check for: missing collection-level isolation, missing metadata filtering by user/tenant ID, shared collections across users without access control
- The system SHALL simulate multi-tenant queries when a live ChromaDB instance is available (opt-in `--live` flag)
- The system SHALL produce findings with evidence (specific code locations, configuration values)

**FR-102: Memory Poisoning Detection**
- The system SHALL scan stored memory/documents for known injection patterns: instruction overrides (`ignore previous instructions`), role hijacking (`you are now`), data exfiltration prompts (`send to`, `forward to`), delimiter attacks
- The system SHALL check whether memory retrieval includes sanitization or filtering
- The system SHALL check whether the agent's system prompt is robust against context injection

**FR-103: Tool Permission Audit**
- The system SHALL enumerate all tools registered with the agent
- The system SHALL classify each tool's risk level using heuristics: name-based (delete, send, transfer, execute → high risk), parameter-based (credentials, API keys → high risk), description-based (NLP keyword matching)
- The system SHALL flag agents where high-risk tools lack access control checks
- The system SHALL detect tools with overly broad parameter schemas (e.g., accepting arbitrary SQL, arbitrary shell commands)

### 10.2 Framework Adapter

**FR-200: LangChain / LangGraph Adapter**
- The system SHALL introspect LangChain agent definitions by analyzing Python AST and module imports
- The system SHALL extract: tool lists (names, descriptions, schemas), memory backend configuration, chain/graph structure
- The system SHALL support LangChain 0.2+ and LangGraph 0.1+

### 10.3 Reporting

**FR-300: Terminal Reporter**
- The system SHALL output colored, formatted scan results to terminal using Rich
- Output SHALL include: summary header (agent name, framework, scan duration), findings grouped by severity, per-finding detail (rule ID, description, evidence, remediation), footer with counts and exit recommendation

**FR-301: JSON Reporter**
- The system SHALL output machine-readable JSON with schema: `{ scan_id, timestamp, project, framework, findings[], summary }`
- Activated via `--output json` or `--output report.json`

**FR-302: SARIF Reporter (Week 3)**
- The system SHALL output SARIF 2.1.0 for GitHub Advanced Security integration
- Activated via `--output report.sarif`

**FR-303: CI Exit Codes**
- Exit 0: No findings above threshold
- Exit 1: Findings at or above `--fail-on` severity (default: high)
- Exit 2: Scanner error (crash, config error)

### 10.4 CLI Interface

```
agentwall scan [PATH]                # Scan project (default: current dir)
agentwall scan --framework langchain # Force framework
agentwall scan --live                # Enable live vector store probing
agentwall scan --fail-on medium      # CI threshold
agentwall scan --output report.json  # JSON output
agentwall scan --output report.sarif # SARIF output
agentwall version                    # Version info
```

No `init`, no `rules`, no `report` subcommands. One command: `scan`.

---

## 11. Non-Functional Requirements

### 11.1 Performance

| ID | Requirement | Target |
|---|---|---|
| NFR-01 | Single agent scan time | < 15 seconds |
| NFR-02 | CLI cold start time | < 1.5 seconds |
| NFR-03 | Memory footprint | < 256 MB RAM |

### 11.2 Reliability

| ID | Requirement | Target |
|---|---|---|
| NFR-10 | Scan completion rate (no crashes) | > 95% |
| NFR-11 | Graceful degradation on parse errors | Warning + continue |

### 11.3 Security

| ID | Requirement | Target |
|---|---|---|
| NFR-20 | No agent code execution | Mandatory (AST analysis only) |
| NFR-21 | No network calls without `--live` flag | Mandatory |
| NFR-22 | No secrets in scan output | Mandatory — redact credentials |
| NFR-23 | Fully offline by default | Mandatory |

### 11.4 Usability

| ID | Requirement | Target |
|---|---|---|
| NFR-30 | Time from `pip install` to first result | < 5 minutes |
| NFR-31 | Zero-config scan (auto-detect) | Mandatory |
| NFR-32 | Actionable remediation per finding | Mandatory |

### 11.5 Compatibility

| ID | Requirement | Target |
|---|---|---|
| NFR-40 | Python | 3.10+ |
| NFR-41 | OS | Linux, macOS |
| NFR-42 | CI | GitHub Actions |
| NFR-43 | LangChain | 0.2+ |

---

## 12. Constraints

| ID | Constraint | Impact | Mitigation |
|---|---|---|---|
| C-01 | **Solo engineer** | No parallel feature tracks. Every decision is a trade-off against time | Ruthless scope. Ship in 3 weeks. Expand only with traction signals |
| C-02 | **Static analysis only (MVP)** | Cannot detect runtime-only memory access patterns | Opt-in `--live` mode for ChromaDB. Label findings as "potential" vs "confirmed" |
| C-03 | **LangChain API instability** | Adapter may break on LC updates | Pin minimum version. Test against LC 0.2 and 0.3. Graceful fallback |
| C-04 | **AST-based parsing limitations** | Cannot resolve dynamic tool registration or conditional memory config | Document limitations. Accept partial coverage. False negatives > false positives |
| C-05 | **No funding, no team** | Cannot sustain multi-month feature development without revenue or adoption | Validate in 3 weeks. Kill or continue decision at week 4 |
| C-06 | **Galileo/Promptfoo competitive pressure** | The "agent security" narrative is being captured by funded players | Don't compete on narrative. Compete on memory depth. Be the tool they integrate |

---

## 13. Potential Technical Blockages

### 13.1 Critical

**TB-01: Memory Isolation Detection via Static Analysis**
- **Problem:** Determining whether a ChromaDB collection is properly isolated requires understanding how the application configures the client — which may happen dynamically at runtime.
- **Impact:** False negatives (missing real leakage) or false positives (flagging properly isolated stores)
- **Mitigation:**
  - Static: Analyze ChromaDB client initialization in AST. Flag `get_or_create_collection()` without metadata filtering
  - Live: `--live` mode connects to running ChromaDB and tests actual queries
  - Conservative: When in doubt, flag as "potential risk" with explanation

**TB-02: LangChain AST Parsing Complexity**
- **Problem:** LangChain agents can be defined in many ways (functional, class-based, LCEL, LangGraph). Parsing all patterns via AST is non-trivial.
- **Impact:** Some agent configurations may not be detected
- **Mitigation:**
  - Start with the 3 most common patterns (AgentExecutor, create_react_agent, StateGraph)
  - Use import analysis as fallback (detect `from langchain` imports → enumerate known patterns)
  - Accept partial coverage. Ship with "X patterns supported" docs

**TB-03: Memory Poisoning Detection Accuracy**
- **Problem:** Pattern-based poisoning detection (regex for injection phrases) has limited accuracy. Sophisticated attacks use semantic manipulation, not explicit injection strings.
- **Impact:** May miss advanced attacks. May over-flag benign content.
- **Mitigation:**
  - Ship with high-confidence patterns only (known injection phrases, delimiter attacks)
  - Clearly document: "AgentWall detects known poisoning patterns. For advanced semantic attacks, see [research links]"
  - Future: Optional LLM-based analysis via Ollama (capital-aware routing)

### 13.2 Moderate

**TB-04: Tool Risk Classification Heuristics**
- **Problem:** Heuristic classification (name/description keyword matching) will misclassify some tools
- **Impact:** Noisy findings reduce trust
- **Mitigation:** Ship with override annotations. Users can mark tools as `# agentwall: safe` in comments

---

# PART IV — TECHNICAL ARCHITECTURE

---

## 14. High-Level Architecture

### 14.1 Architecture Overview

```
┌──────────────────────────────────────────────────────┐
│                     CLI (Typer)                       │
│  agentwall scan [PATH] [--flags]                     │
└──────────────┬───────────────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────────────┐
│                   scan() orchestrator                 │
│                                                      │
│  1. auto_detect_framework(path)                      │
│  2. adapter.parse(path) → AgentSpec                  │
│  3. run_analyzers(agent_spec) → findings[]           │
│  4. render_report(findings, format)                  │
│  5. return exit_code                                 │
└──────────┬────────────┬──────────────────────────────┘
           │            │
           ▼            ▼
┌─────────────────┐ ┌─────────────────┐
│  LangChain      │ │  [Future]       │
│  Adapter        │ │  OpenAI/CrewAI  │
│                 │ │  Adapters       │
│  parse(path)    │ │                 │
│  → AgentSpec    │ │                 │
└────────┬────────┘ └─────────────────┘
         │
         ▼
┌──────────────────────────────────────────────────────┐
│                    AgentSpec                          │
│  { name, framework, tools[], memory_config }         │
└──────────┬────────────┬──────────────────────────────┘
           │            │
           ▼            ▼
┌──────────────────┐ ┌──────────────────┐
│  MemoryAnalyzer  │ │  ToolAnalyzer    │
│                  │ │                  │
│  ├─ leak_check() │ │  ├─ enumerate()  │
│  ├─ poison_scan()│ │  ├─ classify()   │
│  └─ isolation()  │ │  └─ scope_check()│
│                  │ │                  │
│  → findings[]    │ │  → findings[]    │
└──────────────────┘ └──────────────────┘
           │            │
           ▼            ▼
┌──────────────────────────────────────────────────────┐
│                  Report Renderer                     │
│                                                      │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐       │
│  │  Terminal   │ │   JSON     │ │   SARIF    │       │
│  │  (Rich)    │ │            │ │  (week 3)  │       │
│  └────────────┘ └────────────┘ └────────────┘       │
└──────────────────────────────────────────────────────┘
```

### 14.2 Core Data Model

```python
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class Severity(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class Category(str, Enum):
    MEMORY = "memory"
    TOOL = "tool"


class RiskLevel(str, Enum):
    READ_ONLY = "read_only"
    STATE_CHANGING = "state_changing"
    EXTERNAL = "external"
    FINANCIAL = "financial"
    DESTRUCTIVE = "destructive"


@dataclass
class ToolSpec:
    name: str
    description: str
    parameters: dict[str, Any] = field(default_factory=dict)
    risk_level: RiskLevel = RiskLevel.READ_ONLY
    source_file: str = ""
    source_line: int = 0


@dataclass
class MemoryConfig:
    backend: str  # "chroma", "pinecone", "pgvector", etc.
    collection_name: str = ""
    has_user_isolation: bool = False
    has_metadata_filtering: bool = False
    connection_config: dict[str, Any] = field(default_factory=dict)
    source_file: str = ""
    source_line: int = 0


@dataclass
class AgentSpec:
    name: str
    framework: str
    tools: list[ToolSpec] = field(default_factory=list)
    memory: MemoryConfig | None = None
    source_files: list[str] = field(default_factory=list)


@dataclass
class Finding:
    rule_id: str  # "AW-MEM-001"
    severity: Severity
    category: Category
    title: str
    description: str
    evidence: str
    remediation: str
    source_file: str = ""
    source_line: int = 0


@dataclass
class ScanResult:
    project_path: str
    framework: str
    agent_name: str
    duration_ms: int
    findings: list[Finding] = field(default_factory=list)

    @property
    def exit_code(self) -> int:
        severities = {f.severity for f in self.findings}
        if Severity.CRITICAL in severities or Severity.HIGH in severities:
            return 1
        return 0
```

---

## 15. Directory Structure

```
agentwall/
├── pyproject.toml              # Hatch build, dependencies, tool config
├── README.md                   # The marketing doc. Must be excellent.
├── LICENSE                     # MIT
├── .github/
│   └── workflows/
│       └── ci.yml              # Test + lint on push
├── src/
│   └── agentwall/
│       ├── __init__.py         # Version, public API
│       ├── cli.py              # Typer app (scan command, flags)
│       ├── scanner.py          # scan() orchestrator function
│       ├── models.py           # AgentSpec, Finding, ScanResult
│       ├── detector.py         # auto_detect_framework()
│       ├── adapters/
│       │   ├── __init__.py
│       │   ├── base.py         # AbstractAdapter (Protocol)
│       │   └── langchain.py    # LangChain/LangGraph adapter
│       ├── analyzers/
│       │   ├── __init__.py
│       │   ├── memory.py       # MemoryAnalyzer (leak + poison + isolation)
│       │   └── tools.py        # ToolAnalyzer (enumerate + classify + scope)
│       ├── reporters/
│       │   ├── __init__.py
│       │   ├── terminal.py     # Rich terminal output
│       │   ├── json.py         # JSON file output
│       │   └── sarif.py        # SARIF output (week 3)
│       └── rules.py            # All rules defined here (AW-MEM-*, AW-TOOL-*)
├── tests/
│   ├── conftest.py
│   ├── test_scanner.py
│   ├── test_langchain_adapter.py
│   ├── test_memory_analyzer.py
│   ├── test_tool_analyzer.py
│   └── fixtures/
│       ├── langchain_basic/    # Simple agent for testing
│       ├── langchain_unsafe/   # Agent with known vulnerabilities
│       └── langchain_safe/     # Properly configured agent
└── docs/                       # Just README for now
```

**18 source files. That's it.**

---

## 16. Technology Stack

| Layer | Technology | Rationale |
|---|---|---|
| Language | Python 3.10+ | Target user ecosystem |
| CLI | Typer 0.9+ | Type-safe, auto --help, minimal code |
| Terminal UI | Rich | Beautiful output, shareability |
| Config/Models | Pydantic v2 | Validation, type safety |
| AST Parsing | `ast` (stdlib) | Zero dependencies for code analysis |
| Testing | pytest | Standard |
| Build | Hatch + pyproject.toml | Modern Python packaging |
| CI | GitHub Actions | OSS standard |
| Linting | Ruff | Fast, all-in-one |
| Type Check | mypy (strict) | Correctness |

**Total PyPI dependencies: 4** (typer, rich, pydantic, chromadb [optional])

Minimal dependency footprint = fast install, fewer conflicts, trustworthy for security tooling.

---

## 17. Data Flow

```
$ agentwall scan ./my-langchain-agent/

1. CLI parses args (Typer)
2. detector.auto_detect_framework("./my-langchain-agent/")
   → inspects pyproject.toml/requirements.txt for langchain imports
   → returns "langchain"
3. LangChainAdapter.parse("./my-langchain-agent/")
   → walks Python files, builds AST
   → extracts tool definitions, memory config, agent structure
   → returns AgentSpec
4. MemoryAnalyzer.analyze(agent_spec)
   → checks memory isolation (AW-MEM-001, AW-MEM-002, AW-MEM-003)
   → checks poisoning patterns (AW-MEM-004, AW-MEM-005)
   → returns findings[]
5. ToolAnalyzer.analyze(agent_spec)
   → enumerates tools, classifies risk (AW-TOOL-001, AW-TOOL-002, AW-TOOL-003)
   → returns findings[]
6. Merge findings, sort by severity
7. TerminalReporter.render(scan_result)
   → prints colored output
8. If --output: JSONReporter.render() or SARIFReporter.render()
9. sys.exit(scan_result.exit_code)

Total time: < 10 seconds
```

---

## 18. Data Model

### 18.1 Built-in Rules (MVP)

| Rule ID | Category | Severity | Title |
|---|---|---|---|
| AW-MEM-001 | Memory | CRITICAL | Cross-user memory access: no tenant isolation detected |
| AW-MEM-002 | Memory | HIGH | Shared vector collection without metadata filtering |
| AW-MEM-003 | Memory | HIGH | Memory backend has no access control configuration |
| AW-MEM-004 | Memory | HIGH | Known injection patterns detected in memory retrieval path |
| AW-MEM-005 | Memory | MEDIUM | No sanitization on retrieved memory before prompt injection |
| AW-TOOL-001 | Tool | HIGH | Agent has access to destructive tools without approval gate |
| AW-TOOL-002 | Tool | MEDIUM | Over-permissioned tool: accepts arbitrary code/SQL/shell execution |
| AW-TOOL-003 | Tool | MEDIUM | High-risk tool lacks user-scope access check |
| AW-TOOL-004 | Tool | LOW | Tool description missing (hinders risk classification) |
| AW-TOOL-005 | Tool | INFO | Tool count exceeds recommended limit (>15 tools per agent) |

**10 rules. Ship it.**

---

# PART V — EXECUTION

---

## 19. 3-Week Sprint Plan

### Week 1: Skeleton + Memory Analyzer

| Day | Deliverable |
|---|---|
| Mon | Project scaffold: `pyproject.toml`, `src/` layout, Ruff, mypy, pytest, GitHub Actions CI |
| Tue | Core models (`models.py`): AgentSpec, ToolSpec, MemoryConfig, Finding, ScanResult |
| Wed | LangChain adapter (basic): AST walking, extract tools + memory config from AgentExecutor / create_react_agent patterns |
| Thu | MemoryAnalyzer: AW-MEM-001 (tenant isolation), AW-MEM-002 (shared collection), AW-MEM-003 (no access control) |
| Fri | Terminal reporter (Rich): colored output, severity grouping. End-to-end: `agentwall scan ./fixture/` works |

**Week 1 exit criteria:** Can scan a LangChain project and get memory findings with colored terminal output.

### Week 2: Tool Analyzer + Poisoning + CI

| Day | Deliverable |
|---|---|
| Mon | MemoryAnalyzer: AW-MEM-004 (injection patterns), AW-MEM-005 (no sanitization) |
| Tue | ToolAnalyzer: AW-TOOL-001 through AW-TOOL-005. Heuristic risk classification |
| Wed | JSON reporter. `--output`, `--fail-on` flags. Exit code logic |
| Thu | Auto-detect framework (`detector.py`). `pip install -e .` end-to-end test |
| Fri | Test fixtures: `langchain_basic/`, `langchain_unsafe/`, `langchain_safe/`. 60%+ test coverage |

**Week 2 exit criteria:** Full scan with 10 rules, JSON output, CI-ready exit codes. Installable via pip.

### Week 3: Polish + Ship

| Day | Deliverable |
|---|---|
| Mon | SARIF reporter. GitHub Actions example workflow in `docs/` |
| Tue | README.md: install, quickstart, example output screenshot, rule reference, CI setup |
| Wed | `pip install agentwall` — publish to PyPI. GitHub repo public |
| Thu | Write launch blog post: "We found memory leakage in 3 popular LangChain templates" |
| Fri | Launch: Show HN, X/Twitter, r/LangChain, r/MachineLearning |

**Week 3 exit criteria:** Public on PyPI. GitHub repo with README. Blog post published. HN submitted.

---

## 20. Success Metrics

### Week 4 (1 week post-launch)

| Metric | Signal | Target |
|---|---|---|
| PyPI installs | People trying it | 50+ |
| GitHub stars | Interest | 30+ |
| GitHub issues | Engagement | 5+ |
| Blog post views | Content works | 500+ |
| "Can you support X?" requests | Demand for expansion | 3+ |

### Month 2–3

| Metric | Signal | Target |
|---|---|---|
| Weekly PyPI installs | Sustained usage | 200+ |
| GitHub stars | Growing interest | 300+ |
| CI integrations (Actions usage) | Workflow adoption | 20+ repos |
| Framework requests (OpenAI, CrewAI) | Expansion demand | Signal to add adapter |
| Inbound from Galileo/Noma/Operant | Partnership/acquisition interest | 1+ conversation |

### Kill Criteria

If at week 4:
- < 10 installs
- < 5 stars
- 0 issues/engagement
- Blog post gets no traction

**Then:** Shelve the project. The market doesn't want this specific tool from this specific builder. Redirect energy.

---

## 21. Risk Matrix

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| LangChain breaking changes break adapter | High | High | Pin LC 0.2+, test weekly, graceful fallback |
| Low launch traction (noise floor) | Medium | Critical | Attack research blog is the marketing. Make the demo scary. |
| False positive rate erodes trust | Medium | High | Ship conservative rules. Prefer false negatives over false positives for v1 |
| Galileo/Noma builds memory scanning | Low (next 3 months) | High | First-mover in memory niche. Ship fast. Build reputation before they notice |
| Scope creep (adding features before PMF) | High | Medium | This document exists to prevent it. 3 weeks. 2 analyzers. 10 rules. Ship. |
| Solo burnout | Medium | Critical | Hard stop at week 3. Ship whatever is ready. Perfect is the enemy of shipped. |

---

## 22. Growth Path (If Traction)

### Month 2: Expand Detection

- Add OpenAI Agents SDK adapter (based on user demand)
- Add Pinecone memory probe
- Add 5 more rules based on user-reported gaps

### Month 3: Expand Distribution

- Add SARIF → GitHub Security tab deep integration
- Write GitHub Action (`agentwall/scan-action@v1`)
- Partner with 1 framework (pitch to CrewAI — Galileo covers policy, AgentWall covers memory)

### Month 4–6: Decide Path

**Path A: Stay Scanner (Semgrep/Trivy model)**
- Stay OSS, stay focused
- Become the "default memory scan before deploy"
- Monetize via hosted scan history + team features
- Get acquired by Galileo/Noma/Operant for $5–15M

**Path B: Build Platform (Snyk model)**
- Raise seed round ($1–2M) on traction data
- Hire 2–3 engineers
- Build team dashboard + policy templates
- Expand into runtime memory enforcement

**Path C: Get Acquired**
- Galileo, Operant, or Noma acquires AgentWall for memory scanning capability
- Most likely if traction is moderate (500+ stars, 1000+ installs) but solo scaling is hard

The decision depends entirely on data from months 1–3. Don't plan beyond month 3 without traction evidence.

---

## Sources

Market intelligence in this document is based on the following sources:

- [Noma Security Raises $100M Series B](https://noma.security/blog/noma-security-raises-100m-to-drive-adoption-of-ai-agent-security/)
- [Zenity Raises $38M Series B](https://www.bankinfosecurity.com/zenity-gets-38m-series-b-for-agentic-ai-security-expansion-a-26696)
- [Galileo Launches Agent Control (OSS)](https://galileo.ai/blog/announcing-agent-control)
- [Galileo Agent Control — GlobeNewswire](https://www.globenewswire.com/news-release/2026/03/11/3253962/0/en/Galileo-Releases-Open-Source-AI-Agent-Control-Plane-to-Help-Enterprises-Govern-Agents-at-Scale.html)
- [OpenAI Acquires Promptfoo — TechCrunch](https://techcrunch.com/2026/03/09/openai-acquires-promptfoo-to-secure-its-ai-agents/)
- [Operant AI — Agent Protector](https://www.operant.ai/platform/agent-protector)
- [Operant AI — MCP Gateway Launch](https://www.globenewswire.com/news-release/2025/06/16/3099877/0/en/Operant-AI-Launches-MCP-Gateway-Enterprise-Grade-Runtime-Defense-for-MCP-Connected-AI-Applications.html)
- [MINJA: Memory Injection Attack — MintMCP](https://www.mintmcp.com/blog/ai-agent-memory-poisoning)
- [Palo Alto Unit42 — Persistent Memory Poisoning](https://unit42.paloaltonetworks.com/indirect-prompt-injection-poisons-ai-longterm-memory/)
- [Christian Schneider — Memory Poisoning in AI Agents](https://christian-schneider.net/blog/persistent-memory-poisoning-in-ai-agents/)
- [Mem0 — AI Memory Security Best Practices](https://mem0.ai/blog/ai-memory-security-best-practices)
- [LangGrinch CVE — SiliconANGLE](https://siliconangle.com/2025/12/25/critical-langgrinch-vulnerability-langchain-core-puts-ai-agent-secrets-risk/)
- [Agentic AI Security Threats 2025 — Lasso Security](https://www.lasso.security/blog/agentic-ai-security-threats-2025)
- [AI Agent Memory Security — Medium/Oracle](https://medium.com/@oracle_43885/ai-agent-memory-security-requires-more-observability-b12053e39ff0)

---

*End of document. Ship it.*
