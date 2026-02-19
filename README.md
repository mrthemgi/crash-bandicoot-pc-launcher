# 🚀 Crash Bandicoot PC Launcher

> A custom Python-based PC launcher for *Crash of the Titans* and *Mind Over Mutant*, inspired by official game launchers (like Activision’s Crash Bandicoot launchers).

---

## 📌 About

This project provides a **Crash Bandicoot PC Launcher** built in **Python 3.11** with a GUI using **PyQt6**. The launcher lets you browse and launch two Crash games via the *Dolphin emulator* — all inside one unified interface without opening Dolphin manually.

---

## 🕹️ Features

- 🎮 Select between two Crash games:  
  1. *Crash of the Titans*  
  2. *Mind Over Mutant*
  
- 🖼️ Dynamic backgrounds & music for each game  
- ▶️ Launch games directly through the emulator  
- ⚙️ Saves the last selected game choice  
- 🛠️ Full keyboard navigation support  
- 💡 Error prompts if required files are missing

---

## 📂 Repo Structure

| Path | Description |
|------|-------------|
| `launcher.py` | Main launcher GUI logic |
| `config.json` | Saved config (last selected game) |
| `assets/` | Backgrounds, music, UI images |
| `Games/` | ISO files for games |
| `libs/xbox/` | Utilities for Xbox game mode |
| `Component/` | UI widgets & controls |
| `Pages/` | Extra UI pages |

---

## 🧠 Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

Dependencies include:
```
PyQt6 – GUI framework

pygame – music & sound handling

pyinstaller – (optional) packaging to exe

pillow – image support
```

Full list is in `requirements.txt`.

---

## 🛠️ Setup

Put Dolphin emulator executable at the root (named Dolphin.exe)

Add the game ISOs into the `Games/` folder:

`titans.iso`

`mutant.iso`

Make sure assets (images/music) are available in `assets/`

Run the launcher:

`python launcher.py`

---
## 🎮 How It Works

When you launch the app:

PyQt6 builds the window and menu interface

Pygame plays the current game’s music and handles audio

You can switch between games and hit “Start” to launch Dolphin with the selected ISO

Last selection is stored in `config.json` and restored next run.

---
## 🎯 Keyboard Controls

| Key   | Action                   |
| ----- | ------------------------ |
| ← / → | Toggle active buttons    |
| ↑ / ↓ | Change selected game     |
| Enter | Activate selected button |

---
## 👨‍💻 Packaging (Optional)
Bundle the launcher into an `.exe` with PyInstaller:

```bash
pyinstaller --noconfirm --windowed --add-data "assets;assets" launcher.py
```

---
## ⚠️ Notes

Make sure Dolphin and ISO paths exist

The launcher expects Windows environment

No official game files are included

---
## 📜 License

This repository doesn’t currently include a license. Add one if you plan to open-source or distribute it.

---
## ❤️ Credits

Built & maintained by `mrthemgi` — thanks for sharing the project on `GitHub`!
