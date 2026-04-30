# Autonomous Code Generation and Refactoring Agent

An autonomous agent that reads, analyzes, refactors, and generates Python code using an LLM-powered plan-and-execute loop. The agent reasons step by step, selects tools, and iterates until the task is complete.

## Architecture

```
User Task (natural language)
        |
        v
   Planner (GPT-4o)
   - reasons about next step
   - selects tool + args
        |
        v
   Executor
   - calls the selected tool
   - returns result to planner
        |
        v
   Loop (up to N iterations)
   - continues until "finish" tool is called
   - builds history of thought + result pairs
```

## Tools Available to the Agent

| Tool | What it does |
|------|-------------|
| read_file | Read source code from a file |
| write_file | Write generated/refactored code to a file |
| lint_code | Check syntax validity using AST |
| format_code | Auto-format code using Black |
| run_tests | Run pytest and return pass/fail |
| list_python_files | List all .py files in a directory |
| finish | End the loop with a summary |

## Setup

```bash
git clone https://github.com/Jumpinjaws/code-refactor-agent
cd code-refactor-agent
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Add your OPENAI_API_KEY to .env
```

## Run

Refactor a file:
```bash
python main.py --task "Read examples/sample_bad_code.py, refactor it to follow PEP8, add type hints, and write the result to output/refactored.py"
```

Generate new code:
```bash
python main.py --task "Generate a Python function that validates email addresses using regex and write it to output/email_validator.py"
```

## Run Tests

```bash
pytest tests/ -v
```

## Tech Stack

- Python 3.11
- OpenAI GPT-4o (plan-and-execute loop)
- Black (code formatting)
- AST (syntax validation)
- pytest
