---
paths:
  - "src/agentwall/adapters/openai_agents.py"
  - "tests/test_openai_agents_adapter.py"
  - "tests/fixtures/openai_agents_*/**"
---

# OpenAI Agents Adapter Rules

- Detects `openai_agents` and `agents` imports.
- Looks for `Agent()` constructors, `Runner.run()` calls, `@function_tool` decorators, handoff patterns, and vectorstore usage.
- May use same vector store classes as LangChain (`Chroma`, `FAISS`, `Pinecone`, `Qdrant`, `PGVector`).
- All analysis via `ast.parse()`. Never import the SDK from scanned code.
- Returns a valid `AgentSpec` with empty lists when matched but no patterns found — NOT `None`.
