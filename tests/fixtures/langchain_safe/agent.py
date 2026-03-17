from langchain.tools import tool
from langchain_community.vectorstores import Chroma


@tool
def get_user_data(user_id: str) -> str:
    """Get data for a specific user. Requires user_id scope check."""
    if not user_id:
        raise PermissionError("Access denied")
    vectorstore = Chroma(collection_name="user_docs")
    docs = vectorstore.similarity_search("find my documents", filter={"user_id": user_id})
    return f"Data for {user_id}: {docs}"
