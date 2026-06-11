from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QCalendarWidget, QFrame
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QTextCharFormat, QColor # ADD THESE TWO
from config import Config
from .styles import BASECAMP_QSS

class StatsWindow(QWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db = db_manager
        
        self.setWindowTitle("Basecamp Tracking History")
        self.setFixedSize(550, 300)
        
        # Give the main window an ID so we can paint it dark in styles.py
        self.setObjectName("stats_main_window") 
        
        self.setStyleSheet(BASECAMP_QSS)

        self.setup_ui()
        self.update_stats(QDate.currentDate())

    def setup_ui(self):
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(20)

        # --- Left Side: Calendar ---
        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        
        # Hide the ugly week numbers on the left side
        self.calendar.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        
        # Force Sunday to stay a vibrant red in dark mode
        sunday_format = QTextCharFormat()
        sunday_format.setForeground(QColor("#ff4a4a")) 
        self.calendar.setWeekdayTextFormat(Qt.Sunday, sunday_format)

        self.calendar.selectionChanged.connect(self.on_date_selected) 
        self.layout.addWidget(self.calendar)

        # --- Right Side: Stats Panel ---
        self.stats_frame = QFrame()
        self.stats_frame.setObjectName("bg_frame") # Reuses your popup background CSS
        self.stats_layout = QVBoxLayout(self.stats_frame)
        self.stats_layout.setSpacing(15)

        self.date_label = QLabel("Loading...")
        self.date_label.setObjectName("header_text")

        self.water_label = QLabel("💧 Water: 0ml")
        self.water_label.setObjectName("task_text")

        self.screen_label = QLabel("⏱️ Screen Time: 0h 0m")
        self.screen_label.setObjectName("task_text")

        self.exercise_label = QLabel("🏃‍♂️ Exercises: 0")
        self.exercise_label.setObjectName("task_text")

        self.stats_layout.addWidget(self.date_label)
        self.stats_layout.addWidget(self.water_label)
        self.stats_layout.addWidget(self.screen_label)
        self.stats_layout.addWidget(self.exercise_label)
        self.stats_layout.addStretch() # Pushes everything to the top

        self.layout.addWidget(self.stats_frame)
        
    def on_date_selected(self):
        """Fires whenever the user clicks a new date on the calendar."""
        self.update_stats(self.calendar.selectedDate())

    def update_stats(self, qdate):
        """Fetches the data from SQLite and updates the labels."""
        # Convert QDate to the "YYYY-MM-DD" string format your database uses
        date_str = qdate.toString("yyyy-MM-dd") 
        self.date_label.setText(f"STATS FOR: {date_str}")

        stats = self.db.get_stats_for_date(date_str)

        if stats:
            water = stats['water_ml']
            screen_sec = stats['screen_time_sec']
            exercises = stats['exercises_completed']
            
            hours = screen_sec // 3600
            minutes = (screen_sec % 3600) // 60
            
            self.water_label.setText(f"💧 Water: {water}ml / {Config.DAILY_WATER_TARGET_ML}ml")
            self.screen_label.setText(f"⏱️ Screen Time: {hours}h {minutes}m")
            self.exercise_label.setText(f"🏃‍♂️ Exercises: {exercises} sets")
        else:
            self.water_label.setText("💧 Water: No Data")
            self.screen_label.setText("⏱️ Screen Time: No Data")
            self.exercise_label.setText("🏃‍♂️ Exercises: No Data")