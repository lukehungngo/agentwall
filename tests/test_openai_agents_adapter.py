"""Tests for OpenAIAgentsAdapter."""

from __future__ import annotations

from pathlib import Path

import pytest

from agentwall.adapters.openai_agents import OpenAIAgentsAdapter

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture()
def adapter() -> OpenAIAgentsAdapter:
    return OpenAIAgentsAdapter()


class TestOpenAIAgentsAdapterBasic:
    def test_returns_agent_spec(self, adapter: OpenAIAgentsAdapter) -> None:
        spec = adapter.parse(FIXTURES / "openai_agents_basic")
        assert spec.framework == "openai_agents"

    def test_source_files_populated(self, adapter: OpenAIAgentsAdapter) -> None:
        spec = adapter.parse(FIXTURES / "openai_agents_basic")
        assert len(spec.source_files) >= 1

    def test_detects_function_tools(self, adapter: OpenAIAgentsAdapter) -> None:
        """@function_tool decorated function creates a ToolSpec."""
        spec = adapter.parse(FIXTURES / "openai_agents_basic")
        tool_names = [t.name for t in spec.tools]
        assert "search_web" in tool_names
        assert "delete_user" in tool_names

    def test_destructive_tool_flagged(self, adapter: OpenAIAgentsAdapter) -> None:
        spec = adapter.parse(FIXTURES / "openai_agents_basic")
        tool = next(t for t in spec.tools if t.name == "delete_user")
        assert tool.is_destructive is True

    def test_code_exec_detected(self, adapter: OpenAIAgentsAdapter) -> None:
        """subprocess in delete_user detected as code execution."""
        spec = adapter.parse(FIXTURES / "openai_agents_basic")
        tool = next(t for t in spec.tools if t.name == "delete_user")
        assert tool.accepts_code_execution is True

    def test_tool_descriptions(self, adapter: OpenAIAgentsAdapter) -> None:
        spec = adapter.parse(FIXTURES / "openai_agents_basic")
        tool = next(t for t in spec.tools if t.name == "search_web")
        assert tool.description == "Search the web for information."

    def test_detects_agent_count(self, adapter: OpenAIAgentsAdapter) -> None:
        spec = adapter.parse(FIXTURES / "openai_agents_basic")
        assert spec.metadata.get("agent_count") == 1

    def test_detects_runner_count(self, adapter: OpenAIAgentsAdapter) -> None:
        spec = adapter.parse(FIXTURES / "openai_agents_basic")
        assert spec.metadata.get("runner_count") == 1


class TestOpenAIAgentsAdapterEdgeCases:
    def test_empty_directory(self, adapter: OpenAIAgentsAdapter, tmp_path: Path) -> None:
        spec = adapter.parse(tmp_path)
        assert spec.tools == []
        assert spec.memory_configs == []
        assert spec.framework == "openai_agents"

    def test_parse_error_skips_file(self, adapter: OpenAIAgentsAdapter, tmp_path: Path) -> None:
        (tmp_path / "bad.py").write_text("def (\n", encoding="utf-8")
        spec = adapter.parse(tmp_path)
        assert len(spec.source_files) == 0

    def test_no_openai_agents_patterns(self, adapter: OpenAIAgentsAdapter, tmp_path: Path) -> None:
        (tmp_path / "main.py").write_text("x = 1\n", encoding="utf-8")
        spec = adapter.parse(tmp_path)
        assert spec.tools == []
        assert spec.memory_configs == []

    def test_tool_without_docstring(self, adapter: OpenAIAgentsAdapter, tmp_path: Path) -> None:
        (tmp_path / "agent.py").write_text(
            "from agents import function_tool\n"
            "@function_tool\n"
            "def no_desc(query: str) -> str:\n"
            "    return query\n",
            encoding="utf-8",
        )
        spec = adapter.parse(tmp_path)
        assert spec.tools[0].description is None

    def test_agent_with_no_tools(self, adapter: OpenAIAgentsAdapter, tmp_path: Path) -> None:
        (tmp_path / "agent.py").write_text(
            "from agents import Agent\n"
            "agent = Agent(name='helper', instructions='Help')\n",
            encoding="utf-8",
        )
        spec = adapter.parse(tmp_path)
        assert spec.metadata.get("agent_count") == 1
        assert spec.tools == []
