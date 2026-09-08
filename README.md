# KAL.RA AI v0.5 — Universal Windows + Local Memory

KAL.RA automatically detects the current Windows username and standard folders.
It has no hard-coded `C:\Users\name` path. VS Code and Chrome are detected from
common installation locations, and known projects are searched for safely.

> Universal means Windows 10/11 computers. Hardware-specific features such as
> brightness may still depend on the laptop driver and display.

## Install and start

Extract the ZIP, open the extracted folder in Terminal, then run:

```powershell
python -m pip install -r requirements.txt
python app.py
```

## Compact command list

```text
APPS
calc | note | code | files | terminal | cmd | powershell
paint | settings | tasks | edge | chrome | camera | snip | clock | control

PROJECTS
kishan | bujhi | portfolio

FOLDERS
home | desktop folder | documents | downloads | pictures | videos | music | recycle

SYSTEM
shot | battery | volume | vol 40 | mute | unmute
brightness | bright 50 | time | storage | system | cpu | ram | wifi | ip

MEDIA AND WINDOWS
play | pause | next | prev
desktop | minimize | maximize | close window

POWER (confirmation required)
lock | sleep | restart | shutdown | sign out

WEB
youtube | github | gmail | google
google soil testing bangladesh

FILES
find CSE 330
file C:\path\note.pdf
folder Research

CLIPBOARD
copy hello
paste

MEMORY
remember my favorite browser is Chrome
what is my favorite browser
memories
forget my favorite browser
```

Use `help`, `commands`, or `?` inside KAL.RA to show the list.

## Universal configuration

`{HOME}` in `config.json` becomes the current user's Windows home automatically.
KAL.RA searches Desktop, Documents, Downloads, and `D:\Projects` for the known
project names. If a project uses a different name or location, put its full path
in the relevant `projects` value.

## Safety

The assistant uses a fixed tool allowlist. It does not accept arbitrary shell
commands, delete files, install software, reveal passwords, or edit the Registry.
Closing windows and power commands require confirmation because unsaved work can
be lost.

Personal memory is stored locally in `memory/assistant.db` using SQLite. The
database is ignored by Git, so private memories are not uploaded to GitHub.

## Test

```powershell
python -m unittest discover -s tests -v
```
