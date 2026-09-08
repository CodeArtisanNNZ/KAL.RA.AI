import ctypes
import os
import platform
import shutil
from datetime import datetime
from pathlib import Path

from config import load_config


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
    folder = Path(load_config()["screenshots_folder"])
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


def lock_computer() -> str:
    _windows_only()
    ctypes.windll.user32.LockWorkStation()
    return "Computer locked."
