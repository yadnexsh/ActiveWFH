from PySide6.QtWidgets import QSystemTrayIcon, QMenu, QApplication, QStyle # Added QStyle
from PySide6.QtGui import QIcon
from config import Config
from .styles import BASECAMP_QSS

class BasecampTrayIcon(QSystemTrayIcon):
    def __init__(self, db_manager):
        super().__init__()
        self.db = db_manager
        
        # Fallback to standard system icon until you design a custom .ico or .png
        fallback_icon = QApplication.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon)
        self.setIcon(fallback_icon)
        
        self.setToolTip("Basecamp WFH Tracker")
        
        self.setup_menu()

    def setup_menu(self):
        """Builds the right-click context menu."""
        self.menu = QMenu()
        # self.menu.setStyleSheet(BASECAMP_QSS) # Apply dark theme to the right-click menu too
        
        # --- Goal Countdown ---
        days_left = Config.get_days_to_bmc()
        self.bmc_action = self.menu.addAction(f"🏔️ NIM BMC: {days_left} Days")
        self.bmc_action.setEnabled(False) # Greyed out, acts as a permanent label
        
        self.menu.addSeparator()

        # --- Quick Actions ---
        self.add_water_action = self.menu.addAction("💧 Quick Log: +330ml Water")
        self.add_water_action.triggered.connect(self.log_quick_water)
        
        self.view_stats_action = self.menu.addAction("📊 View Today's Stats")
        self.view_stats_action.triggered.connect(self.show_stats)
        
        self.menu.addSeparator()
        
        # --- System ---
        self.quit_action = self.menu.addAction("Quit Basecamp")
        self.quit_action.triggered.connect(self.quit_app)
        
        self.setContextMenu(self.menu)

    def log_quick_water(self):
        """Allows manual water logging outside the hourly popup."""
        self.db.add_water(Config.WATER_PER_INTERVAL_ML)
        self.showMessage(
            "Basecamp", 
            f"Logged +{Config.WATER_PER_INTERVAL_ML}ml.",
            QSystemTrayIcon.Information, 
            2000
        )

    def show_stats(self):
        """Pulls current database row and shows a native Windows notification."""
        stats = self.db.get_today_stats()
        
        water = stats['water_ml']
        screen_sec = stats['screen_time_sec']
        exercises = stats['exercises_completed']
        
        # Format seconds into Hours and Minutes
        hours = screen_sec // 3600
        minutes = (screen_sec % 3600) // 60
        
        msg = (
            f"💧 Water: {water}ml / {Config.DAILY_WATER_TARGET_ML}ml\n"
            f"⏱️ Screen Time: {hours}h {minutes}m\n"
            f"🏃‍♂️ Exercises: {exercises} sets"
        )
        
        self.showMessage("Today's Basecamp Stats", msg, QSystemTrayIcon.Information, 5000)

    def quit_app(self):
        """Safe shutdown."""
        QApplication.quit()