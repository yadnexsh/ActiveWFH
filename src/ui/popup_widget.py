import random
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Signal
from PySide6.QtGui import QGuiApplication
from config import Config
from .styles import BASECAMP_QSS

class PopupWidget(QWidget):
    # UPGRADED SIGNAL: Now sends (Log_Water_Bool, Log_Exercise_Bool)
    log_requested = Signal(bool, bool) 

    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet(BASECAMP_QSS)
        
        self.has_active_exercise = False 
        self.setup_ui()

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        
        self.frame = QFrame()
        self.frame.setObjectName("bg_frame")
        self.frame_layout = QVBoxLayout(self.frame)
        
        self.title = QLabel("BASECAMP: HOURLY CHECK-IN")
        self.title.setObjectName("header_text")
        self.title.setAlignment(Qt.AlignCenter)
        
        self.water_label = QLabel(f"💧 Drink {Config.WATER_PER_INTERVAL_ML}ml of Water")
        self.water_label.setObjectName("task_text")
        self.water_label.setAlignment(Qt.AlignCenter)
        
        self.exercise_label = QLabel("🏃‍♂️ Loading...")
        self.exercise_label.setObjectName("task_text")
        self.exercise_label.setAlignment(Qt.AlignCenter)
        
        # --- Updated Button Layout ---
        self.btn_layout = QHBoxLayout()
        self.btn_layout.setSpacing(10)
        
        self.btn_done = QPushButton("Mark Done")
        self.btn_done.setObjectName("btn_done") # Green primary button
        
        self.btn_water_only = QPushButton("Water Only")
        self.btn_water_only.setObjectName("grid_btn") # Grey secondary button
        
        self.btn_snooze = QPushButton("Snooze (10m)")
        self.btn_snooze.setObjectName("grid_btn") # Grey secondary button
        
        self.btn_done.clicked.connect(self.on_mark_done)
        self.btn_water_only.clicked.connect(self.on_water_only)
        self.btn_snooze.clicked.connect(self.on_snooze)
        
        self.btn_layout.addWidget(self.btn_done)
        self.btn_layout.addWidget(self.btn_water_only)
        self.btn_layout.addWidget(self.btn_snooze)
        
        self.frame_layout.addWidget(self.title)
        self.frame_layout.addSpacing(10)
        self.frame_layout.addWidget(self.water_label)
        self.frame_layout.addSpacing(10)
        self.frame_layout.addWidget(self.exercise_label)
        self.frame_layout.addSpacing(15)
        self.frame_layout.addLayout(self.btn_layout)
        
        self.main_layout.addWidget(self.frame)

    def on_mark_done(self):
        """Emits signal to log water AND exercise (if active)."""
        self.log_requested.emit(True, self.has_active_exercise)
        self.close()

    def on_water_only(self):
        """Emits signal to log water ONLY, bypassing exercise."""
        self.log_requested.emit(True, False)
        self.close()

    def on_snooze(self):
        self.close()

    def show_popup(self):
        active_exercises = Config.get_active_exercises()
        
        if not active_exercises:
            self.has_active_exercise = False
            self.exercise_label.setText("🏃‍♂️ No active exercises in rotation!")
        else:
            self.has_active_exercise = True
            ex = random.choice(active_exercises)
            name = ex.get("name", "Unknown")
            sets, reps, time_sec = ex.get("sets"), ex.get("reps"), ex.get("time_sec")
            
            if time_sec: self.exercise_label.setText(f"🏃‍♂️ {name} ({time_sec} sec)")
            elif sets and reps: self.exercise_label.setText(f"🏃‍♂️ {name} ({sets}x{reps})")
            else: self.exercise_label.setText(f"🏃‍♂️ {name}")

        screen_geometry = QGuiApplication.primaryScreen().availableGeometry()
        target_x = screen_geometry.width() - self.width() - 20
        target_y = screen_geometry.height() - self.height() - 20
        self.move(target_x, target_y)

        self.setWindowOpacity(0.0)
        self.show()
        self.raise_()           
        self.activateWindow()   

        self.anim = QPropertyAnimation(self, b"windowOpacity")
        self.anim.setDuration(400) 
        self.anim.setStartValue(0.0)
        self.anim.setEndValue(1.0)
        self.anim.setEasingCurve(QEasingCurve.InOutQuad)
        self.anim.start()