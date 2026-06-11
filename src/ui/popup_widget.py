import random
from .styles import BASECAMP_QSS
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QApplication, QFrame
from PySide6.QtCore import Qt, QPropertyAnimation, QPoint, QEasingCurve, Signal
from config import Config

class ReminderPopup(QWidget):
    # Custom signals to tell the main app what the user chose
    completed = Signal(int, bool) # Emits (water_ml, exercise_done)
    snoozed = Signal()            # Emits when the user delays

    def __init__(self):
        super().__init__()
        
        # --- WINDOW SETUP ---
        # Frameless, stays on top, and acts as a 'Tool' so it doesn't show in the taskbar
        self.setWindowFlags(
            Qt.FramelessWindowHint | 
            Qt.WindowStaysOnTopHint | 
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground) # Allows for rounded corners via CSS
        
        # Hardcoded size for the popup
        self.setFixedSize(320, 180)
        
        # Pool of micro-exercises for load-carrying prep
        self.exercises = [
            "20 Calf Raises",
            "15 Air Squats",
            "2-Minute Wall Sit",
            "20 Lunges (10 per leg)",
            "30-Second Plank"
        ]

        self.setup_ui()
        self.setup_animation()
        # Add this exact line here:
        self.setStyleSheet(BASECAMP_QSS)
        
    def setup_ui(self):
        """Builds the internal layout of the popup with a background container."""
        # 1. Main layout for the invisible top-level window (0 margins)
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # 2. The visible background container
        self.bg_frame = QFrame(self)
        self.bg_frame.setObjectName("bg_frame") # We will target this in styles.py
        
        # 3. The internal layout for your text/buttons goes INSIDE the frame
        self.layout = QVBoxLayout(self.bg_frame)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(10)

        # Header Label
        self.header_label = QLabel("BASECAMP: HOURLY CHECK-IN")
        self.header_label.setAlignment(Qt.AlignCenter)
        self.header_label.setObjectName("header_text") 
        self.layout.addWidget(self.header_label)

        # Water Prompt
        water_amount = Config.WATER_PER_INTERVAL_ML
        self.water_label = QLabel(f"💧 Drink {water_amount}ml of Water")
        self.water_label.setAlignment(Qt.AlignCenter)
        self.water_label.setObjectName("task_text")
        self.layout.addWidget(self.water_label)

        # Movement Prompt
        self.exercise_label = QLabel("🏃‍♂️ Loading exercise...")
        self.exercise_label.setAlignment(Qt.AlignCenter)
        self.exercise_label.setObjectName("task_text")
        self.layout.addWidget(self.exercise_label)

        # Buttons Layout
        self.button_layout = QHBoxLayout()
        
        self.btn_done = QPushButton("Mark Done")
        self.btn_done.setObjectName("btn_done")
        self.btn_done.clicked.connect(self.on_done_clicked)
        
        self.btn_snooze = QPushButton("Snooze (10m)")
        self.btn_snooze.setObjectName("btn_snooze")
        self.btn_snooze.clicked.connect(self.on_snooze_clicked)

        self.button_layout.addWidget(self.btn_done)
        self.button_layout.addWidget(self.btn_snooze)
        self.layout.addLayout(self.button_layout)

        # 4. Add the finished frame to the invisible main layout
        self.main_layout.addWidget(self.bg_frame)

    def setup_animation(self):
        """Prepares the QPropertyAnimation for the slide-in effect."""
        self.anim = QPropertyAnimation(self, b"pos")
        self.anim.setDuration(400) # 400 milliseconds
        # OutBack gives it a slight "bounce" when it stops sliding
        self.anim.setEasingCurve(QEasingCurve.OutBack) 

    def show_popup(self):
        """Calculates screen position, randomizes the exercise, and slides in."""
        # Randomize the physical task
        task = random.choice(self.exercises)
        self.exercise_label.setText(f"🏃‍♂️ {task}")

        # Calculate position (Bottom Right corner, above the taskbar)
        screen = QApplication.primaryScreen().availableGeometry()
        
        # Target resting position
        end_x = screen.width() - self.width() - 20
        end_y = screen.height() - self.height() - 20
        
        # Start position (just below the screen)
        start_y = screen.height() + 10
        
        # Apply positions and start animation
        self.anim.setStartValue(QPoint(end_x, start_y))
        self.anim.setEndValue(QPoint(end_x, end_y))
        
        self.show()
        self.anim.start()

    def hide_popup(self):
        """Slides the window back down off-screen, then hides it."""
        self.anim.setEasingCurve(QEasingCurve.InBack)
        self.anim.setDirection(QPropertyAnimation.Backward)
        
        # When animation finishes going backward, actually hide the widget
        self.anim.finished.connect(self.hide_and_reset)
        self.anim.start()

    def hide_and_reset(self):
        self.hide()
        # Disconnect to prevent multiple fires next time it hides
        self.anim.finished.disconnect(self.hide_and_reset)
        # Reset direction for the next time it shows
        self.anim.setDirection(QPropertyAnimation.Forward)

    def on_done_clicked(self):
        """User accepted the challenge."""
        self.hide_popup()
        # Tell the main app to log the water and the exercise
        self.completed.emit(Config.WATER_PER_INTERVAL_ML, True)

    def on_snooze_clicked(self):
        """User delayed the challenge."""
        self.hide_popup()
        self.snoozed.emit()