import os
import subprocess
from pathlib import Path

from config import is_allowed_path, load_config


def open_project(project: str) -> str:
    configured = load_config()["projects"].get(project)
    if not configured:
        raise RuntimeError("unknown project alias")
    path = Path(configured)
    if not is_allowed_path(path):
        raise RuntimeError("project path is outside your allowed folders")
    if not path.is_dir():
        raise RuntimeError(f"project folder does not exist: {path}. Update config.json")
    if os.name != "nt":
        raise RuntimeError("project control must be run on Windows")
    subprocess.Popen(["code", str(path)], shell=False, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return f"Opened {project.replace('_', ' ').title()} in VS Code."
