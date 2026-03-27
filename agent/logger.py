import os
import json
from datetime import datetime


class AgentLogger:
    def __init__(self, log_dir: str = "output"):
        os.makedirs(log_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_path = os.path.join(log_dir, f"run_{timestamp}.jsonl")

    def log(self, step: int, thought: str, tool: str, args: dict, result) -> None:
        entry = {
            "step": step,
            "timestamp": datetime.now().isoformat(),
            "thought": thought,
            "tool": tool,
            "args": args,
            "result": str(result)[:500],
        }
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")

    def get_log_path(self) -> str:
        return self.log_path
