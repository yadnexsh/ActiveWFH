# H:\Gamut\Projects\WFHKiller\ui\routine_alerts.py

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QApplication
from PySide6.QtCore import Qt, QPropertyAnimation, QPoint, QEasingCurve

class ScheduleAlert(QWidget):
    def __init__(self, title, message):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(300, 150)
        
        self.title = title
        self.message = message
        
        self.setup_ui()
        self.setup_animation()

    def setup_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        
        self.header_label = QLabel(self.title.upper())
        self.header_label.setAlignment(Qt.AlignCenter)
        self.header_label.setObjectName("header_text")
        
        self.message_label = QLabel(self.message)
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setObjectName("alert_text")
        self.message_label.setWordWrap(True)
        
        self.btn_ack = QPushButton("Understood")
        self.btn_ack.setObjectName("btn_done")
        self.btn_ack.clicked.connect(self.hide_popup)
        
        self.layout.addWidget(self.header_label)
        self.layout.addWidget(self.message_label)
        self.layout.addWidget(self.btn_ack)

    def setup_animation(self):
        self.anim = QPropertyAnimation(self, b"pos")
        self.anim.setDuration(500)
        
    def show_alert(self):
        screen = QApplication.primaryScreen().availableGeometry()
        end_x = screen.width() - self.width() - 20
        end_y = screen.height() - self.height() - 20
        start_y = screen.height() + 10
        
        self.anim.setStartValue(QPoint(end_x, start_y))
        self.anim.setEndValue(QPoint(end_x, end_y))
        self.anim.setEasingCurve(QEasingCurve.OutExpo)
        self.show()
        self.anim.start()

    def hide_popup(self):
        self.anim.setEasingCurve(QEasingCurve.InExpo)
        self.anim.setDirection(QPropertyAnimation.Backward)
        self.anim.finished.connect(self.close) # Safely destroy the widget
        self.anim.start()