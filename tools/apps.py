import os
import shutil
import subprocess

WINDOWS_APPS = {"calculator": ["calc.exe"], "notepad": ["notepad.exe"], "vscode": ["code"],
                "explorer": ["explorer.exe"], "terminal": ["wt.exe"], "command_prompt": ["cmd.exe"],
                "paint": ["mspaint.exe"], "settings": ["explorer.exe", "ms-settings:"], "task_manager": ["taskmgr.exe"],
                "edge": ["cmd.exe", "/c", "start", "", "microsoft-edge:"], "chrome": ["chrome.exe"],
                "powershell": ["powershell.exe"], "control_panel": ["control.exe"],
                "camera": ["explorer.exe", "microsoft.windows.camera:"],
                "snipping_tool": ["snippingtool.exe"], "clock": ["explorer.exe", "ms-clock:"]}
PROCESS_NAMES = {"calculator": "CalculatorApp.exe", "notepad": "notepad.exe", "vscode": "Code.exe",
                 "explorer": "explorer.exe", "terminal": "WindowsTerminal.exe", "command_prompt": "cmd.exe",
                 "paint": "mspaint.exe", "settings": "SystemSettings.exe", "task_manager": "Taskmgr.exe",
                 "edge": "msedge.exe", "chrome": "chrome.exe", "powershell": "powershell.exe",
                 "control_panel": "control.exe", "camera": "WindowsCamera.exe",
                 "snipping_tool": "SnippingTool.exe", "clock": "Time.exe"}

APP_CANDIDATES = {
    "vscode": [r"%LOCALAPPDATA%\Programs\Microsoft VS Code\Code.exe", r"%PROGRAMFILES%\Microsoft VS Code\Code.exe"],
    "chrome": [r"%PROGRAMFILES%\Google\Chrome\Application\chrome.exe", r"%PROGRAMFILES(X86)%\Google\Chrome\Application\chrome.exe", r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"],
}


def _windows_only() -> None:
    if os.name != "nt":
        raise RuntimeError("device controls must be run on Windows")


def open_app(app: str) -> str:
    _windows_only()
    command = WINDOWS_APPS.get(app.lower().strip())
    if command is None:
        raise RuntimeError(f"'{app}' is not in the approved app list")
    if not shutil.which(command[0]) and app in APP_CANDIDATES:
        installed = next((os.path.expandvars(path) for path in APP_CANDIDATES[app]
                          if os.path.isfile(os.path.expandvars(path))), None)
        if not installed:
            raise RuntimeError(f"{app} is not installed or could not be found")
        command = [installed, *command[1:]]
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
