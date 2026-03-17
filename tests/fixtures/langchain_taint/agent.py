"""Fixture: Agent with user_id parameter but no filter on retrieval."""
from langchain_community.vectorstores import Chroma

vectorstore = Chroma(collection_name="shared_docs")


def search_for_user(user_id, query):
    """User identity available but NOT passed to filter — taint doesn't reach sink."""
    docs = vectorstore.similarity_search(query)
    return docs


def search_with_static_filter(user_id, query):
    """Filter exists but only with static value — not user-scoped."""
    docs = vectorstore.similarity_search(query, filter={"source": "web"})
    return docs
