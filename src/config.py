import os
from pathlib import Path
from datetime import date, time

class Config:
    # --- APP METADATA & PATHS ---
    APP_NAME = "Basecamp WFH Tracker"
    
    # Resolves to H:\Gamut\Projects\WFHKiller by stepping up out of /src
    BASE_DIR = Path(__file__).resolve().parent.parent
    
    # Stores the SQLite database in the same directory
    DB_PATH = BASE_DIR / "basecamp_data.sqlite"
    
    # --- HYDRATION & MOVEMENT TRACKING ---
    # Mountain prep baseline
    DAILY_WATER_TARGET_ML = 4000
    
    # 60 minutes in milliseconds (for the QTimer)
    INTERVAL_MS = 10000 
    
    # What the popup demands every 60 minutes
    WATER_PER_INTERVAL_ML = 330
    
    # --- TELEMETRY (SCREEN TIME) SETTINGS ---
    # How long before the app assumes you walked away (in seconds)
    IDLE_TIMEOUT_SECONDS = 300 
    
    # How often the background worker checks system state (in seconds)
    POLLING_RATE_SECONDS = 5 

    # --- FIXED ROUTINE ALARMS ---
    # Using 24-hour time format for exact trigger moments
    ROUTINE_SCHEDULE = {
        "Lunch": time(13, 0),        # 1:00 PM
        "Lunch_Warning": time(13, 15), # 1:15 PM (Hard stop)
        "Snacks": time(18, 0),       # 6:00 PM
        "Dinner": time(20, 0),       # 8:00 PM
        "Sleep_Prep": time(23, 0)    # 11:00 PM (Screen blackout)
    }

    # --- MOUNTAINEERING GOALS ---
    # For the UI countdown widget 
    NIMAS_BMC_DATE = date(2027, 4, 1)
    
    # Used by the telemetry engine to trigger "Trek Mode" and pause WFH 
    # tracking automatically when you are doing your Sinhgad run.
    # 6 represents Sunday in Python's datetime module (Monday is 0)
    WEEKLY_TREK_DAY = 6 
    
    # Required fluid intake on Sunday trek days
    TREK_DAY_WATER_TARGET_ML = 5000 

    @classmethod
    def get_days_to_bmc(cls):
        """Calculates days remaining until the course."""
        delta = cls.NIMAS_BMC_DATE - date.today()
        return max(0, delta.days)