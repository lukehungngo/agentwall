# AgentWall v1.x — Agent Integration & Developer Workflow Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship the three highest-leverage v1.x improvements that unblock launch visibility and AI agent adoption: (1) developer workflow config, (2) `agentwall explain` + `agentwall schema` commands, (3) `agentwall prompt-fragment` + `agentwall mcp-serve`.

**Architecture:** CLAUDE.md gets a Workflow and Skills section pointing at installed superpowers skills; `explainer.py` provides a pure-data explanation engine consumed by both the `explain` CLI command and the MCP server; `mcp_server.py` wraps the existing `Scanner`, `verify` logic, and `explainer` behind 4 MCP tools via stdio transport.

**Tech Stack:** Python 3.10+, Typer (CLI), `mcp` SDK (MCP server, stdio transport), Pydantic v2 (schemas), pytest + coverage, ruff, mypy strict.

---

## Chunk 1: Developer Workflow

### Task 1: Add `gotchas.md` and update `CLAUDE.md`

**Files:**
- Create: `gotchas.md` (at repo root: `/home/soh/working/agent-wall/gotchas.md`)
- Modify: `CLAUDE.md` (at repo root)

- [ ] **Step 0: Establish coverage baseline before any changes**

Run: `pytest --cov=agentwall --cov-report=term-missing -q 2>&1 | tail -3`
Record the TOTAL coverage % — this is the floor. All subsequent commits must not drop below it.

- [ ] **Step 1: Create `gotchas.md` with initial entries from Key Gotchas already in CLAUDE.md**

```markdown
# AgentWall — Gotchas & Lessons Learned

> Append a new entry here after EVERY mistake, unexpected behavior, or near-miss.
> Review this file before starting any new task.

---

## 2026-03-18 — Metadata ≠ isolation

`add_texts(metadata={"user_id": x})` without a matching filter on
`similarity_search()` is insecure. Must detect this mismatch explicitly at L1.
Rule: AW-MEM-002.

## 2026-03-18 — FAISS has zero access control

Always flag FAISS as HIGH (AW-MEM-003). Only question is whether a wrapper exists.
Do not soften this finding — no metadata filter can make FAISS multi-tenant safe.

## 2026-03-18 — Neo4j is graph-specific

Isolation = `BELONGS_TO` relationship scoping, not metadata filters. Do not apply
the same AW-MEM-001 heuristic — it produces false positives.

## 2026-03-18 — LangChain breaks constantly

Pin `langchain>=0.2,<0.4`. Adapter must be tested against both 0.2 and 0.3 before
any LangChain version bump.

## 2026-03-18 — Attack vector count was inflated

Original claim was 16/32 vectors detected. Audit corrected to 10/32. Only claim
detection for a vector when there is a test fixture that produces a confirmed TP.
Never adjust the count without re-running the benchmark.

## 2026-03-18 — Coverage number drifts from PRD

PRD said 72% coverage; actual pytest --cov shows 83%. PRD numbers go stale fast.
Always run `pytest --cov=agentwall --cov-report=term-missing -q` to get the current
number before quoting it.
```

Run: `cat gotchas.md | head -5`
Expected: First line is `# AgentWall — Gotchas & Lessons Learned`

- [ ] **Step 2: Add `## Workflow` section to `CLAUDE.md`**

Add the following block immediately after the `## Rules` section at the end of `CLAUDE.md`:

```markdown
## Workflow

For ANY multi-step task (3+ steps, new feature, refactor, bug fix):

1. **Before touching code** — invoke `writing-plans` skill (`.claude/skills/writing-plans/SKILL.md`).
   Save plan to `docs/superpowers/plans/YYYY-MM-DD-<feature>.md`.
2. **Execute** — use `subagent-driven-development` skill for independent tasks,
   or `executing-plans` for sequential work in a single session.
3. **Before claiming done** — invoke `verification-before-completion` skill.
   Run: `pytest --cov=agentwall --cov-report=term-missing -q && ruff check src/ tests/ && mypy src/`
4. **After any mistake** — append a lesson to `gotchas.md`. Review `gotchas.md` before
   starting any new task.

## Skills

Installed skills in `.claude/skills/`. Use them — they encode hard-won lessons:

| Situation | Skill |
|---|---|
| Planning any multi-step task | `writing-plans` |
| Executing a plan (with subagents) | `subagent-driven-development` |
| Executing a plan (single session) | `executing-plans` |
| Before claiming a fix is done | `verification-before-completion` |
| Debugging unexpected behavior | `systematic-debugging` |
| Implementing new feature | `test-driven-development` |
| After completing a feature | `requesting-code-review` |
| Processing review feedback | `receiving-code-review` |
| Finding bug variants | `variant-analysis` |
| Security audit | `semgrep` + `insecure-defaults` + `sharp-edges` |
| Supply chain risk | `supply-chain-risk-auditor` |
| Finishing a branch | `finishing-a-development-branch` |
```

- [ ] **Step 3: Verify CLAUDE.md renders cleanly**

Run: `grep -c "##" CLAUDE.md`
Expected: output ≥ 8 (Build, Code Style, Architecture Invariants, Core Flow, Key Gotchas, Rules, Workflow, Skills)

- [ ] **Step 4: Commit**

```bash
git add CLAUDE.md gotchas.md
git commit -m "chore: add gotchas.md and workflow/skills sections to CLAUDE.md"
```

---

## Chunk 2: `agentwall explain` + `agentwall schema`

### Task 2: Build the Explanation Engine

**Files:**
- Create: `src/agentwall/explainer.py`
- Create: `tests/test_explainer.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_explainer.py
"""Tests for the explanation engine."""
import pytest
from agentwall.explainer import explain_rule, explain_attack_vector, ExplanationNotFound


def test_explain_known_rule_returns_structured_dict():
    result = explain_rule("AW-MEM-001")
    assert result["rule_id"] == "AW-MEM-001"
    assert result["severity"] == "critical"
    assert "owasp_mapping" in result
    assert isinstance(result["owasp_mapping"], list)
    assert len(result["owasp_mapping"]) >= 1
    assert "description" in result
    assert "fix" in result
    assert "real_world_evidence" in result
    assert "test_procedure" in result


def test_explain_all_ten_rules_present():
    rule_ids = [
        "AW-MEM-001", "AW-MEM-002", "AW-MEM-003", "AW-MEM-004", "AW-MEM-005",
        "AW-TOOL-001", "AW-TOOL-002", "AW-TOOL-003", "AW-TOOL-004", "AW-TOOL-005",
    ]
    for rid in rule_ids:
        result = explain_rule(rid)
        assert result["rule_id"] == rid, f"Missing explanation for {rid}"


def test_explain_unknown_rule_raises():
    with pytest.raises(ExplanationNotFound):
        explain_rule("AW-MEM-999")


def test_explain_attack_vector_mem_001():
    result = explain_attack_vector("AW-ATK-MEM-001")
    assert result["attack_id"] == "AW-ATK-MEM-001"
    assert "category" in result
    assert "owasp_mapping" in result
    assert "research_references" in result


def test_explain_unknown_attack_vector_raises():
    with pytest.raises(ExplanationNotFound):
        explain_attack_vector("AW-ATK-BOGUS-001")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_explainer.py -v`
Expected: `ModuleNotFoundError: No module named 'agentwall.explainer'`

- [ ] **Step 3: Implement `src/agentwall/explainer.py`**

```python
"""Explanation engine for AgentWall rules and attack vectors."""

from __future__ import annotations

from typing import Any


class ExplanationNotFound(KeyError):
    """Raised when no explanation exists for the given ID."""


# ── OWASP mappings ────────────────────────────────────────────────────────────

_OWASP_LLM08 = "LLM08:2025 — Vector and Embedding Weaknesses"
_OWASP_LLM04 = "LLM04:2025 — Data and Model Poisoning"
_OWASP_LLM01 = "LLM01:2025 — Prompt Injection"
_OWASP_LLM07 = "LLM07:2025 — System Prompt Leakage"
_OWASP_AGT06 = "ASI06:2026 — Memory Poisoning (Agentic Top 10)"
_OWASP_AGT01 = "ASI01:2026 — Prompt Injection (Agentic Top 10)"
_OWASP_AGT05 = "ASI05:2026 — Excessive Agency (Agentic Top 10)"

# ── Rule explanations ─────────────────────────────────────────────────────────

_RULE_EXPLANATIONS: dict[str, dict[str, Any]] = {
    "AW-MEM-001": {
        "rule_id": "AW-MEM-001",
        "title": "No tenant isolation in vector store",
        "severity": "critical",
        "category": "memory",
        "description": (
            "Vector store queries are executed without any user/tenant filter. "
            "A similarity search returns the globally closest vectors — including "
            "other users' data. This is a confirmed cross-tenant data leakage vector."
        ),
        "fix": (
            "Add a metadata filter on every retrieval call:\n"
            "  similarity_search(query, filter={'user_id': user_id})\n"
            "Ensure the same user_id is passed at write time:\n"
            "  add_texts(texts, metadatas=[{'user_id': user_id}])"
        ),
        "owasp_mapping": [_OWASP_LLM08],
        "real_world_evidence": (
            "AgentWall benchmark (2026-03-18): 57 confirmed instances across 8 real-world "
            "projects including Langflow (29 hits), Langchain-Chatchat (14 hits), "
            "Mem0/Embedchain (4 hits). This is the most common critical finding."
        ),
        "test_procedure": (
            "1. Run: agentwall scan . --format agent-json\n"
            "2. Filter findings by rule_id == 'AW-MEM-001'\n"
            "3. For each finding: add metadata filter to the flagged similarity_search() call\n"
            "4. Run: agentwall verify --finding AW-MEM-001 .\n"
            "5. Expected: PASS"
        ),
        "attack_vectors": ["AW-ATK-MEM-001"],
    },
    "AW-MEM-002": {
        "rule_id": "AW-MEM-002",
        "title": "Shared collection without metadata filter on retrieval",
        "severity": "high",
        "category": "memory",
        "description": (
            "Documents are written with user-scoped metadata (e.g. user_id) but retrieved "
            "without a matching filter. The write-time metadata provides false security — "
            "similarity_search() ignores it unless explicitly passed as a filter."
        ),
        "fix": (
            "Ensure every retrieval call includes the same metadata filter used at write time:\n"
            "  similarity_search(query, filter={'user_id': user_id})"
        ),
        "owasp_mapping": [_OWASP_LLM08],
        "real_world_evidence": (
            "AgentWall benchmark: 4 instances across 3 projects. "
            "Pattern: metadata added at ingest but forgotten at query time."
        ),
        "test_procedure": (
            "1. Find the add_texts() or add_documents() call with user_id metadata\n"
            "2. Find the corresponding similarity_search() call\n"
            "3. Verify the filter= kwarg is absent or lacks user_id\n"
            "4. Add the filter, then run: agentwall verify --finding AW-MEM-002 ."
        ),
        "attack_vectors": ["AW-ATK-MEM-002"],
    },
    "AW-MEM-003": {
        "rule_id": "AW-MEM-003",
        "title": "Memory backend has no access control configuration",
        "severity": "high",
        "category": "memory",
        "description": (
            "The configured memory backend has no observable access control setup. "
            "FAISS has zero native access control. ChromaDB defaults to a single shared "
            "collection. Without explicit isolation, all agents share the same memory namespace."
        ),
        "fix": (
            "Option A: Use per-user collections (ChromaDB):\n"
            "  client.get_or_create_collection(f'user_{user_id}')\n"
            "Option B: Use metadata-based filtering on a shared collection:\n"
            "  similarity_search(query, filter={'user_id': user_id})\n"
            "FAISS: always use a wrapper that enforces isolation at the application layer."
        ),
        "owasp_mapping": [_OWASP_LLM08],
        "real_world_evidence": (
            "AgentWall benchmark: 19 instances across 6 projects. "
            "FAISS-based projects are disproportionately represented."
        ),
        "test_procedure": (
            "1. Identify which vector store backend is in use (L0 detection)\n"
            "2. Verify per-user collection or metadata filter is configured\n"
            "3. Run: agentwall verify --finding AW-MEM-003 ."
        ),
        "attack_vectors": ["AW-ATK-MEM-003"],
    },
    "AW-MEM-004": {
        "rule_id": "AW-MEM-004",
        "title": "Known injection patterns in memory retrieval path",
        "severity": "high",
        "category": "memory",
        "description": (
            "The memory retrieval path uses unsanitized external input. "
            "This enables memory poisoning (MINJA, MemoryGraft attack patterns). "
            "MINJA achieves >95% injection success rate via query-only interaction."
        ),
        "fix": (
            "Sanitize all content before storing to memory:\n"
            "  content = sanitize_memory_content(raw_content)  # strip control chars, limit length\n"
            "Validate retrieved content before injecting into agent context."
        ),
        "owasp_mapping": [_OWASP_LLM04, _OWASP_AGT06],
        "real_world_evidence": (
            "Research: MINJA (NeurIPS 2025) — >95% memory injection success rate via query-only "
            "interaction, no write access required. CorruptRAG (2026) — single poisoned document "
            "sufficient per target query."
        ),
        "test_procedure": (
            "1. Identify memory retrieval path (similarity_search → context injection)\n"
            "2. Verify a sanitization step exists between retrieval and context injection\n"
            "3. Run: agentwall verify --finding AW-MEM-004 ."
        ),
        "attack_vectors": ["AW-ATK-POI-001", "AW-ATK-INJ-001"],
    },
    "AW-MEM-005": {
        "rule_id": "AW-MEM-005",
        "title": "No sanitization on retrieved memory before context injection",
        "severity": "medium",
        "category": "memory",
        "description": (
            "Retrieved memory content is injected directly into the agent context without "
            "sanitization. Poisoned memories can influence agent behavior across sessions. "
            "Embedding Inversion research shows 50-70% of original words are recoverable "
            "from stored vectors — retrieval paths are high-value attack surfaces."
        ),
        "fix": (
            "Pass retrieved memories through a sanitization step:\n"
            "  memories = [sanitize(m) for m in vector_store.similarity_search(query)]\n"
            "Minimum: strip prompt injection markers, limit retrieved content length."
        ),
        "owasp_mapping": [_OWASP_LLM01, _OWASP_AGT06],
        "real_world_evidence": (
            "Research: EchoLeak — single crafted email triggered Microsoft 365 Copilot to "
            "disclose confidential emails and files. Embedding Inversion (ACL 2024): "
            "50-70% word recovery from stored vectors."
        ),
        "test_procedure": (
            "1. Trace the path from similarity_search() to the LLM context injection\n"
            "2. Verify a sanitization/validation step is present\n"
            "3. Run: agentwall verify --finding AW-MEM-005 ."
        ),
        "attack_vectors": ["AW-ATK-INJ-001", "AW-ATK-EMB-001"],
    },
    "AW-TOOL-001": {
        "rule_id": "AW-TOOL-001",
        "title": "Destructive tool accessible without approval gate",
        "severity": "high",
        "category": "tool",
        "description": (
            "A tool classified as destructive (deletes data, modifies files, sends messages) "
            "is registered without a human-in-the-loop approval gate. An LLM could invoke "
            "this tool in response to a crafted prompt."
        ),
        "fix": (
            "Wrap destructive tools with an approval gate:\n"
            "  from langchain.callbacks import HumanApprovalCallbackHandler\n"
            "  tool = Tool(..., callbacks=[HumanApprovalCallbackHandler()])"
        ),
        "owasp_mapping": [_OWASP_AGT05],
        "real_world_evidence": (
            "AgentWall benchmark: 4 instances across 2 projects. "
            "Pattern: file deletion and email sending tools registered without callbacks."
        ),
        "test_procedure": (
            "1. Identify all @tool or Tool(...) registrations\n"
            "2. For each destructive tool, verify HumanApprovalCallbackHandler is present\n"
            "3. Run: agentwall verify --finding AW-TOOL-001 ."
        ),
        "attack_vectors": ["AW-ATK-AGT-001"],
    },
    "AW-TOOL-002": {
        "rule_id": "AW-TOOL-002",
        "title": "Tool accepts arbitrary code/SQL/shell execution",
        "severity": "medium",
        "category": "tool",
        "description": (
            "A tool can execute arbitrary code, SQL queries, or shell commands. "
            "Without input validation this enables prompt-injection-to-RCE escalation."
        ),
        "fix": (
            "Restrict tool inputs with an allowlist schema. Avoid eval/exec patterns:\n"
            "  # Bad: eval(user_input)\n"
            "  # Good: execute_query(query_template.format(**validated_params))"
        ),
        "owasp_mapping": [_OWASP_LLM07, _OWASP_AGT05],
        "real_world_evidence": (
            "Common pattern in database tools and code interpreter tools. "
            "Any eval/exec accepting LLM-generated input is a confirmed RCE vector."
        ),
        "test_procedure": (
            "1. Find all tools with exec, eval, subprocess, or raw SQL execution\n"
            "2. Verify input validation / allowlist is present\n"
            "3. Run: agentwall verify --finding AW-TOOL-002 ."
        ),
        "attack_vectors": ["AW-ATK-AGT-001"],
    },
    "AW-TOOL-003": {
        "rule_id": "AW-TOOL-003",
        "title": "High-risk tool lacks user-scope access check",
        "severity": "medium",
        "category": "tool",
        "description": (
            "A high-risk tool (file access, database query, API call) does not verify "
            "that the requesting user has permission to perform the requested action. "
            "Privilege escalation via prompt injection is the primary risk."
        ),
        "fix": (
            "Add a user-scope check at the start of the tool function:\n"
            "  def my_tool(user_id: str, resource_id: str) -> str:\n"
            "      if not has_permission(user_id, resource_id):\n"
            "          raise PermissionError(f'{user_id} cannot access {resource_id}')"
        ),
        "owasp_mapping": [_OWASP_AGT05],
        "real_world_evidence": (
            "Theoretical but well-documented attack path. OWASP Agentic Top 10 ASI05 "
            "explicitly covers this pattern."
        ),
        "test_procedure": (
            "1. Identify high-risk tool functions\n"
            "2. Verify a permission check exists before any resource access\n"
            "3. Run: agentwall verify --finding AW-TOOL-003 ."
        ),
        "attack_vectors": ["AW-ATK-AGT-001"],
    },
    "AW-TOOL-004": {
        "rule_id": "AW-TOOL-004",
        "title": "Tool has no description",
        "severity": "low",
        "category": "tool",
        "description": (
            "A registered tool has no description. This blocks risk classification and "
            "degrades the LLM's ability to select tools correctly, increasing the risk "
            "of unintended tool invocation."
        ),
        "fix": (
            "Add a docstring or description= argument to every tool:\n"
            "  @tool\n"
            "  def search_documents(query: str) -> str:\n"
            "      \"\"\"Search user documents for relevant context. Input: search query string.\"\"\""
        ),
        "owasp_mapping": [],
        "real_world_evidence": (
            "AgentWall benchmark: found in 7+ projects including Onyx/Danswer (2 hits), "
            "GPT-Researcher (1 hit)."
        ),
        "test_procedure": (
            "1. Find all @tool or Tool() registrations\n"
            "2. Verify each has a non-empty description\n"
            "3. Run: agentwall verify --finding AW-TOOL-004 ."
        ),
        "attack_vectors": [],
    },
    "AW-TOOL-005": {
        "rule_id": "AW-TOOL-005",
        "title": "Agent has >15 tools (exceeds recommended limit)",
        "severity": "info",
        "category": "tool",
        "description": (
            "The agent has more than 15 registered tools. Large tool sets increase "
            "token usage and reduce tool-selection accuracy, increasing the risk "
            "of the LLM selecting an incorrect or dangerous tool."
        ),
        "fix": (
            "Split the agent into specialized sub-agents with focused tool sets:\n"
            "  # e.g. SearchAgent (3 tools), WriteAgent (3 tools), ReviewAgent (2 tools)"
        ),
        "owasp_mapping": [],
        "real_world_evidence": (
            "OpenAI best practices recommend <20 tools per agent for reliable selection. "
            "Empirical degradation observed above 15 tools in GPT-4 evaluations."
        ),
        "test_procedure": (
            "1. Count all registered tools in the agent\n"
            "2. If > 15, refactor into sub-agents\n"
            "3. Run: agentwall verify --finding AW-TOOL-005 ."
        ),
        "attack_vectors": [],
    },
}

# ── Attack vector explanations ────────────────────────────────────────────────

_ATTACK_EXPLANATIONS: dict[str, dict[str, Any]] = {
    "AW-ATK-MEM-001": {
        "attack_id": "AW-ATK-MEM-001",
        "title": "Cross-tenant retrieval (no user filter)",
        "category": "MEM — Memory Isolation",
        "owasp_mapping": [_OWASP_LLM08],
        "description": (
            "Similarity search returns the globally closest vectors regardless of ownership. "
            "Any user can retrieve any other user's stored memories or documents."
        ),
        "research_references": [
            "OWASP LLM08:2025 — Vector and Embedding Weaknesses",
        ],
        "detected_by": ["AW-MEM-001"],
        "detection_layers": ["L1 AST", "L3 Taint", "L5 Semgrep"],
    },
    "AW-ATK-MEM-002": {
        "attack_id": "AW-ATK-MEM-002",
        "title": "Weak static filter bypass",
        "category": "MEM — Memory Isolation",
        "owasp_mapping": [_OWASP_LLM08],
        "description": (
            "Filter exists at write time but is not enforced at retrieval. "
            "Static metadata provides a false sense of isolation."
        ),
        "research_references": ["OWASP LLM08:2025"],
        "detected_by": ["AW-MEM-002"],
        "detection_layers": ["L1 AST", "L3 Taint"],
    },
    "AW-ATK-MEM-003": {
        "attack_id": "AW-ATK-MEM-003",
        "title": "Namespace confusion / shared collection",
        "category": "MEM — Memory Isolation",
        "owasp_mapping": [_OWASP_LLM08],
        "description": (
            "All users share a single vector store collection with no partitioning. "
            "Any retrieval call returns results from the entire corpus."
        ),
        "research_references": ["OWASP LLM08:2025"],
        "detected_by": ["AW-MEM-003"],
        "detection_layers": ["L1 AST"],
    },
    "AW-ATK-POI-001": {
        "attack_id": "AW-ATK-POI-001",
        "title": "Stored prompt injection via memory",
        "category": "POI — Memory Poisoning",
        "owasp_mapping": [_OWASP_LLM04, _OWASP_AGT06],
        "description": (
            "Adversary stores crafted prompt instructions in the vector store. "
            "When retrieved, the injected content overrides the system prompt."
        ),
        "research_references": [
            "MINJA (NeurIPS 2025): >95% injection success rate",
            "CorruptRAG (2026): single-document poisoning per target query",
        ],
        "detected_by": ["AW-MEM-004"],
        "detection_layers": ["L1 AST", "L5 Semgrep"],
    },
    "AW-ATK-INJ-001": {
        "attack_id": "AW-ATK-INJ-001",
        "title": "Indirect prompt injection via retrieved memory",
        "category": "INJ — Prompt Injection",
        "owasp_mapping": [_OWASP_LLM01, _OWASP_AGT01],
        "description": (
            "Malicious instructions embedded in stored documents are retrieved and injected "
            "into the agent context. The LLM executes the injected instructions."
        ),
        "research_references": [
            "EchoLeak: single crafted email triggered Microsoft 365 Copilot data disclosure",
            "OWASP LLM01:2025 — Prompt Injection",
        ],
        "detected_by": ["AW-MEM-005"],
        "detection_layers": ["L1 AST", "L5 Semgrep"],
    },
    "AW-ATK-CFG-001": {
        "attack_id": "AW-ATK-CFG-001",
        "title": "Unsafe reset enabled in production",
        "category": "CFG — Configuration",
        "owasp_mapping": [_OWASP_LLM08],
        "description": (
            "allow_reset=True on ChromaDB client enables the entire vector store to be "
            "wiped with a single API call. In production this is a data destruction vector."
        ),
        "research_references": ["ChromaDB docs: allow_reset parameter"],
        "detected_by": ["AW-MEM-003"],
        "detection_layers": ["L4 Config"],
    },
    "AW-ATK-CFG-003": {
        "attack_id": "AW-ATK-CFG-003",
        "title": "No TLS / No authentication on vector DB",
        "category": "CFG — Configuration",
        "owasp_mapping": [_OWASP_LLM08],
        "description": (
            "Vector database is accessible without authentication or TLS encryption. "
            "Any network-adjacent attacker can read or write the entire vector store."
        ),
        "research_references": ["OWASP LLM08:2025"],
        "detected_by": ["AW-MEM-005"],
        "detection_layers": ["L4 Config"],
    },
    "AW-ATK-CFG-004": {
        "attack_id": "AW-ATK-CFG-004",
        "title": "Hardcoded API keys in source",
        "category": "CFG — Configuration",
        "owasp_mapping": [_OWASP_LLM08],
        "description": (
            "API keys, passwords, or tokens are hardcoded in source files or config. "
            "Exposure via version control or log leakage grants full API access to attackers."
        ),
        "research_references": [
            "AgentWall benchmark: 45 instances across 8 projects — most common CFG finding"
        ],
        "detected_by": ["AW-MEM-004"],
        "detection_layers": ["L4 Config"],
    },
    "AW-ATK-AGT-001": {
        "attack_id": "AW-ATK-AGT-001",
        "title": "Unsafe tool access without approval gate",
        "category": "AGT — Agentic Attacks",
        "owasp_mapping": [_OWASP_AGT05],
        "description": (
            "Destructive or high-risk tools are accessible without human approval. "
            "A crafted prompt can trigger irreversible actions (deletion, exfiltration)."
        ),
        "research_references": ["OWASP ASI05:2026 — Excessive Agency"],
        "detected_by": ["AW-TOOL-001", "AW-TOOL-002", "AW-TOOL-003"],
        "detection_layers": ["L1 AST"],
    },
}


def explain_rule(rule_id: str) -> dict[str, Any]:
    """Return structured explanation for a rule ID.

    Raises ExplanationNotFound if rule_id is unknown.
    """
    if rule_id not in _RULE_EXPLANATIONS:
        raise ExplanationNotFound(f"No explanation found for rule: {rule_id!r}")
    return _RULE_EXPLANATIONS[rule_id]


def explain_attack_vector(attack_id: str) -> dict[str, Any]:
    """Return structured explanation for an attack vector ID.

    Raises ExplanationNotFound if attack_id is unknown.
    """
    if attack_id not in _ATTACK_EXPLANATIONS:
        raise ExplanationNotFound(f"No explanation found for attack vector: {attack_id!r}")
    return _ATTACK_EXPLANATIONS[attack_id]


def list_rules() -> list[str]:
    """Return sorted list of all rule IDs with explanations."""
    return sorted(_RULE_EXPLANATIONS.keys())


def list_attack_vectors() -> list[str]:
    """Return sorted list of all attack vector IDs with explanations."""
    return sorted(_ATTACK_EXPLANATIONS.keys())
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_explainer.py -v`
Expected: 5 tests PASS

- [ ] **Step 5: Commit**

```bash
git add src/agentwall/explainer.py tests/test_explainer.py
git commit -m "feat: add explanation engine (explainer.py) with 10 rules and 9 attack vectors"
```

---

### Task 3: Add `agentwall explain` CLI command

**Files:**
- Modify: `src/agentwall/cli.py`
- Modify: `tests/test_cli.py`

- [ ] **Step 1: Write the failing tests**

Add to `tests/test_cli.py`:

```python
from typer.testing import CliRunner
from agentwall.cli import app

runner = CliRunner()


def test_explain_rule_terminal_output():
    result = runner.invoke(app, ["explain", "AW-MEM-001"])
    assert result.exit_code == 0
    assert "AW-MEM-001" in result.output
    assert "critical" in result.output.lower()
    assert "OWASP" in result.output


def test_explain_rule_json_output():
    import json
    result = runner.invoke(app, ["explain", "AW-MEM-001", "--format", "json"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data["rule_id"] == "AW-MEM-001"
    assert "owasp_mapping" in data


def test_explain_attack_vector():
    result = runner.invoke(app, ["explain", "AW-ATK-MEM-001"])
    assert result.exit_code == 0
    assert "AW-ATK-MEM-001" in result.output


def test_explain_unknown_id_exits_nonzero():
    result = runner.invoke(app, ["explain", "AW-BOGUS-999"])
    assert result.exit_code != 0
    assert "not found" in result.output.lower() or "unknown" in result.output.lower()


def test_explain_list_flag():
    result = runner.invoke(app, ["explain", "--list"])
    assert result.exit_code == 0
    assert "AW-MEM-001" in result.output
    assert "AW-TOOL-001" in result.output
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_cli.py -k "explain" -v`
Expected: All 5 FAIL with `Error: No such command 'explain'`

- [ ] **Step 3: Add `explain` command to `cli.py`**

Add after the `verify` command:

```python
@app.command()
def explain(
    id_or_list: str | None = typer.Argument(
        None, help="Rule ID (AW-MEM-001) or attack vector ID (AW-ATK-MEM-001)."
    ),  # noqa: B008
    fmt: str = typer.Option("terminal", "--format", help="Output format: terminal|json"),  # noqa: B008
    list_all: bool = typer.Option(False, "--list", help="List all explainable IDs."),  # noqa: B008
) -> None:
    """Show detailed explanation for a rule or attack vector ID."""
    import json as _json

    from agentwall.explainer import (
        ExplanationNotFound,
        explain_attack_vector,
        explain_rule,
        list_attack_vectors,
        list_rules,
    )

    if list_all:
        rules = list_rules()
        vectors = list_attack_vectors()
        typer.echo("Rules:")
        for r in rules:
            typer.echo(f"  {r}")
        typer.echo("\nAttack Vectors:")
        for v in vectors:
            typer.echo(f"  {v}")
        raise typer.Exit(0)

    if id_or_list is None:
        typer.echo("Error: provide a rule ID or --list", err=True)
        raise typer.Exit(2)

    # Attempt rule lookup first, then attack vector
    try:
        if id_or_list.startswith("AW-ATK-"):
            data = explain_attack_vector(id_or_list)
        else:
            data = explain_rule(id_or_list)
    except ExplanationNotFound:
        typer.echo(f"Error: unknown ID {id_or_list!r}. Use --list to see valid IDs.", err=True)
        raise typer.Exit(1)

    if fmt == "json":
        typer.echo(_json.dumps(data, indent=2))
    else:
        # Terminal rendering
        typer.echo(f"\n{'=' * 60}")
        typer.echo(f"  {data.get('rule_id', data.get('attack_id'))}  —  {data['title']}")
        typer.echo(f"{'=' * 60}")
        sev = data.get("severity", data.get("category", ""))
        if sev:
            typer.echo(f"\nSeverity/Category: {sev.upper()}")
        typer.echo(f"\nDescription:\n  {data['description']}")
        if "fix" in data:
            typer.echo(f"\nFix:\n  {data['fix']}")
        owasp = data.get("owasp_mapping", [])
        if owasp:
            typer.echo("\nOWASP Mapping:")
            for o in owasp:
                typer.echo(f"  • {o}")
        evidence = data.get("real_world_evidence", data.get("research_references", []))
        if evidence:
            typer.echo(f"\nReal-World Evidence:")
            if isinstance(evidence, list):
                for e in evidence:
                    typer.echo(f"  • {e}")
            else:
                typer.echo(f"  {evidence}")
        proc = data.get("test_procedure")
        if proc:
            typer.echo(f"\nTest Procedure:\n  {proc}")
        typer.echo("")
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_cli.py -k "explain" -v`
Expected: 5 tests PASS

- [ ] **Step 5: Manual smoke test**

Run: `agentwall explain AW-MEM-001`
Expected: Formatted terminal output with description, fix, OWASP mapping

Run: `agentwall explain AW-ATK-MEM-001 --format json | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['attack_id'])"`
Expected: `AW-ATK-MEM-001`

Run: `agentwall explain --list | grep AW-MEM`
Expected: Lines for AW-MEM-001 through AW-MEM-005

- [ ] **Step 6: Commit**

```bash
git add src/agentwall/cli.py tests/test_cli.py
git commit -m "feat: add agentwall explain command (FR-531)"
```

---

### Task 4: Add `agentwall schema` command

**Files:**
- Create: `src/agentwall/schema_cmd.py`
- Modify: `src/agentwall/cli.py`
- Modify: `tests/test_cli.py`

- [ ] **Step 1: Write the failing tests**

Add to `tests/test_cli.py`:

```python
def test_schema_agent_json_is_valid_json():
    import json
    result = runner.invoke(app, ["schema", "agent-json"])
    assert result.exit_code == 0
    schema = json.loads(result.output)
    assert schema.get("$schema") or "properties" in schema or "type" in schema


def test_schema_sarif_is_valid_json():
    import json
    result = runner.invoke(app, ["schema", "sarif"])
    assert result.exit_code == 0
    json.loads(result.output)  # must not raise


def test_schema_unknown_format_exits_nonzero():
    result = runner.invoke(app, ["schema", "bogus"])
    assert result.exit_code != 0


def test_schema_finding_model():
    import json
    result = runner.invoke(app, ["schema", "finding"])
    assert result.exit_code == 0
    schema = json.loads(result.output)
    assert "rule_id" in str(schema)
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_cli.py -k "schema" -v`
Expected: 4 FAIL with `No such command 'schema'`

- [ ] **Step 3: Create `src/agentwall/schema_cmd.py`**

```python
"""JSON Schema output for AgentWall output formats."""

from __future__ import annotations

import json
from typing import Any

from agentwall.models import Finding, ScanResult


def get_finding_schema() -> dict[str, Any]:
    """Return JSON Schema for the Finding model."""
    return Finding.model_json_schema()


def get_scan_result_schema() -> dict[str, Any]:
    """Return JSON Schema for the ScanResult model."""
    return ScanResult.model_json_schema()


def get_agent_json_schema() -> dict[str, Any]:
    """Return JSON Schema for --format agent-json output."""
    return {
        "$schema": "https://json-schema.org/draft/2020-12",
        "title": "AgentWall agent-json output",
        "type": "object",
        "required": ["scan_id", "target", "framework", "findings", "summary"],
        "properties": {
            "scan_id": {"type": "string"},
            "target": {"type": "string"},
            "framework": {"type": ["string", "null"]},
            "findings": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["rule_id", "severity", "confidence", "fix_confidence", "file", "line"],
                    "properties": {
                        "rule_id": {"type": "string", "pattern": "^AW-(MEM|TOOL)-\\d{3}$"},
                        "severity": {"enum": ["critical", "high", "medium", "low", "info"]},
                        "confidence": {"enum": ["high", "medium", "low"]},
                        "fix_confidence": {"enum": ["AUTO", "GUIDED", "MANUAL"]},
                        "file": {"type": ["string", "null"]},
                        "line": {"type": ["integer", "null"]},
                        "description": {"type": "string"},
                        "fix": {"type": ["string", "null"]},
                        "patch": {"type": ["string", "null"]},
                        "verification_command": {"type": "string"},
                        "related_findings": {"type": "array", "items": {"type": "string"}},
                    },
                },
            },
            "summary": {
                "type": "object",
                "properties": {
                    "total": {"type": "integer"},
                    "critical": {"type": "integer"},
                    "high": {"type": "integer"},
                    "medium": {"type": "integer"},
                    "low": {"type": "integer"},
                    "info": {"type": "integer"},
                },
            },
        },
    }


def get_sarif_schema() -> dict[str, Any]:
    """Return a minimal JSON Schema for SARIF v2.1.0 output."""
    return {
        "$schema": "https://json-schema.org/draft/2020-12",
        "title": "AgentWall SARIF v2.1.0 output",
        "type": "object",
        "required": ["version", "runs"],
        "properties": {
            "version": {"type": "string", "const": "2.1.0"},
            "runs": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["tool", "results"],
                    "properties": {
                        "tool": {"type": "object"},
                        "results": {"type": "array"},
                    },
                },
            },
        },
    }


_SCHEMAS: dict[str, Any] = {
    "finding": get_finding_schema,
    "scan-result": get_scan_result_schema,
    "agent-json": get_agent_json_schema,
    "sarif": get_sarif_schema,
}

VALID_FORMATS = sorted(_SCHEMAS.keys())


def get_schema(fmt: str) -> dict[str, Any]:
    """Return the schema for the given format name.

    Raises KeyError if fmt is unknown.
    """
    if fmt not in _SCHEMAS:
        raise KeyError(f"Unknown schema format {fmt!r}. Valid: {VALID_FORMATS}")
    return _SCHEMAS[fmt]()
```

- [ ] **Step 4: Add `schema` command to `cli.py`**

Add after the `explain` command:

```python
@app.command()
def schema(
    fmt: str = typer.Argument(
        ..., help="Schema to output: finding|scan-result|agent-json|sarif"
    ),  # noqa: B008
) -> None:
    """Print JSON Schema for an AgentWall output format."""
    import json as _json

    from agentwall.schema_cmd import VALID_FORMATS, get_schema

    try:
        s = get_schema(fmt)
    except KeyError:
        typer.echo(f"Error: unknown format {fmt!r}. Valid: {VALID_FORMATS}", err=True)
        raise typer.Exit(1)

    typer.echo(_json.dumps(s, indent=2))
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `pytest tests/test_cli.py -k "schema" -v`
Expected: 4 PASS

- [ ] **Step 6: Commit**

```bash
git add src/agentwall/schema_cmd.py src/agentwall/cli.py tests/test_cli.py
git commit -m "feat: add agentwall schema command (NFR-84)"
```

---

## Chunk 3: AI Agent Integration (`prompt-fragment` + `mcp-serve`)

### Task 5: Add `agentwall prompt-fragment` + `.claude/commands/scan.md`

**Files:**
- Create: `src/agentwall/prompt_fragment.py`
- Create: `.claude/commands/scan.md`
- Modify: `src/agentwall/cli.py`
- Modify: `tests/test_cli.py`

- [ ] **Step 1: Write the failing tests**

Add to `tests/test_cli.py`:

```python
def test_prompt_fragment_outputs_nonempty_text():
    result = runner.invoke(app, ["prompt-fragment"])
    assert result.exit_code == 0
    assert len(result.output.strip()) > 100
    assert "agentwall" in result.output.lower()


def test_prompt_fragment_contains_key_instructions():
    result = runner.invoke(app, ["prompt-fragment"])
    assert "agent-json" in result.output
    assert "AW-MEM-001" in result.output
    assert "verify" in result.output.lower()
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_cli.py -k "prompt_fragment" -v`
Expected: 2 FAIL with `No such command 'prompt-fragment'`

- [ ] **Step 3: Create `src/agentwall/prompt_fragment.py`**

```python
"""System prompt fragment for AI agent integration (FR-522)."""

_FRAGMENT = """\
## AgentWall — Memory Security Scanner

You have access to AgentWall, a static memory security scanner for AI agent codebases.

### When to use AgentWall
- Before reviewing or modifying any RAG / vector store code
- When a user reports unexpected data appearing in agent responses
- Before creating a pull request that touches memory, retrieval, or tool registration code

### Core workflow

1. **Scan the target directory:**
   ```
   agentwall scan <path> --format agent-json
   ```
   Parse the JSON output. Each finding has: rule_id, severity, confidence, fix_confidence,
   file, line, description, fix, patch, verification_command.

2. **For AUTO fix_confidence findings:** Apply the `patch` field directly via `git apply`.

3. **For GUIDED fix_confidence findings:** Use the `fix` field as a template. Adapt to the
   project's existing patterns (check imports, variable names, auth context).

4. **For MANUAL fix_confidence findings:** Add a TODO comment at the flagged line and surface
   the finding to the human developer with the full `description` and `fix`.

5. **Verify each fix:**
   ```
   agentwall verify --finding <rule_id> <path>
   ```
   Expected output: `PASS: <rule_id> resolved`

6. **Re-scan to confirm zero regressions:**
   ```
   agentwall scan <path> --format agent-json --fail-on critical
   ```
   Exit code 0 = no CRITICAL findings remain.

### Rule severity reference
- CRITICAL (AW-MEM-001): Cross-tenant data leakage — fix before any other finding
- HIGH (AW-MEM-002–004, AW-TOOL-001): Data exposure or unsafe tool access
- MEDIUM (AW-MEM-005, AW-TOOL-002–003): Defense-in-depth gaps
- LOW/INFO (AW-TOOL-004–005): Code quality, LLM usability

### Getting more context
```
agentwall explain <rule_id>          # Full explanation + OWASP mapping + real-world evidence
agentwall explain <attack_vector_id> # Attack vector details (e.g. AW-ATK-MEM-001)
agentwall explain --list             # All explainable IDs
agentwall schema agent-json          # JSON Schema for output format
```
"""


def get_prompt_fragment() -> str:
    """Return the system prompt fragment for AI agent integration."""
    return _FRAGMENT.strip()
```

- [ ] **Step 4: Create `.claude/commands/scan.md`**

```markdown
# AgentWall Security Scan

Run AgentWall memory security scan and fix all findings.

## Steps

1. Run scan:
   ```bash
   agentwall scan . --format agent-json --output /tmp/agentwall-scan.json
   ```

2. Parse `/tmp/agentwall-scan.json`. For each finding:
   - `fix_confidence: AUTO` → apply the `patch` field via `git apply`
   - `fix_confidence: GUIDED` → adapt the `fix` field to project conventions
   - `fix_confidence: MANUAL` → add TODO comment, surface to human

3. After each fix, verify:
   ```bash
   agentwall verify --finding <rule_id> .
   ```

4. Re-scan to confirm clean:
   ```bash
   agentwall scan . --format agent-json --fail-on critical
   ```
   Exit code 0 = success.

5. If any finding unclear:
   ```bash
   agentwall explain <rule_id>
   ```
```

- [ ] **Step 5: Add `prompt-fragment` command to `cli.py`**

```python
@app.command(name="prompt-fragment")
def prompt_fragment() -> None:
    """Print a system prompt fragment for AI agent integration (FR-522)."""
    from agentwall.prompt_fragment import get_prompt_fragment

    typer.echo(get_prompt_fragment())
```

- [ ] **Step 6: Run tests to verify they pass**

Run: `pytest tests/test_cli.py -k "prompt_fragment" -v`
Expected: 2 PASS

- [ ] **Step 7: Commit**

```bash
git add src/agentwall/prompt_fragment.py src/agentwall/cli.py tests/test_cli.py .claude/commands/scan.md
git commit -m "feat: add agentwall prompt-fragment command and .claude/commands/scan.md (FR-522)"
```

---

### Task 6: Add `agentwall mcp-serve` (MCP Server, FR-523)

**Files:**
- Create: `src/agentwall/mcp_server.py`
- Modify: `src/agentwall/cli.py`
- Create: `tests/test_mcp_server.py`
- Modify: `pyproject.toml` — add `mcp` optional dependency

Architecture note: The MCP server exposes 4 tools over stdio JSON-RPC:
`agentwall_scan`, `agentwall_verify`, `agentwall_explain`, `agentwall_remediation_plan`.
All analysis uses the existing static pipeline — never executes user code (Architecture Invariant #1, NFR-90).

- [ ] **Step 1: Add `mcp` to `pyproject.toml` as optional dependency**

In `pyproject.toml`, add:
```toml
[project.optional-dependencies]
# existing extras...
mcp = ["mcp>=1.0"]
```

Verify: `grep 'mcp' pyproject.toml`

- [ ] **Step 2: Write failing tests**

```python
# tests/test_mcp_server.py
"""Tests for the MCP server module (offline, no actual stdio)."""
import json
import pytest
from agentwall.mcp_server import (
    handle_scan,
    handle_verify,
    handle_explain,
    handle_remediation_plan,
    TOOL_DEFINITIONS,
)


def test_tool_definitions_has_four_tools():
    names = {t["name"] for t in TOOL_DEFINITIONS}
    assert names == {
        "agentwall_scan",
        "agentwall_verify",
        "agentwall_explain",
        "agentwall_remediation_plan",
    }


def test_tool_definitions_each_has_description_and_schema():
    for tool in TOOL_DEFINITIONS:
        assert tool.get("description"), f"{tool['name']} missing description"
        assert "inputSchema" in tool, f"{tool['name']} missing inputSchema"
        schema = tool["inputSchema"]
        assert schema.get("type") == "object"
        assert "properties" in schema


def test_handle_explain_known_rule(tmp_path):
    result = handle_explain({"id": "AW-MEM-001"})
    assert result["isError"] is False
    assert "AW-MEM-001" in result["content"][0]["text"]


def test_handle_explain_unknown_id_returns_error():
    result = handle_explain({"id": "AW-BOGUS-999"})
    assert result["isError"] is True
    assert "not found" in result["content"][0]["text"].lower()


def test_handle_remediation_plan_known_rule():
    result = handle_remediation_plan({"rule_id": "AW-MEM-001"})
    assert result["isError"] is False
    text = result["content"][0]["text"]
    assert "AW-MEM-001" in text
    assert "step" in text.lower() or "fix" in text.lower()


def test_handle_remediation_plan_unknown_rule_returns_error():
    result = handle_remediation_plan({"rule_id": "AW-BOGUS-999"})
    assert result["isError"] is True


def test_handle_scan_requires_path():
    result = handle_scan({})
    assert result["isError"] is True
    assert "path" in result["content"][0]["text"].lower()


def test_handle_scan_nonexistent_path():
    result = handle_scan({"path": "/nonexistent/path/xyz"})
    assert result["isError"] is True


def test_handle_scan_real_fixture(tmp_path):
    """Scan a minimal valid Python file — should not crash."""
    f = tmp_path / "agent.py"
    f.write_text("from langchain.vectorstores import Chroma\nvs = Chroma()\n")
    result = handle_scan({"path": str(tmp_path)})
    assert result["isError"] is False
    data = json.loads(result["content"][0]["text"])
    assert "findings" in data
    assert "summary" in data


def test_handle_verify_requires_path_and_rule():
    result = handle_verify({})
    assert result["isError"] is True


def test_handle_verify_unknown_rule():
    result = handle_verify({"path": ".", "rule_id": "AW-BOGUS-999"})
    assert result["isError"] is True
    assert "unknown rule" in result["content"][0]["text"].lower()


def test_tool_input_schemas_are_valid_json_schema():
    """Each tool's inputSchema must be a valid JSON Schema object with required fields."""
    import jsonschema  # only needed if installed; skip gracefully
    pytest.importorskip("jsonschema")
    validator_cls = jsonschema.Draft7Validator
    for tool in TOOL_DEFINITIONS:
        schema = tool["inputSchema"]
        validator_cls.check_schema(schema)  # raises SchemaError if invalid
```

- [ ] **Step 3: Run tests to verify they fail**

Run: `pytest tests/test_mcp_server.py -v`
Expected: `ImportError: cannot import name 'handle_scan' from 'agentwall.mcp_server'`

- [ ] **Step 4: Create `src/agentwall/mcp_server.py`**

```python
"""MCP server for AgentWall (FR-523).

Exposes 4 MCP tools over stdio JSON-RPC:
  agentwall_scan, agentwall_verify, agentwall_explain, agentwall_remediation_plan

Architecture invariant: Never executes user code. All analysis via existing
static pipeline only (ast.parse, config regex, etc.). NFR-90 compliant.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

# ── Tool definitions (MCP list_tools response) ────────────────────────────────

TOOL_DEFINITIONS: list[dict[str, Any]] = [
    {
        "name": "agentwall_scan",
        "description": (
            "Run AgentWall static memory security scan on a Python project directory. "
            "Returns findings with rule IDs, severities, file locations, fix instructions, "
            "and patch diffs for AUTO-fixable issues. Use this before reviewing or modifying "
            "any RAG, vector store, or agent tool code."
        ),
        "inputSchema": {
            "type": "object",
            "required": ["path"],
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Absolute path to the directory to scan.",
                },
                "fail_on": {
                    "type": "string",
                    "enum": ["critical", "high", "medium", "low", "none"],
                    "default": "high",
                    "description": "Minimum severity to consider a failing scan.",
                },
                "fast": {
                    "type": "boolean",
                    "default": False,
                    "description": "Fast mode (L0-L2 only, ~1s). Full scan includes L4 config audit.",
                },
            },
        },
    },
    {
        "name": "agentwall_verify",
        "description": (
            "Re-scan a directory targeting a specific rule to verify if a finding is resolved. "
            "Run this after applying a fix. Returns PASS or FAIL with remaining finding count."
        ),
        "inputSchema": {
            "type": "object",
            "required": ["path", "rule_id"],
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Absolute path to the directory to scan.",
                },
                "rule_id": {
                    "type": "string",
                    "description": "Rule ID to verify (e.g. AW-MEM-001).",
                    "pattern": "^AW-(MEM|TOOL)-\\d{3}$",
                },
            },
        },
    },
    {
        "name": "agentwall_explain",
        "description": (
            "Get a detailed explanation for an AgentWall rule ID or attack vector ID. "
            "Includes severity, OWASP mapping, real-world evidence, fix instructions, "
            "and test procedure. Use this to understand what a finding means and how to fix it."
        ),
        "inputSchema": {
            "type": "object",
            "required": ["id"],
            "properties": {
                "id": {
                    "type": "string",
                    "description": (
                        "Rule ID (e.g. AW-MEM-001) or attack vector ID (e.g. AW-ATK-MEM-001). "
                        "Pass 'list' to get all valid IDs."
                    ),
                },
            },
        },
    },
    {
        "name": "agentwall_remediation_plan",
        "description": (
            "Generate a step-by-step remediation plan for a specific AgentWall rule. "
            "Returns ordered fix steps with estimated scope (files changed, lines changed) "
            "and a breaking_change flag. Use this to plan fixes before modifying code."
        ),
        "inputSchema": {
            "type": "object",
            "required": ["rule_id"],
            "properties": {
                "rule_id": {
                    "type": "string",
                    "description": "Rule ID to remediate (e.g. AW-MEM-001).",
                    "pattern": "^AW-(MEM|TOOL)-\\d{3}$",
                },
                "codebase_context": {
                    "type": "string",
                    "description": (
                        "Optional: brief description of the codebase "
                        "(e.g. 'FastAPI + LangChain + ChromaDB, multi-tenant SaaS')."
                    ),
                },
            },
        },
    },
]

# ── Remediation plan data ─────────────────────────────────────────────────────

_REMEDIATION_PLANS: dict[str, dict[str, Any]] = {
    "AW-MEM-001": {
        "rule_id": "AW-MEM-001",
        "fix_confidence": "AUTO",
        "estimated_files_changed": 1,
        "estimated_lines_changed": 2,
        "breaking_change": False,
        "steps": [
            {
                "step": 1,
                "description": "Find every similarity_search() or similarity_search_with_score() call.",
                "command": "grep -rn 'similarity_search' src/",
            },
            {
                "step": 2,
                "description": "Add filter={'user_id': user_id} kwarg to each call.",
                "patch_template": (
                    "# Before:\n"
                    "docs = vectorstore.similarity_search(query)\n"
                    "# After:\n"
                    "docs = vectorstore.similarity_search(query, filter={'user_id': user_id})"
                ),
            },
            {
                "step": 3,
                "description": "Ensure user_id is available in scope. Trace from request context if needed.",
            },
            {
                "step": 4,
                "description": "Verify the fix:",
                "command": "agentwall verify --finding AW-MEM-001 .",
                "expected_output": "PASS: AW-MEM-001 resolved",
            },
        ],
    },
    "AW-MEM-002": {
        "rule_id": "AW-MEM-002",
        "fix_confidence": "GUIDED",
        "estimated_files_changed": 1,
        "estimated_lines_changed": 1,
        "breaking_change": False,
        "steps": [
            {
                "step": 1,
                "description": "Locate the add_texts()/add_documents() call that passes user-scoped metadata.",
            },
            {
                "step": 2,
                "description": "Find the corresponding similarity_search() call.",
            },
            {
                "step": 3,
                "description": "Add the same metadata filter to the retrieval call.",
                "patch_template": (
                    "docs = vectorstore.similarity_search(query, filter={'user_id': user_id})"
                ),
            },
            {
                "step": 4,
                "description": "Verify:",
                "command": "agentwall verify --finding AW-MEM-002 .",
                "expected_output": "PASS: AW-MEM-002 resolved",
            },
        ],
    },
    "AW-MEM-003": {
        "rule_id": "AW-MEM-003",
        "fix_confidence": "GUIDED",
        "estimated_files_changed": 1,
        "estimated_lines_changed": 3,
        "breaking_change": True,
        "steps": [
            {
                "step": 1,
                "description": "Choose isolation strategy: per-user collection OR metadata filter on shared collection.",
            },
            {
                "step": 2,
                "description": (
                    "Option A — per-user collection (stronger isolation):\n"
                    "  collection = client.get_or_create_collection(f'user_{user_id}')"
                ),
            },
            {
                "step": 3,
                "description": (
                    "Option B — metadata filter on shared collection:\n"
                    "  similarity_search(query, filter={'user_id': user_id})"
                ),
            },
            {
                "step": 4,
                "description": "If using per-user collections: ensure existing data migration plan for existing shared data.",
            },
            {
                "step": 5,
                "description": "Verify:",
                "command": "agentwall verify --finding AW-MEM-003 .",
                "expected_output": "PASS: AW-MEM-003 resolved",
            },
        ],
    },
    "AW-TOOL-001": {
        "rule_id": "AW-TOOL-001",
        "fix_confidence": "GUIDED",
        "estimated_files_changed": 1,
        "estimated_lines_changed": 4,
        "breaking_change": False,
        "steps": [
            {
                "step": 1,
                "description": "Identify all destructive tools (delete, write, send operations).",
            },
            {
                "step": 2,
                "description": "Wrap each with HumanApprovalCallbackHandler:",
                "patch_template": (
                    "from langchain.callbacks import HumanApprovalCallbackHandler\n"
                    "tool = StructuredTool.from_function(\n"
                    "    func=my_tool_func,\n"
                    "    callbacks=[HumanApprovalCallbackHandler()],\n"
                    ")"
                ),
            },
            {
                "step": 3,
                "description": "Verify:",
                "command": "agentwall verify --finding AW-TOOL-001 .",
                "expected_output": "PASS: AW-TOOL-001 resolved",
            },
        ],
    },
}

# Add stub plans for remaining rules
for _rid in ["AW-MEM-004", "AW-MEM-005", "AW-TOOL-002", "AW-TOOL-003", "AW-TOOL-004", "AW-TOOL-005"]:
    if _rid not in _REMEDIATION_PLANS:
        _REMEDIATION_PLANS[_rid] = {
            "rule_id": _rid,
            "fix_confidence": "MANUAL",
            "estimated_files_changed": 1,
            "estimated_lines_changed": 5,
            "breaking_change": False,
            "steps": [
                {
                    "step": 1,
                    "description": f"Run: agentwall explain {_rid} for full fix instructions.",
                    "command": f"agentwall explain {_rid}",
                },
                {
                    "step": 2,
                    "description": "Apply the fix described in the explanation.",
                },
                {
                    "step": 3,
                    "description": "Verify:",
                    "command": f"agentwall verify --finding {_rid} .",
                    "expected_output": f"PASS: {_rid} resolved",
                },
            ],
        }


# ── Tool handler functions ────────────────────────────────────────────────────

def _make_result(text: str, is_error: bool = False) -> dict[str, Any]:
    return {"content": [{"type": "text", "text": text}], "isError": is_error}


def handle_scan(args: dict[str, Any]) -> dict[str, Any]:
    """Handle agentwall_scan tool call.

    NFR-90: Never executes user code. Analysis via ast.parse() only.
    """
    path_str = args.get("path")
    if not path_str:
        return _make_result("Error: 'path' argument is required.", is_error=True)

    path = Path(path_str)
    if not path.exists():
        return _make_result(f"Error: path does not exist: {path}", is_error=True)

    # Lazy imports (Architecture Invariant #5)
    from agentwall.models import ScanConfig
    from agentwall.reporters.agent_json import build_agent_json
    from agentwall.scanner import scan as run_scan

    fast = bool(args.get("fast", False))
    config = ScanConfig.fast() if fast else ScanConfig.default()
    # Fail safe (Architecture Invariant #3): scanner returns errors in result, never crashes caller
    result = run_scan(target=path, config=config)
    output = build_agent_json(result)
    return _make_result(json.dumps(output))


def handle_verify(args: dict[str, Any]) -> dict[str, Any]:
    """Handle agentwall_verify tool call."""
    path_str = args.get("path")
    rule_id = args.get("rule_id")

    if not path_str or not rule_id:
        return _make_result("Error: 'path' and 'rule_id' are required.", is_error=True)

    from agentwall.rules import ALL_RULES

    if rule_id not in ALL_RULES:
        return _make_result(
            f"Error: unknown rule ID {rule_id!r}. Valid: {sorted(ALL_RULES)}",
            is_error=True,
        )

    path = Path(path_str)
    if not path.exists():
        return _make_result(f"Error: path does not exist: {path}", is_error=True)

    from agentwall.models import ScanConfig
    from agentwall.scanner import scan as run_scan

    config = ScanConfig.fast()
    result = run_scan(target=path, config=config)
    matching = [f for f in result.findings if f.rule_id == rule_id]

    output = {
        "rule_id": rule_id,
        "status": "FAIL" if matching else "PASS",
        "finding_count": len(matching),
        "findings": [f.model_dump(mode="json") for f in matching],
    }
    return _make_result(json.dumps(output))


def handle_explain(args: dict[str, Any]) -> dict[str, Any]:
    """Handle agentwall_explain tool call."""
    id_str = args.get("id")
    if not id_str:
        return _make_result("Error: 'id' argument is required.", is_error=True)

    from agentwall.explainer import ExplanationNotFound, explain_attack_vector, explain_rule, list_attack_vectors, list_rules

    if id_str == "list":
        data: dict[str, Any] = {"rules": list_rules(), "attack_vectors": list_attack_vectors()}
        return _make_result(json.dumps(data))

    try:
        if id_str.startswith("AW-ATK-"):
            explanation = explain_attack_vector(id_str)
        else:
            explanation = explain_rule(id_str)
        return _make_result(json.dumps(explanation))
    except ExplanationNotFound as exc:
        return _make_result(f"Not found: {exc}", is_error=True)


def handle_remediation_plan(args: dict[str, Any]) -> dict[str, Any]:
    """Handle agentwall_remediation_plan tool call."""
    rule_id = args.get("rule_id")
    if not rule_id:
        return _make_result("Error: 'rule_id' argument is required.", is_error=True)

    if rule_id not in _REMEDIATION_PLANS:
        return _make_result(
            f"Error: no remediation plan for {rule_id!r}. "
            f"Valid: {sorted(_REMEDIATION_PLANS)}",
            is_error=True,
        )

    plan = _REMEDIATION_PLANS[rule_id].copy()
    context = args.get("codebase_context")
    if context:
        plan["codebase_context"] = context

    return _make_result(json.dumps(plan))


_HANDLERS: dict[str, Any] = {
    "agentwall_scan": handle_scan,
    "agentwall_verify": handle_verify,
    "agentwall_explain": handle_explain,
    "agentwall_remediation_plan": handle_remediation_plan,
}


# ── MCP stdio server ──────────────────────────────────────────────────────────

def serve_stdio() -> None:
    """Run the MCP server over stdio (JSON-RPC 2.0).

    Reads newline-delimited JSON from stdin, writes responses to stdout.
    Suitable for use as a stdio-transport MCP server.

    This function blocks until stdin is closed.
    """
    # Lazy import — mcp package is optional
    try:
        import mcp.server.stdio  # noqa: F401  # verify package present
    except ImportError:
        sys.stderr.write(
            "Error: 'mcp' package not installed. "
            "Run: pip install agentwall[mcp]\n"
        )
        sys.exit(1)

    import asyncio
    import mcp.server.stdio
    from mcp.server import Server
    from mcp.types import Tool, TextContent, CallToolResult

    server = Server("agentwall")

    @server.list_tools()
    async def list_tools():  # type: ignore[override]
        return [
            Tool(
                name=t["name"],
                description=t["description"],
                inputSchema=t["inputSchema"],
            )
            for t in TOOL_DEFINITIONS
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict[str, Any]):  # type: ignore[override]
        handler = _HANDLERS.get(name)
        if handler is None:
            result = _make_result(f"Unknown tool: {name!r}", is_error=True)
        else:
            result = handler(arguments or {})

        return CallToolResult(
            content=[TextContent(type="text", text=c["text"]) for c in result["content"]],
            isError=result.get("isError", False),
        )

    async def _run() -> None:
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await server.run(read_stream, write_stream, server.create_initialization_options())

    asyncio.run(_run())
```

- [ ] **Step 5: Add `mcp-serve` command to `cli.py`**

```python
@app.command(name="mcp-serve")
def mcp_serve() -> None:
    """Start AgentWall MCP server (stdio transport, FR-523).

    Exposes 4 tools: agentwall_scan, agentwall_verify,
    agentwall_explain, agentwall_remediation_plan.

    Install MCP support: pip install agentwall[mcp]
    """
    from agentwall.mcp_server import serve_stdio

    serve_stdio()
```

- [ ] **Step 6: Run tests to verify they pass**

Run: `pytest tests/test_mcp_server.py -v`
Expected: All 10 tests PASS (no `mcp` package required for unit tests — handler functions are tested directly)

- [ ] **Step 7: Full test suite — verify nothing regressed**

Run: `pytest --cov=agentwall --cov-report=term-missing -q`
Expected: All tests PASS, coverage ≥ 83%

- [ ] **Step 8: Lint and type check**

Run: `ruff check src/ tests/ && mypy src/`
Expected: No errors

- [ ] **Step 9: Smoke test MCP handlers without package**

```python
python3 -c "
from agentwall.mcp_server import handle_explain, handle_remediation_plan
r = handle_explain({'id': 'AW-MEM-001'})
assert not r['isError']
r2 = handle_remediation_plan({'rule_id': 'AW-MEM-001'})
assert not r2['isError']
print('MCP handlers OK')
"
```
Expected: `MCP handlers OK`

- [ ] **Step 10: Commit**

```bash
git add src/agentwall/mcp_server.py src/agentwall/cli.py tests/test_mcp_server.py pyproject.toml
git commit -m "feat: add agentwall mcp-serve command with 4 MCP tools (FR-523)"
```

---

## Final verification

- [ ] **Run full test suite one last time**

Run: `pytest --cov=agentwall --cov-report=term-missing -q && ruff check src/ tests/ && mypy src/`
Expected: All pass, coverage ≥ 83%, no lint or type errors.

- [ ] **Smoke test all new commands end-to-end**

```bash
agentwall explain AW-MEM-001
agentwall explain AW-ATK-MEM-001 --format json | python3 -m json.tool > /dev/null
agentwall explain --list | wc -l
agentwall schema agent-json | python3 -m json.tool > /dev/null
agentwall schema finding | python3 -m json.tool > /dev/null
agentwall prompt-fragment | grep "agent-json"
agentwall --help | grep -E "explain|schema|prompt-fragment|mcp-serve"
```
Expected: All commands produce valid output, `--help` lists all 4 new commands.

- [ ] **Final commit (if any post-verification fixes)**

```bash
git add -p
git commit -m "fix: post-verification cleanup"
```

---

Plan complete and saved to `docs/superpowers/plans/2026-03-19-agentwall-v1-agent-integration.md`. Ready to execute?
