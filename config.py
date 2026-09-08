import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent


def load_config() -> dict[str, Any]:
    with (ROOT / "config.json").open("r", encoding="utf-8") as file:
        return json.load(file)


def allowed_roots() -> list[Path]:
    return [Path(value).expanduser().resolve() for value in load_config()["allowed_folders"]]


def is_allowed_path(path: Path) -> bool:
    resolved = path.expanduser().resolve()
    return any(resolved == root or root in resolved.parents for root in allowed_roots())
