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

if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DOLPHIN = os.path.join(BASE_DIR, "Dolphin", "dolphin.exe")
GAMES = [
    ("Crash of the Titans", os.path.join(BASE_DIR, "Games", "titans.iso")),
    ("Mind Over Mutant", os.path.join(BASE_DIR, "Games", "mutant.iso"))
]
MENU_MUSIC = os.path.join(BASE_DIR, "assets", "audio", "menu.mp3")
BACKGROUND_IMAGE = os.path.join(BASE_DIR, "assets", "images", "bg.jpeg")

pygame.mixer.init()
pygame.mixer.music.load(MENU_MUSIC)
pygame.mixer.music.set_volume(0.6)
pygame.mixer.music.play(-1)


class Launcher(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Crash Launcher")
        self.showFullScreen()
        self.current_game = 0
        self.current_btn_idx = 0

        # Background
        self.bg_pixmap = QPixmap(BACKGROUND_IMAGE)
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

        # Title
        self.title = QLabel(GAMES[self.current_game][0])
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet("font-size:40px; color:white; font-weight:bold;")
        central_layout.addWidget(self.title)

        # Bottom Bar
        bottom_callbacks = {
            "start": self.start_game,
            "change": self.change_game,
            "settings": self.open_settings,
            "exit": self.close
        }
        bottom = BottomControllBar(parent=central, callbacks=bottom_callbacks, games=[g[0] for g in GAMES])
        central_layout.addStretch()
        central_layout.addWidget(bottom)

        # map دکمه‌ها
        self.btn_start = bottom.btn_start
        self.game_selector = bottom.game_selector
        self.btn_settings = bottom.btn_settings
        self.btn_exit = bottom.btn_exit
        self.btn_list = bottom.btn_list

        # highlight اولیه
        self.set_active(self.btn_list[0])

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
        game_path = GAMES[self.current_game][1]
        if not os.path.exists(DOLPHIN) or not os.path.exists(game_path):
            self.show_error("Dolphin.exe or Game ISO not found!")
            return
        pygame.mixer.music.stop()
        proc = subprocess.Popen([DOLPHIN, game_path])
        if sys.platform == "win32":
            game_mode.set_game_mode_for_pid(proc.pid)
        self.close()

    def change_game(self, index):
        self.current_game = index
        self.title.setText(GAMES[self.current_game][0])

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

