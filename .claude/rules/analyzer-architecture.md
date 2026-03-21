---
paths:
  - "src/agentwall/analyzers/**"
  - "src/agentwall/scanner.py"
  - "src/agentwall/context.py"
---

# Analyzer Architecture Rules

## Analyzer registry

All analyzers registered in `analyzers/__init__.py` → `ANALYZERS` list. Order doesn't matter — `_resolve_order()` topologically sorts by `depends_on`.

## 16 analyzers across layers

| Name | Layer | Framework-Agnostic | Opt-in | Purpose |
|---|---|---|---|---|
| VersionsAnalyzer | L0-versions | Yes | No | Dependency version checks |
| SecretsAnalyzer | L1-secrets | Yes | No | Hardcoded secrets detection |
| SerializationAnalyzer | L1-serialization | Yes | No | Unsafe deserialization, dynamic imports |
| MCPSecurityAnalyzer | L1-mcp | Yes | No | MCP server/tool security |
| RAGAnalyzer | L1-rag | Yes | No | RAG pipeline security |
| MemoryAnalyzer | L1-memory | Yes | No | Memory isolation, poisoning |
| ToolAnalyzer | L1-tools | Yes | No | Tool permissions, dangerous calls |
| AgentArchAnalyzer | L2-agent | Yes | No | Multi-agent architecture |
| CallGraphAnalyzer | L2 | No | No | Cross-function data flow |
| TaintAnalyzer | L3 | No | No | Taint propagation |
| ConfigAuditor | L4 | Yes | No | docker-compose, .env files |
| SemgrepAnalyzer | L5 | No | No | Semgrep rule matching |
| SymbolicAnalyzer | L6 | No | No | Symbolic execution |
| ASMAnalyzer | ASM | No | No | Attack surface mapping |
| RuntimeAnalyzer | L7 | No | Yes | Runtime patching |
| ConfidenceScorerAnalyzer | L8 | Yes | Yes | LLM-assisted FP reduction |

## Scanner gating logic

```python
# scanner.py:171 — the critical gate
if ctx.spec is None and not getattr(analyzer_cls, "framework_agnostic", False):
    continue
```

When `spec is None` (no adapter matched), only `framework_agnostic = True` analyzers run. This is how unrecognized frameworks still get basic security scanning.

## Key invariants

- **`replace = True`** analyzers (like L8 ConfidenceScorer) replace `ctx.findings` entirely — they transform, not extend.
- **Shadow mode**: analyzers in `config.shadow_layers` run but suppress output (findings go to DEBUG log only).
- **Fail safe**: any analyzer exception → warning + skip. Never crash the scan.
- **Severity discipline**: CRITICAL only for confirmed cross-tenant data access. Runtime (L7) and Taint (L3) must use HIGH, not CRITICAL — they detect patterns, not confirmed exploitation.

## Adding a new analyzer

1. Create `analyzers/<name>.py` with class having: `name`, `depends_on`, `replace`, `opt_in`, `framework_agnostic`
2. Implement `analyze(self, ctx: AnalysisContext) -> list[Finding]`
3. Add import + entry in `analyzers/__init__.py`
4. Add rules to `rules.py` if needed
5. Add tests
