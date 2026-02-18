# --------- launcher.py (Edited) ---------
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QDialog, \
    QListWidget, QStackedWidget, QMessageBox
from PyQt6.QtGui import QPixmap, QPalette, QBrush, QFont
from PyQt6.QtCore import Qt
import sys, os, subprocess, pygame

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
        self.btn_list = []

        # Background
        self.bg_pixmap = QPixmap(BACKGROUND_IMAGE)
        palette = QPalette()
        palette.setBrush(QPalette.ColorRole.Window, QBrush(self.bg_pixmap.scaled(
            self.screen().size(),
            Qt.AspectRatioMode.IgnoreAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )))
        self.setPalette(palette)

        central = QWidget()
        central_layout = QVBoxLayout(central)
        central_layout.addStretch()

        # Title
        self.title = QLabel(GAMES[self.current_game][0])
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet("font-size:40px; color:white; font-weight:bold;")
        central_layout.addWidget(self.title)

        # Bottom Bar
        bar = QHBoxLayout()
        self.btn_start = QPushButton("START")
        self.btn_change = QPushButton("CHANGE GAME ▲▼")
        self.btn_settings = QPushButton("SETTINGS")
        self.btn_exit = QPushButton("EXIT")

        for btn in [self.btn_start, self.btn_change, self.btn_settings, self.btn_exit]:
            btn.setFont(QFont("Arial", 14, QFont.Weight.Bold))
            btn.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.btn_start.clicked.connect(self.start_game)
        self.btn_change.clicked.connect(self.change_game)
        self.btn_settings.clicked.connect(self.open_settings)
        self.btn_exit.clicked.connect(self.close)

        bar.addWidget(self.btn_start)
        bar.addWidget(self.btn_change)
        bar.addWidget(self.btn_settings)
        bar.addStretch()
        bar.addWidget(self.btn_exit)

        bottom = QWidget()
        bottom.setFixedHeight(80)
        bottom.setStyleSheet("background:#000; border-radius:15px;")
        bottom.setLayout(bar)
        central_layout.addWidget(bottom)

        self.setCentralWidget(central)
        self.btn_list = [self.btn_start, self.btn_change, self.btn_settings, self.btn_exit]
        self.set_active(self.btn_start)

    # ---------------- Logic ----------------
    def set_active(self, btn):
        for b in self.btn_list:
            b.setStyleSheet("color:white; font-weight:bold;")
        btn.setStyleSheet("color:#ff3c3c; font-weight:bold;")

    def start_game(self):
        game_path = GAMES[self.current_game][1]
        if not os.path.exists(DOLPHIN):
            self.show_error("Dolphin.exe not found!")
            return
        if not os.path.exists(game_path):
            self.show_error("Game ISO not found!")
            return
        pygame.mixer.music.stop()
        subprocess.Popen([DOLPHIN, game_path])
        self.close()

    def change_game(self, step=1):
        self.current_game = (self.current_game + step) % len(GAMES)
        self.title.setText(GAMES[self.current_game][0])
        self.set_active(self.btn_change)

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
        elif event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            self.btn_list[self.current_btn_idx].click()
        elif event.key() == Qt.Key.Key_Up:
            self.change_game(step=-1)
        elif event.key() == Qt.Key.Key_Down:
            self.change_game(step=1)


class SettingsDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setModal(True)
        self.setFixedSize(700, 400)
        self.setStyleSheet("background:#111; color:white;")

        layout = QHBoxLayout(self)
        self.menu = QListWidget()
        self.menu.addItems(["System Info", "Audio", "Network", "About"])
        layout.addWidget(self.menu)

        self.stack = QStackedWidget()
        for text in ["GPU: Auto Detect", "Volume Settings", "Internet: Connected", "Crash Launcher v1.0"]:
            lbl = QLabel(text)
            lbl.setStyleSheet("font-weight:bold; font-size:16px;")
            self.stack.addWidget(lbl)
        layout.addWidget(self.stack)

        self.menu.currentRowChanged.connect(self.stack.setCurrentIndex)
        self.menu.setCurrentRow(0)

        self.menu.setFocusPolicy(Qt.FocusPolicy.StrongFocus)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Launcher()
    win.show()
    sys.exit(app.exec())
