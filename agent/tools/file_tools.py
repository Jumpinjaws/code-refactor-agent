import os
import shutil
from datetime import datetime


def create_backup(path: str) -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{path}.backup_{timestamp}"
    shutil.copy2(path, backup_path)
    return backup_path


def delete_file(path: str) -> str:
    if not os.path.exists(path):
        return f"File not found: {path}"
    os.remove(path)
    return f"Deleted: {path}"


def list_directory(path: str) -> list[str]:
    if not os.path.isdir(path):
        return []
    return os.listdir(path)


def file_stats(path: str) -> dict:
    if not os.path.exists(path):
        return {"error": f"File not found: {path}"}
    stat = os.stat(path)
    return {
        "path": path,
        "size_bytes": stat.st_size,
        "lines": sum(1 for _ in open(path, "r", encoding="utf-8")),
        "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
    }
