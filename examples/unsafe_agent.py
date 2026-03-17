"""Unsafe LangChain agent — AgentWall will flag 5+ issues here.

Run: agentwall scan examples/
"""

import os
import subprocess

from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import Tool
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

# --- Memory: no tenant isolation ---

embeddings = OpenAIEmbeddings()
vectorstore = Chroma(
    collection_name="all_user_documents",
    embedding_function=embeddings,
)


def search_docs(query: str) -> str:
    """Search the knowledge base."""
    # BUG: no filter= kwarg → returns docs from ALL users
    docs = vectorstore.similarity_search(query, k=5)
    return "\n".join(doc.page_content for doc in docs)


# --- Tools: no approval gate, arbitrary execution ---

shell_tool = Tool(
    name="RunShell",
    func=lambda cmd: subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout,
    description="Execute a shell command and return output",
)

delete_tool = Tool(
    name="DeleteFile",
    func=lambda path: os.remove(path),
    description="Delete a file from disk",
)

search_tool = Tool(
    name="SearchDocs",
    func=search_docs,
    description="Search the document knowledge base",
)

# --- Agent: wired up with unsafe tools + unfiltered memory ---

llm = ChatOpenAI(model="gpt-4o-mini")
tools = [shell_tool, delete_tool, search_tool]
agent = create_react_agent(llm, tools, prompt=None)  # type: ignore[arg-type]
executor = AgentExecutor(agent=agent, tools=tools)
