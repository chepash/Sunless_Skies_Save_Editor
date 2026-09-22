# Sunless Skies Save Editor
Python-based save editor for Sunless Skies.

# Usage
Use it with reference to [1410c's save guide](https://steamcommunity.com/sharedfiles/filedetails/?id=1456294858) on Steam Forums.

Always backup your save files prior to modification.

- **Open Game Save** finds the most recently played character in your default
  Sunless Skies save folder and opens it directly, no file dialog needed. It
  offers to back up the whole save folder (all characters) to a timestamped
  zip in `SaveEditorBackups/` before opening.
- **Save** overwrites the currently loaded file directly and briefly shows a
  green "Saved" confirmation. Use **Save As...** to save to a different file
  or location instead.
- The editor also remembers and reopens your last-used save file on startup.

# Installation
## Prebuilt executable
The easiest way to get started is to download the latest executable from the
[releases](https://github.com/markossipow/Sunless_Skies_Save_Editor/releases) page.

## Running from source
Requires **Python 3.8+**.

```sh
python -m pip install -r requirements.txt
python __main__.py
```

The editor looks for save files in the default Sunless Skies location for your
platform and opens an "Open" dialog there; you can browse to any other location.

| Platform | Default save folder |
| --- | --- |
| Windows | `%USERPROFILE%\AppData\LocalLow\Failbetter Games\Sunless Skies\storage\characterrepository` |
| macOS | `~/Library/Application Support/unity.Failbetter Games.Sunless Skies/storage/characterrepository` |
| Linux | `$XDG_DATA_HOME/unity.Failbetter Games.Sunless Skies/storage/characterrepository` |

# Building an executable
Development/build dependencies are listed in `requirements-dev.txt`:

```sh
python -m pip install -r requirements-dev.txt
```

Then build the standalone application with the bundled PyInstaller spec:

```sh
pyinstaller sunless_skies_editor.spec --noconfirm --clean
```

The result appears in `dist/SunlessSkiesSaveEditor/`. Ship the whole folder —
`SunlessSkiesSaveEditor.exe` needs the files next to it. Use `--onedir` (the
spec's default) for fast startup; a single-file build is possible but slower to
launch.

# Regenerating the UI
The files in `Windows/` are **generated** from the `.ui` design files in
`Qt Designer UI/` by PyQt5's UI compiler. Edit the `.ui` files (e.g. with Qt
Designer), then run:

```
Qt Designer UI\generate.bat
```

You can also invoke the compiler directly:

```sh
python -m PyQt5.uic.pyuic "Qt Designer UI/sunless_skies.ui" -o "Windows/main_window.py"
python -m PyQt5.uic.pyuic "Qt Designer UI/cargo_dialog.ui"  -o "Windows/cargo_dialog.py"
python -m PyQt5.uic.pyuic "Qt Designer UI/about_window.ui"  -o "Windows/about_window.py"
```

> Do not edit the files under `Windows/` by hand — they are overwritten the next
time the UI is regenerated.
