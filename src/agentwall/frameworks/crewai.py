"""Declarative framework model for CrewAI.

CrewAI uses LangChain vector stores internally. Tool registration is
primarily via the ``@tool`` decorator from ``crewai.tools``.
"""

from __future__ import annotations

from agentwall.frameworks.base import DecoratorPattern, FrameworkModel, StoreModel

CREWAI_MODEL: FrameworkModel = FrameworkModel(
    name="crewai",
    stores={
        "Chroma": StoreModel(
            backend="chromadb",
            isolation_params=["collection_name"],
            write_methods={"add_texts": "metadata"},
            read_methods={"similarity_search": "filter"},
        ),
    },
    decorator_patterns=[
        DecoratorPattern(decorator="tool", registers_as="agent_tool"),
        DecoratorPattern(decorator="task", registers_as="agent_task"),
    ],
)
