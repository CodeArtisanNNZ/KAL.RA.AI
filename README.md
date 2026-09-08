# KAL.RA AI

**A private, personal and local desktop assistant for Windows.**

KAL.RA AI is an open-source Python project that lets you control common Windows functions using short text commands. It can open applications, manage media, search for files, open coding projects, control volume and brightness, take screenshots, check system information and perform approved Windows actions.

It is designed for people searching for a:

* Local AI assistant for Windows
* Offline desktop assistant
* Python computer-control project
* Private alternative to cloud assistants
* Text-based personal assistant
* Safe Windows automation tool

KAL.RA currently uses a deterministic command router rather than a full language model. This makes its actions predictable and prevents user messages from being executed directly as terminal commands. A local language model can be connected in a future version through the existing permission-controlled tool system.

## Why KAL.RA?

Most personal assistants depend heavily on cloud services and send requests to external servers. KAL.RA is designed to work mainly on your own computer.

The assistant does not receive unrestricted access to your system. It can only use explicitly approved tools, and sensitive actions require confirmation.

## Features

* Automatically detects the current Windows username
* Opens common Windows applications
* Opens VS Code and coding projects
* Searches allowed folders for files
* Opens Documents, Downloads, Pictures and other folders
* Controls system volume, mute and brightness
* Controls music and video playback
* Takes and saves screenshots
* Reads battery, storage, CPU, RAM, Wi-Fi and IP information
* Opens approved websites
* Performs Google searches
* Reads and writes clipboard text
* Minimizes or maximizes windows
* Supports sleep, restart, shutdown and sign-out with confirmation
* Restricts file access to configured folders
* Rejects unknown or unapproved tools

## Requirements

* Windows 10 or Windows 11
* Python 3.10 or newer
* Internet connection only for installing the required Python packages
* Internet connection is not required for the main local system-control commands

## Installation

### 1. Download KAL.RA

Download the latest ZIP from the repository and extract it.

You can also clone the repository:

```powershell
git clone https://github.com/CodeArtisanNNZ/KAL-RA-AI.git
cd KAL-RA-AI
```

### 2. Open the project folder

Open the extracted folder in File Explorer.

Click the File Explorer address bar, type:

```text
cmd
```

Press Enter.

### 3. Install the requirements

Run:

```powershell
python -m pip install -r requirements.txt
```

### 4. Start KAL.RA

Run:

```powershell
python app.py
```

Type:

```text
help
```

KAL.RA will show the available commands.

## Quick Commands

### Applications

```text
calc
note
code
files
terminal
cmd
powershell
paint
settings
tasks
edge
chrome
camera
snip
clock
control
```

### Projects

```text
kishan
bujhi
portfolio
```

Project paths can be added manually inside `config.json`. If a path is empty, KAL.RA searches common safe folders for a matching project folder.

### Folders

```text
home
desktop folder
documents
downloads
pictures
videos
music
recycle
```

### System controls

```text
shot
battery
volume
vol 40
mute
unmute
brightness
bright 50
time
storage
system
cpu
ram
wifi
ip
```

### Media controls

```text
play
pause
next
prev
```

### Window controls

```text
desktop
minimize
maximize
close window
```

### Websites and search

```text
youtube
github
gmail
google
google soil testing bangladesh
```

### Files and clipboard

```text
find CSE 330
file C:\path\to\note.pdf
folder Research
copy hello
paste
```

### Power controls

These commands require confirmation:

```text
lock
sleep
restart
shutdown
sign out
```

## Configuration

KAL.RA uses `{HOME}` inside `config.json`.

At runtime, `{HOME}` is automatically converted to the current Windows user folder.

For example:

```text
{HOME}\Downloads
```

becomes:

```text
C:\Users\CurrentUser\Downloads
```

This means users do not need to edit the code or enter their Windows username.

You can add project locations inside `config.json`:

```json
"projects": {
  "kishan_bari": "D:\\Projects\\kishan-bari",
  "bujhi": "D:\\Projects\\bujhi",
  "portfolio": "D:\\Projects\\portfolio"
}
```

Use two backslashes inside JSON paths.

## Safety

KAL.RA does not give natural-language messages direct access to PowerShell, Command Prompt or arbitrary Python execution.

Every action follows this process:

```text
User message
→ Command router
→ Approved tool
→ Permission check
→ Optional confirmation
→ Windows action
→ Result
```

KAL.RA intentionally does not support:

* Arbitrary terminal commands
* Password extraction
* Browser-password access
* Registry modification
* Unrestricted file deletion
* Silent software installation
* Security bypasses

## Run the Tests

```powershell
python -m unittest discover -s tests -v
```

## Current Limitation

KAL.RA is currently a Windows text-command assistant with deterministic language matching. It is not yet powered by a full local language model, so unsupported natural-language sentences may not be understood.

Future versions can add:

* Local language-model integration
* SQLite personal memory
* Multiple actions from one request
* Custom commands and app registration
* Voice control
* Android connection
* A graphical chat interface

## Privacy

KAL.RA is designed to run locally. Standard device-control commands do not need an online AI API, cloud database, user account or external authentication.

## Contributing

Bug reports, feature suggestions and pull requests are welcome.

If you add a new computer-control feature, it should:

1. Be implemented as a separate tool.
2. Validate all arguments.
3. Avoid unrestricted shell execution.
4. Require confirmation for risky actions.
5. Be included in the permission allowlist.
6. Include automated tests.

## License

Add an open-source license before public distribution. The MIT License is a practical choice if you want others to use, modify and distribute the project while keeping your copyright notice.

---

**KAL.RA AI — Private. Personal. Local.**
