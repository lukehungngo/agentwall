"""Tests for CrewAIAdapter."""

from __future__ import annotations

from pathlib import Path

import pytest

from agentwall.adapters.crewai import CrewAIAdapter
from agentwall.frameworks.crewai import CREWAI_MODEL

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture()
def adapter() -> CrewAIAdapter:
    return CrewAIAdapter()


class TestCrewAIAdapterBasic:
    def test_returns_agent_spec(self, adapter: CrewAIAdapter) -> None:
        spec = adapter.parse(FIXTURES / "crewai_basic")
        assert spec.framework == "crewai"

    def test_source_files_populated(self, adapter: CrewAIAdapter) -> None:
        spec = adapter.parse(FIXTURES / "crewai_basic")
        assert len(spec.source_files) >= 1

    def test_detects_tool_decorator(self, adapter: CrewAIAdapter) -> None:
        """@tool decorated function creates a ToolSpec."""
        spec = adapter.parse(FIXTURES / "crewai_basic")
        tool_names = [t.name for t in spec.tools]
        assert "search_tool" in tool_names

    def test_tool_has_description(self, adapter: CrewAIAdapter) -> None:
        spec = adapter.parse(FIXTURES / "crewai_basic")
        tool = next(t for t in spec.tools if t.name == "search_tool")
        assert tool.description == "Search the knowledge base for information."

    def test_destructive_tool_flagged(self, adapter: CrewAIAdapter) -> None:
        spec = adapter.parse(FIXTURES / "crewai_basic")
        tool = next(t for t in spec.tools if t.name == "delete_records")
        assert tool.is_destructive is True

    def test_detects_chroma_backend(self, adapter: CrewAIAdapter) -> None:
        spec = adapter.parse(FIXTURES / "crewai_basic")
        backends = [m.backend for m in spec.memory_configs]
        assert "chroma" in backends

    def test_detects_agent_count(self, adapter: CrewAIAdapter) -> None:
        """Agent(tools=[...]) extracts tool references."""
        spec = adapter.parse(FIXTURES / "crewai_basic")
        assert spec.metadata.get("agent_count") == 2

    def test_detects_crew_count(self, adapter: CrewAIAdapter) -> None:
        spec = adapter.parse(FIXTURES / "crewai_basic")
        assert spec.metadata.get("crew_count") == 1


class TestCrewAIAdapterEdgeCases:
    def test_empty_directory(self, adapter: CrewAIAdapter, tmp_path: Path) -> None:
        spec = adapter.parse(tmp_path)
        assert spec.tools == []
        assert spec.memory_configs == []
        assert spec.framework == "crewai"

    def test_parse_error_skips_file(self, adapter: CrewAIAdapter, tmp_path: Path) -> None:
        (tmp_path / "bad.py").write_text("def (\n", encoding="utf-8")
        spec = adapter.parse(tmp_path)
        assert len(spec.source_files) == 0

    def test_no_crewai_patterns(self, adapter: CrewAIAdapter, tmp_path: Path) -> None:
        (tmp_path / "main.py").write_text("x = 1\n", encoding="utf-8")
        spec = adapter.parse(tmp_path)
        assert spec.tools == []
        assert spec.memory_configs == []

    def test_tool_without_docstring(self, adapter: CrewAIAdapter, tmp_path: Path) -> None:
        (tmp_path / "agent.py").write_text(
            "from crewai.tools import tool\n"
            "@tool\n"
            "def no_desc(query: str) -> str:\n"
            "    return query\n",
            encoding="utf-8",
        )
        spec = adapter.parse(tmp_path)
        assert spec.tools[0].description is None

    def test_agent_with_no_tools(self, adapter: CrewAIAdapter, tmp_path: Path) -> None:
        (tmp_path / "agent.py").write_text(
            "from crewai import Agent\n"
            "agent = Agent(role='writer', goal='Write things')\n",
            encoding="utf-8",
        )
        spec = adapter.parse(tmp_path)
        assert spec.metadata.get("agent_count") == 1
        assert spec.tools == []

    def test_code_exec_in_tool(self, adapter: CrewAIAdapter, tmp_path: Path) -> None:
        (tmp_path / "agent.py").write_text(
            "from crewai.tools import tool\n"
            "@tool\n"
            "def run_code(code: str) -> str:\n"
            "    return eval(code)\n",
            encoding="utf-8",
        )
        spec = adapter.parse(tmp_path)
        assert spec.tools[0].accepts_code_execution is True


class TestCrewAIFrameworkModel:
    """Test the declarative framework model covers crewai patterns."""

    def test_model_name(self) -> None:
        assert CREWAI_MODEL.name == "crewai"

    def test_chroma_store_defined(self) -> None:
        assert "Chroma" in CREWAI_MODEL.stores
        store = CREWAI_MODEL.stores["Chroma"]
        assert store.backend == "chromadb"
        assert "collection_name" in store.isolation_params

    def test_decorator_patterns(self) -> None:
        names = [p.decorator for p in CREWAI_MODEL.decorator_patterns]
        assert "tool" in names
        assert "task" in names
