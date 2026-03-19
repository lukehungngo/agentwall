# AgentWall — AI Agent Integration & Guided Remediation

## Making AgentWall Consumable by Autonomous Coding Agents

**Version:** 1.0
**Date:** 2026-03-17
**Author:** SoH Engineering
**Status:** Draft
**Parent:** AgentWall PRD v2 (Solo-Engineer Edition)

---

## 1. Problem Statement

AgentWall's primary users will not run the tool manually. They will instruct an AI coding agent to do it:

```
"Scan this project for memory security issues and fix them."
```

The AI agent (Claude Code, Codex, OpenClaw, Cursor, Aider, Devin, etc.) then needs to:
1. Install AgentWall
2. Run the scan
3. Parse the output
4. Understand each finding
5. Implement the correct fix
6. Re-scan to verify

Today's `agentwall scan` produces terminal-formatted output designed for human eyes. An AI agent reading this output faces several problems:

- **Ambiguous remediation.** "Add metadata filtering to your retrieval calls" — which calls? What filter shape? What metadata key? The AI guesses, often wrong.
- **No structured diff.** The finding says what's wrong but doesn't show the before/after code change needed. The AI has to infer the fix from a description.
- **No verification protocol.** After applying a fix, the AI re-scans, but there's no way to confirm a specific finding was resolved vs. a new finding was introduced.
- **No context about the codebase.** The finding says "line 67 in chroma_service.py" but doesn't explain how `kb_name` flows through the system, making it hard for the AI to scope the fix correctly.
- **Framework-specific fixes not provided.** The remediation is generic ("add a filter") but LangChain, CrewAI, and OpenAI SDK each have different APIs for applying filters. The AI needs framework-specific code.

This is a first-class product problem, not a nice-to-have. If the tool's output can't be acted on by the agents that will use it, adoption stalls.

---

## 2. Target Integration Environments

| Agent | How It Runs AgentWall | What It Needs |
|---|---|---|
| **Claude Code** | Bash tool → `agentwall scan . --format json` | JSON output, file paths, line numbers, code snippets, fix suggestions |
| **Codex (OpenAI)** | Shell command in sandbox | Same as above + exit codes for pass/fail gating |
| **OpenClaw** | Frontline agent delegates to tool-use agent | Structured findings with remediation as executable steps |
| **Cursor / Windsurf** | Terminal panel or plugin | SARIF for IDE integration + inline fix suggestions |
| **Aider** | Shell command + file context | Diff-ready patches per finding |
| **Devin** | Autonomous execution in sandbox | Full scan → fix → verify loop with structured I/O |
| **GitHub Copilot Workspace** | CI/CD integration | SARIF upload to GitHub Security tab |
| **Custom MAS (multi-agent systems)** | Python SDK import | Programmatic API with typed return values |

**Common denominator:** Every agent needs structured, machine-parseable output with actionable remediation that can be applied without human interpretation.

---

## 3. Functional Requirements

### FR-500: Machine-Readable Output Format

The system SHALL produce output optimized for AI agent consumption.

**FR-501: Agent-Optimized JSON Format**

Beyond the existing JSON reporter, provide an `--format agent-json` output that includes:

```json
{
  "scan_id": "uuid",
  "timestamp": "ISO-8601",
  "target": "/path/to/project",
  "framework": "langchain",
  "framework_version": "0.2.x",
  "summary": {
    "total_findings": 6,
    "critical": 3,
    "high": 3,
    "medium": 0,
    "low": 0,
    "pass": false
  },
  "findings": [
    {
      "id": "AW-MEM-001-001",
      "rule_id": "AW-MEM-001",
      "severity": "CRITICAL",
      "title": "No tenant isolation on vector store retrieval",
      "category": "memory",
      "attack_vector": "AW-ATK-MEM-001",
      "location": {
        "file": "server/kb_service/chromadb_kb_service.py",
        "line": 67,
        "column": 8,
        "function": "do_search",
        "class": "ChromaKBService"
      },
      "evidence": {
        "code_snippet": "retriever = get_Retriever(\"vectorstore\").from_vectorstore(\n    self.chroma, top_k=top_k, score_threshold=score_threshold,\n)",
        "explanation": "similarity_search is called via get_Retriever without a metadata filter. Any user querying this knowledge base retrieves documents from all users.",
        "data_flow": [
          "kb_api.py:search_docs() → base.py:KBService.do_search() → chromadb_kb_service.py:ChromaKBService.do_search()",
          "No user_id or tenant_id parameter flows from the API request into the retrieval filter."
        ]
      },
      "remediation": {
        "summary": "Add a metadata filter scoped to the authenticated user's identity on every retrieval call.",
        "framework_specific": {
          "langchain": {
            "description": "Pass a filter dict to the retriever's search_kwargs containing the user's tenant identifier.",
            "before": "retriever = get_Retriever(\"vectorstore\").from_vectorstore(\n    self.chroma, top_k=top_k, score_threshold=score_threshold,\n)",
            "after": "retriever = get_Retriever(\"vectorstore\").from_vectorstore(\n    self.chroma, top_k=top_k, score_threshold=score_threshold,\n    search_kwargs={\"filter\": {\"user_id\": user_id}},\n)",
            "diff": "--- a/chromadb_kb_service.py\n+++ b/chromadb_kb_service.py\n@@ -67,6 +67,7 @@\n     retriever = get_Retriever(\"vectorstore\").from_vectorstore(\n-        self.chroma, top_k=top_k, score_threshold=score_threshold,\n+        self.chroma, top_k=top_k, score_threshold=score_threshold,\n+        search_kwargs={\"filter\": {\"user_id\": user_id}},\n     )",
            "dependencies": [
              "The do_search method signature must accept a user_id parameter.",
              "The caller (KBService.do_search in base.py) must pass user_id from the API request context.",
              "Documents must be stored with user_id in metadata during ingestion."
            ]
          }
        },
        "verification": {
          "re_scan_command": "agentwall scan . --rule AW-MEM-001",
          "expected_result": "Finding AW-MEM-001-001 should no longer appear.",
          "manual_test": "Insert docs for user_a and user_b. Query as user_b. Verify user_a docs are not returned."
        },
        "references": [
          "https://python.langchain.com/docs/how_to/vectorstores/#search-with-filtering",
          "https://docs.trychroma.com/docs/collections/query#filtering"
        ]
      },
      "related_findings": ["AW-MEM-001-002", "AW-MEM-001-003"],
      "confidence": "HIGH",
      "false_positive_hint": "If this application is single-tenant (one user per deployment), this finding can be suppressed via agentwall.yaml: suppress: [AW-MEM-001]"
    }
  ],
  "suppressed": [],
  "scan_config": {
    "rules_applied": ["AW-MEM-001", "AW-MEM-003"],
    "layers_run": ["L0", "L1"],
    "scan_duration_ms": 1200
  }
}
```

**Key fields that don't exist in current JSON output:**
- `attack_vector` — links finding to catalog entry
- `evidence.data_flow` — cross-file call chain (from L2 when available)
- `remediation.framework_specific` — per-framework before/after code
- `remediation.framework_specific.diff` — unified diff ready to apply
- `remediation.framework_specific.dependencies` — prerequisite changes the AI must also make
- `remediation.verification` — how to confirm the fix worked
- `related_findings` — group findings that share a root cause
- `false_positive_hint` — when to suppress

**FR-502: Unified Diff Output**

```bash
agentwall scan . --format patch
```

Produces a `.patch` file that an AI agent can apply directly:

```
agentwall scan . --format patch > fixes.patch
git apply fixes.patch
```

For findings where an automated fix is possible (filter insertion, config change), generate the diff. For findings requiring architectural changes (redesign isolation model), produce a `TODO` comment with instructions instead.

**FR-503: SARIF with AI Extensions**

Extend SARIF output with custom properties in the `properties` bag:

```json
{
  "runs": [{
    "results": [{
      "ruleId": "AW-MEM-001",
      "message": { "text": "..." },
      "properties": {
        "agentwall:attack_vector": "AW-ATK-MEM-001",
        "agentwall:framework_fix": "langchain",
        "agentwall:diff": "...",
        "agentwall:dependencies": ["..."],
        "agentwall:verification_command": "agentwall scan . --rule AW-MEM-001"
      }
    }]
  }]
}
```

---

### FR-510: Guided Remediation Engine

The system SHALL provide step-by-step remediation plans, not just descriptions.

**FR-511: Remediation Plan Generation**

For each finding, generate an ordered list of changes required:

```json
{
  "finding_id": "AW-MEM-001-001",
  "remediation_plan": {
    "steps": [
      {
        "order": 1,
        "action": "modify_function_signature",
        "file": "server/kb_service/base.py",
        "function": "KBService.do_search",
        "description": "Add user_id parameter to do_search method signature.",
        "diff": "..."
      },
      {
        "order": 2,
        "action": "modify_function_body",
        "file": "server/kb_service/chromadb_kb_service.py",
        "function": "ChromaKBService.do_search",
        "description": "Pass user_id as metadata filter to retriever.",
        "diff": "..."
      },
      {
        "order": 3,
        "action": "modify_caller",
        "file": "server/kb_api.py",
        "function": "search_docs",
        "description": "Extract user_id from request context and pass to kb.do_search().",
        "diff": "..."
      },
      {
        "order": 4,
        "action": "modify_ingestion",
        "file": "server/kb_service/chromadb_kb_service.py",
        "function": "ChromaKBService.do_add_doc",
        "description": "Include user_id in document metadata during ingestion.",
        "diff": "..."
      },
      {
        "order": 5,
        "action": "verify",
        "command": "agentwall scan . --rule AW-MEM-001",
        "expected": "0 findings for AW-MEM-001"
      }
    ],
    "estimated_files_changed": 3,
    "estimated_lines_changed": 15,
    "breaking_change": true,
    "breaking_change_reason": "do_search signature change requires updating all callers."
  }
}
```

**FR-512: Fix Confidence Level**

Each remediation step SHALL have a confidence level:

| Level | Meaning | AI Agent Action |
|---|---|---|
| `AUTO` | Fix can be applied mechanically with no ambiguity | Apply directly |
| `GUIDED` | Fix pattern is known but requires codebase-specific adaptation | Apply with review |
| `MANUAL` | Fix requires architectural decision or domain knowledge | Present to human |

**FR-513: Incremental Verification**

```bash
agentwall verify --finding AW-MEM-001-001
```

Checks if a specific finding has been resolved without running the full scan. Returns:

```json
{
  "finding_id": "AW-MEM-001-001",
  "status": "RESOLVED",
  "verification_method": "AST re-check at chromadb_kb_service.py:67",
  "scan_duration_ms": 200
}
```

This enables the AI agent's fix-verify loop to be fast.

---

### FR-520: Agent Workflow Integration

**FR-521: Claude Code Integration**

Provide a `.claude/commands/scan.md` template that teams can drop into their repo:

```markdown
# Security Scan

Run AgentWall memory security scan and fix any findings.

## Steps

1. Run `agentwall scan . --format agent-json > /tmp/aw-results.json`
2. Read the results file
3. For each finding with confidence AUTO or GUIDED:
   - Apply the remediation diff
   - Run `agentwall verify --finding {finding_id}` to confirm
4. For findings with confidence MANUAL:
   - Add a TODO comment at the flagged location with the remediation description
5. Re-run full scan to confirm all AUTO/GUIDED findings resolved
6. Report remaining MANUAL findings to the user
```

**FR-522: System Prompt Fragment**

Provide a reusable system prompt fragment that any AI agent can include:

```bash
agentwall prompt-fragment
```

Outputs:

```
You have access to AgentWall, a memory security scanner for AI agents.

To scan a project: agentwall scan {path} --format agent-json
To verify a fix:   agentwall verify --finding {finding_id}
To list rules:     agentwall rules list --format json

When you receive scan results:
- Findings with confidence AUTO: apply the provided diff directly.
- Findings with confidence GUIDED: adapt the diff to the codebase, then verify.
- Findings with confidence MANUAL: explain to the user and request guidance.
- Always verify each fix before moving to the next finding.
- Group related findings (same rule_id) and fix the root cause once.
```

**FR-523: MCP Server Mode**

Expose AgentWall as an MCP (Model Context Protocol) server so AI agents can call it as a tool without shell access:

```json
{
  "tools": [
    {
      "name": "agentwall_scan",
      "description": "Scan a project for AI agent memory security vulnerabilities.",
      "parameters": {
        "target": { "type": "string", "description": "Path to project root" },
        "rules": { "type": "array", "items": { "type": "string" }, "description": "Rule IDs to run (default: all)" },
        "format": { "type": "string", "enum": ["agent-json", "sarif", "patch"] }
      }
    },
    {
      "name": "agentwall_verify",
      "description": "Verify if a specific finding has been resolved.",
      "parameters": {
        "finding_id": { "type": "string" },
        "target": { "type": "string" }
      }
    },
    {
      "name": "agentwall_explain",
      "description": "Get detailed explanation of a rule or attack vector.",
      "parameters": {
        "id": { "type": "string", "description": "Rule ID (AW-MEM-001) or attack vector ID (AW-ATK-MEM-001)" }
      }
    },
    {
      "name": "agentwall_remediation_plan",
      "description": "Get step-by-step remediation plan for a finding.",
      "parameters": {
        "finding_id": { "type": "string" },
        "target": { "type": "string" }
      }
    }
  ]
}
```

**FR-524: GitHub Actions with AI Agent Output**

```yaml
# .github/workflows/agentwall.yml
- name: AgentWall Scan
  run: agentwall scan . --format sarif --output results.sarif

- name: Upload SARIF
  uses: github/codeql-action/upload-sarif@v3
  with:
    sarif_file: results.sarif

- name: Agent-Readable Summary
  run: agentwall scan . --format agent-json --output results.json

- name: Post PR Comment
  run: agentwall comment --format github-pr --input results.json
```

---

### FR-530: Contextual Explanation Engine

**FR-531: Attack Vector Explanation**

```bash
agentwall explain AW-ATK-MEM-001
```

Returns structured explanation an AI agent can include in its reasoning:

```json
{
  "id": "AW-ATK-MEM-001",
  "title": "Cross-Tenant Retrieval (No Filter)",
  "severity": "CRITICAL",
  "description": "Vector store similarity_search called without metadata filter...",
  "owasp_mapping": ["LLM08:2025"],
  "real_world_evidence": [
    "Langchain-Chatchat (37K stars): 3 KB services affected",
    "Long-Trainer: 2 retrieval paths affected"
  ],
  "test_procedure": {
    "steps": [
      "Insert doc with metadata={\"user_id\": \"user_a\", \"content\": \"secret\"}",
      "Insert doc with metadata={\"user_id\": \"user_b\", \"content\": \"public\"}",
      "Query as user_b with semantic match to user_a's doc",
      "FAIL if user_a's doc appears in results"
    ]
  },
  "why_it_matters": "In multi-tenant deployments, this allows any user to retrieve any other user's private documents through normal search queries. No elevated privileges required."
}
```

**FR-532: Codebase Context Enrichment**

When generating remediation, the system SHALL analyze the target codebase to provide context-aware fixes:

1. Detect the authentication pattern (how `user_id` is available in the request context)
2. Detect the ingestion pipeline (where documents are stored, whether metadata is already present)
3. Detect existing filter patterns (if some retrievals are already filtered, match the pattern)
4. Detect the test framework (pytest, unittest) and generate test cases in the correct style

```json
{
  "codebase_context": {
    "auth_pattern": {
      "type": "fastapi_dependency",
      "user_id_accessor": "request.state.user.id",
      "detected_in": "server/auth.py:get_current_user()"
    },
    "ingestion_pattern": {
      "metadata_fields": ["source", "filename", "created_at"],
      "missing_field": "user_id",
      "ingestion_file": "server/kb_service/base.py:add_doc()"
    },
    "existing_filter_pattern": {
      "example_file": "server/search_api.py:filtered_search()",
      "pattern": "search_kwargs={\"filter\": {\"user_id\": user_id}}"
    },
    "test_framework": "pytest",
    "test_directory": "tests/"
  }
}
```

This context lets the AI agent write fixes that match the project's existing conventions instead of producing generic boilerplate.

---

## 4. Non-Functional Requirements

### 4.1 Performance

| ID | Requirement | Target |
|---|---|---|
| NFR-50 | `--format agent-json` overhead vs plain JSON | < 20% additional time |
| NFR-51 | `agentwall verify --finding X` execution time | < 3 seconds |
| NFR-52 | Remediation plan generation per finding | < 2 seconds |
| NFR-53 | MCP server cold start | < 3 seconds |
| NFR-54 | MCP server per-request latency | < 5 seconds for scan, < 1 second for explain/verify |

### 4.2 Accuracy

| ID | Requirement | Target |
|---|---|---|
| NFR-60 | Auto-confidence fix correctness (applies cleanly and resolves finding) | > 90% |
| NFR-61 | Guided-confidence fix relevance (correct approach, may need adaptation) | > 80% |
| NFR-62 | Framework-specific fix API correctness (uses correct API for framework version) | > 95% |
| NFR-63 | Codebase context detection accuracy (auth pattern, test framework) | > 85% |

### 4.3 Compatibility

| ID | Requirement | Target |
|---|---|---|
| NFR-70 | Agent-JSON schema backward compatibility | Semver — no breaking changes in minor versions |
| NFR-71 | MCP protocol compliance | MCP specification v1.0+ |
| NFR-72 | SARIF compliance | SARIF v2.1.0 |
| NFR-73 | Patch format | Unified diff (git apply compatible) |

### 4.4 Usability (for AI agents)

| ID | Requirement | Target |
|---|---|---|
| NFR-80 | Zero ambiguity in remediation steps — each step maps to exactly one code change | Mandatory |
| NFR-81 | All file paths in output are absolute or relative to scan target root | Mandatory |
| NFR-82 | All code snippets include sufficient context (5 lines before/after) for unambiguous location | Mandatory |
| NFR-83 | Error messages include structured error codes, not just human-readable strings | Mandatory |
| NFR-84 | Schema is self-documenting — `agentwall schema agent-json` outputs JSON Schema | Mandatory |

### 4.5 Security

| ID | Requirement | Target |
|---|---|---|
| NFR-90 | MCP server SHALL NOT execute arbitrary code from agent requests | Mandatory |
| NFR-91 | Patch output SHALL NOT modify files outside the scan target directory | Mandatory |
| NFR-92 | Agent-JSON output SHALL NOT include raw secrets even if found during scan | Mandatory |

---

## 5. Constraints

| ID | Constraint | Impact |
|---|---|---|
| C-30 | **Diff generation requires deterministic AST manipulation** — generating correct patches from findings requires precise source location tracking. Off-by-one line numbers produce broken patches. | Must track exact source ranges, not just line numbers. |
| C-31 | **Framework API surface is large** — generating framework-specific fixes for every finding × every framework version is combinatorially expensive. | Start with top 3 patterns per framework. Community contributes the long tail. |
| C-32 | **Codebase context detection is heuristic** — detecting auth patterns, ingestion pipelines, and test frameworks from static analysis is imperfect. | Provide `agentwall.yaml` overrides for context the scanner can't detect. |
| C-33 | **AI agents have varying tool-use capabilities** — Claude Code can read files and run commands; Codex has limited shell; some agents only have MCP. | Support multiple integration modes: CLI, MCP, Python SDK. |
| C-34 | **Remediation plans may conflict with each other** — fixing AW-MEM-001 and AW-MEM-003 on the same file may produce conflicting diffs. | Remediation engine must detect conflicts and merge or sequence changes. |

---

## 6. Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                     AI AGENT (Claude Code, Codex, etc.)      │
│                                                              │
│  reads system prompt fragment                                │
│  calls agentwall via CLI / MCP / Python SDK                  │
└──────┬────────────────┬────────────────┬─────────────────────┘
       │ CLI            │ MCP            │ Python SDK
       ▼                ▼                ▼
┌──────────────────────────────────────────────────────────────┐
│                     AGENTWALL INTERFACE LAYER                 │
│                                                              │
│  CLIApp              MCPServer          Scanner class         │
│  (Typer)             (MCP protocol)     (importable)         │
│                                                              │
│  All three produce the same ScanResult object                │
└──────────────────────┬───────────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────────┐
│                   REMEDIATION ENGINE (NEW)                    │
│                                                              │
│  ┌─────────────────┐  ┌─────────────────┐                   │
│  │ ContextDetector  │  │ FixGenerator    │                   │
│  │ - auth pattern   │  │ - per framework │                   │
│  │ - ingestion path │  │ - per rule      │                   │
│  │ - test framework │  │ - diff output   │                   │
│  │ - existing filters│  │ - confidence    │                   │
│  └────────┬────────┘  └────────┬────────┘                   │
│           │                    │                              │
│           ▼                    ▼                              │
│  ┌─────────────────────────────────────────┐                │
│  │ RemediationPlan                          │                │
│  │ - ordered steps                          │                │
│  │ - per-step diffs                         │                │
│  │ - dependencies                           │                │
│  │ - verification commands                  │                │
│  │ - conflict detection                     │                │
│  └─────────────────────────────────────────┘                │
└──────────────────────┬───────────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────────┐
│                   OUTPUT FORMATTERS                           │
│                                                              │
│  AgentJSONFormatter   PatchFormatter   SARIFFormatter        │
│  (--format agent-json) (--format patch) (--format sarif)     │
│                                                              │
│  + ExplainFormatter   + VerifyFormatter                      │
│  (agentwall explain)  (agentwall verify)                     │
└──────────────────────────────────────────────────────────────┘
```

---

## 7. CLI Surface (New Commands)

```
agentwall scan [PATH] --format agent-json     # AI-optimized output
agentwall scan [PATH] --format patch          # Unified diff output
agentwall verify --finding FINDING_ID         # Fast single-finding re-check
agentwall explain RULE_OR_ATTACK_ID           # Structured explanation
agentwall remediate FINDING_ID                # Generate remediation plan
agentwall schema [FORMAT]                     # Output JSON Schema for format
agentwall prompt-fragment                     # System prompt for AI agents
agentwall mcp-serve                           # Start MCP server
```

---

## 8. Implementation Priority

| Phase | Feature | Effort | Impact |
|---|---|---|---|
| W2 | `--format agent-json` with remediation fields | Medium | HIGH — unlocks AI agent consumption |
| W2 | `--format patch` for auto-fixable findings | Medium | HIGH — direct apply workflow |
| W2 | `agentwall verify --finding` | Low | HIGH — fast fix-verify loop |
| W3 | `agentwall explain` | Low | MEDIUM — improves agent reasoning |
| W3 | `agentwall prompt-fragment` | Trivial | MEDIUM — adoption accelerator |
| W3 | JSON Schema export (`agentwall schema`) | Low | MEDIUM — agent validation |
| Post | MCP server (`agentwall mcp-serve`) | Medium | HIGH — broadest agent compatibility |
| Post | `agentwall remediate` with codebase context | High | HIGH — autonomous fix generation |
| Post | Conflict detection in remediation plans | Medium | MEDIUM — multi-finding fix reliability |

---

## 9. Success Metrics

| Metric | Target |
|---|---|
| AI agent can install + scan + parse output without human help | 100% for Claude Code, Codex |
| AUTO-confidence fixes apply cleanly (`git apply` succeeds) | > 90% |
| AUTO-confidence fixes resolve the finding on re-scan | > 85% |
| Fix-verify loop completes in under 60 seconds per finding | > 90% of findings |
| MCP server adopted by >= 3 AI agent platforms | Within 6 months of launch |
| Community-contributed remediation templates | >= 20 within 6 months |

---

## 10. Open Questions

| # | Question | Impact | Decision Needed By |
|---|---|---|---|
| 1 | Should `--format patch` attempt fixes for GUIDED-confidence findings or only AUTO? | Broken patches erode trust. Conservative = AUTO only. | W2 |
| 2 | Should MCP server support streaming (SSE) for long scans or only request-response? | Streaming needed for large codebases (>60s scan). | Post-launch |
| 3 | Should remediation plans include generated test cases? | Significant effort but high value for AI agents. | W3 |
| 4 | How to handle framework version differences in fix templates? | LangChain 0.2 vs 0.3 have different retriever APIs. | W2 |
| 5 | Should `agentwall explain` fetch latest attack research from a remote registry? | Breaks offline-first promise. Maybe opt-in. | Post-launch |

---

*End of document.*
