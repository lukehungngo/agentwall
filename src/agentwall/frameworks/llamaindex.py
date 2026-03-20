"""Declarative framework model for LlamaIndex.

Covers three vector store backends: Pinecone, Chroma, and Qdrant.
LlamaIndex uses "filters" as the read-method kwarg (not "filter" as in LangChain),
and Qdrant uses "query_filter" specifically.
"""

from __future__ import annotations

from agentwall.frameworks.base import FrameworkModel, StoreModel

LLAMAINDEX_MODEL: FrameworkModel = FrameworkModel(
    name="llamaindex",
    stores={
        "PineconeVectorStore": StoreModel(
            backend="pinecone",
            isolation_params=["namespace"],
            write_methods={"add": "metadata"},
            read_methods={"query": "filters"},
            auth_params=["api_key", "environment"],
        ),
        "ChromaVectorStore": StoreModel(
            backend="chromadb",
            isolation_params=["collection_name"],
            write_methods={"add": "metadata"},
            read_methods={"query": "filters"},
            auth_params=["chroma_collection"],
        ),
        "QdrantVectorStore": StoreModel(
            backend="qdrant",
            isolation_params=["collection_name"],
            write_methods={"add": "metadata"},
            read_methods={"query": "query_filter"},
            auth_params=["url", "api_key"],
        ),
    },
)
