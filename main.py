import argparse
from dotenv import load_dotenv
from agent.loop import run

load_dotenv()


def main():
    parser = argparse.ArgumentParser(description="Autonomous Code Refactoring Agent")
    parser.add_argument("--task", required=True, help="Natural language task description")
    args = parser.parse_args()
    summary = run(args.task)
    print(f"\n[agent] Done: {summary}")


if __name__ == "__main__":
    main()
