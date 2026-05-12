import pytest
from agent.registry import ToolRegistry
from agent.result import is_ok


def test_register_and_execute():
    registry = ToolRegistry()
    registry.register("add", lambda x, y: x + y)
    result = registry.execute("add", {"x": 2, "y": 3})
    assert is_ok(result)
    assert result.value == 5


def test_execute_unknown_tool():
    registry = ToolRegistry()
    result = registry.execute("nonexistent", {})
    assert not is_ok(result)
    assert "Unknown tool" in result.error


def test_duplicate_registration_raises():
    registry = ToolRegistry()
    registry.register("tool", lambda: None)
    with pytest.raises(ValueError, match="already registered"):
        registry.register("tool", lambda: None)


def test_finish_tool():
    registry = ToolRegistry()
    result = registry.execute("finish", {"summary": "all done"})
    assert is_ok(result)
    assert result.value["status"] == "finished"
    assert result.value["summary"] == "all done"


def test_wrong_args_returns_err():
    registry = ToolRegistry()
    registry.register("greet", lambda name: f"hello {name}")
    result = registry.execute("greet", {"wrong_arg": "value"})
    assert not is_ok(result)


def test_list_tools():
    registry = ToolRegistry()
    registry.register("tool_a", lambda: None)
    registry.register("tool_b", lambda: None)
    assert "tool_a" in registry.list_tools()
    assert "tool_b" in registry.list_tools()


def test_result_ok():
    from agent.result import ok, err, is_ok, unwrap
    r = ok(42)
    assert is_ok(r)
    assert unwrap(r) == 42


def test_result_err():
    from agent.result import ok, err, is_ok, unwrap
    r = err("something went wrong")
    assert not is_ok(r)
    with pytest.raises(ValueError):
        unwrap(r)
