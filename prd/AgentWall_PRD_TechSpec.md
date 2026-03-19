# AgentWall — Product Requirements Document & Technical Specification

**Version:** 1.0
**Date:** 2026-03-17
**Author:** SoH Engineering
**Status:** Draft
**Classification:** Internal — Confidential

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Product Vision & Strategy](#2-product-vision--strategy)
3. [User Personas & Stakeholders](#3-user-personas--stakeholders)
4. [Product Scope](#4-product-scope)
5. [Functional Requirements](#5-functional-requirements)
6. [Non-Functional Requirements](#6-non-functional-requirements)
7. [Constraints](#7-constraints)
8. [Potential Technical Blockages](#8-potential-technical-blockages)
9. [High-Level Technical Architecture](#9-high-level-technical-architecture)
10. [Data Model](#10-data-model)
11. [API Specification Overview](#11-api-specification-overview)
12. [Phased Delivery Plan](#12-phased-delivery-plan)
13. [Risk Matrix](#13-risk-matrix)
14. [Success Metrics](#14-success-metrics)
15. [Glossary](#15-glossary)

---

## 1. Executive Summary

AgentWall is a **trust and control layer for production AI agents**. It provides runtime security scanning, permission enforcement, memory isolation auditing, and full audit trails for AI agent systems that access memory, call tools, and take actions on behalf of users.

The product enters the market as an **open-source CLI scanner** that exposes unsafe agent behaviors (memory leakage, tool permission violations, risky action paths), then expands into a runtime control plane with policy enforcement, approval workflows, and enterprise audit infrastructure.

**The core problem:** AI agents are transitioning from stateless prompt-response systems into stateful, tool-using, action-taking autonomous systems. Existing AI safety tooling covers model evaluation and input/output guardrails but leaves a critical gap in memory safety, tool permission control, runtime action governance, and agent auditability.

**The core solution:** A layered security product that starts as a developer-facing scanner (bottom-up adoption) and evolves into enterprise trust infrastructure (top-down expansion).

---

## 2. Product Vision & Strategy

### 2.1 Vision Statement

As AI agents evolve from chat interfaces into persistent systems that access memory, use tools, and take real actions, companies need a new trust layer that governs what those agents can know, do, and change. AgentWall is that layer: a runtime control plane for AI agents that enforces permissions, blocks unsafe actions, isolates memory, creates full audit trails, and provides the trust infrastructure required for autonomous AI to operate safely in production.

### 2.2 Strategic Positioning

AgentWall is **not** an AI governance dashboard, a compliance checkbox tool, or a model evaluation framework. It is a **runtime security and control system** positioned at the execution boundary between agents and the real world.

**Market gap addressed:**

| Existing Coverage | AgentWall's Target Gap |
|---|---|
| Model evaluation (evals) | Memory safety & isolation |
| Input/output guardrails | Tool permission enforcement |
| Prompt injection detection | Runtime action control |
| Observability / monitoring | Agent auditability & forensics |
| Compliance documentation | Approval workflows for risky actions |

### 2.3 Competitive Landscape

| Category | Players | AgentWall Differentiation |
|---|---|---|
| AI Red-teaming | Promptfoo, Garak | AgentWall focuses on **stateful agent behavior** (memory, tools, actions), not prompt-level attacks |
| AI Guardrails | Guardrails AI, NeMo Guardrails | These are I/O filters. AgentWall operates at the **runtime execution layer** |
| AI Observability | LangSmith, Arize, Helicone | Observability watches. AgentWall **enforces and blocks** |
| AI Governance | Credo AI, Holistic AI | Governance platforms are top-down compliance. AgentWall is bottom-up developer tooling first |

### 2.4 Product Evolution Ladder

```
Level 1: Agent Trust Scanner (CLI)        → "Is my agent safe to ship?"
Level 2: Team Trust Platform (Dashboard)   → "Are our agents safe across repos?"
Level 3: Policy & Permission Layer         → "What is this agent allowed to do?"
Level 4: Runtime Control Plane             → "Every action goes through us"
Level 5: Enterprise Trust Infrastructure   → "We are the system of record"
```

---

## 3. User Personas & Stakeholders

### 3.1 Primary Personas

**P1 — AI Engineer (Phase 0–1 target)**
- Builds agents using LangChain, OpenAI Agents SDK, CrewAI
- Needs to validate agent safety before deployment
- Comfort zone: CLI, Python, CI/CD pipelines
- Pain: "I have no idea if my agent can leak user data or call tools it shouldn't"

**P2 — Platform Engineer (Phase 2–3 target)**
- Manages shared infrastructure for multiple agent applications
- Needs standardized policies across teams
- Pain: "Every team builds agents differently. I can't enforce any safety baseline"

**P3 — Security Engineer (Phase 3–4 target)**
- Responsible for threat modeling and security review of agent systems
- Needs audit trails and forensic capability
- Pain: "I can't answer 'why did the agent do this?' after an incident"

**P4 — Head of AI Platform / CISO (Phase 4–5 target)**
- Executive buyer for enterprise trust infrastructure
- Needs compliance evidence, org-wide governance
- Pain: "Regulators are asking about our AI controls and I have nothing to show"

### 3.2 Stakeholders

| Stakeholder | Interest | Influence |
|---|---|---|
| AI Engineers | Daily users, adoption drivers | High (bottom-up) |
| Security Teams | Risk assessment, policy definition | High (gate-keeper) |
| Compliance / Legal | Regulatory evidence | Medium |
| Engineering Leadership | Platform decisions, budget | High |
| End Users (of agents) | Trust in AI-powered features | Indirect |

---

## 4. Product Scope

### 4.1 In Scope — Phase 0/1 (MVP)

| ID | Feature | Priority |
|---|---|---|
| S-01 | CLI scanner with `agentwall scan` command | P0 |
| S-02 | Cross-user memory leakage detection | P0 |
| S-03 | Memory poisoning / injection risk analysis | P0 |
| S-04 | Tool permission audit (over-permissioned tools) | P0 |
| S-05 | Unsafe action path detection (no approval gates) | P0 |
| S-06 | Traceability / auditability gap detection | P1 |
| S-07 | LangChain/LangGraph adapter | P0 |
| S-08 | OpenAI Agents SDK adapter | P0 |
| S-09 | CrewAI adapter | P1 |
| S-10 | YAML/TOML configuration file support | P0 |
| S-11 | JSON/HTML scan report output | P0 |
| S-12 | CI/CD exit code integration | P0 |
| S-13 | `pip install agentwall` distribution | P0 |

### 4.2 Out of Scope — Phase 0/1

- Runtime policy enforcement (Phase 3)
- SaaS dashboard (Phase 2)
- Approval workflow engine (Phase 3)
- SSO / RBAC (Phase 5)
- Real-time monitoring / streaming (Phase 4)
- Agent identity management (Phase 4)
- Compliance report generation (Phase 5)

---

## 5. Functional Requirements

### 5.1 Core Scanner Engine

**FR-100: Agent Configuration Parsing**
- The system SHALL parse agent configurations from supported frameworks (LangChain, OpenAI Agents SDK, CrewAI)
- The system SHALL accept configuration via YAML file (`agentwall.yaml`), CLI flags, or automatic detection from project structure
- The system SHALL support scanning a single agent or multiple agents in a monorepo

**FR-101: Memory Leakage Detection**
- The system SHALL detect cross-user memory access patterns where Agent A can retrieve memories belonging to User B
- The system SHALL simulate multi-tenant memory queries against the configured vector store / memory backend
- The system SHALL flag any retrieval result that returns data outside the scoped user/session boundary
- The system SHALL support detection for: ChromaDB, Pinecone, Weaviate, Qdrant, pgvector, Redis, Milvus (extensible via adapters)

**FR-102: Memory Poisoning Analysis**
- The system SHALL detect whether injected/malicious content in memory can influence agent behavior
- The system SHALL test for: prompt injection via stored memory, instruction override via retrieved context, data exfiltration via memory-to-tool chains
- The system SHALL generate synthetic poisoned memory entries and test whether the agent acts on them

**FR-103: Tool Permission Audit**
- The system SHALL enumerate all tools/functions available to an agent
- The system SHALL classify each tool's risk level (read-only, state-changing, external-calling, financial, destructive)
- The system SHALL flag agents with access to tools that exceed their stated purpose
- The system SHALL detect missing tool-level access controls (e.g., no user-role check before tool invocation)

**FR-104: Unsafe Action Path Detection**
- The system SHALL trace possible execution paths from user input → tool calls → side effects
- The system SHALL flag paths where high-risk actions (data deletion, financial transactions, external API calls, PII exposure) occur without an approval gate or confirmation step
- The system SHALL support configurable risk thresholds per action type

**FR-105: Traceability Gap Detection**
- The system SHALL verify that agent execution produces audit-compatible logs
- The system SHALL flag agents that: lack request-level trace IDs, don't log tool invocations, don't record memory retrievals, don't capture approval/denial decisions
- The system SHALL output a traceability score (0–100)

### 5.2 Framework Adapters

**FR-200: LangChain / LangGraph Adapter**
- The system SHALL introspect LangChain agent definitions including: tool lists, memory backends, chain/graph structure, callback handlers
- The system SHALL support LangGraph state machines and detect unsafe state transitions

**FR-201: OpenAI Agents SDK Adapter**
- The system SHALL parse OpenAI agent definitions including: function/tool schemas, instruction prompts, handoff configurations
- The system SHALL detect over-permissioned function definitions

**FR-202: CrewAI Adapter**
- The system SHALL parse CrewAI agent/task/crew definitions
- The system SHALL detect cross-agent tool sharing risks and delegation chain vulnerabilities

**FR-203: Generic Adapter Interface**
- The system SHALL provide an `AbstractFrameworkAdapter` base class for community-contributed framework support
- Adapter interface: `parse_config()`, `enumerate_tools()`, `enumerate_memory()`, `trace_action_paths()`

### 5.3 Reporting

**FR-300: Scan Report Generation**
- The system SHALL produce reports in: JSON (machine-readable), HTML (human-readable), SARIF (for GitHub Security tab integration), plain text (terminal output)
- Each finding SHALL include: severity (critical/high/medium/low/info), category, description, affected component, remediation guidance, evidence

**FR-301: CI/CD Integration**
- The system SHALL exit with code 0 (pass), 1 (findings above threshold), 2 (scanner error)
- The system SHALL support `--fail-on` flag to set minimum severity threshold
- The system SHALL support SARIF output for GitHub Advanced Security integration

### 5.4 Configuration

**FR-400: Configuration File**
- The system SHALL support `agentwall.yaml` at project root
- Configuration SHALL include: framework type, memory backend config, scan targets, severity thresholds, custom policy rules, ignore patterns

**FR-401: Policy Rules**
- The system SHALL support built-in policy rules (default ruleset)
- The system SHALL support custom policy rules defined in YAML
- Policy rule format: `id`, `description`, `severity`, `check_type`, `parameters`, `remediation`

---

## 6. Non-Functional Requirements

### 6.1 Performance

| ID | Requirement | Target |
|---|---|---|
| NFR-01 | Single agent scan time (10 tools, 1 memory backend) | < 30 seconds |
| NFR-02 | Full project scan (5 agents, 50 tools) | < 3 minutes |
| NFR-03 | Memory footprint during scan | < 512 MB RAM |
| NFR-04 | CLI cold start time | < 2 seconds |
| NFR-05 | CI pipeline overhead | < 5 minutes total |

### 6.2 Reliability

| ID | Requirement | Target |
|---|---|---|
| NFR-10 | Scanner crash rate | < 0.1% of scans |
| NFR-11 | False positive rate (memory leakage) | < 15% |
| NFR-12 | False negative rate (critical findings) | < 5% |
| NFR-13 | Graceful degradation on unsupported config | Warning, not crash |

### 6.3 Security

| ID | Requirement | Target |
|---|---|---|
| NFR-20 | Scanner SHALL NOT execute agent code in production mode | Mandatory |
| NFR-21 | Scanner SHALL NOT exfiltrate scanned project data | Mandatory |
| NFR-22 | All network calls SHALL be opt-in and documented | Mandatory |
| NFR-23 | Scanner SHALL operate fully offline (no cloud dependency) | Mandatory |
| NFR-24 | Scan results SHALL NOT contain raw secrets/credentials | Mandatory |

### 6.4 Usability

| ID | Requirement | Target |
|---|---|---|
| NFR-30 | Time from `pip install` to first scan result | < 10 minutes |
| NFR-31 | Zero-config scan (auto-detect framework) | Supported |
| NFR-32 | Clear, actionable remediation guidance per finding | Mandatory |
| NFR-33 | Colored terminal output with severity indicators | Mandatory |

### 6.5 Compatibility

| ID | Requirement | Target |
|---|---|---|
| NFR-40 | Python version support | 3.10+ |
| NFR-41 | OS support | Linux, macOS, Windows (WSL) |
| NFR-42 | CI platforms | GitHub Actions, GitLab CI, Jenkins, CircleCI |
| NFR-43 | Framework versions | LangChain 0.2+, OpenAI SDK 1.0+, CrewAI 0.5+ |

### 6.6 Extensibility

| ID | Requirement | Target |
|---|---|---|
| NFR-50 | Plugin architecture for custom checks | Supported |
| NFR-51 | Custom framework adapter interface | Documented API |
| NFR-52 | Custom report format via templates | Supported |
| NFR-53 | Policy rule authoring by end users | YAML-based |

### 6.7 Maintainability

| ID | Requirement | Target |
|---|---|---|
| NFR-60 | Test coverage | > 80% |
| NFR-61 | Automated release pipeline | GitHub Actions |
| NFR-62 | Semantic versioning | Mandatory |
| NFR-63 | Changelog generation | Automated |

---

## 7. Constraints

### 7.1 Technical Constraints

| ID | Constraint | Impact | Mitigation |
|---|---|---|---|
| C-01 | **Static analysis only (Phase 0/1)** — Scanner cannot execute agent code at runtime; must rely on configuration introspection and simulation | Limits detection accuracy for dynamic behavior | Design adapter interface to support both static and dynamic modes; dynamic mode in Phase 3 |
| C-02 | **Framework API instability** — LangChain, OpenAI SDK, and CrewAI ship breaking changes frequently | Adapter maintenance burden | Pin minimum versions, use abstraction layer, automated compatibility tests |
| C-03 | **No universal agent definition standard** — Each framework defines agents, tools, and memory differently | Increases adapter complexity | Normalize into internal canonical model (AgentSpec) |
| C-04 | **Memory backend diversity** — 8+ vector store backends with different APIs and access patterns | Large integration surface | Start with top 3 (ChromaDB, Pinecone, pgvector), plugin architecture for rest |
| C-05 | **Python-only CLI** — Limits adoption in Go/Rust/Node agent ecosystems | Misses non-Python agent builders | Phase 2: consider polyglot support or language-agnostic config scanning |
| C-06 | **Offline-first requirement** — No cloud calls in base product | Cannot leverage cloud-based analysis or threat intelligence | Local rule engine; optional cloud intelligence feed in Pro tier |

### 7.2 Business Constraints

| ID | Constraint | Impact |
|---|---|---|
| C-10 | Small team (1–3 engineers initially) | Must prioritize ruthlessly; no parallel feature tracks |
| C-11 | OSS-first model requires delaying monetization | Revenue deferred to Phase 2+ (team tier) |
| C-12 | Enterprise features must not gate developer adoption | Core scanner must remain fully free/OSS |
| C-13 | Must not require API keys or accounts for basic usage | Frictionless onboarding is critical for bottom-up distribution |

### 7.3 Regulatory / Compliance Constraints

| ID | Constraint | Impact |
|---|---|---|
| C-20 | EU AI Act compliance (when applicable) | Phase 5 features must support regulatory evidence export |
| C-21 | SOC 2 readiness for SaaS tier | Required before enterprise sales (Phase 4+) |
| C-22 | GDPR implications if SaaS tier stores scan results | Data residency and retention policies required |

---

## 8. Potential Technical Blockages

### 8.1 Critical Blockages

**TB-01: Memory Isolation Testing Without Runtime Access**
- **Problem:** Detecting cross-user memory leakage in vector stores requires either: (a) runtime access to the actual vector store, or (b) a simulation environment that mirrors the store's access control model. In Phase 0/1 (static analysis only), we cannot connect to production stores.
- **Severity:** High
- **Impact:** Core feature (FR-101) may produce theoretical findings rather than confirmed vulnerabilities
- **Mitigation:**
  - Provide a "live scan" mode that connects to a staging vector store (opt-in)
  - Build a simulation engine that models common vector store configurations
  - Ship with test fixtures that reproduce known leakage patterns
  - Clearly label findings as "potential" vs "confirmed" based on scan mode

**TB-02: Framework Adapter Fragility**
- **Problem:** LangChain ships breaking changes roughly every 2–4 weeks. OpenAI SDK has undergone 3 major restructures in 12 months. Adapter code may break on framework updates.
- **Severity:** High
- **Impact:** Users on latest framework versions may get scan failures or false results
- **Mitigation:**
  - Version-pinned adapter modules with compatibility matrices
  - Automated weekly CI against latest framework versions
  - Graceful degradation: partial scan > crash
  - Community adapter contributions via plugin interface

**TB-03: Tool Risk Classification Accuracy**
- **Problem:** Classifying whether a tool is "read-only" vs "state-changing" vs "destructive" requires understanding tool semantics, which varies wildly across custom tool implementations.
- **Severity:** Medium-High
- **Impact:** False positives (safe tools flagged as dangerous) erode user trust; false negatives (dangerous tools missed) are security risks
- **Mitigation:**
  - Heuristic classification based on tool name, docstring, and parameter schema
  - LLM-assisted classification as optional enhancement (uses local model via Ollama or API)
  - User-defined tool risk annotations in `agentwall.yaml`
  - Community-maintained tool risk database

### 8.2 Moderate Blockages

**TB-04: Action Path Explosion**
- **Problem:** Tracing all possible execution paths through an agent with 20+ tools and conditional routing can produce exponential path combinations.
- **Severity:** Medium
- **Impact:** Scan time exceeds NFR-02 targets; incomplete path coverage
- **Mitigation:**
  - Depth-limited traversal (configurable, default: 5 hops)
  - Prioritize paths containing high-risk tools
  - Cache and prune duplicate sub-paths
  - Parallel path evaluation

**TB-05: Memory Poisoning Detection Requires LLM Inference**
- **Problem:** Determining whether a poisoned memory entry can influence agent behavior requires running (or simulating) LLM inference with the poisoned context.
- **Severity:** Medium
- **Impact:** Without inference, poisoning detection is pattern-matching only (lower accuracy)
- **Mitigation:**
  - Phase 0/1: Pattern-based detection (known injection patterns, instruction overrides in memory content)
  - Phase 2+: Optional LLM-based verification using local Ollama or cheap API calls
  - Capital-aware routing: regex → local model → API (last resort)

**TB-06: CrewAI Multi-Agent Delegation Complexity**
- **Problem:** CrewAI allows agents to delegate tasks to other agents, creating delegation chains where tool permissions are inherited/escalated in non-obvious ways.
- **Severity:** Medium
- **Impact:** Delegation-based privilege escalation may be missed
- **Mitigation:**
  - Model delegation chains as directed graphs
  - Flag any delegation that escalates tool access beyond the delegating agent's own permissions
  - Depth limit on delegation chain analysis

### 8.3 Low-Probability Blockages

**TB-07: Vector Store SDK Incompatibilities**
- Different vector stores require different Python SDK versions that may conflict in the same environment.
- **Mitigation:** Lazy imports, optional dependencies, isolated adapter environments

**TB-08: SARIF Schema Evolution**
- GitHub may update SARIF spec requirements.
- **Mitigation:** Pin SARIF version, automated schema validation tests

---

## 9. High-Level Technical Architecture

### 9.1 Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│                                                                 │
│  CLI (Click/Typer)    CI/CD Runner    [Future: Web Dashboard]   │
└──────────────┬──────────────┬───────────────────────────────────┘
               │              │
               ▼              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      ORCHESTRATOR LAYER                         │
│                                                                 │
│  ScanOrchestrator                                               │
│  ├── ConfigLoader (YAML/CLI/auto-detect)                        │
│  ├── FrameworkResolver (detect which framework)                  │
│  ├── ScanPlanBuilder (determine which checks to run)            │
│  └── ReportAggregator (collect findings → output)               │
└──────────────┬──────────────────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FRAMEWORK ADAPTER LAYER                      │
│                                                                 │
│  ┌───────────────┐ ┌───────────────┐ ┌───────────────┐         │
│  │  LangChain    │ │  OpenAI SDK   │ │   CrewAI      │         │
│  │  Adapter      │ │  Adapter      │ │   Adapter     │         │
│  └──────┬────────┘ └──────┬────────┘ └──────┬────────┘         │
│         │                 │                 │                   │
│         ▼                 ▼                 ▼                   │
│  ┌─────────────────────────────────────────────────────┐       │
│  │            Canonical AgentSpec Model                 │       │
│  │  { agents[], tools[], memory_config, action_graph } │       │
│  └─────────────────────────────────────────────────────┘       │
└──────────────┬──────────────────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────────────────┐
│                      ANALYSIS ENGINE                            │
│                                                                 │
│  ┌──────────────────┐  ┌──────────────────┐                    │
│  │  Memory Analyzer  │  │  Tool Analyzer   │                    │
│  │  ├─ LeakDetector  │  │  ├─ PermAuditor  │                    │
│  │  ├─ PoisonDetect  │  │  ├─ RiskClassify │                    │
│  │  └─ IsolatCheck   │  │  └─ ScopeCheck   │                    │
│  └──────────────────┘  └──────────────────┘                    │
│                                                                 │
│  ┌──────────────────┐  ┌──────────────────┐                    │
│  │  Action Analyzer  │  │  Trace Analyzer  │                    │
│  │  ├─ PathTracer    │  │  ├─ LogAuditor   │                    │
│  │  ├─ RiskScorer    │  │  ├─ TraceIDCheck │                    │
│  │  └─ ApprovalGap   │  │  └─ ScoreCalc    │                    │
│  └──────────────────┘  └──────────────────┘                    │
└──────────────┬──────────────────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────────────────┐
│                       POLICY ENGINE                             │
│                                                                 │
│  RuleRegistry                                                   │
│  ├── BuiltinRules (default security checks)                     │
│  ├── CustomRules (user YAML definitions)                        │
│  ├── RuleEvaluator (match findings against policy)              │
│  └── SeverityResolver (contextual severity assignment)          │
└──────────────┬──────────────────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────────────────┐
│                      REPORTING LAYER                            │
│                                                                 │
│  ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐      │
│  │   JSON    │ │   HTML    │ │   SARIF   │ │  Terminal  │      │
│  │  Reporter │ │  Reporter │ │  Reporter │ │  Reporter  │      │
│  └───────────┘ └───────────┘ └───────────┘ └───────────┘      │
└─────────────────────────────────────────────────────────────────┘
```

### 9.2 Component Details

#### 9.2.1 CLI Layer

```
Technology: Typer (Click-based, type-safe CLI framework)
Entry points:
  agentwall scan [PATH]           # Run trust scan
  agentwall scan --framework X    # Force framework detection
  agentwall init                  # Generate agentwall.yaml template
  agentwall rules list            # List available rules
  agentwall rules check RULE_ID   # Run single rule
  agentwall report PATH           # Re-render report from JSON
  agentwall version               # Version info
```

#### 9.2.2 Canonical AgentSpec Model

All framework adapters normalize into this internal model:

```python
@dataclass
class AgentSpec:
    """Framework-agnostic agent representation."""
    name: str
    framework: FrameworkType          # langchain | openai | crewai | generic
    tools: list[ToolSpec]
    memory: MemorySpec | None
    action_graph: ActionGraph         # DAG of possible execution paths
    metadata: dict[str, Any]

@dataclass
class ToolSpec:
    name: str
    description: str
    parameters: dict[str, ParamSpec]
    risk_level: RiskLevel             # read_only | state_changing | external | financial | destructive
    requires_approval: bool
    scope: ToolScope                  # user | admin | system

@dataclass
class MemorySpec:
    backend: MemoryBackendType        # chroma | pinecone | pgvector | ...
    isolation_model: IsolationModel   # none | session | user | tenant
    access_pattern: AccessPattern     # shared | scoped | filtered
    connection_config: dict[str, Any] # sanitized, no secrets

@dataclass
class ActionGraph:
    nodes: list[ActionNode]           # tool calls, memory ops, decisions
    edges: list[ActionEdge]           # transitions with conditions
    entry_points: list[str]
    risk_paths: list[RiskPath]        # pre-computed high-risk paths
```

#### 9.2.3 Analysis Engine

Four independent analyzers run in parallel:

| Analyzer | Input | Output | Method |
|---|---|---|---|
| **MemoryAnalyzer** | MemorySpec + backend config | Memory findings (leaks, poisoning, isolation gaps) | Config analysis + simulation probes |
| **ToolAnalyzer** | ToolSpec[] | Tool findings (over-permission, missing scope, risk) | Schema analysis + heuristic classification |
| **ActionAnalyzer** | ActionGraph | Action findings (unsafe paths, missing approvals) | Graph traversal + risk scoring |
| **TraceAnalyzer** | AgentSpec + logging config | Trace findings (missing logs, no trace IDs) | Config audit + pattern matching |

#### 9.2.4 Policy Engine

```python
class PolicyRule:
    id: str              # e.g., "AW-MEM-001"
    name: str
    category: Category   # memory | tool | action | trace
    severity: Severity   # critical | high | medium | low | info
    description: str
    check: Callable[[AgentSpec], list[Finding]]
    remediation: str
    references: list[str]
    tags: list[str]
```

Rule ID convention:
- `AW-MEM-XXX` — Memory rules
- `AW-TOOL-XXX` — Tool rules
- `AW-ACT-XXX` — Action rules
- `AW-TRACE-XXX` — Traceability rules

### 9.3 Directory Structure

```
agentwall/
├── pyproject.toml
├── README.md
├── agentwall/
│   ├── __init__.py
│   ├── cli/
│   │   ├── __init__.py
│   │   ├── main.py                 # Typer app entry
│   │   ├── commands/
│   │   │   ├── scan.py
│   │   │   ├── init.py
│   │   │   ├── rules.py
│   │   │   └── report.py
│   │   └── output.py               # Terminal formatting (Rich)
│   ├── core/
│   │   ├── __init__.py
│   │   ├── orchestrator.py          # ScanOrchestrator
│   │   ├── config.py                # ConfigLoader
│   │   ├── models.py                # AgentSpec, ToolSpec, etc.
│   │   └── findings.py              # Finding, ScanResult
│   ├── adapters/
│   │   ├── __init__.py
│   │   ├── base.py                  # AbstractFrameworkAdapter
│   │   ├── langchain_adapter.py
│   │   ├── openai_adapter.py
│   │   ├── crewai_adapter.py
│   │   └── generic_adapter.py
│   ├── analyzers/
│   │   ├── __init__.py
│   │   ├── memory.py                # MemoryAnalyzer
│   │   ├── tools.py                 # ToolAnalyzer
│   │   ├── actions.py               # ActionAnalyzer
│   │   └── trace.py                 # TraceAnalyzer
│   ├── policy/
│   │   ├── __init__.py
│   │   ├── engine.py                # PolicyEngine
│   │   ├── rules/
│   │   │   ├── memory_rules.py
│   │   │   ├── tool_rules.py
│   │   │   ├── action_rules.py
│   │   │   └── trace_rules.py
│   │   └── registry.py              # RuleRegistry
│   ├── reporters/
│   │   ├── __init__.py
│   │   ├── json_reporter.py
│   │   ├── html_reporter.py
│   │   ├── sarif_reporter.py
│   │   └── terminal_reporter.py
│   └── memory_backends/
│       ├── __init__.py
│       ├── base.py                  # AbstractMemoryProbe
│       ├── chroma_probe.py
│       ├── pinecone_probe.py
│       └── pgvector_probe.py
├── rules/
│   └── default.yaml                 # Default built-in policy rules
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/
│       ├── langchain_agents/
│       ├── openai_agents/
│       └── crewai_agents/
└── docs/
    ├── rules.md
    ├── adapters.md
    └── configuration.md
```

### 9.4 Technology Stack

| Layer | Technology | Rationale |
|---|---|---|
| Language | Python 3.10+ | Matches target user ecosystem (AI/ML engineers) |
| CLI Framework | Typer + Rich | Type-safe CLI with beautiful terminal output |
| Config Parsing | Pydantic v2 | Strict validation, great error messages |
| Graph Analysis | NetworkX | Mature graph library for action path traversal |
| Async Execution | asyncio + concurrent.futures | Parallel analyzer execution |
| Testing | pytest + pytest-asyncio | Standard Python testing |
| Packaging | pyproject.toml + Hatch | Modern Python packaging |
| CI/CD | GitHub Actions | Standard for OSS projects |
| Documentation | MkDocs Material | Developer-friendly docs |
| Linting | Ruff | Fast, comprehensive Python linter |
| Type Checking | mypy (strict) | Type safety enforcement |

### 9.5 Data Flow

```
User runs: agentwall scan ./my-agent-project/

1. CLI parses args → ConfigLoader reads agentwall.yaml (or auto-detects)
2. FrameworkResolver inspects project → identifies LangChain
3. LangChainAdapter.parse() → produces AgentSpec (canonical model)
4. ScanPlanBuilder selects applicable rules based on config + AgentSpec
5. Analyzers run in parallel:
   ├── MemoryAnalyzer → memory findings
   ├── ToolAnalyzer → tool findings
   ├── ActionAnalyzer → action path findings
   └── TraceAnalyzer → traceability findings
6. PolicyEngine evaluates findings against active rules
7. SeverityResolver assigns final severity based on context
8. ReportAggregator merges all findings → ScanResult
9. Reporter renders output (terminal + optional JSON/HTML/SARIF)
10. CLI exits with appropriate code (0=pass, 1=fail, 2=error)
```

### 9.6 Future Architecture Extensions (Phase 2–5)

```
Phase 2: + ScanHistoryStore (SQLite/PostgreSQL)
         + WebDashboard (FastAPI + React)
         + NotificationService (Slack, GitHub)

Phase 3: + PolicyEnforcementService (runtime middleware)
         + ApprovalGateway (webhook-based approval flow)
         + PermissionService (agent role/permission management)

Phase 4: + RuntimeProxy (intercepts agent↔tool↔memory calls)
         + AuditLogService (append-only event store)
         + DecisionTraceService (per-action decision recording)
         + StreamProcessor (real-time policy evaluation)

Phase 5: + ComplianceExportService
         + ForensicReplayEngine
         + OrgPolicyManager
         + IdentityBridge (SSO/SAML integration)
```

---

## 10. Data Model

### 10.1 Core Entities

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   ScanRun    │────▶│   Finding    │────▶│    Rule      │
│              │     │              │     │              │
│ id           │     │ id           │     │ id           │
│ timestamp    │     │ scan_run_id  │     │ category     │
│ project_path │     │ rule_id      │     │ severity     │
│ framework    │     │ severity     │     │ description  │
│ agent_count  │     │ category     │     │ remediation  │
│ status       │     │ description  │     │ check_fn     │
│ duration_ms  │     │ evidence     │     └──────────────┘
│ config_hash  │     │ component    │
└──────────────┘     │ remediation  │
                     └──────────────┘
                            │
                            ▼
                     ┌──────────────┐
                     │   Evidence   │
                     │              │
                     │ type         │
                     │ detail       │
                     │ location     │
                     │ snippet      │
                     └──────────────┘
```

### 10.2 Finding Severity Model

```
CRITICAL  → Confirmed exploitable vulnerability (cross-user data access)
HIGH      → High-confidence risk requiring immediate attention
MEDIUM    → Moderate risk, should be addressed before production
LOW       → Minor risk or best-practice violation
INFO      → Informational observation, no direct risk
```

---

## 11. API Specification Overview

### 11.1 Python SDK (Phase 1)

```python
from agentwall import Scanner, ScanConfig

config = ScanConfig(
    framework="langchain",
    memory_backend="chroma",
    fail_on="high",
)

scanner = Scanner(config)
result = scanner.scan("./my-agent/")

print(result.summary)          # Quick overview
print(result.findings)         # All findings
print(result.exit_code)        # 0 or 1
result.export("report.sarif")  # Export to file
```

### 11.2 REST API (Phase 2+)

```
POST   /api/v1/scans              # Trigger scan
GET    /api/v1/scans/{id}         # Get scan result
GET    /api/v1/scans/{id}/findings # Get findings
GET    /api/v1/projects           # List projects
GET    /api/v1/rules              # List rules
POST   /api/v1/policies           # Create policy
PUT    /api/v1/policies/{id}      # Update policy
```

---

## 12. Phased Delivery Plan

### Phase 0 — Validation (Weeks 1–4)

| Week | Deliverable |
|---|---|
| 1 | Project scaffold, CI setup, core models (AgentSpec), CLI skeleton |
| 2 | LangChain adapter (basic), ToolAnalyzer (permission audit) |
| 3 | MemoryAnalyzer (leakage detection — ChromaDB), terminal reporter |
| 4 | End-to-end scan flow, 3 demo agents, internal dogfooding |

**Exit criteria:** Can run `agentwall scan` on a LangChain project and get meaningful findings.

### Phase 1 — MVP (Weeks 5–12)

| Week | Deliverable |
|---|---|
| 5–6 | OpenAI Agents SDK adapter, ActionAnalyzer |
| 7–8 | CrewAI adapter, TraceAnalyzer, policy engine |
| 9–10 | SARIF + HTML reporters, CI integration, `pip install` packaging |
| 11 | Documentation (MkDocs), README, example configs |
| 12 | Public beta release, Show HN, GitHub launch |

**Exit criteria:** Public OSS release with 3 framework adapters, 4 analyzers, 20+ built-in rules.

---

## 13. Risk Matrix

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| Framework breaking changes break adapters | High | High | Version pinning, weekly CI, adapter abstraction |
| Low initial adoption / discovery | Medium | High | Content marketing (attack research), HN launch, framework community engagement |
| False positive rate erodes trust | Medium | High | Confidence scoring, user feedback loop, severity tuning |
| Competitor copies wedge quickly | Medium | Medium | Move fast to Phase 2/3; moat comes from depth, not wedge |
| Scope creep into governance dashboard | Medium | Medium | Strict phase gates; no dashboard before Phase 2 |
| Memory backend diversity overwhelms | Medium | Low | Start with top 3, plugin architecture for rest |

---

## 14. Success Metrics

### Phase 0

| Metric | Target |
|---|---|
| Internal dogfood: findings on real agent projects | >= 5 meaningful findings |
| Scan completion rate (no crashes) | > 95% |
| Time to first scan | < 10 minutes |

### Phase 1

| Metric | Target |
|---|---|
| GitHub stars (3 months post-launch) | 500+ |
| Weekly active CLI installs | 200+ |
| CI integrations (GitHub Actions usage) | 50+ repos |
| Community-reported issues (engagement signal) | 30+ |
| Framework coverage | 3 frameworks, 3 memory backends |
| Built-in rules | 20+ |

---

## 15. Glossary

| Term | Definition |
|---|---|
| **Agent** | An AI system that uses memory, tools, and can take actions autonomously |
| **AgentSpec** | AgentWall's canonical, framework-agnostic model of an agent's configuration |
| **Memory leakage** | When an agent can access memory entries belonging to a different user/tenant |
| **Memory poisoning** | Injection of malicious content into an agent's memory to influence its behavior |
| **Tool permission audit** | Analysis of which tools an agent can call vs. which it should be allowed to call |
| **Action path** | A sequence of tool calls and decisions an agent can take from input to side effect |
| **Approval gate** | A checkpoint requiring human approval before a high-risk action executes |
| **SARIF** | Static Analysis Results Interchange Format — standard for security tool output |
| **Control plane** | Infrastructure that manages and enforces policies on a system's behavior |
| **Trust boundary** | The line between what an agent is allowed and not allowed to access/do |

---

*End of document.*
