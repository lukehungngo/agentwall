"""Agent with mixed tools and no sanitization — no framework."""
from langchain.tools import tool


@tool
def read_database(query: str) -> str:
    """Read data from database."""
    return "results"


@tool
def delete_records(ids: list) -> str:
    """Delete records from database."""
    return "deleted"


# LLM call that consumes tool output
def run_agent(query):
    result = read_database(query)
    output = invoke(result)
    add_texts(output)
    return output


def invoke(text):
    return text
