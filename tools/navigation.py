import os
import webbrowser
from pathlib import Path
from urllib.parse import quote_plus


def open_folder(folder: str) -> str:
    folders = {
        "home": Path.home(), "desktop": Path.home() / "Desktop",
        "documents": Path.home() / "Documents", "downloads": Path.home() / "Downloads",
        "pictures": Path.home() / "Pictures", "videos": Path.home() / "Videos",
        "music": Path.home() / "Music", "recycle": Path("shell:RecycleBinFolder"),
    }
    target = folders.get(folder)
    if target is None:
        raise ValueError("unknown folder")
    if os.name != "nt":
        raise RuntimeError("folder control must run on Windows")
    os.startfile(str(target))  # type: ignore[attr-defined]
    return f"Opened {folder}."


def search_web(query: str) -> str:
    if not query.strip():
        raise ValueError("search cannot be empty")
    webbrowser.open("https://www.google.com/search?q=" + quote_plus(query))
    return f"Searching: {query}"
