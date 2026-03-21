---
paths:
  - "src/agentwall/adapters/crewai.py"
  - "tests/test_crewai_adapter.py"
  - "tests/fixtures/crewai_*/**"
---

# CrewAI Adapter Rules

- Detects `crewai` imports.
- CrewAI uses LangChain vector stores internally — detects same class names (`Chroma`, `FAISS`, `Pinecone`, `Qdrant`, `PGVector`).
- Uses `_CrewAIVisitor` AST node visitor to extract agents, tasks, crews, and tool assignments.
- All analysis via `ast.parse()`. Never import CrewAI from scanned code.
- Returns a valid `AgentSpec` with empty lists when matched but no patterns found — NOT `None`.
