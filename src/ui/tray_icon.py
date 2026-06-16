import sys
from PySide6.QtWidgets import QSystemTrayIcon, QMenu, QStyle
from PySide6.QtGui import QAction, QIcon
from PySide6.QtCore import QDate, QTimer
from config import Config
from .stats_window import StatsWindow
from .popup_widget import PopupWidget

class TrayIcon(QSystemTrayIcon):
    def __init__(self, db_manager, app):
        super().__init__()
        self.db = db_manager
        self.app = app
        
        # Temporarily use a built-in system computer icon
        default_icon = self.app.style().standardIcon(QStyle.SP_ComputerIcon)
        self.setIcon(default_icon)

        self.stats_window = None
        
        self.popup = PopupWidget()
        self.popup.log_requested.connect(self.handle_popup_log)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.popup.show_popup)
        self.timer.start(Config.INTERVAL_MS)
        
        self.setup_menu()

    def setup_menu(self):
        self.menu = QMenu()
        
        # --- THE FIX: Greyed-out Countdown Header ---
        days_left = Config.get_days_to_bmc()
        location = Config.BMC_LOCATION
        self.action_countdown = QAction(f"🏔️ {location} in {days_left} Days", self)
        self.action_countdown.setEnabled(False) # This is the magic line that greys it out!
        self.menu.addAction(self.action_countdown)
        
        self.menu.addSeparator() # Adds a nice line below the countdown
        # ---------------------------------------------
        
        self.action_log_water = QAction(f"💧 Quick Log +{Config.WATER_PER_INTERVAL_ML}ml", self)
        self.action_log_water.triggered.connect(lambda: self.handle_popup_log(True, False)) 
        self.menu.addAction(self.action_log_water)
        
        self.action_show_stats = QAction("📊 Open Dashboard", self)
        self.action_show_stats.triggered.connect(self.show_stats)
        self.menu.addAction(self.action_show_stats)
        
        self.menu.addSeparator()
        
        self.action_exit = QAction("❌ Exit Basecamp", self)
        self.action_exit.triggered.connect(self.exit_app)
        self.menu.addAction(self.action_exit)
        
        self.setContextMenu(self.menu)

    def handle_popup_log(self, log_water, log_exercise):
        """Dynamically logs based on the exact buttons clicked in the UI."""
        today_str = QDate.currentDate().toString("yyyy-MM-dd")
        
        if log_water:
            self.db.add_water(Config.WATER_PER_INTERVAL_ML, today_str)
        
        if log_exercise:
            self.db.add_exercise(today_str)
            
        if self.stats_window and self.stats_window.isVisible():
            self.stats_window.on_date_selected()
            self.stats_window.refresh_graph_data(7, self.stats_window.btn_1w) 

    def show_stats(self):
        if not self.stats_window:
            self.stats_window = StatsWindow(self.db)
        
        self.stats_window.on_date_selected()
        self.stats_window.refresh_graph_data(7, self.stats_window.btn_1w)
        
        self.stats_window.show()
        self.stats_window.activateWindow()

    def exit_app(self):
        self.app.quit()
        sys.exit()