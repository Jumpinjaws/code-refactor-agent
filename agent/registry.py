from typing import Callable
from agent.result import Result, ok, err


class ToolRegistry:
    """
    Pluggable tool registry. Tools register themselves with a name and callable.
    The executor resolves by name at runtime — adding a new tool requires zero
    changes to the executor or planner.
    """

    def __init__(self):
        self._tools: dict[str, Callable] = {}

    def register(self, name: str, fn: Callable) -> None:
        if name in self._tools:
            raise ValueError(f"Tool '{name}' is already registered")
        self._tools[name] = fn

    def execute(self, name: str, args: dict) -> Result:
        if name == "finish":
            return ok({"status": "finished", "summary": args.get("summary", "")})
        fn = self._tools.get(name)
        if fn is None:
            return err(f"Unknown tool: '{name}'. Registered tools: {list(self._tools.keys())}")
        try:
            result = fn(**args)
            return ok(result)
        except TypeError as e:
            return err(f"Tool '{name}' called with wrong arguments: {e}")
        except Exception as e:
            return err(f"Tool '{name}' raised an error: {e}")

    def list_tools(self) -> list[str]:
        return list(self._tools.keys())


def build_default_registry() -> ToolRegistry:
    from agent.tools.code_tools import (
        read_file, write_file, lint_code, format_code, run_tests, list_python_files,
    )
    from agent.tools.file_tools import create_backup, delete_file, list_directory, file_stats
    from agent.tools.search_tools import (
        search_in_file, search_in_directory, find_function_definition, find_class_definition,
    )

    registry = ToolRegistry()
    registry.register("read_file", read_file)
    registry.register("write_file", write_file)
    registry.register("lint_code", lint_code)
    registry.register("format_code", format_code)
    registry.register("run_tests", run_tests)
    registry.register("list_python_files", list_python_files)
    registry.register("create_backup", create_backup)
    registry.register("delete_file", delete_file)
    registry.register("list_directory", list_directory)
    registry.register("file_stats", file_stats)
    registry.register("search_in_file", search_in_file)
    registry.register("search_in_directory", search_in_directory)
    registry.register("find_function_definition", find_function_definition)
    registry.register("find_class_definition", find_class_definition)
    return registry
