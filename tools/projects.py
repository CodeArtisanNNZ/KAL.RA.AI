import os
import subprocess
from pathlib import Path

from config import expand_path, is_allowed_path, load_config


def open_project(project: str) -> str:
    config = load_config()
    configured = config["projects"].get(project)
    path = expand_path(configured) if configured else _discover_project(project, config)
    if not is_allowed_path(path):
        raise RuntimeError("project path is outside your allowed folders")
    if not path.is_dir():
        raise RuntimeError(f"project folder does not exist: {path}. Update config.json")
    if os.name != "nt":
        raise RuntimeError("project control must be run on Windows")
    subprocess.Popen(["code", str(path)], shell=False, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return f"Opened {project.replace('_', ' ').title()} in VS Code."


def _discover_project(project: str, config: dict) -> Path:
    names = {
        "kishan_bari": {"kishan-bari", "kishan", ".kishan"},
        "bujhi": {"bujhi"},
        "portfolio": {"portfolio", "personal-portfolio"},
    }[project]
    for raw_root in config["project_search_folders"]:
        root = expand_path(raw_root)
        if not root.is_dir():
            continue
        for candidate in root.glob("*"):
            if candidate.is_dir() and candidate.name.lower() in names:
                return candidate
    raise RuntimeError(f"Could not find {project.replace('_', ' ')}. Add its path in config.json")
