from langchain_community.vectorstores import Chroma

db = Chroma(collection_name="docs")


def search_docs(query, user_id):
    return db.similarity_search(query, filter={"user_id": user_id})
