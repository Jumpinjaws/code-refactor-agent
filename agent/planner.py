import json
from openai import OpenAI
from agent.config import settings

client = OpenAI(api_key=settings.openai_api_key)

SYSTEM_PROMPT_TEMPLATE = """You are an autonomous code refactoring and generation agent.

Given a task, you reason step by step and decide which tool to call next.
Always think before acting. After every tool result, decide whether the task
is complete or if another step is needed.

Available tools: {tool_list}

Also available: finish(summary) — call this to end the task.

Respond in JSON:
{{
  "thought": "your reasoning",
  "tool": "tool_name",
  "args": {{"arg1": "value1"}}
}}
"""


def plan_next_step(task: str, history: list[dict], tool_list: list[str]) -> dict:
    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(tool_list=", ".join(tool_list))
    messages = [{"role": "system", "content": system_prompt}]
    messages.append({"role": "user", "content": f"Task: {task}"})

    for entry in history:
        messages.append({"role": "assistant", "content": json.dumps(entry)})
        messages.append({"role": "user", "content": f"Result: {entry.get('result', '')}"})

    response = client.chat.completions.create(
        model=settings.model,
        messages=messages,
        response_format={"type": "json_object"},
        temperature=0,
    )
    return json.loads(response.choices[0].message.content)
