import ctypes
import os
import platform
import shutil
import socket
import subprocess
from datetime import datetime
from pathlib import Path

from config import expand_path, load_config


def _windows_only() -> None:
    if os.name != "nt":
        raise RuntimeError("device controls must run on Windows")


def get_battery() -> str:
    import psutil
    battery = psutil.sensors_battery()
    if battery is None:
        return "No battery reported."
    state = "charging" if battery.power_plugged else "not charging"
    return f"Battery: {round(battery.percent)}% ({state})."


def take_screenshot() -> str:
    _windows_only()
    from PIL import ImageGrab
    folder = expand_path(load_config()["screenshots_folder"])
    folder.mkdir(parents=True, exist_ok=True)
    target = folder / f"screenshot-{datetime.now():%Y-%m-%d-%H%M%S}.png"
    ImageGrab.grab(all_screens=True).save(target)
    return f"Saved: {target}"


def read_clipboard() -> str:
    import pyperclip
    content = pyperclip.paste()
    return f"Clipboard: {content}" if content else "Clipboard is empty."


def write_clipboard(text: str) -> str:
    import pyperclip
    pyperclip.copy(text)
    return "Copied."


def _volume_controller():
    from pycaw.pycaw import AudioUtilities
    return AudioUtilities.GetSpeakers().EndpointVolume


def set_volume(level: int) -> str:
    _windows_only()
    if not 0 <= level <= 100:
        raise ValueError("volume must be 0-100")
    volume = _volume_controller()
    volume.SetMasterVolumeLevelScalar(level / 100.0, None)
    actual = round(volume.GetMasterVolumeLevelScalar() * 100)
    return f"Volume: {actual}%"


def get_volume() -> str:
    _windows_only()
    level = round(_volume_controller().GetMasterVolumeLevelScalar() * 100)
    return f"Volume: {level}%"


def set_mute(muted: bool) -> str:
    _windows_only()
    _volume_controller().SetMute(1 if muted else 0, None)
    return "Muted." if muted else "Unmuted."


def set_brightness(level: int) -> str:
    _windows_only()
    if not 0 <= level <= 100:
        raise ValueError("brightness must be 0-100")
    import screen_brightness_control as sbc
    sbc.set_brightness(level)
    return f"Brightness: {level}%"


def get_brightness() -> str:
    _windows_only()
    import screen_brightness_control as sbc
    values = sbc.get_brightness()
    return f"Brightness: {round(sum(values) / len(values))}%"


def media_control(action: str) -> str:
    _windows_only()
    import pyautogui
    keys = {"play_pause": "playpause", "next": "nexttrack", "previous": "prevtrack"}
    if action not in keys:
        raise ValueError("unknown media action")
    pyautogui.press(keys[action])
    return {"play_pause": "Play/pause sent.", "next": "Next track.", "previous": "Previous track."}[action]


def get_time() -> str:
    return datetime.now().strftime("%A, %d %B %Y — %I:%M %p")


def get_storage() -> str:
    drive = Path.home().anchor or "/"
    total, used, free = shutil.disk_usage(drive)
    gb = 1024 ** 3
    return f"Storage C: {used / gb:.1f} GB used, {free / gb:.1f} GB free."


def get_system_info() -> str:
    return f"{platform.system()} {platform.release()} | {platform.machine()} | Python {platform.python_version()}"


def get_performance() -> str:
    import psutil
    cpu = psutil.cpu_percent(interval=0.2)
    memory = psutil.virtual_memory()
    return f"CPU: {cpu:.0f}% | RAM: {memory.percent:.0f}% ({memory.available / 1024**3:.1f} GB free)"


def get_network() -> str:
    hostname = socket.gethostname()
    try:
        ip = socket.gethostbyname(hostname)
    except socket.gaierror:
        ip = "unavailable"
    return f"Device: {hostname} | Local IP: {ip}"


def get_wifi() -> str:
    _windows_only()
    result = subprocess.run(["netsh", "wlan", "show", "interfaces"], shell=False,
                            capture_output=True, text=True, timeout=10)
    if result.returncode != 0:
        return "Wi-Fi information unavailable."
    details = {}
    for line in result.stdout.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            if key.strip().lower() in {"state", "ssid", "signal"}:
                details[key.strip()] = value.strip()
    return "Wi-Fi: " + " | ".join(f"{key}: {value}" for key, value in details.items())


def window_control(action: str) -> str:
    _windows_only()
    import pyautogui
    actions = {"desktop": ("win", "d"), "minimize": ("win", "m"),
               "maximize": ("win", "up"), "close_window": ("alt", "f4")}
    if action not in actions:
        raise ValueError("unknown window action")
    pyautogui.hotkey(*actions[action])
    return {"desktop": "Desktop toggled.", "minimize": "Windows minimized.",
            "maximize": "Window maximized.", "close_window": "Window closed."}[action]


def power_action(action: str) -> str:
    _windows_only()
    commands = {"shutdown": ["shutdown", "/s", "/t", "0"],
                "restart": ["shutdown", "/r", "/t", "0"],
                "signout": ["shutdown", "/l"]}
    if action == "sleep":
        ctypes.windll.powrprof.SetSuspendState(False, True, False)
    elif action in commands:
        subprocess.Popen(commands[action], shell=False)
    else:
        raise ValueError("unknown power action")
    return f"Power action started: {action}."


def lock_computer() -> str:
    _windows_only()
    ctypes.windll.user32.LockWorkStation()
    return "Computer locked."
