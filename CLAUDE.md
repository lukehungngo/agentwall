# AgentWall

Static AST-based memory security scanner for AI agents. Detects cross-user memory leakage, memory poisoning, and unsafe tool permissions before deployment. OSS CLI — `pip install agentwall`.

## Build & Test

```bash
pip install -e ".[dev]"        # dev install
pytest                         # run tests
pytest --cov=agentwall --cov-report=term-missing  # with coverage
ruff check src/ tests/         # lint
ruff format src/ tests/        # format
mypy src/                      # type check (strict mode)
agentwall scan .               # run scanner
hatch build                    # build package
```

## Code Style

- Python 3.10+, PEP 8 enforced by Ruff, strict mypy
- Pydantic v2 for all models. Type hints on all public functions
- Tests in `tests/`, fixtures in `tests/fixtures/`

## Architecture Invariants

These are non-negotiable — violating any of these is a P0:

1. **Never execute user code.** All analysis via `ast.parse()` only. No `exec()`, no `import` of scanned code. This is a security scanner — running user code is a critical vulnerability.
2. **Static by default.** No network calls unless `--live` flag is passed.
3. **Fail safe.** Parse error on a file → warning + skip. Never crash the entire scan.
4. **Probe registry pattern.** Each vector store backend is one self-contained module in `probes/`. Adding a backend = one file + one registry entry in `probes/__init__.py`.
5. **Lazy SDK imports.** Probe SDKs only imported inside `probe_live()`. Default install has zero vector store dependencies.
6. **Severity discipline.** CRITICAL only for confirmed cross-tenant data access. Everything else is HIGH or below. Inflated severity kills user trust.

## Core Flow

```
agentwall scan ./project/
  → detector.auto_detect_framework()    # inspect imports/pyproject.toml
  → Adapter.parse()                     # AST → AgentSpec
  → MemoryAnalyzer.analyze()            # leak + poison + isolation
  → ToolAnalyzer.analyze()              # enumerate + classify + scope
  → Reporter.render()                   # terminal / JSON / SARIF
  → sys.exit(0 | 1 | 2)
```

## Key Gotchas

- **Metadata ≠ isolation.** `add_texts(metadata={"user_id": x})` without a matching filter on `similarity_search()` is insecure. Detect this mismatch explicitly.
- **FAISS has zero access control.** Always flag as HIGH. Only question is whether a wrapper exists.
- **Neo4j is graph-specific.** Isolation = `BELONGS_TO` relationship scoping, not metadata filters. Don't treat like vector stores.
- **LangChain breaks constantly.** Pin `langchain>=0.2,<0.4`. Test adapter against both 0.2 and 0.3.
- **`--live` requires extras.** `pip install agentwall[chroma]` for live probing. Document clearly.

## Rules

All rules defined in `src/agentwall/rules.py`. Two categories:

- **AW-MEM-***: Memory rules (001–005) — tenant isolation, metadata filters, access control, injection, sanitization
- **AW-TOOL-***: Tool rules (001–005) — approval gates, arbitrary execution, scope checks, descriptions, tool count
