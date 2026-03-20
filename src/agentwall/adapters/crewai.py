"""CrewAI adapter -- AST-based parser for CrewAI agent code."""

from __future__ import annotations

import ast
import warnings
from pathlib import Path

from agentwall.detector import _SKIP_DIRS
from agentwall.models import (
    AgentSpec,
    MemoryConfig,
    ToolSpec,
)
from agentwall.patterns import (
    CODE_EXEC_CALLS,
    DESTRUCTIVE_KEYWORDS,
)

# CrewAI uses LangChain vector stores internally -- detect same class names.
_VECTOR_STORES: dict[str, str] = {
    "Chroma": "chroma",
    "FAISS": "faiss",
    "Pinecone": "pinecone",
    "Qdrant": "qdrant",
    "PGVector": "pgvector",
}


class _CrewAIVisitor(ast.NodeVisitor):
    """AST visitor for a single Python file -- extracts CrewAI patterns."""

    def __init__(self, source_file: Path) -> None:
        self.source_file = source_file
        self.tools: list[ToolSpec] = []
        self.memory_configs: list[MemoryConfig] = []
        self._tool_decorated_funcs: set[str] = set()
        # Track Agent(..., tools=[...]) tool references.
        self.agent_tool_refs: list[str] = []
        self.agent_count: int = 0
        self.crew_count: int = 0

    # -- Decorators: @tool -----------------------------------------------------

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._check_tool_decorator(node)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self._check_tool_decorator(node)
        self.generic_visit(node)

    def _check_tool_decorator(
        self, node: ast.FunctionDef | ast.AsyncFunctionDef
    ) -> None:
        for dec in node.decorator_list:
            name = _get_name(dec)
            if name == "tool":
                self._tool_decorated_funcs.add(node.name)
                desc = ast.get_docstring(node)
                tool_spec = ToolSpec(
                    name=node.name,
                    description=desc,
                    source_file=self.source_file,
                    source_line=node.lineno,
                    is_destructive=_name_is_destructive(node.name),
                    accepts_code_execution=_body_has_code_exec(node),
                )
                self.tools.append(tool_spec)

    # -- Assignments: Agent(...), Crew(...), vector stores ---------------------

    def visit_Assign(self, node: ast.Assign) -> None:
        if isinstance(node.value, ast.Call):
            var_name: str | None = None
            if node.targets and isinstance(node.targets[0], ast.Name):
                var_name = node.targets[0].id
            self._check_vectorstore_call(node.value, node.lineno, var_name)
            self._check_agent_call(node.value)
            self._check_crew_call(node.value)
        self.generic_visit(node)

    def _check_vectorstore_call(
        self, call: ast.Call, lineno: int, var_name: str | None = None
    ) -> None:
        class_name = _get_name(call.func)
        if class_name not in _VECTOR_STORES:
            return
        backend = _VECTOR_STORES[class_name]
        coll_name = _get_keyword_str(call, "collection_name")
        mc = MemoryConfig(
            backend=backend,
            collection_name=coll_name,
            source_file=self.source_file,
            source_line=lineno,
        )
        self.memory_configs.append(mc)

    def _check_agent_call(self, call: ast.Call) -> None:
        """Detect Agent(role=..., tools=[...])."""
        class_name = _get_name(call.func)
        if class_name != "Agent":
            return
        self.agent_count += 1
        # Extract tool references from tools=[...] kwarg.
        for kw in call.keywords:
            if kw.arg == "tools" and isinstance(kw.value, ast.List):
                for elt in kw.value.elts:
                    name = _get_name(elt)
                    if name:
                        self.agent_tool_refs.append(name)

    def _check_crew_call(self, call: ast.Call) -> None:
        """Detect Crew(agents=[...], tasks=[...])."""
        class_name = _get_name(call.func)
        if class_name == "Crew":
            self.crew_count += 1


# -- Module-level helpers ------------------------------------------------------


def _get_name(node: ast.expr) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    return None


def _get_keyword_str(call: ast.Call, key: str) -> str | None:
    for kw in call.keywords:
        if kw.arg == key and isinstance(kw.value, ast.Constant):
            return str(kw.value.value)
    return None


def _name_is_destructive(name: str) -> bool:
    low = name.lower()
    return any(kw in low for kw in DESTRUCTIVE_KEYWORDS)


def _body_has_code_exec(node: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    for child in ast.walk(node):
        if isinstance(child, ast.Call):
            func = child.func
            if isinstance(func, ast.Name) and func.id in CODE_EXEC_CALLS:
                return True
            if isinstance(func, ast.Attribute) and func.attr in CODE_EXEC_CALLS:
                return True
    return False


# -- Adapter -------------------------------------------------------------------


class CrewAIAdapter:
    """Parse a CrewAI agent directory into an AgentSpec."""

    def parse(self, target: Path) -> AgentSpec:
        py_files = sorted(
            f
            for f in target.rglob("*.py")
            if not any(part in _SKIP_DIRS for part in f.relative_to(target).parts)
        )
        all_tools: list[ToolSpec] = []
        all_memory: list[MemoryConfig] = []
        scanned: list[Path] = []
        total_agents = 0
        total_crews = 0

        for py_file in py_files:
            try:
                source = py_file.read_text(encoding="utf-8")
                tree = ast.parse(source, filename=str(py_file))
            except (OSError, SyntaxError) as exc:
                warnings.warn(f"Skipping {py_file}: {exc}", stacklevel=2)
                continue

            visitor = _CrewAIVisitor(source_file=py_file)
            visitor.visit(tree)
            all_tools.extend(visitor.tools)
            all_memory.extend(visitor.memory_configs)
            total_agents += visitor.agent_count
            total_crews += visitor.crew_count
            scanned.append(py_file)

        metadata: dict[str, object] = {}
        if total_agents:
            metadata["agent_count"] = total_agents
        if total_crews:
            metadata["crew_count"] = total_crews

        return AgentSpec(
            framework="crewai",
            source_files=scanned,
            tools=all_tools,
            memory_configs=all_memory,
            metadata=metadata,
        )
