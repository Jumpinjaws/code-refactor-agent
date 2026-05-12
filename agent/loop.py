from agent.planner import plan_next_step
from agent.registry import ToolRegistry, build_default_registry
from agent.memory import AgentMemory
from agent.logger import AgentLogger
from agent.result import is_ok
from agent.config import settings


def run(task: str, registry: ToolRegistry = None) -> str:
    if registry is None:
        registry = build_default_registry()

    memory = AgentMemory(max_steps=settings.max_iterations)
    logger = AgentLogger(log_dir=settings.output_dir)

    print(f"\n[agent] Task: {task}")
    print(f"[agent] Available tools: {registry.list_tools()}\n")

    for step in range(settings.max_iterations):
        decision = plan_next_step(task, memory.get_all(), registry.list_tools())
        tool = decision.get("tool")
        args = decision.get("args", {})
        thought = decision.get("thought", "")

        print(f"[step {step + 1}] Thought: {thought}")
        print(f"[step {step + 1}] Tool: {tool} | Args: {args}")

        result = registry.execute(tool, args)
        logger.log(step + 1, thought, tool, args, result)

        if is_ok(result):
            value = result.value
            print(f"[step {step + 1}] Result: {value}\n")
            memory.add(thought, tool, args, value)

            if tool == "finish" or (isinstance(value, dict) and value.get("status") == "finished"):
                return value.get("summary", "Task complete.")
        else:
            print(f"[step {step + 1}] Error: {result.error}\n")
            memory.add(thought, tool, args, {"error": result.error})

    return "Max iterations reached."
