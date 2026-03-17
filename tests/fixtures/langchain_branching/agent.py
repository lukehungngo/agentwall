"""Fixture: Agent with branching filter logic for L6 symbolic analysis."""
from langchain_community.vectorstores import Chroma

vectorstore = Chroma(collection_name="shared_docs")


def search_mixed_paths(query, is_admin=False):
    """Filter on admin path only — L6 should detect missing filter on default path."""
    if is_admin:
        docs = vectorstore.similarity_search(query, filter={"role": "admin"})
    else:
        docs = vectorstore.similarity_search(query)
    return docs


def search_always_filtered(query, user_id=None):
    """Filter on all paths — L6 should NOT flag this."""
    if user_id:
        docs = vectorstore.similarity_search(query, filter={"user_id": user_id})
    else:
        docs = vectorstore.similarity_search(query, filter={"scope": "public"})
    return docs
