---
paths:
  - "src/agentwall/probes/**"
---

# Probe Development

## Build priority

```
P1 (MVP):          chroma, pgvector
P2 (week 2–3):     pinecone, qdrant
P3 (week 3–4):     neo4j, weaviate
P4 (post-launch):  milvus, redis, mongodb
P5 (community):    elasticsearch, opensearch, faiss, lancedb
```

## Probe contract

Every probe module must:
- Implement the `MemoryProbe` Protocol from `probes/base.py`
- Be self-contained in a single file under `probes/`
- Register itself in `PROBE_REGISTRY` in `probes/__init__.py`
- Import SDK dependencies lazily inside `probe_live()` only
- Return `ProbeResult` with appropriate severity
