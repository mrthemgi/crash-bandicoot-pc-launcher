# Component/MainPage/BottomControllBar.py
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QComboBox
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt


class BottomControllBar(QWidget):
    def __init__(self, parent=None, callbacks=None, games=None):
        super().__init__(parent)

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.callbacks = callbacks or {}
        self.games = games or []
        self.btn_list = []

        layout = QHBoxLayout()
        layout.setContentsMargins(20, 10, 20, 10)
        layout.setSpacing(20)

        # START
        self.btn_start = self.create_button("START", self.callbacks.get("start"))

        # GAME DROPDOWN
        self.game_selector = QComboBox()
        self.game_selector.addItems(self.games)
        self.game_selector.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.game_selector.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.game_selector.currentIndexChanged.connect(
            self.callbacks.get("change")
        )

        self.game_selector.setStyleSheet("""
            QComboBox {
                color: white;
                background-color: transparent;
                border: none;
            }
            QComboBox QAbstractItemView {
                background-color: #111;
                color: white;
                selection-background-color: #ff3c3c;
            }
        """)

        # SETTINGS
        self.btn_settings = self.create_button("SETTINGS", self.callbacks.get("settings"))

        # EXIT
        self.btn_exit = self.create_button("EXIT", self.callbacks.get("exit"))

        # Layout
        layout.addWidget(self.btn_start)
        layout.addWidget(self.game_selector)
        layout.addWidget(self.btn_settings)
        layout.addStretch()
        layout.addWidget(self.btn_exit)

        self.setLayout(layout)
        self.setFixedHeight(80)

        self.setStyleSheet("""
            QWidget {
                background-color: rgba(0,0,0,200);
                border-radius: 15px;
            }
        """)

        # برای ناوبری کیبورد
        self.btn_list = [
            self.btn_start,
            self.game_selector,
            self.btn_settings,
            self.btn_exit
        ]

        self.set_active(self.btn_start)

    def create_button(self, text, callback):
        btn = QPushButton(text)
        btn.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        btn.setStyleSheet("color:white; border:none;")
        btn.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        if callback:
            btn.clicked.connect(callback)
        return btn

    def set_active(self, widget):
        for w in self.btn_list:
            if isinstance(w, QComboBox):
                w.setStyleSheet("""
                    QComboBox {
                        color: white;
                        background-color: transparent;
                        border: none;
                    }
                """)
            else:
                w.setStyleSheet("color:white; border:none; font-weight:bold;")

        if isinstance(widget, QComboBox):
            widget.setStyleSheet("""
                QComboBox {
                    color: #ff3c3c;
                    background-color: transparent;
                    border: none;
                    font-weight:bold;
                }
            """)
        else:
            widget.setStyleSheet("color:#ff3c3c; border:none; font-weight:bold;")
