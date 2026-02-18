import sys
import os

from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QApplication,
    QGraphicsOpacityEffect,
    QHBoxLayout
)
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QSize
from PyQt6.QtGui import QFont, QMovie


class BeforeStart(QWidget):
    def __init__(self, duration=15000):
        super().__init__()

        # ---------------- Window ----------------
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.showFullScreen()
        self.setStyleSheet("background-color: #000000;")

        screen_width = self.screen().size().width()
        max_text_width = int(screen_width * 0.65)

        # ---------------- Main Text ----------------
        main_text = """
Non-transferable access to special features such as exclusive, unlockable, downloadable, online content, services, and functions may require single-use serial code, additional fee, and/or online account registration (13+).

Your gameplay information may be displayed on leaderboards and other pages managed through Dazho 360.

Contests void where prohibited. Sponsored by Dazho Game Studio.
"""

        self.main_label = QLabel(main_text.strip())
        self.main_label.setWordWrap(True)
        self.main_label.setMaximumWidth(max_text_width)
        self.main_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.main_label.setFont(QFont("Segoe UI", 20, QFont.Weight.DemiBold))
        self.main_label.setStyleSheet("""
            color: #f2f2f2;
            line-height: 160%;
        """)

        # ---------------- Loading Lines ----------------
        loading_lines = [
            "Do not turn off your system while the save icon is showing.",
            "Do not turn off your system while the loading icon is showing.",
            "Do not turn off your system while the cloud save icon is showing."
        ]

        loading_layout = QVBoxLayout()
        loading_layout.setSpacing(14)
        loading_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        gif_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "assets", "images", "loading.gif")
        )

        self.movies = []

        for line in loading_lines:
            row = QHBoxLayout()
            row.setAlignment(Qt.AlignmentFlag.AlignCenter)
            row.setSpacing(10)

            gif_label = QLabel()
            gif_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            movie = QMovie(gif_path)
            movie.setScaledSize(QSize(22, 22))
            gif_label.setMovie(movie)
            movie.start()

            self.movies.append(movie)

            text_label = QLabel(line)
            text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            text_label.setStyleSheet("""
                color: #cccccc;
                font-size: 16px;
            """)

            row.addWidget(gif_label)
            row.addWidget(text_label)

            loading_layout.addLayout(row)

        # ---------------- Main Layout ----------------
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(60)

        layout.addWidget(self.main_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(loading_layout)

        self.setLayout(layout)

        # ---------------- Fade Animation ----------------
        self.opacity_effect = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.opacity_effect)

        self.anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.anim.setDuration(duration)
        self.anim.setStartValue(0.0)
        self.anim.setKeyValueAt(0.1, 1.0)
        self.anim.setKeyValueAt(0.9, 1.0)
        self.anim.setEndValue(0.0)
        self.anim.start()

        QTimer.singleShot(duration, self.close)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = BeforeStart()
    win.show()
    sys.exit(app.exec())
