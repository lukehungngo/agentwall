from crewai import Agent, Crew, Task
from crewai.tools import tool
from langchain_community.vectorstores import Chroma


@tool
def search_tool(query: str) -> str:
    """Search the knowledge base for information."""
    return f"Results for {query}"


@tool
def delete_records(record_id: str) -> str:
    """Delete records from the database."""
    return f"Deleted {record_id}"


vectorstore = Chroma(collection_name="shared_docs")

researcher = Agent(
    role="researcher",
    goal="Research topics thoroughly",
    tools=[search_tool, delete_records],
)

writer = Agent(
    role="writer",
    goal="Write compelling content",
    tools=[],
)

research_task = Task(
    description="Research the given topic",
    agent=researcher,
)

crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task],
)
