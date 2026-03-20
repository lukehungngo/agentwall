from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.tools import FunctionTool, QueryEngineTool
from llama_index.vector_stores.chroma import ChromaVectorStore

# Load documents and build index
documents = SimpleDirectoryReader("data").load_data()
index = VectorStoreIndex.from_documents(documents)

# Create a ChromaVectorStore
vector_store = ChromaVectorStore(chroma_collection=collection)  # noqa: F821

# Create query engine and retriever
query_engine = index.as_query_engine()
retriever = index.as_retriever(similarity_top_k=5)

# Create tools
search_tool = QueryEngineTool.from_defaults(
    query_engine=query_engine, name="search", description="Search the knowledge base"
)


def my_func(query: str) -> str:
    """A custom function."""
    return f"Result: {query}"


custom_tool = FunctionTool.from_defaults(fn=my_func, name="custom_func")

# Memory
memory = ChatMemoryBuffer.from_defaults(token_limit=1500)
