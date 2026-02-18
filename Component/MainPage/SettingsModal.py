# Component/MainPage/SettingsModal.py
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QListWidget, QStackedWidget, QLabel
from PyQt6.QtCore import Qt

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setModal(True)
        self.setFixedSize(700, 400)
        self.setStyleSheet("background:#111; color:white;")

        layout = QVBoxLayout(self)
        self.menu = QListWidget()
        self.menu.addItems(["System Info", "Audio", "Network", "About"])
        layout.addWidget(self.menu)

        self.stack = QStackedWidget()
        for text in ["GPU: Auto Detect", "Volume Settings", "Internet: Connected", "Crash Launcher v1.1"]:
            lbl = QLabel(text)
            lbl.setStyleSheet("font-weight:bold; font-size:16px;")
            self.stack.addWidget(lbl)
        layout.addWidget(self.stack)

        self.menu.currentRowChanged.connect(self.stack.setCurrentIndex)
        self.menu.setCurrentRow(0)
        self.menu.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
