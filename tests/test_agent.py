import pytest
from unittest.mock import patch, MagicMock
from agent.tools.code_tools import lint_code, format_code, list_python_files


def test_lint_valid_code():
    code = "def hello():\n    return 'world'\n"
    result = lint_code(code)
    assert result["syntax_valid"] is True
    assert result["errors"] == []


def test_lint_invalid_code():
    code = "def hello(\n    return 'world'\n"
    result = lint_code(code)
    assert result["syntax_valid"] is False
    assert len(result["errors"]) > 0


def test_format_code():
    messy = "x=1+2\ny   =   3\n"
    formatted = format_code(messy)
    assert "x = 1 + 2" in formatted


def test_list_python_files(tmp_path):
    (tmp_path / "a.py").write_text("x = 1")
    (tmp_path / "b.py").write_text("y = 2")
    (tmp_path / "c.txt").write_text("not python")
    files = list_python_files(str(tmp_path))
    assert len(files) == 2
    assert all(f.endswith(".py") for f in files)


def test_executor_unknown_tool():
    from agent.executor import execute
    result = execute("nonexistent_tool", {})
    assert "error" in result


def test_executor_finish():
    from agent.executor import execute
    result = execute("finish", {"summary": "all done"})
    assert result["status"] == "finished"
    assert result["summary"] == "all done"
