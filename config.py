import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent


def load_config() -> dict[str, Any]:
    with (ROOT / "config.json").open("r", encoding="utf-8") as file:
        return json.load(file)


def allowed_roots() -> list[Path]:
    home = str(Path.home())
    return [Path(value.replace("{HOME}", home)).expanduser().resolve() for value in load_config()["allowed_folders"]]


def expand_path(value: str) -> Path:
    return Path(value.replace("{HOME}", str(Path.home()))).expanduser()


def is_allowed_path(path: Path) -> bool:
    resolved = path.expanduser().resolve()
    return any(resolved == root or root in resolved.parents for root in allowed_roots())
