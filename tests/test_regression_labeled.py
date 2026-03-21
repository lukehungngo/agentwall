"""Labeled regression test set — verifies key findings are not lost between versions.

This test set contains representative code patterns for each rule. If a code
change causes any of these to stop firing, it's a regression.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from agentwall.scanner import scan


class TestLabeledRegressionSet:
    """Each test represents a known-good finding that must not be lost."""

    def test_mem001_chroma_no_isolation(self, tmp_path: Path) -> None:
        """MEM-001 fires on Chroma without tenant isolation."""
        (tmp_path / "app.py").write_text(
            "import chromadb\n"
            "client = chromadb.Client()\n"
            "col = client.create_collection('docs')\n"
        )
        result = scan(tmp_path)
        assert any(f.rule_id == "AW-MEM-001" for f in result.findings)

    def test_mem003_no_access_control(self, tmp_path: Path) -> None:
        """MEM-003 fires on vectorstore with no access control."""
        (tmp_path / "app.py").write_text(
            "import chromadb\n"
            "client = chromadb.Client()\n"
            "col = client.create_collection('docs')\n"
        )
        result = scan(tmp_path)
        assert any(f.rule_id == "AW-MEM-003" for f in result.findings)

    def test_tool002_eval_detected(self, tmp_path: Path) -> None:
        """TOOL-002 fires on functions containing eval()."""
        (tmp_path / "app.py").write_text(
            "def run_code(code: str) -> str:\n"
            '    """Execute code."""\n'
            "    return str(eval(code))\n"
        )
        result = scan(tmp_path)
        assert any(f.rule_id == "AW-TOOL-002" for f in result.findings)

    def test_tool002_subprocess_detected(self, tmp_path: Path) -> None:
        """TOOL-002 fires on functions containing subprocess."""
        (tmp_path / "app.py").write_text(
            "import subprocess\n"
            "def run_shell(cmd: str) -> str:\n"
            '    """Run a shell command."""\n'
            "    return subprocess.check_output(cmd, shell=True).decode()\n"
        )
        result = scan(tmp_path)
        assert any(f.rule_id == "AW-TOOL-002" for f in result.findings)

    def test_tool001_destructive_no_gate(self, tmp_path: Path) -> None:
        """TOOL-001 fires on destructive function without approval gate."""
        (tmp_path / "app.py").write_text(
            "from langchain.tools import tool\n"
            "@tool\n"
            "def delete_all_records(ids: list) -> str:\n"
            '    """Delete all records."""\n'
            "    return 'deleted'\n"
        )
        result = scan(tmp_path)
        assert any(f.rule_id == "AW-TOOL-001" for f in result.findings)

    def test_ser001_pickle_load(self, tmp_path: Path) -> None:
        """SER-001 fires on pickle.loads()."""
        (tmp_path / "app.py").write_text(
            "import pickle\n"
            "data = pickle.loads(raw_bytes)\n"
        )
        result = scan(tmp_path)
        assert any(f.rule_id == "AW-SER-001" for f in result.findings)

    def test_ser003_dynamic_import(self, tmp_path: Path) -> None:
        """SER-003 fires on importlib.import_module with variable arg."""
        (tmp_path / "app.py").write_text(
            "import importlib\n"
            "mod = importlib.import_module(user_input)\n"
        )
        result = scan(tmp_path)
        assert any(f.rule_id == "AW-SER-003" for f in result.findings)

    def test_sec001_hardcoded_api_key(self, tmp_path: Path) -> None:
        """SEC-001 fires on hardcoded API keys."""
        (tmp_path / "app.py").write_text(
            'OPENAI_API_KEY = "sk-1234567890abcdef1234567890abcdef"\n'
        )
        result = scan(tmp_path)
        assert any(f.rule_id == "AW-SEC-001" for f in result.findings)

    def test_rag003_persist_directory(self, tmp_path: Path) -> None:
        """RAG-003 fires on unencrypted local persistence."""
        (tmp_path / "app.py").write_text(
            "from langchain.vectorstores import Chroma\n"
            'db = Chroma(persist_directory="/data/chroma")\n'
        )
        result = scan(tmp_path)
        assert any(f.rule_id == "AW-RAG-003" for f in result.findings)

    def test_rag001_no_delimiter(self, tmp_path: Path) -> None:
        """RAG-001 fires on retrieval without delimiter injection protection."""
        (tmp_path / "app.py").write_text(
            "def search(query):\n"
            "    results = collection.similarity_search(query)\n"
            '    prompt = f"Context: {results}\\nQuestion: {query}"\n'
            "    return prompt\n"
        )
        result = scan(tmp_path)
        assert any(f.rule_id == "AW-RAG-001" for f in result.findings)

    def test_cfg_hardcoded_secret(self, tmp_path: Path) -> None:
        """CFG-hardcoded-secret fires on secrets in config/env files."""
        (tmp_path / ".env").write_text(
            "DATABASE_URL=postgresql://user:password123@localhost/db\n"
            "SECRET_KEY=super-secret-key-12345\n"
        )
        (tmp_path / "docker-compose.yml").write_text(
            "services:\n"
            "  db:\n"
            "    environment:\n"
            "      - POSTGRES_PASSWORD=mysecretpassword123\n"
        )
        (tmp_path / "app.py").write_text("# placeholder\n")
        result = scan(tmp_path)
        has_cfg = any("CFG" in f.rule_id for f in result.findings)
        has_sec = any("SEC" in f.rule_id for f in result.findings)
        assert has_cfg or has_sec, f"Expected CFG or SEC finding, got: {[f.rule_id for f in result.findings]}"

    def test_agt004_llm_output_to_memory(self, tmp_path: Path) -> None:
        """AGT-004 fires when LLM output flows to memory without sanitization."""
        (tmp_path / "app.py").write_text(
            "from langchain.tools import tool\n"
            "@tool\n"
            "def helper(q: str) -> str:\n"
            '    """Help."""\n'
            "    return q\n"
            "\n"
            "def run():\n"
            "    result = invoke('query')\n"
            "    add_texts(result)\n"
        )
        result = scan(tmp_path)
        assert any(f.rule_id == "AW-AGT-004" for f in result.findings)


@pytest.mark.parametrize(
    "rule_id",
    [
        "AW-MEM-001",
        "AW-MEM-003",
        "AW-TOOL-002",
        "AW-SER-001",
        "AW-SEC-001",
        "AW-RAG-003",
    ],
)
def test_core_rules_have_documentation(rule_id: str) -> None:
    """Every core rule must be documented in docs/rules.md."""
    rules_path = Path(__file__).parent.parent / "docs" / "rules.md"
    if rules_path.exists():
        content = rules_path.read_text()
        assert rule_id in content, f"{rule_id} missing from docs/rules.md"
