"""Tests for framework auto-detection."""

from __future__ import annotations

from pathlib import Path

from agentwall.detector import auto_detect_framework


def test_detects_pydantic_ai(tmp_path: Path) -> None:
    (tmp_path / "app.py").write_text("from pydantic_ai import Agent\n")
    assert auto_detect_framework(tmp_path) == "pydantic_ai"


def test_detects_graphrag(tmp_path: Path) -> None:
    (tmp_path / "app.py").write_text("from graphrag import query\n")
    assert auto_detect_framework(tmp_path) == "graphrag"


def test_detects_dspy(tmp_path: Path) -> None:
    (tmp_path / "app.py").write_text("import dspy\n")
    assert auto_detect_framework(tmp_path) == "dspy"


def test_detects_semantic_kernel(tmp_path: Path) -> None:
    (tmp_path / "app.py").write_text("from semantic_kernel import Kernel\n")
    assert auto_detect_framework(tmp_path) == "semantic_kernel"


def test_returns_none_for_empty_dir(tmp_path: Path) -> None:
    assert auto_detect_framework(tmp_path) is None


def test_returns_none_for_no_framework(tmp_path: Path) -> None:
    (tmp_path / "app.py").write_text("import os\n")
    assert auto_detect_framework(tmp_path) is None
