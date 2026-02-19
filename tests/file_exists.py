# dist/test_file_exists.py
import os
import sys

BASE_DIR = os.path.dirname(sys.executable)  # مسیر کنار exe

DOLPHIN = os.path.join(BASE_DIR, "Dolphin", "Dolphin.exe")
GAMES = [
    ("Crash of the Titans", os.path.join(BASE_DIR, "Games", "titans.iso")),
    ("Mind Over Mutant", os.path.join(BASE_DIR, "Games", "mutant.iso"))
]

print("BASE_DIR:", BASE_DIR)
print("DOLPHIN exists:", os.path.exists(DOLPHIN))
for name, path in GAMES:
    print(f"{name} exists:", os.path.exists(path))
