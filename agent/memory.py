from collections import deque


class AgentMemory:
    """Stores recent agent steps for context window management."""

    def __init__(self, max_steps: int = 20):
        self._history = deque(maxlen=max_steps)

    def add(self, thought: str, tool: str, args: dict, result) -> None:
        self._history.append({
            "thought": thought,
            "tool": tool,
            "args": args,
            "result": result,
        })

    def get_all(self) -> list[dict]:
        return list(self._history)

    def clear(self) -> None:
        self._history.clear()

    def __len__(self) -> int:
        return len(self._history)
