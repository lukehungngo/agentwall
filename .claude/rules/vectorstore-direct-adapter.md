---
paths:
  - "src/agentwall/adapters/vectorstore_direct.py"
  - "tests/test_vectorstore_direct_adapter.py"
  - "tests/fixtures/vectorstore_direct_*/**"
---

# VectorStore Direct Adapter Rules

- Catch-all adapter for raw vector store SDK usage without a framework wrapper.
- Detects: `chromadb` (Client, PersistentClient, HttpClient), `faiss` (IndexFlatL2, IndexIVFFlat), `pinecone`, `qdrant_client`, `pymilvus`, `weaviate`.
- Handles both `module.Constructor()` (Attribute) and bare `Constructor()` (Name) call patterns.
- This is the last-resort adapter before falling back to framework-agnostic AST scanning.
- All analysis via `ast.parse()`. Never import vector store SDKs from scanned code.
- Returns a valid `AgentSpec` with empty lists when matched but no patterns found — NOT `None`.
