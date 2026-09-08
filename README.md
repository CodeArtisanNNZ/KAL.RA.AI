# KAL.RA AI v0.3

Private, personal and local Windows assistant with short commands.

## Start

Open this folder in Terminal and run:

```powershell
python -m pip install -r requirements.txt
python app.py
```

The included configuration already uses the Windows username `nusai`.
Project folders still use `D:\Projects`; change those three paths in
`config.json` if your projects are stored elsewhere.

## Quick commands

```text
APPS
calc            Calculator
note            Notepad
code            VS Code
files           File Explorer
terminal        Windows Terminal
cmd             Command Prompt
paint           Paint
settings        Windows Settings
tasks           Task Manager
edge            Microsoft Edge
chrome          Google Chrome

PROJECTS
kishan          Open Kishan Bari in VS Code
bujhi           Open Bujhi in VS Code
portfolio       Open Portfolio in VS Code

SYSTEM
shot            Take screenshot
battery         Battery percentage
volume          Current volume
vol 40          Set volume to 40%
mute            Mute sound
unmute          Unmute sound
brightness      Current brightness
bright 50       Set brightness to 50%
time            Current date and time
storage         C drive storage
system          Windows and Python information
lock            Lock computer (asks first)

MEDIA
play            Play or pause
pause           Play or pause
next            Next track
prev            Previous track

WEBSITES
youtube         Open YouTube
github          Open GitHub
gmail           Open Gmail
google          Open Google

FILES AND CLIPBOARD
find CSE 330    Find matching files
file D:\path\note.pdf
folder Research Create a folder (asks first)
copy hello      Copy "hello"
paste           Read clipboard (asks first)
```

Type `help` inside KAL.RA to display this compact command guide.

## Safety boundary

KAL.RA only executes registered tools. It cannot delete files, reveal passwords,
edit the Registry, install software, or run arbitrary text as terminal code.
File operations are limited to folders listed in `config.json`.

## Tests

```powershell
python -m unittest discover -s tests -v
```
