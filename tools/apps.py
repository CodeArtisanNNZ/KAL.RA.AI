import os
import subprocess

WINDOWS_APPS = {"calculator": ["calc.exe"], "notepad": ["notepad.exe"], "vscode": ["code"],
                "explorer": ["explorer.exe"], "terminal": ["wt.exe"], "command_prompt": ["cmd.exe"],
                "paint": ["mspaint.exe"], "settings": ["explorer.exe", "ms-settings:"], "task_manager": ["taskmgr.exe"],
                "edge": ["cmd.exe", "/c", "start", "", "microsoft-edge:"], "chrome": ["chrome.exe"]}
PROCESS_NAMES = {"calculator": "CalculatorApp.exe", "notepad": "notepad.exe", "vscode": "Code.exe",
                 "explorer": "explorer.exe", "terminal": "WindowsTerminal.exe", "command_prompt": "cmd.exe",
                 "paint": "mspaint.exe", "settings": "SystemSettings.exe", "task_manager": "Taskmgr.exe",
                 "edge": "msedge.exe", "chrome": "chrome.exe"}


def _windows_only() -> None:
    if os.name != "nt":
        raise RuntimeError("device controls must be run on Windows")


def open_app(app: str) -> str:
    _windows_only()
    command = WINDOWS_APPS.get(app.lower().strip())
    if command is None:
        raise RuntimeError(f"'{app}' is not in the approved app list")
    subprocess.Popen(command, shell=False, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return f"Opened {app}."


def close_app(app: str) -> str:
    _windows_only()
    process = PROCESS_NAMES.get(app.lower().strip())
    if process is None:
        raise RuntimeError(f"'{app}' is not in the approved app list")
    result = subprocess.run(["taskkill", "/IM", process, "/T"], shell=False, capture_output=True, text=True, timeout=10)
    if result.returncode != 0:
        raise RuntimeError(f"Windows could not close {app}; it may not be running")
    return f"Closed {app}."
