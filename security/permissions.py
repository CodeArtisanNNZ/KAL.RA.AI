from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class PermissionDecision:
    allowed: bool
    needs_confirmation: bool = False
    reason: str = ""


class PermissionPolicy:
    ALLOWED_APPS = {"calculator", "notepad", "vscode", "explorer", "terminal", "command_prompt", "paint", "settings", "task_manager", "edge", "chrome"}
    ALLOWED_PROJECTS = {"kishan_bari", "bujhi", "portfolio"}
    SAFE_TOOLS = {"find_file", "open_file", "take_screenshot", "get_battery", "get_volume", "set_volume", "set_mute", "get_brightness", "set_brightness", "media_control", "get_time", "get_storage", "get_system_info", "write_clipboard", "open_website"}
    CONFIRM_TOOLS = {"close_app", "create_folder", "read_clipboard", "lock_computer"}

    def check(self, tool: str, arguments: dict[str, Any], confirmed: bool = False) -> PermissionDecision:
        if tool == "open_app" and arguments.get("app") not in self.ALLOWED_APPS:
            return PermissionDecision(False, reason="That app is not on the allowlist.")
        if tool == "open_project" and arguments.get("project") not in self.ALLOWED_PROJECTS:
            return PermissionDecision(False, reason="That project is not on the allowlist.")
        known = self.SAFE_TOOLS | self.CONFIRM_TOOLS | {"open_app", "open_project"}
        if tool not in known:
            return PermissionDecision(False, reason="That action is not allowed by the security policy.")
        if tool in self.CONFIRM_TOOLS and not confirmed:
            reasons = {"close_app": "this may discard unsaved work", "create_folder": "this will change your filesystem",
                       "read_clipboard": "clipboard contents may contain private information", "lock_computer": "this will lock your Windows session"}
            return PermissionDecision(True, True, reasons[tool])
        return PermissionDecision(True)
