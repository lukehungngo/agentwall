"""Fixed LangChain agent — same functionality, AgentWall clean.

Run: agentwall scan examples/
Compare with unsafe_agent.py to see the fixes.
"""

from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import tool
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

# --- Memory: tenant-scoped retrieval ---

embeddings = OpenAIEmbeddings()
vectorstore = Chroma(
    collection_name="all_user_documents",
    embedding_function=embeddings,
)


def search_docs(query: str, user_id: str) -> str:
    """Search the knowledge base, scoped to a specific user."""
    # FIX: filter= ensures only this user's documents are returned
    docs = vectorstore.similarity_search(
        query,
        k=5,
        filter={"user_id": user_id},
    )
    return "\n".join(doc.page_content for doc in docs)


# --- Tools: scoped, non-destructive, approval-gated ---


@tool
def search_knowledge_base(query: str, user_id: str) -> str:
    """Search the document knowledge base for the current user.

    Requires user_id for tenant scoping.
    """
    if not user_id:
        raise PermissionError("user_id is required")
    return search_docs(query, user_id)


@tool
def read_file(path: str, user_id: str) -> str:
    """Read a file from the user's sandboxed directory.

    Only allows reading from the user's own directory.
    """
    import pathlib

    safe_root = pathlib.Path(f"/data/users/{user_id}")
    target = (safe_root / path).resolve()
    if not str(target).startswith(str(safe_root)):
        raise PermissionError("Access denied: path traversal blocked")
    return target.read_text()


# --- Agent: safe tools only ---

llm = ChatOpenAI(model="gpt-4o-mini")
tools = [search_knowledge_base, read_file]
agent = create_react_agent(llm, tools, prompt=None)  # type: ignore[arg-type]
executor = AgentExecutor(agent=agent, tools=tools)
