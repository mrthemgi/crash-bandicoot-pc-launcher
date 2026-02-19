from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import QTimer, Qt

class SavedChangesToaster(QLabel):
    def __init__(self, parent=None, message="Changed Saved Successfully", duration=2000):
        super().__init__(parent)
        self.setText(message)
        self.setStyleSheet("""
            QLabel {
                background-color: #323232;
                color: white;
                padding: 10px 20px;
                border-radius: 8px;
                font-weight: bold;
            }
        """)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.hide)
        self.duration = duration

    def show_toaster(self):
        if self.parent():
            parent_rect = self.parent().rect()
            self.setGeometry(
                (parent_rect.width() - self.width()) // 2,
                20,
                self.sizeHint().width(),
                self.sizeHint().height()
            )
        self.show()
        self.timer.start(self.duration)
