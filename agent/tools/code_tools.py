import subprocess
import sys
import os
import ast
import black
import isort.main


def read_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_file(path: str, content: str) -> str:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return f"Written to {path}"


def lint_code(code: str) -> dict:
    result = {"syntax_valid": False, "errors": []}
    try:
        ast.parse(code)
        result["syntax_valid"] = True
    except SyntaxError as e:
        result["errors"].append(f"SyntaxError at line {e.lineno}: {e.msg}")
    return result


def format_code(code: str) -> str:
    try:
        formatted = black.format_str(code, mode=black.Mode())
        return formatted
    except Exception:
        return code


def run_tests(test_dir: str = "tests") -> dict:
    result = subprocess.run(
        [sys.executable, "-m", "pytest", test_dir, "--tb=short", "-q"],
        capture_output=True,
        text=True,
    )
    return {
        "passed": result.returncode == 0,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


def list_python_files(directory: str) -> list[str]:
    py_files = []
    for root, _, files in os.walk(directory):
        for f in files:
            if f.endswith(".py"):
                py_files.append(os.path.join(root, f))
    return py_files
