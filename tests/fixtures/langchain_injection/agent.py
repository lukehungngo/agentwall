"""Fixture: LangChain agent with memory injection vulnerabilities."""
from langchain.memory import ConversationBufferMemory
from langchain_community.vectorstores import Chroma

# Memory class — stores conversation history without tenant isolation
# This is an injection vector: user-supplied content persists across sessions
memory = ConversationBufferMemory()

# Vector store — no filter on retrieval
vectorstore = Chroma(collection_name="shared_knowledge")
query = "what is the meaning of life"
docs = vectorstore.similarity_search(query)

# Direct context injection — no sanitization between retrieval and prompt
context = "\n".join([doc.page_content for doc in docs])
prompt = f"Based on this context: {context}\nAnswer the question: {query}"
