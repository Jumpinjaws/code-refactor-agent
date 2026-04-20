from agent.tools.code_tools import (
    read_file,
    write_file,
    lint_code,
    format_code,
    run_tests,
    list_python_files,
)

TOOL_MAP = {
    "read_file": read_file,
    "write_file": write_file,
    "lint_code": lint_code,
    "format_code": format_code,
    "run_tests": run_tests,
    "list_python_files": list_python_files,
}


def execute(tool: str, args: dict):
    if tool == "finish":
        return {"status": "finished", "summary": args.get("summary", "")}
    fn = TOOL_MAP.get(tool)
    if not fn:
        return {"error": f"Unknown tool: {tool}"}
    try:
        return fn(**args)
    except Exception as e:
        return {"error": str(e)}
