---
paths:
  - "src/agentwall/adapters/llamaindex.py"
  - "tests/test_llamaindex_adapter.py"
  - "tests/fixtures/llamaindex_*/**"
---

# LlamaIndex Adapter Rules

- Detects `llama_index` / `llama-index` / `llamaindex` imports.
- Maps LlamaIndex-specific vector store classes: `VectorStoreIndex`, `SimpleVectorStore`, `PineconeVectorStore`, `ChromaVectorStore`, `QdrantVectorStore`.
- Also detects memory classes that persist conversation history.
- All analysis via `ast.parse()`. Never import LlamaIndex from scanned code.
- Returns a valid `AgentSpec` with empty lists when matched but no patterns found — NOT `None`.
