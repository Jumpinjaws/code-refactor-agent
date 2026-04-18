from openai import OpenAI
from agent.config import settings

client = OpenAI(api_key=settings.openai_api_key)

SYSTEM_PROMPT = """You are an autonomous code refactoring and generation agent.

Given a task, you reason step by step and decide which tool to call next.
Always think before acting. After every tool result, decide whether the task
is complete or if another step is needed.

Available tools:
- read_file(path): read source code from a file
- write_file(path, content): write code to a file
- lint_code(code): check for syntax errors
- format_code(code): auto-format with black
- run_tests(test_dir): run pytest and return results
- list_python_files(directory): list all .py files in a directory
- finish(summary): end the task with a summary

Respond in JSON:
{
  "thought": "your reasoning",
  "tool": "tool_name",
  "args": {"arg1": "value1"}
}
"""


def plan_next_step(task: str, history: list[dict]) -> dict:
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.append({"role": "user", "content": f"Task: {task}"})
    for entry in history:
        messages.append({"role": "assistant", "content": str(entry["agent"])})
        messages.append({"role": "user", "content": f"Tool result: {entry['result']}"})

    response = client.chat.completions.create(
        model=settings.model,
        messages=messages,
        response_format={"type": "json_object"},
        temperature=0,
    )
    import json
    return json.loads(response.choices[0].message.content)
