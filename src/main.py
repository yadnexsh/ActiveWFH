import sys
import logging
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer

# Importing from our newly created modules
from config import Config
from database import DatabaseManager
from telemetry import TelemetryWorker
from ui import ReminderPopup, BasecampTrayIcon

def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger("Basecamp")
    logger.info("Booting up Basecamp WFH Tool...")

    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    # 1. Boot Database
    logger.info("Connecting to local database...")
    db = DatabaseManager(Config.DB_PATH)

    # 2. Boot Background Telemetry (Screen Time)
    logger.info("Starting telemetry engine...")
    telemetry_thread = TelemetryWorker(db)
    telemetry_thread.start()

    # 3. Boot System Tray
    logger.info("Initializing system tray...")
    tray_icon = BasecampTrayIcon(db_manager=db)
    tray_icon.show()

    # 4. Boot Hourly Popup Engine
    hourly_popup = ReminderPopup()

    # Connect the popup's "Mark Done" button directly to the database
    def handle_popup_completed(water_ml, exercise_done):
        db.add_water(water_ml)
        if exercise_done:
            db.increment_exercise()
        logger.info(f"UI Logged: {water_ml}ml and 1 exercise.")

    hourly_popup.completed.connect(handle_popup_completed)

    # 5. Start the 60-Minute Master Timer
    timer = QTimer()
    timer.timeout.connect(hourly_popup.show_popup)
    timer.start(Config.INTERVAL_MS)

    logger.info("Basecamp is running. Check your system tray!")
    
    # 6. Execute loop and ensure safe shutdown
    exit_code = app.exec()
    telemetry_thread.stop() 
    sys.exit(exit_code)

if __name__ == "__main__":
    main()