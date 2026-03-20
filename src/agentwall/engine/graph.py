"""L2 engine: assignment-based project call graph with composition detection.

Implements a two-pass algorithm inspired by PyCG (ICSE '21):
  Pass 1 (_Pass1Visitor): collect function/class definitions, imports,
          module-level assignments, and class hierarchy.
  Pass 2 (_Pass2Visitor): seed variable types from Pass 1, collect call
          sites with arg names, detect pipe/factory/decorator composition.

build_project_graph() runs both passes over all source files, then
resolves cross-file calls using the import map built in Pass 1.
"""

from __future__ import annotations

import ast
import logging
from dataclasses import dataclass, field
from pathlib import Path

from agentwall.engine.models import UnresolvedCall, UnresolvedReason
from agentwall.frameworks.base import FrameworkModel

logger = logging.getLogger(__name__)

# ── Data structures ────────────────────────────────────────────────────────────


@dataclass
class IdentifierState:
    """Points-to state for one identifier (variable or attribute)."""

    name: str
    pointsto: set[str] = field(default_factory=set)
    scope: str = "<module>"


@dataclass(frozen=True)
class CallEdgeV2:
    """A resolved call between two named functions/methods."""

    caller_name: str
    callee_name: str
    caller_file: Path
    callee_file: Path | None
    line: int
    resolved: bool = True
    arg_names: tuple[str, ...] = ()


@dataclass(frozen=True)
class CompositionEdge:
    """A composition relationship between two components."""

    source: str
    target: str
    kind: str  # "pipe", "factory", "decorator"
    file: Path
    line: int


@dataclass
class ProjectGraph:
    """Complete project-level call and composition graph."""

    call_edges: list[CallEdgeV2]
    composition_edges: list[CompositionEdge]
    identifiers: dict[str, IdentifierState]
    extends: dict[str, str]  # child class → parent class (single-level)
    unresolved: list[UnresolvedCall]

    def callers_of(self, func_name: str) -> list[CallEdgeV2]:
        """Return all edges where func_name is the callee."""
        return [e for e in self.call_edges if e.callee_name == func_name]

    def callees_of(self, func_name: str) -> list[CallEdgeV2]:
        """Return all edges where func_name is the caller."""
        return [e for e in self.call_edges if e.caller_name == func_name]

    def resolve_method(self, class_name: str, method_name: str) -> str | None:
        """Resolve class_name.method_name with single-level inheritance.

        Returns:
            '<ClassName>.<method_name>' if the class defines the method,
            '<ParentClass>.<method_name>' if only the parent defines it or
            the parent is external (unknown methods), None if the class is
            not in the graph at all.
        """
        class_known = class_name in self._class_methods or class_name in self.extends
        if not class_known:
            return None
        if method_name in self._class_methods.get(class_name, set()):
            return f"{class_name}.{method_name}"
        parent = self.extends.get(class_name)
        if parent is None:
            return None
        # Parent defines the method, or parent is external (methods unknown —
        # fall back to parent as best-effort).
        if method_name in self._class_methods.get(parent, set()):
            return f"{parent}.{method_name}"
        # Parent is external: no local method record, assume it may define it.
        if parent not in self._class_methods:
            return f"{parent}.{method_name}"
        return None

    # Internal index: class name → set of method names defined in that class.
    # Populated by build_project_graph after Pass 1.
    _class_methods: dict[str, set[str]] = field(default_factory=dict)


# ── Module mapper ──────────────────────────────────────────────────────────────


class _ModuleMapper:
    """Map bare module names to file paths for import resolution."""

    def __init__(self, source_files: list[Path], root: Path | None) -> None:
        self._map: dict[str, Path] = {}
        for f in source_files:
            stem = f.stem
            self._map[stem] = f
        # Also map relative to root for dotted paths
        if root:
            for f in source_files:
                try:
                    rel = f.relative_to(root)
                    module_dotted = ".".join(rel.with_suffix("").parts)
                    self._map[module_dotted] = f
                except ValueError:
                    pass

    def resolve(self, module_name: str) -> Path | None:
        """Return the file path for module_name, or None if external."""
        return self._map.get(module_name)


# ── Pass 1: definitions, imports, assignments, hierarchy ──────────────────────


@dataclass
class _Pass1Result:
    # function name → file path
    functions: dict[str, Path] = field(default_factory=dict)
    # class name → file path
    classes: dict[str, Path] = field(default_factory=dict)
    # class name → set of method names
    class_methods: dict[str, set[str]] = field(default_factory=dict)
    # child class → parent class (single-level, first base only)
    extends: dict[str, str] = field(default_factory=dict)
    # local name → canonical class/function name (from imports)
    imports: dict[str, str] = field(default_factory=dict)
    # variable name → IdentifierState
    identifiers: dict[str, IdentifierState] = field(default_factory=dict)
    # module-level name → file where it is defined
    module_of: dict[str, str] = field(default_factory=dict)


class _Pass1Visitor(ast.NodeVisitor):
    """Collect definitions, imports, assignments, class hierarchy."""

    def __init__(self, file: Path) -> None:
        self._file = file
        self._result = _Pass1Result()
        self._current_class: str | None = None
        self._current_func: str | None = None

    def result(self) -> _Pass1Result:
        return self._result

    # ── imports ───────────────────────────────────────────────────────────────

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            local = alias.asname if alias.asname else alias.name.split(".")[-1]
            self._result.imports[local] = alias.name
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        module = node.module or ""
        for alias in node.names:
            local = alias.asname if alias.asname else alias.name
            canonical = f"{module}.{alias.name}" if module else alias.name
            self._result.imports[local] = canonical
        self.generic_visit(node)

    # ── class definitions ─────────────────────────────────────────────────────

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self._result.classes[node.name] = self._file
        self._result.class_methods.setdefault(node.name, set())
        # Single-level inheritance: use first base that is a plain Name
        for base in node.bases:
            if isinstance(base, ast.Name):
                self._result.extends[node.name] = base.id
                break
            if isinstance(base, ast.Attribute):
                self._result.extends[node.name] = base.attr
                break
        prev = self._current_class
        self._current_class = node.name
        self.generic_visit(node)
        self._current_class = prev

    # ── function definitions ──────────────────────────────────────────────────

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._visit_funcdef(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self._visit_funcdef(node)

    def _visit_funcdef(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
        if self._current_class:
            self._result.class_methods.setdefault(self._current_class, set()).add(node.name)
        else:
            self._result.functions[node.name] = self._file
        prev = self._current_func
        self._current_func = node.name
        self.generic_visit(node)
        self._current_func = prev

    # ── assignments ───────────────────────────────────────────────────────────

    def visit_Assign(self, node: ast.Assign) -> None:
        # Only track module-level and class-level assignments for now
        if self._current_func is not None:
            self.generic_visit(node)
            return
        rhs_type = self._extract_type(node.value)
        for target in node.targets:
            if isinstance(target, ast.Name):
                state = self._result.identifiers.setdefault(
                    target.id,
                    IdentifierState(name=target.id),
                )
                if rhs_type:
                    state.pointsto.add(rhs_type)
        self.generic_visit(node)

    def _extract_type(self, node: ast.expr) -> str | None:
        """Best-effort: return the class name being instantiated or called."""
        if isinstance(node, ast.Call):
            return _callee_name(node.func)
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.Attribute):
            return node.attr
        return None


# ── Pass 2: call sites and composition patterns ────────────────────────────────


class _Pass2Visitor(ast.NodeVisitor):
    """Collect call edges and composition edges."""

    def __init__(
        self,
        file: Path,
        pass1: _Pass1Result,
        all_pass1: _Pass1Result,
        model: FrameworkModel,
        mapper: _ModuleMapper,
    ) -> None:
        self._file = file
        self._pass1 = pass1
        self._all = all_pass1  # merged across all files
        self._model = model
        self._mapper = mapper
        self._current_func: str | None = None

        self.call_edges: list[CallEdgeV2] = []
        self.composition_edges: list[CompositionEdge] = []
        self.unresolved: list[UnresolvedCall] = []

    # ── scope tracking + decorator capture ───────────────────────────────────

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._collect_decorators(node)
        prev = self._current_func
        self._current_func = node.name
        self.generic_visit(node)
        self._current_func = prev

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self._collect_decorators(node)
        prev = self._current_func
        self._current_func = node.name
        self.generic_visit(node)
        self._current_func = prev

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self.generic_visit(node)

    # ── assignments: detect pipe and factory composition ─────────────────────

    def visit_Assign(self, node: ast.Assign) -> None:
        for target in node.targets:
            target_name = _name_of(target)
            # Pipe: BinOp with BitOr
            if isinstance(node.value, ast.BinOp):
                self._collect_pipe_edges(node.value, node.lineno)
            # Factory: Call with factory method pattern
            if isinstance(node.value, ast.Call):
                self._try_factory(node.value, target_name, node.lineno)
        self.generic_visit(node)

    # ── call sites ────────────────────────────────────────────────────────────

    def visit_Call(self, node: ast.Call) -> None:
        caller = self._current_func or "<module>"
        callee = _callee_name(node.func)
        arg_names = tuple(_arg_name(a) for a in node.args)

        if callee is None:
            self.unresolved.append(
                UnresolvedCall(
                    file=self._file,
                    line=node.lineno,
                    callee_expr=ast.unparse(node.func),
                    reason=UnresolvedReason.DYNAMIC_ATTR,
                )
            )
            self.generic_visit(node)
            return

        # Resolve callee to a file
        callee_file = self._resolve_callee_file(callee)
        resolved = callee_file is not None or callee in self._all.functions

        if not resolved:
            # Check if it's from an import (external module)
            bare = callee.split(".")[-1]
            if bare in self._pass1.imports or callee in self._pass1.imports:
                self.unresolved.append(
                    UnresolvedCall(
                        file=self._file,
                        line=node.lineno,
                        callee_expr=callee,
                        reason=UnresolvedReason.EXTERNAL_MODULE,
                    )
                )
                self.generic_visit(node)
                return

        self.call_edges.append(
            CallEdgeV2(
                caller_name=caller,
                callee_name=callee,
                caller_file=self._file,
                callee_file=callee_file,
                line=node.lineno,
                resolved=resolved,
                arg_names=arg_names,
            )
        )
        self.generic_visit(node)

    # ── decorator composition ─────────────────────────────────────────────────

    def _collect_decorators(self, func_node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
        for dec in func_node.decorator_list:
            dec_name = _callee_name(dec) or ast.unparse(dec)
            for pat in self._model.decorator_patterns:
                if dec_name == pat.decorator or dec_name.endswith(f".{pat.decorator}"):
                    self.composition_edges.append(
                        CompositionEdge(
                            source=func_node.name,
                            target=pat.registers_as,
                            kind="decorator",
                            file=self._file,
                            line=func_node.lineno,
                        )
                    )

    # ── pipe helper ───────────────────────────────────────────────────────────

    def _collect_pipe_edges(self, node: ast.BinOp, lineno: int) -> None:
        """Recursively collect pipe edges from a | b | c chains."""
        if not isinstance(node.op, ast.BitOr):
            return
        # Check that at least one pipe pattern uses "|"
        has_pipe = any(p.operator == "|" for p in self._model.pipe_patterns)
        if not has_pipe:
            return

        left_name = _expr_name(node.left)
        right_name = _expr_name(node.right)

        # Recurse into left side first (handles a | b | c as (a|b)|c)
        if isinstance(node.left, ast.BinOp):
            self._collect_pipe_edges(node.left, lineno)
            # After recursing, left_name is the "output" of the sub-chain
            left_name = _rightmost_name(node.left)

        self.composition_edges.append(
            CompositionEdge(
                source=left_name or "<unknown>",
                target=right_name or "<unknown>",
                kind="pipe",
                file=self._file,
                line=lineno,
            )
        )

    # ── factory helper ────────────────────────────────────────────────────────

    def _try_factory(self, node: ast.Call, target_name: str | None, lineno: int) -> None:
        method_name = _callee_name(node.func)
        if method_name is None:
            return
        bare_method = method_name.split(".")[-1]
        for pat in self._model.factory_patterns:
            if bare_method != pat.method:
                continue
            # Find the kwarg matching pat.kwarg
            kwarg_val: str | None = None
            for kw in node.keywords:
                if kw.arg == pat.kwarg:
                    kwarg_val = _expr_name(kw.value)
                    break
            self.composition_edges.append(
                CompositionEdge(
                    source=target_name or method_name,
                    target=kwarg_val or pat.kwarg,
                    kind="factory",
                    file=self._file,
                    line=lineno,
                )
            )

    # ── callee resolution ─────────────────────────────────────────────────────

    def _resolve_callee_file(self, callee: str) -> Path | None:
        """Try to find the file that defines callee."""
        # Direct function name
        if callee in self._all.functions:
            return self._all.functions[callee]
        # Bare name may be imported — find its module
        bare = callee.split(".")[-1]
        imported_as = self._pass1.imports.get(bare) or self._pass1.imports.get(callee)
        if imported_as:
            mod = imported_as.split(".")[0]
            return self._mapper.resolve(mod)
        return None


# ── Merge helper ──────────────────────────────────────────────────────────────


def _merge_pass1(results: list[tuple[Path, _Pass1Result]]) -> _Pass1Result:
    """Merge multiple Pass 1 results into one global index."""
    merged = _Pass1Result()
    for _file, r in results:
        merged.functions.update(r.functions)
        merged.classes.update(r.classes)
        merged.extends.update(r.extends)
        merged.imports.update(r.imports)
        merged.identifiers.update(r.identifiers)
        for cls, methods in r.class_methods.items():
            merged.class_methods.setdefault(cls, set()).update(methods)
    return merged


# ── Public API ─────────────────────────────────────────────────────────────────


def build_project_graph(
    source_files: list[Path],
    model: FrameworkModel,
    root: Path | None = None,
) -> ProjectGraph:
    """Build a project-level call and composition graph.

    Args:
        source_files: Python source files to analyse.
        model: Framework model declaring pipe/factory/decorator patterns.
        root: Optional root directory for resolving relative imports.

    Returns:
        A ProjectGraph with call edges, composition edges, identifier states,
        class hierarchy, and unresolved call records.

    Files that fail to parse are skipped with a warning. Never executes
    user code — all analysis via ast.parse() only.
    """
    if not source_files:
        return ProjectGraph(
            call_edges=[],
            composition_edges=[],
            identifiers={},
            extends={},
            unresolved=[],
            _class_methods={},
        )

    mapper = _ModuleMapper(source_files, root)

    # ── Pass 1 ────────────────────────────────────────────────────────────────
    pass1_results: list[tuple[Path, _Pass1Result]] = []
    parsed: list[tuple[Path, ast.Module]] = []

    for path in source_files:
        try:
            source = path.read_text(encoding="utf-8")
            tree = ast.parse(source, filename=str(path))
        except SyntaxError:
            logger.warning("Skipping %s: syntax error", path)
            continue
        except OSError as exc:
            logger.warning("Skipping %s: %s", path, exc)
            continue

        visitor = _Pass1Visitor(path)
        visitor.visit(tree)
        pass1_results.append((path, visitor.result()))
        parsed.append((path, tree))

    merged_pass1 = _merge_pass1(pass1_results)

    # ── Pass 2 ────────────────────────────────────────────────────────────────
    all_call_edges: list[CallEdgeV2] = []
    all_composition_edges: list[CompositionEdge] = []
    all_unresolved: list[UnresolvedCall] = []

    for path, tree in parsed:
        # Find the Pass1Result for this file
        file_pass1 = next(r for p, r in pass1_results if p == path)
        visitor2 = _Pass2Visitor(
            file=path,
            pass1=file_pass1,
            all_pass1=merged_pass1,
            model=model,
            mapper=mapper,
        )
        visitor2.visit(tree)
        all_call_edges.extend(visitor2.call_edges)
        all_composition_edges.extend(visitor2.composition_edges)
        all_unresolved.extend(visitor2.unresolved)

    return ProjectGraph(
        call_edges=all_call_edges,
        composition_edges=all_composition_edges,
        identifiers=merged_pass1.identifiers,
        extends=merged_pass1.extends,
        unresolved=all_unresolved,
        _class_methods=merged_pass1.class_methods,
    )


# ── AST utilities ──────────────────────────────────────────────────────────────


def _callee_name(node: ast.expr) -> str | None:
    """Extract a string name from a function call's func node."""
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        owner = _callee_name(node.value)
        if owner:
            return f"{owner}.{node.attr}"
        return node.attr
    return None


def _name_of(node: ast.expr) -> str | None:
    """Return the name string for an assignment target."""
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    return None


def _expr_name(node: ast.expr) -> str | None:
    """Return the string name of a simple expression (Name or Attribute)."""
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    return None


def _arg_name(node: ast.expr) -> str:
    """Best-effort string name for a positional call argument."""
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    if isinstance(node, ast.Constant):
        return repr(node.value)
    return ast.unparse(node)


def _rightmost_name(node: ast.expr) -> str | None:
    """Return the rightmost operand name from a nested BinOp chain."""
    if isinstance(node, ast.BinOp):
        return _rightmost_name(node.right)
    return _expr_name(node)
