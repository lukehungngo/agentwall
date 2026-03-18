# AgentWall: Competitive Landscape Analysis

**Research Date:** March 2026
**Market Gap:** No tool currently performs **pre-deployment static analysis specifically for AI agent memory security** (vector store tenant isolation, memory leakage detection, embedding security).

---

## Executive Summary

The AI security market has fragmented across five major categories:
1. **Traditional SAST tools** (code security) that added AI/LLM support
2. **AI-specific red-teaming tools** (runtime testing, post-deploy)
3. **Observability platforms** with security features (runtime monitoring)
4. **AI governance/compliance** (enterprise policy & audit)
5. **Runtime guardrails** (behavioral enforcement at inference)

**AgentWall is the only tool in the "pre-deploy static analysis for agent memory security" category.** It shifts-left to catch memory and permission misconfigurations before agents reach production.

---

## Category 1: SAST / Code Security Tools

These tools scan code for vulnerabilities. Some have added LLM/AI support, but **none analyze agent memory configurations statically**.

### Snyk Code
- **Category:** SAST (code scanning) + LLM-aware
- **Agent Memory Security:** NO
- **Deployment:** Pre-deploy (static)
- **Open Source:** Commercial
- **Differentiation:**
  Focuses on supply chain security for AI-generated code. Detects taint flows from LLM libraries (OpenAI, HuggingFace, Anthropic) to outputs. Covers ~48% of AI-generated code contains vulnerabilities. Does NOT audit vector store isolation or memory configurations.
  **Gap:** No analysis of agent-level memory isolation or tool permissions.

**Sources:** [Snyk Code](https://snyk.io/product/snyk-code/) | [Snyk AI Security Fabric](https://snyk.io/)

### Semgrep
- **Category:** SAST (pattern matching) + AI-assisted triage
- **Agent Memory Security:** NO
- **Deployment:** Pre-deploy (static)
- **Open Source:** Yes (OSS + Pro)
- **Differentiation:**
  AST-based pattern matching with AI-powered noise filtering. Recently added Semgrep Memories (learns from security decisions) and multimodal detection (SAST + LLM-powered analysis for logic flaws). Does NOT understand agent memory architecture.
  **Gap:** Generic code scanning; no agent-specific security rules.

**Sources:** [Semgrep App Security Platform](https://semgrep.dev/) | [AI-Powered Detection](https://semgrep.dev/blog/2025/ai-powered-detection-with-semgrep/)

### CodeQL
- **Category:** SAST (semantic code analysis)
- **Agent Memory Security:** NO
- **Deployment:** Pre-deploy (static)
- **Open Source:** Yes (with proprietary extensions)
- **Differentiation:**
  GitHub's semantic query language for code. Recently integrated LLMs to auto-model APIs and reduce false negatives. Framework CQLLM automates CodeQL rule generation. Does NOT analyze agent architectures or memory systems.
  **Gap:** LLM/AI framework context not included.

**Sources:** [CodeQL](https://codeql.github.com/) | [GitHub Blog: AI Vulnerability Detection](https://github.blog/security/vulnerability-research/codeql-team-uses-ai-to-power-vulnerability-detection-in-code/)

### SonarQube
- **Category:** SAST + code quality + AI integration
- **Agent Memory Security:** NO
- **Deployment:** Pre-deploy (static)
- **Open Source:** OSS + Commercial
- **Differentiation:**
  Analyzes 35+ languages. AI CodeFix auto-generates fixes. AI Code Assurance detects AI-generated code. As of Jan 2026, integrated with AI-native IDEs (Cursor, Claude Code, Windsurf). Does NOT audit agent memory architecture.
  **Gap:** AI code quality, not agent security.

**Sources:** [SonarQube](https://www.sonarsource.com/products/sonarqube/) | [SonarQube 2026.1 Release](https://www.almtoolbox.com/blog/sonarqube-2026-1-release/)

### Checkmarx
- **Category:** SAST + SCA + AI hybrid analysis
- **Agent Memory Security:** NO
- **Deployment:** Pre-deploy (static)
- **Open Source:** Commercial
- **Differentiation:**
  Developer Assist (agentic AI inside IDE) provides real-time SCA of dependencies. AI SAST + DAST hybrid engine. Specialized security for LLMs: detects insecure deserialization, dangerous model loaders, shell execution, pickle gadgets. Does NOT audit agent memory systems.
  **Gap:** Code-level LLM security; no agent-level memory audit.

**Sources:** [Checkmarx AI Security](https://checkmarx.com/ai-llm-tools-in-application-security/) | [Developer Assist](https://checkmarx.com/ai-llm-tools-in-application-security/revolutionizing-sca-with-agentic-ai-how-checkmarx-developer-assist-transforms-open-source-security-within-the-ide/)

---

## Category 2: AI/LLM-Specific Security Tools

Tools built for LLM vulnerabilities: prompt injection, jailbreaks, red-teaming. **Most are runtime (post-deploy), not pre-deploy static analysis.**

### Lakera Guard
- **Category:** Runtime guardrails + prompt injection detection
- **Agent Memory Security:** Partial (detects prompt injection, not memory isolation)
- **Deployment:** Runtime (live API)
- **Open Source:** Commercial (SaaS + self-hosted)
- **Differentiation:**
  Detects instruction overrides, jailbreaks, indirect injections, obfuscated prompts. Screens 100+ languages. Learns from 100K+ daily attacks (Gandalf dataset). Does NOT audit memory configuration or vector store isolation statically.
  **Gap:** Input/output filtering, not memory architecture audit.

**Sources:** [Lakera Guard](https://www.lakera.ai/lakera-guard) | [Prompt Defense](https://www.lakera.ai/prompt-defense)

### Promptfoo (Acquired by OpenAI, March 2026)
- **Category:** Red-teaming + security testing
- **Agent Memory Security:** NO (tests behavior, not code)
- **Deployment:** Pre-deploy testing (automated red-teaming)
- **Open Source:** Commercial (being integrated into OpenAI Frontier)
- **Differentiation:**
  Tests 50+ vulnerability types (injection, jailbreaks, data leaks, tool misuse). Automatically generates adversarial inputs. Community: 300K+ users. Recently acquired by OpenAI to integrate into Frontier platform. Does NOT statically analyze code; runs behavioral tests against live agents.
  **Gap:** Behavioral testing, not static code analysis.

**Sources:** [OpenAI Acquires Promptfoo](https://openai.com/index/openai-to-acquire-promptfoo/) | [Promptfoo Website](https://www.promptfoo.dev/)

### Garak (NVIDIA/OWASP)
- **Category:** Red-teaming / LLM vulnerability scanner
- **Agent Memory Security:** NO
- **Deployment:** Pre-deploy testing (probes model directly)
- **Open Source:** Yes (Apache 2.0)
- **Differentiation:**
  Probes for hallucination, data leakage, prompt injection, misinformation, jailbreaks. Combines static, dynamic, and adaptive probes. Mapped to OWASP Top 10 for LLM. Does NOT analyze agent code or memory systems.
  **Gap:** Model-level testing, not agent architecture audit.

**Sources:** [Garak GitHub](https://github.com/NVIDIA/garak) | [Garak Website](https://garak.ai/)

### Giskard
- **Category:** AI model testing + governance
- **Agent Memory Security:** Partial (black-box testing for hallucination/leakage, not static analysis)
- **Deployment:** Pre-deploy testing (black-box API endpoint)
- **Open Source:** Yes (OSS library) + Commercial hub
- **Differentiation:**
  Black-box testing library for LLM agents & RAG. Tests hallucinations, harmful content, robustness, data leakage. Hub for compliance (EU AI Act, ISO42001). Does NOT analyze code; requires agent to be callable via API endpoint.
  **Gap:** Black-box behavior testing, not static code analysis.

**Sources:** [Giskard Website](https://www.giskard.ai/) | [Giskard GitHub](https://github.com/Giskard-AI/giskard-oss)

### Rebuff
- **Category:** Prompt injection detection framework
- **Agent Memory Security:** NO
- **Deployment:** Runtime (inference-time detection)
- **Open Source:** Yes (GitHub)
- **Differentiation:**
  4-layer defense: heuristics, LLM-based detection, VectorDB embeddings of attacks, canary tokens. Self-hardening framework. Prototype status (not 100% secure). Does NOT audit memory isolation or agent permissions.
  **Gap:** Injection detection only, not memory architecture.

**Sources:** [Rebuff GitHub](https://github.com/protectai/rebuff) | [LangChain Blog: Rebuff](https://blog.langchain.com/rebuff/)

### LLM Guard (Protect AI)
- **Category:** Input/output filtering + guardrails
- **Agent Memory Security:** Partial (PII anonymization, secrets detection, not memory isolation)
- **Deployment:** Runtime (inference-time scanning)
- **Open Source:** Yes (MIT license)
- **Differentiation:**
  15 input + 20 output scanners. Covers prompt injection, PII, toxicity, secrets, malicious URLs, bias, factual consistency, data leakage. Modular design. Deployable as library or API. Does NOT statically analyze agent code.
  **Gap:** Inference-time filtering, not pre-deploy code audit.

**Sources:** [LLM Guard GitHub](https://github.com/protectai/llm-guard) | [LLM Guard Website](https://protectai.com/llm-guard)

---

## Category 3: AI Observability Platforms

Platforms for monitoring and debugging LLM agents in production. Some have security features, but **observability ≠ security audit**.

### LangSmith
- **Category:** Observability + evals + tracing
- **Agent Memory Security:** Partial (multi-tenant isolation configs, not static analysis)
- **Deployment:** Runtime (live monitoring)
- **Open Source:** Commercial
- **Differentiation:**
  LangChain's observability platform. Managed cloud + BYOC + self-hosted options. Multi-tenant isolation via project scoping and API key rotation. Automated evals for prompt injection/jailbreak detection. Does NOT statically analyze code before deployment.
  **Gap:** Runtime observability, not pre-deploy scanning.

**Sources:** [LangSmith Observability](https://www.langchain.com/langsmith/observability) | [LangSmith Docs](https://docs.langchain.com/langsmith/observability)

### Arize
- **Category:** ML/LLM observability + evaluation
- **Agent Memory Security:** Partial (on-premise for data isolation, not memory audit)
- **Deployment:** Runtime monitoring
- **Open Source:** Commercial (with open-source components like Phoenix)
- **Differentiation:**
  Decision-level visibility into agent state changes between tool calls. Trace inspection, embedding drift detection, retrieval monitoring. On-premise for strict data isolation. Does NOT analyze agent code statically.
  **Gap:** Production observability, not pre-deploy audit.

**Sources:** [Arize AI](https://arize.com/blog/best-ai-observability-tools-for-autonomous-agents-in-2026/)

### Helicone
- **Category:** LLMOps observability + security
- **Agent Memory Security:** Partial (prompt injection detection via Meta's Llama Guard, not memory isolation audit)
- **Deployment:** Runtime (inference monitoring)
- **Open Source:** Yes (OSS + commercial)
- **Differentiation:**
  One-line integration for trace/session inspection. Built-in security via Llama Guard (meta-llama/Llama-Guard-2) and Prompt Guard. Self-hosting support. Does NOT analyze agent code.
  **Gap:** Runtime security checks, not pre-deploy analysis.

**Sources:** [Helicone Website](https://www.helicone.ai/) | [Helicone LLM Security](https://docs.helicone.ai/features/advanced-usage/llm-security)

### Langfuse
- **Category:** LLM observability + tracing + security & guardrails
- **Agent Memory Security:** Partial (can integrate LLM Guard for runtime filtering, not static analysis)
- **Deployment:** Runtime monitoring
- **Open Source:** Yes (YC W23)
- **Differentiation:**
  Open-source LLM engineering platform. Trace/observability + prompt management + evals. Can integrate LLM Guard for input/output scanning. ISO27001 + SOC2 + GDPR/HIPAA compliance. Does NOT statically analyze agent memory configuration.
  **Gap:** Runtime integration, not pre-deploy audit.

**Sources:** [Langfuse Website](https://langfuse.com/docs/observability/overview) | [Langfuse Security & Guardrails](https://langfuse.com/docs/security-and-guardrails)

---

## Category 4: AI Governance & Compliance Platforms

Enterprise platforms for AI risk management, policy enforcement, and compliance. **Focus is governance, not memory security.**

### Noma Security
- **Category:** AI governance + compliance (AI-SPM)
- **Agent Memory Security:** NO (governance/compliance, not memory audit)
- **Deployment:** Runtime governance
- **Open Source:** Commercial
- **Differentiation:**
  Unified platform to secure and govern AI agents. Real-time monitoring, policy enforcement, compliance for SOC2, ISO27001, EU AI Act. Recently raised $100M Series B (March 2026). Dashboard-centric for CISOs. Does NOT analyze agent code; focuses on runtime policies and audit.
  **Gap:** Enterprise governance layer, not pre-deploy security scanning.

**Sources:** [Noma Security](https://noma.security/) | [Noma Raises $100M](https://noma.security/blog/noma-security-raises-100m-to-drive-adoption-of-ai-agent-security/)

### Galileo Agent Control
- **Category:** Agent governance + observability
- **Agent Memory Security:** NO (policy enforcement, not code audit)
- **Deployment:** Runtime + control plane
- **Open Source:** Yes (Apache 2.0, March 2026)
- **Differentiation:**
  Open-source agent control plane for enterprise governance. Define policies once, deploy anywhere. Runtime mitigation avoids downtime. Integrations: LangGraph, CrewAI, Glean, Cisco AI Defense. Does NOT analyze code; enforces runtime policies.
  **Gap:** Policy/governance layer, not static analysis.

**Sources:** [Galileo Releases Agent Control Plane](https://www.globenewswire.com/news-release/2026/03/11/3253962/0/en/Galileo-Releases-Open-Source-AI-Agent-Control-Plane-to-Help-Enterprises-Govern-Agents-at-Scale.html)

### Operant AI Agent Protector
- **Category:** Runtime agent security + governance
- **Agent Memory Security:** Partial (detects prompt injection, data leaks, over-permissioning at runtime; not static analysis)
- **Deployment:** Runtime (real-time protection)
- **Open Source:** Commercial
- **Differentiation:**
  Real-time agentic security solution (Feb 2026 launch). Combines: shadow agent discovery, secure dev enclaves, observability, inline behavioral threat detection, zero-trust enforcement. Integrates with LangGraph, CrewAI, n8n, ChatGPT SDK. Does NOT statically analyze code before deployment.
  **Gap:** Runtime threat detection, not pre-deploy audit.

**Sources:** [Operant Agent Protector](https://www.operant.ai/platform/agent-protector) | [Press Release](https://www.globenewswire.com/news-release/2026/02/05/3233044/0/en/Operant-AI-Launches-Agent-Protector-The-First-Real-Time-Agentic-Security-Solution-Enabling-Safe-AI-Agent-Innovation-at-Scale.html)

### Zenity
- **Category:** AI agent governance + compliance
- **Agent Memory Security:** Partial (runtime monitoring for data leaks, prompt injection, over-permissioning; not static analysis)
- **Deployment:** Runtime monitoring
- **Open Source:** Commercial
- **Differentiation:**
  Runtime governance for AI agents. Monitors: prompt injection, data leaks, over-permissioned actions. Compliance: ISO/IEC 27701 (PII), GDPR, CCPA. Gartner Cool Vendor 2025. Does NOT analyze code statically.
  **Gap:** Runtime compliance monitoring, not pre-deploy scanning.

**Sources:** [Zenity Website](https://zenity.io) | [2026 Threat Landscape](https://zenity.io/resources/white-papers/2026-threat-landscape-report)

### Credo AI
- **Category:** Responsible AI governance platform
- **Agent Memory Security:** NO (governance/policy, not memory security audit)
- **Deployment:** Governance layer (policy + audit)
- **Open Source:** Commercial
- **Differentiation:**
  Founded 2020. Governance for every model/agent/app. Policy Intelligence Engine merges technical AI risks with regulatory requirements. AI Registry for tracking deployments. Does NOT analyze memory architecture or tool permissions.
  **Gap:** Policy governance, not security scanning.

**Sources:** [Credo AI Website](https://www.credo.ai/) | [AWS Marketplace](https://aws.amazon.com/marketplace/pp/prodview-x67krdatcdday)

### Holistic AI
- **Category:** AI governance + compliance + risk management
- **Agent Memory Security:** NO (governance framework, not memory audit)
- **Deployment:** Governance layer
- **Open Source:** Commercial
- **Differentiation:**
  End-to-end AI governance platform. Discovers every AI system, tests for security/bias/hallucinations/toxicity/privacy leaks, generates compliance proof. Does NOT analyze code; focuses on risk assessment framework.
  **Gap:** Governance framework, not code-level security audit.

**Sources:** [Holistic AI Website](https://www.holisticai.com/)

---

## Category 5: Runtime Guardrails

Tools that enforce safety policies at inference time by intercepting inputs/outputs.

### Guardrails AI
- **Category:** Runtime guardrails + validation
- **Agent Memory Security:** NO (validates outputs, not memory isolation)
- **Deployment:** Runtime (inference-time)
- **Open Source:** Yes (GitHub)
- **Differentiation:**
  Python framework: Input/Output Guards. Wraps model with policies (what it sees, says, can do). Guardrails Hub: pre-built validators. Deployable as Flask REST API or library. Does NOT analyze agent memory configuration.
  **Gap:** Output validation, not memory architecture audit.

**Sources:** [Guardrails GitHub](https://github.com/guardrails-ai/guardrails) | [LangChain Docs](https://docs.langchain.com/oss/python/langchain/guardrails)

### NVIDIA NeMo Guardrails
- **Category:** Runtime guardrails + safety rails
- **Agent Memory Security:** NO (content moderation, not memory isolation)
- **Deployment:** Runtime (inference-time)
- **Open Source:** Yes (GitHub)
- **Differentiation:**
  Programmable guardrails for LLM conversational systems. 5 types of rails: input, dialog, retrieval, output, message. GPU-accelerated. Supports content safety, RAG grounding, jailbreak prevention. Does NOT audit agent memory architecture.
  **Gap:** Inference-time safety, not pre-deploy code audit.

**Sources:** [NVIDIA NeMo Guardrails](https://developer.nvidia.com/nemo-guardrails) | [GitHub](https://github.com/NVIDIA-NeMo/Guardrails)

---

## Category 6: OWASP Agent Memory Guard

OWASP initiative providing **guidelines and best practices** (not automated tooling).

### OWASP Agent Memory Guard
- **Category:** Guidelines / Security Framework (NOT automated tooling)
- **Agent Memory Security:** YES (defines memory poisoning mitigations)
- **Deployment:** N/A (reference guide)
- **Open Source:** Yes (OWASP Cheat Sheet Series)
- **Differentiation:**
  Part of OWASP Top 10 for Agentic Applications 2026. Provides mitigations for memory poisoning:
  - Validate/sanitize data before storing
  - Memory isolation between users/sessions
  - Memory expiration and size limits
  - Audit memory contents for PII before persistence
  - Cryptographic integrity checks (SHA-256 hashing)

  **This is guidance, not automation. No scanner, no AST analysis, no CI/CD integration.**
  **Gap:** Manual audit checklist only. No automated scanning.

**Sources:** [OWASP Agent Memory Guard](https://owasp.org/www-project-agent-memory-guard/) | [AI Agent Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html)

---

## Market Gap Analysis: The AgentWall Niche

### What the Market Provides

| Tool | SAST | Red-Team | Observability | Governance | Guardrails | **Pre-Deploy Static Memory Audit** |
|---|---|---|---|---|---|---|
| Snyk | ✓ | | | | | ✗ |
| Semgrep | ✓ | | | | | ✗ |
| CodeQL | ✓ | | | | | ✗ |
| SonarQube | ✓ | | | | | ✗ |
| Checkmarx | ✓ | | | | | ✗ |
| Lakera Guard | | | | | ✓ | ✗ |
| Promptfoo | | ✓ | | | | ✗ |
| Garak | | ✓ | | | | ✗ |
| Giskard | | ✓ | | | | ✗ |
| Rebuff | | | | | ✓ | ✗ |
| LLM Guard | | | | | ✓ | ✗ |
| LangSmith | | | ✓ | | | ✗ |
| Arize | | | ✓ | | | ✗ |
| Helicone | | | ✓ | | ✓ | ✗ |
| Langfuse | | | ✓ | | ✓ | ✗ |
| Noma | | | | ✓ | | ✗ |
| Galileo | | | ✓ | ✓ | | ✗ |
| Operant | | | ✓ | | | ✗ |
| Zenity | | | ✓ | | | ✗ |
| Credo AI | | | | ✓ | | ✗ |
| Holistic AI | | | | ✓ | | ✗ |
| Guardrails AI | | | | | ✓ | ✗ |
| NeMo Guardrails | | | | | ✓ | ✗ |
| OWASP Guard | Manual Checklist Only | | | | | ✗ |
| **AgentWall** | | | | | | **✓** |

### Why the Gap Exists

1. **SAST tools** (Snyk, Semgrep, CodeQL) are language-generic. They don't understand agent-specific architectures (vector stores, memory backends, tool registries).

2. **Red-teaming tools** (Promptfoo, Garak, Giskard) require a live agent to test. They can't detect misconfigurations in code before deployment.

3. **Observability platforms** (LangSmith, Arize, Helicone) are post-deploy. They monitor runtime behavior, not pre-deploy code structure.

4. **Governance platforms** (Noma, Galileo, Zenity) enforce policies at runtime via human review or behavioral gates. They don't analyze code before commit.

5. **Guardrails** (Lakera, Rebuff, LLM Guard) filter inputs/outputs at inference time. They don't audit memory architecture or tool permissions.

6. **OWASP Agent Memory Guard** is a manual checklist. No automation, no CI/CD integration, no AST analysis.

### What AgentWall Provides (Unique)

```
Development         Pre-Deploy             Runtime              Post-Incident
───────────       ─────────────          ─────────────        ─────────────
Code → Build  →  ★ AgentWall ★      →  Galileo/Operant  →  Noma/Zenity
                 (static analysis)      (enforce policy)     (audit/forensics)
                 - Memory isolation
                 - Tool permissions
                 - Embedding security
```

**AgentWall's unique capabilities:**

1. **AST-based memory audit** — parses agent code without running it
   - Detects unfiltered vector store queries (AW-MEM-001)
   - Flags metadata mismatch (AW-MEM-002)
   - Identifies access control gaps (AW-MEM-003)
   - Catches injection patterns (AW-MEM-004)

2. **Tool permission analysis** — scans tool definitions for destructive/arbitrary actions
   - Flags tools without approval gates (AW-TOOL-001)
   - Detects code/SQL/shell command tools (AW-TOOL-002)
   - Identifies over-scoped tools (AW-TOOL-003)

3. **Pre-commit, zero-dependency** — runs in CI/CD before merge
   - No vector store SDKs required (L7/L8 optional)
   - Fully offline by default
   - Fails safe: never crashes entire scan

4. **Framework-aware** — understands LangChain/LangGraph agent architecture
   - Extracts vector stores, memory backends, tools from AST
   - Inter-procedural call graph for cross-file resolution
   - Taint analysis from request entry to filter sink

---

## AgentWall's Market Positioning

### Customers

- **Solo AI engineers** shipping side projects → fast, free, no bloat
- **Seed/Series A startups** with multi-tenant agents → catch memory leaks before launch
- **OSS contributors** building agent frameworks → integrate pre-deploy checks
- **Teams without $50K+ budget** for enterprise platforms → open-source alternative

### Complementary (Not Competitive)

- **For Galileo/Operant** (runtime governance): AgentWall handles pre-deploy, they handle runtime enforcement
- **For Noma/Zenity** (audit/compliance): AgentWall catches issues before deployment, they audit post-incident
- **For observability platforms**: AgentWall prevents misconfigurations, they monitor what's deployed

### Not Competing With

- Traditional SAST tools (language-generic, not agent-aware)
- Red-teaming tools (require live agent)
- Inference-time guardrails (different phase of pipeline)

---

## Sources

### SAST Tools
- [Snyk Code](https://snyk.io/product/snyk-code/)
- [Semgrep](https://semgrep.dev/)
- [CodeQL](https://codeql.github.com/)
- [SonarQube](https://www.sonarsource.com/products/sonarqube/)
- [Checkmarx](https://checkmarx.com/)

### AI/LLM-Specific Tools
- [Lakera Guard](https://www.lakera.ai/lakera-guard)
- [Promptfoo](https://www.promptfoo.dev/) (Acquired by OpenAI March 2026)
- [Garak](https://garak.ai/)
- [Giskard](https://www.giskard.ai/)
- [Rebuff](https://github.com/protectai/rebuff)
- [LLM Guard](https://protectai.com/llm-guard)

### Observability Platforms
- [LangSmith](https://www.langchain.com/langsmith/observability)
- [Arize](https://arize.com/)
- [Helicone](https://www.helicone.ai/)
- [Langfuse](https://langfuse.com/)

### Governance & Compliance
- [Noma Security](https://noma.security/)
- [Galileo](https://galileo.ai/)
- [Operant AI](https://www.operant.ai/)
- [Zenity](https://zenity.io)
- [Credo AI](https://www.credo.ai/)
- [Holistic AI](https://www.holisticai.com/)

### Runtime Guardrails
- [Guardrails AI](https://github.com/guardrails-ai/guardrails)
- [NVIDIA NeMo Guardrails](https://developer.nvidia.com/nemo-guardrails)

### Guidelines & Research
- [OWASP Agent Memory Guard](https://owasp.org/www-project-agent-memory-guard/)
- [OWASP Top 10 Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)
- [Mend: Securing AI Agent Configurations (2026)](https://www.mend.io/blog/ai-agent-configuration-scanning/)
- [Multi-Tenant RAG Security (2026)](https://www.maviklabs.com/blog/multi-tenancy-rag-2026)

---

## Conclusion

**AgentWall fills a critical market gap:** the absence of **automated, pre-deployment static analysis for AI agent memory and permission security**.

Every other tool operates at a different phase:
- Earlier phases focus on code vulnerabilities, not agent architecture
- Later phases enforce runtime policies or monitor post-deploy behavior
- Governance platforms audit after incidents

AgentWall is the **shift-left security scanner** for agents — catching memory leaks, poisoning risks, and unsafe permissions before code reaches CI/CD or production.

This positions AgentWall as the **essential first step** in the agent security pipeline:

```
1. AgentWall (pre-deploy static scan)  ← Shift left
2. Galileo/Operant (runtime governance)
3. Noma/Zenity (audit & response)
```
