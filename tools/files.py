import os
from pathlib import Path

from config import allowed_roots, is_allowed_path


def find_file(query: str, limit: int = 10) -> str:
    words = [word.lower() for word in query.split() if word]
    if not words:
        raise ValueError("search text cannot be empty")
    matches: list[str] = []
    for root in allowed_roots():
        if not root.exists():
            continue
        for current, directories, files in os.walk(root):
            directories[:] = [d for d in directories if not d.startswith(".") and d not in {"node_modules", ".git", "venv", ".venv"}]
            for name in files:
                if all(word in name.lower() for word in words):
                    matches.append(str(Path(current) / name))
                    if len(matches) >= limit:
                        return "Found:\n" + "\n".join(matches)
    return "Found:\n" + "\n".join(matches) if matches else f"No file matching '{query}' was found in allowed folders."


def open_file(path: str) -> str:
    candidate = Path(path)
    if not is_allowed_path(candidate):
        raise RuntimeError("that path is outside your allowed folders")
    if not candidate.is_file():
        raise RuntimeError("the file does not exist")
    if os.name != "nt":
        raise RuntimeError("file opening must be run on Windows")
    os.startfile(candidate)  # type: ignore[attr-defined]
    return f"Opened {candidate.name}."


def create_folder(name: str) -> str:
    if any(char in name for char in '<>:"/\\|?*') or name in {".", ".."}:
        raise ValueError("the folder name contains invalid characters")
    destination = allowed_roots()[0] / name
    if not is_allowed_path(destination):
        raise RuntimeError("the folder would be outside your allowed folders")
    destination.mkdir(exist_ok=False)
    return f"Created {destination}."
