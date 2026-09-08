import re
from dataclasses import dataclass
from typing import Any, Callable

from security.permissions import PermissionPolicy
from tools.apps import close_app, open_app
from tools.files import create_folder, find_file, open_file
from tools.navigation import open_folder, search_web
from tools.memory_tools import forget, list_memories, recall, remember
from tools.projects import open_project
from tools.system import (
    get_battery, get_brightness, get_storage, get_system_info, get_time,
    get_volume, lock_computer, media_control, read_clipboard, set_brightness,
    set_mute, set_volume, take_screenshot, write_clipboard, get_performance,
    get_network, get_wifi, window_control, power_action,
)
from tools.websites import open_website


@dataclass(frozen=True)
class ToolCall:
    name: str
    arguments: dict[str, Any]


class KalraBrain:
    def __init__(self) -> None:
        self.policy = PermissionPolicy()
        self.pending: ToolCall | None = None
        self.tools: dict[str, Callable[..., str]] = {
            "open_app": open_app, "close_app": close_app, "open_project": open_project,
            "find_file": find_file, "open_file": open_file, "create_folder": create_folder,
            "take_screenshot": take_screenshot, "get_battery": get_battery,
            "get_volume": get_volume, "set_volume": set_volume, "set_mute": set_mute,
            "get_brightness": get_brightness, "set_brightness": set_brightness,
            "media_control": media_control, "get_time": get_time, "get_storage": get_storage,
            "get_system_info": get_system_info, "read_clipboard": read_clipboard,
            "write_clipboard": write_clipboard, "lock_computer": lock_computer,
            "open_website": open_website,
            "open_folder": open_folder, "search_web": search_web,
            "get_performance": get_performance, "get_network": get_network,
            "get_wifi": get_wifi, "window_control": window_control,
            "power_action": power_action,
            "remember": remember, "recall": recall,
            "list_memories": list_memories, "forget": forget,
        }

    @staticmethod
    def _clean(message: str) -> str:
        return " ".join(message.lower().strip().rstrip(".!?").split())

    def understand(self, message: str) -> ToolCall | None:
        text = self._clean(message)

        remember_match = re.fullmatch(r"remember (?:that )?(.+?) is (.+)", text)
        if remember_match:
            return ToolCall("remember", {
                "key": remember_match.group(1).strip(),
                "value": remember_match.group(2).strip(),
            })
        forget_match = re.fullmatch(r"forget (?:my )?(.+)", text)
        if forget_match:
            return ToolCall("forget", {"key": forget_match.group(1).strip()})
        recall_match = re.fullmatch(r"(?:what is|recall) (?:my )?(.+)", text)
        if recall_match:
            return ToolCall("recall", {"key": recall_match.group(1).strip()})

        short_exact = {
            "shot": ToolCall("take_screenshot", {}), "screenshot": ToolCall("take_screenshot", {}),
            "battery": ToolCall("get_battery", {}), "volume": ToolCall("get_volume", {}),
            "mute": ToolCall("set_mute", {"muted": True}), "unmute": ToolCall("set_mute", {"muted": False}),
            "brightness": ToolCall("get_brightness", {}), "time": ToolCall("get_time", {}),
            "date": ToolCall("get_time", {}), "storage": ToolCall("get_storage", {}),
            "system": ToolCall("get_system_info", {}), "info": ToolCall("get_system_info", {}),
            "performance": ToolCall("get_performance", {}), "cpu": ToolCall("get_performance", {}),
            "ram": ToolCall("get_performance", {}), "network": ToolCall("get_network", {}),
            "ip": ToolCall("get_network", {}), "wifi": ToolCall("get_wifi", {}),
            "paste": ToolCall("read_clipboard", {}), "clipboard": ToolCall("read_clipboard", {}),
            "lock": ToolCall("lock_computer", {}), "play": ToolCall("media_control", {"action": "play_pause"}),
            "pause": ToolCall("media_control", {"action": "play_pause"}), "next": ToolCall("media_control", {"action": "next"}),
            "previous": ToolCall("media_control", {"action": "previous"}), "prev": ToolCall("media_control", {"action": "previous"}),
            "desktop": ToolCall("window_control", {"action": "desktop"}),
            "minimize": ToolCall("window_control", {"action": "minimize"}),
            "maximize": ToolCall("window_control", {"action": "maximize"}),
            "close window": ToolCall("window_control", {"action": "close_window"}),
            "shutdown": ToolCall("power_action", {"action": "shutdown"}),
            "restart": ToolCall("power_action", {"action": "restart"}),
            "sleep": ToolCall("power_action", {"action": "sleep"}),
            "sign out": ToolCall("power_action", {"action": "signout"}),
            "memories": ToolCall("list_memories", {}),
            "memory": ToolCall("list_memories", {}),
        }
        if text in short_exact:
            return short_exact[text]


        number = re.fullmatch(r"(?:vol|volume)\s+(\d{1,3})%?", text)
        if number:
            return ToolCall("set_volume", {"level": int(number.group(1))})
        number = re.fullmatch(r"(?:bright|brightness)\s+(\d{1,3})%?", text)
        if number:
            return ToolCall("set_brightness", {"level": int(number.group(1))})
        volume = re.search(r"(?:set|change|turn) (?:the )?volume (?:to )?(\d{1,3})", text)
        if volume:
            return ToolCall("set_volume", {"level": int(volume.group(1))})
        bright = re.search(r"(?:set|change|turn) (?:the )?brightness (?:to )?(\d{1,3})", text)
        if bright:
            return ToolCall("set_brightness", {"level": int(bright.group(1))})
        if "battery" in text:
            return ToolCall("get_battery", {})
        if "screenshot" in text or "screen shot" in text:
            return ToolCall("take_screenshot", {})
        if "read clipboard" in text or "what is in my clipboard" in text:
            return ToolCall("read_clipboard", {})
        clipboard = re.match(r"(?:copy|clip)\s+(.+)", text)
        if clipboard:
            return ToolCall("write_clipboard", {"text": clipboard.group(1)})
        if "lock" in text and any(x in text for x in ("computer", "laptop", "pc", "screen")):
            return ToolCall("lock_computer", {})

        folder = re.match(r"(?:new folder|folder|mkdir)(?: named| called)?\s+(.+)", text)
        if folder:
            return ToolCall("create_folder", {"name": folder.group(1).strip("\"'")})
        file_search = re.match(r"(?:find|search|locate)\s+(?:my\s+)?(.+?)(?:\s+file|\s+notes)?$", text)
        if file_search:
            return ToolCall("find_file", {"query": file_search.group(1)})
        file_open = re.match(r"(?:open file|file)\s+(.+)", text)
        if file_open:
            return ToolCall("open_file", {"path": file_open.group(1).strip("\"'")})

        web_search = re.match(r"(?:search web|web search|google)\s+(.+)", text)
        if web_search:
            return ToolCall("search_web", {"query": web_search.group(1)})

        folders = {"home": "home", "desktop folder": "desktop", "documents": "documents",
                   "downloads": "downloads", "pictures": "pictures", "videos": "videos",
                   "music": "music", "recycle": "recycle", "recycle bin": "recycle"}
        if text in folders:
            return ToolCall("open_folder", {"folder": folders[text]})

        projects = {"kishan bari": "kishan_bari", "kishan": "kishan_bari", "soil": "kishan_bari",
                    "bujhi": "bujhi", "education": "bujhi", "portfolio": "portfolio"}
        if text in projects:
            return ToolCall("open_project", {"project": projects[text]})
        if any(word in text for word in ("open", "work on", "coding mode")):
            for phrase, project in projects.items():
                if phrase in text:
                    return ToolCall("open_project", {"project": project})

        websites = {"youtube": "youtube", "github": "github", "git": "github", "gmail": "gmail", "google": "google"}
        if text in websites:
            return ToolCall("open_website", {"website": websites[text]})
        if text.startswith("open "):
            site = text.removeprefix("open ")
            if site in websites:
                return ToolCall("open_website", {"website": websites[site]})

        apps = {"calc": "calculator", "calculator": "calculator", "note": "notepad", "notepad": "notepad",
                "code": "vscode", "vscode": "vscode", "vs code": "vscode", "files": "explorer",
                "explorer": "explorer", "terminal": "terminal", "cmd": "command_prompt", "paint": "paint",
                "settings": "settings", "tasks": "task_manager", "task manager": "task_manager",
                "edge": "edge", "chrome": "chrome", "powershell": "powershell",
                "control": "control_panel", "camera": "camera", "snip": "snipping_tool",
                "clock": "clock"}
        if text in apps:
            return ToolCall("open_app", {"app": apps[text]})
        action_open = any(re.search(rf"\b{x}\b", text) for x in ("open", "launch", "start", "run"))
        action_close = any(re.search(rf"\b{x}\b", text) for x in ("close", "stop", "quit"))
        for phrase in sorted(apps, key=len, reverse=True):
            if phrase in text:
                if action_close:
                    return ToolCall("close_app", {"app": apps[phrase]})
                if action_open:
                    return ToolCall("open_app", {"app": apps[phrase]})
        return None

    def execute(self, call: ToolCall, confirmed: bool = False) -> str:
        decision = self.policy.check(call.name, call.arguments, confirmed)
        if not decision.allowed:
            return decision.reason
        if decision.needs_confirmation:
            self.pending = call
            return f"Confirmation required: {decision.reason}. YES or NO?"
        tool = self.tools.get(call.name)
        if tool is None:
            return f"Tool '{call.name}' is not installed."
        try:
            return tool(**call.arguments)
        except Exception as error:
            return f"Action failed: {type(error).__name__}: {error}"

    def handle(self, message: str) -> str:
        answer = self._clean(message)
        if self.pending:
            call, self.pending = self.pending, None
            return self.execute(call, confirmed=True) if answer in {"yes", "y", "confirm"} else "Action cancelled."
        if answer in {"help", "commands", "?"}:
            return HELP_TEXT
        call = self.understand(message)
        return self.execute(call) if call else "Not understood. Type help."


HELP_TEXT = """QUICK COMMANDS
Apps: calc | note | code | files | terminal | cmd | powershell | paint | settings | tasks | edge | chrome | camera | snip | clock | control
Projects: kishan | bujhi | portfolio
Folders: desktop | documents | downloads | pictures | videos | music | recycle
System: shot | battery | volume | vol 40 | mute | unmute | bright 50 | time | storage | system | cpu | ram | wifi | ip | lock
Media: play | pause | next | prev
Windows: desktop | minimize | maximize | close window
Power: sleep | restart | shutdown | sign out (confirmation required)
Web: youtube | github | gmail | google
Memory: remember my browser is Chrome | what is my browser | memories | forget my browser
Search: google soil testing bangladesh
Files: find CSE 330 | file D:\\path\\note.pdf | folder Research
Clipboard: copy hello | paste"""
