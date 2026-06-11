import time
import ctypes
import logging
from PySide6.QtCore import QThread
from config import Config

logger = logging.getLogger("Basecamp.Telemetry")

# C-struct required by Windows API for user input tracking
class LASTINPUTINFO(ctypes.Structure):
    _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_uint)]

class TelemetryWorker(QThread):
    def __init__(self, db_manager):
        super().__init__()
        self.db = db_manager
        self._is_running = True
        
        # Load Windows DLLs once to save overhead
        self.user32 = ctypes.windll.user32
        self.kernel32 = ctypes.windll.kernel32

    def run(self):
        """The main loop running continuously in the background."""
        logger.info("Telemetry thread started. Monitoring system state...")
        
        while self._is_running:
            # Pause the thread for the duration of the polling rate (e.g., 60 seconds)
            time.sleep(Config.POLLING_RATE_SECONDS)
            
            idle_seconds = self.get_idle_time()
            is_watching_media = self.check_media_presence()
            
            # Logic: If you've touched the mouse recently OR you're watching a video
            if idle_seconds < Config.IDLE_TIMEOUT_SECONDS or is_watching_media:
                self.db.add_screen_time(Config.POLLING_RATE_SECONDS)
                logger.debug(f"Active. Logged +{Config.POLLING_RATE_SECONDS}s screen time.")
            else:
                logger.debug(f"Idle for {idle_seconds}s. Tracking paused.")

    def stop(self):
        """Safely kills the thread when the application closes."""
        self._is_running = False
        self.wait()

    def get_idle_time(self):
        """Calculates seconds since the last mouse move or keystroke."""
        lastInputInfo = LASTINPUTINFO()
        lastInputInfo.cbSize = ctypes.sizeof(lastInputInfo)
        
        if self.user32.GetLastInputInfo(ctypes.byref(lastInputInfo)):
            # GetTickCount returns milliseconds since Windows booted
            millis_since_boot = self.kernel32.GetTickCount()
            millis_since_input = millis_since_boot - lastInputInfo.dwTime
            return millis_since_input / 1000.0
        return 0

    def check_media_presence(self):
        """
        Layer 1 Media Check: Inspects the active foreground window.
        If the window title contains media keywords, assumes passive watching.
        """
        # Get the handle to the window currently in focus
        hwnd = self.user32.GetForegroundWindow()
        if not hwnd:
            return False
            
        # Extract the text (title) of the window
        length = self.user32.GetWindowTextLengthW(hwnd)
        buf = ctypes.create_unicode_buffer(length + 1)
        self.user32.GetWindowTextW(hwnd, buf, length + 1)
        
        window_title = buf.value.lower()
        
        # Keywords that indicate you are staring at the screen without clicking
        media_keywords = [
            'youtube', 'vlc media player', 'netflix', 'prime video', 
            'disney+', 'potplayer', 'windows media player', 'tutorial'
        ]
        
        for keyword in media_keywords:
            if keyword in window_title:
                return True
                
        return False