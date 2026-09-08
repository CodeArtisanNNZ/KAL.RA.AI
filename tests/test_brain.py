import unittest
from unittest.mock import Mock

from brain import KalraBrain, ToolCall


class BrainTests(unittest.TestCase):
    def setUp(self) -> None:
        self.brain = KalraBrain()

    def assert_command(self, text: str, tool: str, arguments: dict) -> None:
        self.assertEqual(self.brain.understand(text), ToolCall(tool, arguments))

    def test_apps(self) -> None:
        self.assert_command("open calculator", "open_app", {"app": "calculator"})
        self.assert_command("Can you launch VS Code?", "open_app", {"app": "vscode"})
        self.assert_command("calc", "open_app", {"app": "calculator"})
        self.assert_command("code", "open_app", {"app": "vscode"})

    def test_projects(self) -> None:
        self.assert_command("I want to work on Kishan", "open_project", {"project": "kishan_bari"})
        self.assert_command("open my portfolio", "open_project", {"project": "portfolio"})

    def test_system_tools(self) -> None:
        self.assert_command("set volume to 40%", "set_volume", {"level": 40})
        self.assert_command("check my battery", "get_battery", {})
        self.assert_command("take a screenshot", "take_screenshot", {})
        self.assert_command("vol 40", "set_volume", {"level": 40})
        self.assert_command("bright 50", "set_brightness", {"level": 50})
        self.assert_command("next", "media_control", {"action": "next"})
        self.assert_command("cpu", "get_performance", {})
        self.assert_command("wifi", "get_wifi", {})
        self.assert_command("shutdown", "power_action", {"action": "shutdown"})

    def test_navigation(self) -> None:
        self.assert_command("downloads", "open_folder", {"folder": "downloads"})
        self.assert_command("google windows shortcuts", "search_web", {"query": "windows shortcuts"})

    def test_power_requires_confirmation(self) -> None:
        first = self.brain.handle("restart")
        self.assertIn("Confirmation required", first)
        self.assertEqual(self.brain.handle("no"), "Action cancelled.")

    def test_memory_commands(self) -> None:
        self.assert_command(
            "remember my favorite browser is Chrome",
            "remember",
            {"key": "my favorite browser", "value": "chrome"},
        )
        self.assert_command(
            "what is my favorite browser",
            "recall",
            {"key": "favorite browser"},
        )
        self.assert_command("memories", "list_memories", {})
        self.assert_command("forget my favorite browser", "forget", {"key": "favorite browser"})

    def test_git_alias(self) -> None:
        self.assert_command("git", "open_website", {"website": "github"})

    def test_file_search(self) -> None:
        self.assert_command("find my CSE 330 notes", "find_file", {"query": "cse 330"})

    def test_unknown_tool_is_denied(self) -> None:
        result = self.brain.execute(ToolCall("terminal_command", {"command": "format c:"}))
        self.assertIn("not allowed", result)

    def test_confirmation_then_execution(self) -> None:
        fake = Mock(return_value="Closed notepad.")
        self.brain.tools["close_app"] = fake
        first = self.brain.handle("close notepad")
        self.assertIn("Confirmation required", first)
        self.assertEqual(self.brain.handle("yes"), "Closed notepad.")
        fake.assert_called_once_with(app="notepad")

    def test_confirmation_can_be_cancelled(self) -> None:
        self.brain.handle("lock my computer")
        self.assertEqual(self.brain.handle("no"), "Action cancelled.")


if __name__ == "__main__":
    unittest.main()
