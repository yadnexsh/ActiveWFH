from PySide6.QtWidgets import QSystemTrayIcon, QMenu, QApplication, QStyle # Added QStyle
from PySide6.QtGui import QIcon
from config import Config
from .styles import BASECAMP_QSS
from .stats_window import StatsWindow

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
        
        self.view_stats_action = self.menu.addAction("📊 View Stats History") 
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
        """Opens the dedicated PySide calendar window."""
        # We store it as self.stats_window so it doesn't get garbage collected and close immediately
        if not hasattr(self, 'stats_window') or self.stats_window is None:
            self.stats_window = StatsWindow(self.db)
            
        self.stats_window.show()
        
        # Forces the window to the front if it was hidden behind another app
        self.stats_window.raise_()
        self.stats_window.activateWindow()

    def quit_app(self):
        """Safe shutdown."""
        QApplication.quit()