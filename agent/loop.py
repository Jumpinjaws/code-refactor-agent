from agent.planner import plan_next_step
from agent.executor import execute
from agent.config import settings


def run(task: str) -> str:
    history = []
    print(f"\n[agent] Task: {task}\n")

    for step in range(settings.max_iterations):
        decision = plan_next_step(task, history)
        tool = decision.get("tool")
        args = decision.get("args", {})
        thought = decision.get("thought", "")

        print(f"[step {step + 1}] Thought: {thought}")
        print(f"[step {step + 1}] Tool: {tool} | Args: {args}")

        result = execute(tool, args)
        print(f"[step {step + 1}] Result: {result}\n")

        history.append({"agent": decision, "result": result})

        if tool == "finish" or (isinstance(result, dict) and result.get("status") == "finished"):
            return result.get("summary", "Task complete.")

    return "Max iterations reached."
