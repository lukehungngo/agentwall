"""Tests for project scoping (self-library detection)."""

from __future__ import annotations

from pathlib import Path

from agentwall.scoping import is_self_library_project


class TestIsSelfLibraryProject:
    """Detect when scan target IS a known framework/vector-store library."""

    def test_langchain_pyproject(self, tmp_path: Path) -> None:
        (tmp_path / "pyproject.toml").write_text(
            '[project]\nname = "langchain"\nversion = "0.3.0"\n'
        )
        assert is_self_library_project(tmp_path) is True

    def test_langchain_community_pyproject(self, tmp_path: Path) -> None:
        (tmp_path / "pyproject.toml").write_text(
            '[project]\nname = "langchain-community"\nversion = "0.2.0"\n'
        )
        assert is_self_library_project(tmp_path) is True

    def test_chromadb_pyproject(self, tmp_path: Path) -> None:
        (tmp_path / "pyproject.toml").write_text(
            '[project]\nname = "chromadb"\nversion = "0.5.0"\n'
        )
        assert is_self_library_project(tmp_path) is True

    def test_llama_index_pyproject(self, tmp_path: Path) -> None:
        (tmp_path / "pyproject.toml").write_text(
            '[project]\nname = "llama-index"\nversion = "0.10.0"\n'
        )
        assert is_self_library_project(tmp_path) is True

    def test_user_app_pyproject(self, tmp_path: Path) -> None:
        (tmp_path / "pyproject.toml").write_text(
            '[project]\nname = "my-chatbot"\nversion = "1.0.0"\n'
        )
        assert is_self_library_project(tmp_path) is False

    def test_no_pyproject(self, tmp_path: Path) -> None:
        assert is_self_library_project(tmp_path) is False

    def test_setup_cfg_langchain(self, tmp_path: Path) -> None:
        (tmp_path / "setup.cfg").write_text(
            "[metadata]\nname = langchain\nversion = 0.2.0\n"
        )
        assert is_self_library_project(tmp_path) is True

    def test_setup_py_chromadb(self, tmp_path: Path) -> None:
        (tmp_path / "setup.py").write_text(
            'from setuptools import setup\nsetup(name="chromadb", version="0.4.0")\n'
        )
        assert is_self_library_project(tmp_path) is True

    def test_setup_py_user_app(self, tmp_path: Path) -> None:
        (tmp_path / "setup.py").write_text(
            'from setuptools import setup\nsetup(name="my-app")\n'
        )
        assert is_self_library_project(tmp_path) is False

    def test_pyproject_with_poetry(self, tmp_path: Path) -> None:
        (tmp_path / "pyproject.toml").write_text(
            '[tool.poetry]\nname = "pinecone"\nversion = "3.0.0"\n'
        )
        assert is_self_library_project(tmp_path) is True

    def test_malformed_pyproject(self, tmp_path: Path) -> None:
        (tmp_path / "pyproject.toml").write_text("this is not valid toml {{{{")
        assert is_self_library_project(tmp_path) is False

    def test_qdrant_client_normalized(self, tmp_path: Path) -> None:
        (tmp_path / "pyproject.toml").write_text(
            '[project]\nname = "qdrant-client"\nversion = "1.0.0"\n'
        )
        assert is_self_library_project(tmp_path) is True

    def test_weaviate_client(self, tmp_path: Path) -> None:
        (tmp_path / "pyproject.toml").write_text(
            '[project]\nname = "weaviate-client"\nversion = "4.0.0"\n'
        )
        assert is_self_library_project(tmp_path) is True

    def test_langgraph(self, tmp_path: Path) -> None:
        (tmp_path / "pyproject.toml").write_text(
            '[project]\nname = "langgraph"\nversion = "0.1.0"\n'
        )
        assert is_self_library_project(tmp_path) is True


class TestModuleLayoutDetection:
    """Secondary signal: module layout matches known framework name."""

    def test_chromadb_module_with_setup_py(self, tmp_path: Path) -> None:
        """chromadb/ package + setup.py (library marker) → True."""
        pkg = tmp_path / "chromadb"
        pkg.mkdir()
        (pkg / "__init__.py").touch()
        (tmp_path / "setup.py").write_text("from setuptools import setup\nsetup()\n")
        assert is_self_library_project(tmp_path) is True

    def test_src_layout_langchain_with_manifest(self, tmp_path: Path) -> None:
        """src/langchain_community/ package + MANIFEST.in → True."""
        pkg = tmp_path / "src" / "langchain_community"
        pkg.mkdir(parents=True)
        (pkg / "__init__.py").touch()
        (tmp_path / "MANIFEST.in").touch()
        assert is_self_library_project(tmp_path) is True

    def test_random_dir_no_init(self, tmp_path: Path) -> None:
        """Directory named 'chromadb' but no __init__.py → False."""
        (tmp_path / "chromadb").mkdir()
        (tmp_path / "setup.py").write_text("from setuptools import setup\nsetup()\n")
        assert is_self_library_project(tmp_path) is False

    def test_user_app_module_not_matched(self, tmp_path: Path) -> None:
        """myapp/ package → not in known names → False."""
        pkg = tmp_path / "myapp"
        pkg.mkdir()
        (pkg / "__init__.py").touch()
        (tmp_path / "setup.py").write_text("from setuptools import setup\nsetup()\n")
        assert is_self_library_project(tmp_path) is False

    def test_metadata_overrides_layout(self, tmp_path: Path) -> None:
        """If pyproject.toml says 'my-app', module layout is NOT checked."""
        (tmp_path / "pyproject.toml").write_text(
            '[project]\nname = "my-app"\nversion = "1.0"\n'
        )
        pkg = tmp_path / "chromadb"
        pkg.mkdir()
        (pkg / "__init__.py").touch()
        assert is_self_library_project(tmp_path) is False

    def test_module_without_library_marker_is_false(self, tmp_path: Path) -> None:
        """chromadb/ package but no setup.py/setup.cfg/MANIFEST.in → False.
        This prevents FPs on user apps with vendored framework dirs."""
        pkg = tmp_path / "graphrag"
        pkg.mkdir()
        (pkg / "__init__.py").touch()
        assert is_self_library_project(tmp_path) is False
