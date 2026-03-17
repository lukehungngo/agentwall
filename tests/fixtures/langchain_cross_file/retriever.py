"""Fixture: Cross-file retrieval — retriever defined here."""
from langchain_community.vectorstores import Chroma

vectorstore = Chroma(collection_name="shared_docs")


def do_search(query):
    """Search without filter — called from service.py."""
    return vectorstore.similarity_search(query)
