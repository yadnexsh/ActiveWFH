import sys
import logging
from PySide6.QtWidgets import QApplication

# Importing from our newly created modules
from config import Config
from database import DatabaseManager
from telemetry import TelemetryWorker
from ui import TrayIcon

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

    # 3. Boot System Tray (This now handles the Popup and Timer internally!)
    logger.info("Initializing system tray...")
    tray_icon = TrayIcon(db_manager=db, app=app)
    tray_icon.show()

    logger.info("Basecamp is running. Check your system tray!")
    
    # 4. Execute loop and ensure safe shutdown
    exit_code = app.exec()
    
    # Clean up background threads when the user exits via the Tray Icon
    telemetry_thread.stop() 
    sys.exit(exit_code)

if __name__ == "__main__":
    main()