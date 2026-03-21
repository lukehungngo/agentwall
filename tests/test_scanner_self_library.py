"""Integration test: self-library scoping for MEM-001."""

from __future__ import annotations

from pathlib import Path

from agentwall.models import Severity
from agentwall.scanner import scan


class TestSelfLibraryScan:
    """When scanning a project that IS a vector-store SDK, core library code → INFO."""

    def test_chromadb_core_library_mem001_is_info(self, tmp_path: Path) -> None:
        """Core library code in self-library project → MEM-001 = INFO."""
        (tmp_path / "pyproject.toml").write_text(
            '[project]\nname = "chromadb"\nversion = "0.5.0"\n'
        )
        # Core library path (not in examples/demos/apps)
        src = tmp_path / "chromadb" / "api" / "segment.py"
        src.parent.mkdir(parents=True, exist_ok=True)
        src.write_text(
            "import chromadb\n"
            "from fastapi import FastAPI\n"
            "\n"
            "client = chromadb.Client()\n"
            "collection = client.get_collection('docs')\n"
            "results = collection.query(query_texts=['hello'])\n"
        )

        result = scan(tmp_path, framework="vectorstore_direct")

        mem001 = [f for f in result.findings if f.rule_id == "AW-MEM-001"]
        assert len(mem001) > 0, "Expected at least one MEM-001 finding"
        for f in mem001:
            assert f.severity == Severity.INFO, (
                f"MEM-001 in core library code should be INFO, got {f.severity}"
            )

    def test_user_app_with_chromadb_not_self_library(self, tmp_path: Path) -> None:
        """User app that USES chromadb → MEM-001 is NOT automatically INFO."""
        (tmp_path / "pyproject.toml").write_text(
            '[project]\nname = "my-chatbot"\nversion = "1.0.0"\n'
        )
        src = tmp_path / "app.py"
        src.write_text(
            "import chromadb\n"
            "from fastapi import FastAPI\n"
            "\n"
            "app = FastAPI()\n"
            "client = chromadb.Client()\n"
            "collection = client.get_collection('docs')\n"
            "results = collection.similarity_search('hello')\n"
        )

        result = scan(tmp_path, framework="vectorstore_direct")

        mem001 = [f for f in result.findings if f.rule_id == "AW-MEM-001"]
        high_or_above = [
            f for f in mem001
            if f.severity in (Severity.CRITICAL, Severity.HIGH)
        ]
        assert len(high_or_above) > 0, (
            f"User app MEM-001 should be CRITICAL/HIGH, got {[f.severity for f in mem001]}"
        )

    def test_langchain_community_core_code_is_info(self, tmp_path: Path) -> None:
        """Core library code in langchain-community → INFO."""
        (tmp_path / "pyproject.toml").write_text(
            '[project]\nname = "langchain-community"\nversion = "0.2.0"\n'
        )
        src = tmp_path / "langchain_community" / "vectorstores" / "chroma.py"
        src.parent.mkdir(parents=True, exist_ok=True)
        src.write_text(
            "from langchain_core.vectorstores import VectorStore\n"
            "import chromadb\n"
            "\n"
            "class Chroma(VectorStore):\n"
            "    def similarity_search(self, query):\n"
            "        return self._collection.query(query_texts=[query])\n"
        )

        result = scan(tmp_path, framework="langchain")

        mem001 = [f for f in result.findings if f.rule_id == "AW-MEM-001"]
        for f in mem001:
            assert f.severity == Severity.INFO, (
                f"MEM-001 in core langchain-community code should be INFO, got {f.severity}"
            )

    def test_self_library_recipes_not_auto_info(self, tmp_path: Path) -> None:
        """Recipes/examples in self-library still use normal severity logic."""
        (tmp_path / "pyproject.toml").write_text(
            '[project]\nname = "chromadb"\nversion = "0.5.0"\n'
        )
        # recipes/ is a mini-app, not core library code
        src = tmp_path / "recipes" / "rag_app.py"
        src.parent.mkdir(parents=True, exist_ok=True)
        src.write_text(
            "import chromadb\n"
            "from fastapi import FastAPI\n"
            "\n"
            "app = FastAPI()\n"
            "collection = chromadb.Client().get_collection('docs')\n"
            "results = collection.similarity_search('hello')\n"
        )

        result = scan(tmp_path, framework="vectorstore_direct")

        mem001 = [f for f in result.findings if f.rule_id == "AW-MEM-001"]
        # recipes/ is NOT excluded from normal severity — findings should NOT
        # be downgraded to INFO just because the project is a self-library
        for f in mem001:
            assert "library" not in (f.description or "").lower() or f.severity != Severity.INFO, (
                "MEM-001 in recipes/ should not be INFO from self-library logic"
            )
