import os
import re


def search_in_file(path: str, pattern: str) -> list[dict]:
    results = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            for i, line in enumerate(f, 1):
                if re.search(pattern, line):
                    results.append({"line": i, "content": line.rstrip()})
    except Exception as e:
        return [{"error": str(e)}]
    return results


def search_in_directory(directory: str, pattern: str, ext: str = ".py") -> list[dict]:
    matches = []
    for root, _, files in os.walk(directory):
        for fname in files:
            if fname.endswith(ext):
                path = os.path.join(root, fname)
                hits = search_in_file(path, pattern)
                if hits:
                    matches.append({"file": path, "matches": hits})
    return matches


def find_function_definition(directory: str, func_name: str) -> list[dict]:
    pattern = rf"^def {re.escape(func_name)}\s*\("
    return search_in_directory(directory, pattern)


def find_class_definition(directory: str, class_name: str) -> list[dict]:
    pattern = rf"^class {re.escape(class_name)}\s*[:(]"
    return search_in_directory(directory, pattern)
