"""RAG app using raw chromadb — no LangChain/LlamaIndex."""
import chromadb

client = chromadb.Client()
collection = client.create_collection("docs")

# Unencrypted local persistence (AW-RAG-003 trigger: persist_directory kwarg)
store = chromadb.Chroma(persist_directory="/data/chroma")

# Save locally (AW-RAG-003 trigger: save_local call)
store.save_local("/data/backup")


# Retrieval with f-string prompt assembly (AW-RAG-001 trigger)
def search(query):
    results = collection.similarity_search(query)
    prompt = f"Context: {results}\nQuestion: {query}"
    return prompt
