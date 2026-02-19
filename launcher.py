# launcher.py
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QLabel, QDialog, \
    QListWidget, QStackedWidget, QMessageBox
from PyQt6.QtGui import QPixmap, QPalette, QBrush, QFont
from PyQt6.QtCore import Qt
import subprocess, pygame
from libs.xbox import game_mode
from Component.MainPage.BottomControllBar import BottomControllBar
from Component.MainPage.SettingsModal import SettingsDialog
from Pages.BeforeStart import BeforeStart
import json
from Component.Ui.Toaster.SavedChanges import SavedChangesToaster

if getattr(sys, 'frozen', False):
    EXE_DIR = os.path.dirname(sys.executable)
    BASE_DIR = getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
else:
    EXE_DIR = BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# فایل‌های بازی و assets اختصاصی
DOLPHIN = os.path.join(EXE_DIR, "Dolphin", "Dolphin.exe")
GAMES = [
    {
        "name": "Crash of the Titans",
        "iso": os.path.join(EXE_DIR, "Games", "titans.iso"),
        "bg": os.path.join(BASE_DIR, "assets", "images", "bg.jpeg"),
        "music": os.path.join(BASE_DIR, "assets", "audio", "menu.mp3")
    },
    {
        "name": "Mind Over Mutant",
        "iso": os.path.join(EXE_DIR, "Games", "mutant.iso"),
        "bg": os.path.join(BASE_DIR, "assets", "images", "bg2.jpg"),
        "music": os.path.join(BASE_DIR, "assets", "audio", "menu2.mp3")
    }
]

# init pygame
pygame.mixer.init()
pygame.mixer.music.load(GAMES[0]["music"])
pygame.mixer.music.set_volume(0.6)
pygame.mixer.music.play(-1)

CONFIG_FILE = os.path.join(EXE_DIR, "config.json")

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_config(data):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


class Launcher(QMainWindow):
    def __init__(self):
        super().__init__()
        config = load_config()
        self.setWindowTitle("Crash Launcher")
        self.showFullScreen()
        self.current_game = config.get("current_game", 0)
        self.current_btn_idx = 0

        # Background
        self.bg_pixmap = QPixmap(GAMES[0]["bg"])
        palette = QPalette()
        palette.setBrush(QPalette.ColorRole.Window, QBrush(self.bg_pixmap.scaled(
            self.screen().size(),
            Qt.AspectRatioMode.IgnoreAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )))
        self.setPalette(palette)

        # Central Widget
        central = QWidget()
        self.setCentralWidget(central)
        central_layout = QVBoxLayout(central)
        central_layout.setContentsMargins(50, 50, 50, 50)
        central_layout.addStretch()

        # Bottom Bar
        bottom_callbacks = {
            "start": self.start_game,
            "change": self.change_game,
            "settings": self.open_settings,
            "exit": self.close
        }
        bottom = BottomControllBar(parent=central, callbacks=bottom_callbacks, games=[g["name"] for g in GAMES])
        central_layout.addStretch()
        central_layout.addWidget(bottom)

        # map دکمه‌ها
        self.btn_start = bottom.btn_start
        self.game_selector = bottom.game_selector
        self.btn_settings = bottom.btn_settings
        self.btn_exit = bottom.btn_exit
        self.btn_list = bottom.btn_list

        self.game_selector.setCurrentIndex(self.current_game)

        # highlight اولیه
        self.set_active(self.btn_list[0])

        self.update_assets()

    # ---------------- Logic ----------------
    def set_active(self, btn):
        for b in self.btn_list:
            b.setStyleSheet("""
                QPushButton {
                    color: white;
                    background-color: transparent;
                    border: none;
                }
                QPushButton:hover {
                    color: #ff3c3c;
                }
            """)
        btn.setStyleSheet("""
            QPushButton {
                color: #ff3c3c;
                background-color: transparent;
                border: none;
                font-weight:bold;
            }
        """)

    def start_game(self):
        game_path = GAMES[self.current_game]["iso"]
        if not os.path.exists(DOLPHIN) or not os.path.exists(game_path):
            self.show_error("Dolphin.exe or Game ISO not found!")
            return

        # توقف موزیک و خاموش کردن pygame قبل از اجرای بازی
        pygame.mixer.music.stop()
        pygame.mixer.quit()

        proc = subprocess.Popen([DOLPHIN, game_path], shell=True)
        if sys.platform == "win32":
            game_mode.set_game_mode_for_pid(proc.pid)
        self.close()

    def change_game(self, index=None, step=0):
        old_game = self.current_game  # ذخیره وضعیت قبلی
        if index is not None:
            self.current_game = index
        else:
            self.current_game = (self.current_game + step) % len(GAMES)

        self.update_assets()

        # ذخیره در config اگر تغییر کرده
        if self.current_game != old_game:
            save_config({"current_game": self.current_game})

            # نمایش toaster (ذخیره به self تا حذف نشه)
            self.toaster = SavedChangesToaster(parent=self)
            self.toaster.show_toaster()

    def open_settings(self):
        self.set_active(self.btn_settings)
        SettingsDialog(self).exec()

    def show_error(self, text):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Error")
        dlg.setText(text)
        dlg.setIcon(QMessageBox.Icon.Critical)
        dlg.exec()

    # ---------------- Keyboard Navigation ----------------
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Right:
            self.current_btn_idx = (self.current_btn_idx + 1) % len(self.btn_list)
            self.set_active(self.btn_list[self.current_btn_idx])
        elif event.key() == Qt.Key.Key_Left:
            self.current_btn_idx = (self.current_btn_idx - 1) % len(self.btn_list)
            self.set_active(self.btn_list[self.current_btn_idx])
        elif event.key() in [Qt.Key.Key_Return, Qt.Key.Key_Enter]:
            self.btn_list[self.current_btn_idx].click()
        elif event.key() == Qt.Key.Key_Up:
            self.change_game(step=-1)
        elif event.key() == Qt.Key.Key_Down:
            self.change_game(step=1)

    # ---------------- Panel Navigation ----------------
    def update_assets(self):
        # تغییر بک‌گراند
        bg_path = GAMES[self.current_game]["bg"]
        pixmap = QPixmap(bg_path).scaled(
            self.screen().size(),
            Qt.AspectRatioMode.IgnoreAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        palette = QPalette()
        palette.setBrush(QPalette.ColorRole.Window, QBrush(pixmap))
        self.setPalette(palette)
        self.update()  # مهم برای repaint

        # تغییر موزیک
        music_path = GAMES[self.current_game]["music"]
        pygame.mixer.music.stop()
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(0.6)
        pygame.mixer.music.play(-1)


if sys.platform == "win32":
    game_mode.set_game_mode("DazhoGames.CrashLauncher")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # نمایش متن قبل از لانچر
    pre_window = BeforeStart()
    pre_window.show()
    app.processEvents()

    # صبر کردن تا پنجره قبل بسته شود
    while pre_window.isVisible():
        app.processEvents()

    # حالا لانچر اصلی
    win = Launcher()
    win.show()
    sys.exit(app.exec())
