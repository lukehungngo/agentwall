---
paths:
  - "src/agentwall/adapters/langchain.py"
  - "tests/test_langchain_adapter.py"
  - "tests/fixtures/langchain_*/**"
---

# LangChain Adapter Rules

- Pin `langchain>=0.2,<0.4`. Test against both 0.2 and 0.3.
- LangChain API breaks frequently — adapter must be resilient to import path changes (`langchain`, `langchain_core`, `langchain_community`, `langgraph` are all valid).
- All analysis via `ast.parse()`. Never `import langchain` from scanned code.
- The adapter converts AST into `AgentSpec` (defined in `models.py`).
- When the adapter matches but finds no relevant patterns, it returns a valid `AgentSpec` with empty lists — NOT `None`.
