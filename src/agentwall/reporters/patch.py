"""Patch reporter — unified diff output for auto-fixable findings (FR-502)."""

from __future__ import annotations

import difflib
from collections.abc import Callable
from pathlib import Path

from agentwall.models import Finding, ScanResult

# Patterns for auto-fixable rules. Each maps a rule_id to a function that
# takes (source_lines, finding) and returns patched_lines, or None if no
# auto-fix is possible.


def _find_call_args(line: str, method_name: str) -> tuple[int, int, str] | None:
    """Find a method call and extract the args span using paren-depth counting.

    Returns (start_of_call, end_of_close_paren, args_string) or None.
    Handles nested parentheses safely. Returns None if nested parens are
    detected (fall back to manual comment).
    """
    prefix = f".{method_name}"
    idx = line.find(prefix)
    if idx == -1:
        return None

    # Find the opening paren (possibly with whitespace after method name)
    pos = idx + len(prefix)
    while pos < len(line) and line[pos] in " \t":
        pos += 1
    if pos >= len(line) or line[pos] != "(":
        return None

    open_pos = pos
    depth = 1
    has_nested = False
    pos += 1
    while pos < len(line) and depth > 0:
        ch = line[pos]
        if ch == "(":
            depth += 1
            has_nested = True
        elif ch == ")":
            depth -= 1
        pos += 1

    if depth != 0:
        # Unbalanced parens — cannot safely patch
        return None

    if has_nested:
        # Nested parens detected — fall back to manual comment
        return None

    close_pos = pos  # one past the closing paren
    args_str = line[open_pos + 1 : close_pos - 1]
    return (idx, close_pos, args_str)


def _fix_mem001(lines: list[str], finding: Finding) -> list[str] | None:
    """Add filter={'user_id': user_id} to similarity_search calls."""
    if finding.line is None:
        return None

    idx = finding.line - 1
    if idx < 0 or idx >= len(lines):
        return None

    line = lines[idx]
    patched = lines[:]

    # Try similarity_search
    result = _find_call_args(line, "similarity_search")
    if result is not None:
        call_start, call_end, args = result
        args = args.strip()
        if args:
            new_args = f'{args}, filter={{"user_id": user_id}}'
        else:
            new_args = 'filter={"user_id": user_id}'
        # Reconstruct: everything before the dot, then .similarity_search(new_args), then rest
        method_prefix = ".similarity_search("
        patched[idx] = line[:call_start] + method_prefix + new_args + ")" + line[call_end:]
        return patched

    # Try as_retriever
    result = _find_call_args(line, "as_retriever")
    if result is not None:
        call_start, call_end, args = result
        args = args.strip()
        filter_arg = 'search_kwargs={"filter": {"user_id": user_id}}'
        new_args = f"{args}, {filter_arg}" if args else filter_arg
        patched[idx] = line[:call_start] + ".as_retriever(" + new_args + ")" + line[call_end:]
        return patched

    return None


_AUTO_FIXERS: dict[str, Callable[[list[str], Finding], list[str] | None]] = {
    "AW-MEM-001": _fix_mem001,
}


def _generate_diff(
    original: list[str],
    patched: list[str],
    filepath: str,
) -> str:
    """Generate a unified diff between original and patched content."""
    return "".join(
        difflib.unified_diff(
            original,
            patched,
            fromfile=f"a/{filepath}",
            tofile=f"b/{filepath}",
        )
    )


def _manual_comment(finding: Finding) -> str:
    """Generate a comment for findings that need manual intervention."""
    parts = [
        f"# {finding.rule_id}: {finding.title}",
    ]
    if finding.file:
        loc = str(finding.file)
        if finding.line:
            loc += f":{finding.line}"
        parts.append(f"# Location: {loc}")
    parts.append(f"# {finding.description}")
    if finding.fix:
        parts.append(f"# Suggested fix: {finding.fix}")
    parts.append("# This finding requires manual intervention.")
    return "\n".join(parts)


def build_patch(result: ScanResult) -> str:
    """Build unified diff output for all findings."""
    output_parts: list[str] = []

    # Group findings by file for efficient processing
    by_file: dict[Path, list[Finding]] = {}
    no_file: list[Finding] = []
    for finding in result.findings:
        if finding.file is not None:
            by_file.setdefault(finding.file, []).append(finding)
        else:
            no_file.append(finding)

    for filepath, findings in sorted(by_file.items()):
        # Try to read the source file
        try:
            source_text = filepath.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            for f in findings:
                output_parts.append(_manual_comment(f))
            continue

        source_lines = source_text.splitlines(keepends=True)

        for finding in findings:
            fixer = _AUTO_FIXERS.get(finding.rule_id)
            if fixer is not None:
                patched = fixer(source_lines, finding)
                if patched is not None:
                    diff = _generate_diff(source_lines, patched, str(filepath))
                    if diff:
                        output_parts.append(diff)
                        continue

            # No auto-fix available or fixer returned None
            output_parts.append(_manual_comment(finding))

    # Findings without a file
    for finding in no_file:
        output_parts.append(_manual_comment(finding))

    return "\n".join(output_parts)


class PatchReporter:
    """Unified diff output for auto-fixable findings (FR-502)."""

    def render(self, result: ScanResult, output: Path) -> None:
        patch_text = build_patch(result)
        output.write_text(patch_text, encoding="utf-8")
