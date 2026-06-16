import json
from pathlib import Path

class ConfigManager:
    # 1. Path Resolutions
    SRC_DIR = Path(__file__).resolve().parent
    CONFIG_DIR = SRC_DIR / "config"
    
    MAIN_CONFIG_PATH = CONFIG_DIR / "config.json"
    EXERCISE_JSON_PATH = CONFIG_DIR / "exercise.json"
    
    # The database stays in the main project root
    DB_PATH = SRC_DIR.parent / "basecamp_data.sqlite"

    @classmethod
    def initialize(cls):
        """Creates the config directory and default JSONs if they do not exist."""
        cls.CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        
        # Generate default config.json
        if not cls.MAIN_CONFIG_PATH.exists():
            default_config = {
                "app_settings": {
                    "interval_minutes": 60, # <-- CHANGED: Now using human-readable minutes
                    "polling_rate_seconds": 60
                },
                "targets": {
                    "daily_water_target_ml": 4000,
                    "trek_day_water_target_ml": 5000,
                    "water_per_interval_ml": 330,
                    "bmc_target_date": "2027-04-01",
                    "bmc_location": "NIMAS Dirang"
                },
                "alarms": {
                    "lunch_time": "13:00",
                    "dinner_time": "20:00",
                    "sleep_prep_time": "23:00"
                }
            }
            with open(cls.MAIN_CONFIG_PATH, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=4)
                
        # Generate default exercise.json
        if not cls.EXERCISE_JSON_PATH.exists():
            default_exercises = {
                "exercises": [
                    {"name": "Squats", "sets": 3, "reps": 15, "time_sec": None},
                    {"name": "Plank", "sets": 1, "reps": None, "time_sec": 30},
                    {"name": "Calf Raises", "sets": 3, "reps": 20, "time_sec": None},
                    {"name": "Lunges", "sets": 3, "reps": 10, "time_sec": None}
                ]
            }
            with open(cls.EXERCISE_JSON_PATH, 'w', encoding='utf-8') as f:
                json.dump(default_exercises, f, indent=4)

    @classmethod
    def load_main_config(cls):
        cls.initialize()
        with open(cls.MAIN_CONFIG_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)

    @classmethod
    def get_exercises(cls):
        cls.initialize()
        with open(cls.EXERCISE_JSON_PATH, 'r', encoding='utf-8') as f:
            return json.load(f).get("exercises", [])

    @classmethod
    def save_exercises(cls, exercise_list):
        """Overwrites the exercise.json file with new data."""
        cls.initialize()
        with open(cls.EXERCISE_JSON_PATH, 'w', encoding='utf-8') as f:
            json.dump({"exercises": exercise_list}, f, indent=4)

    @classmethod
    def get_active_exercises(cls):
        """Returns only the exercises that have been moved to the Active list."""
        all_ex = cls.get_exercises()
        return [ex for ex in all_ex if ex.get("is_active", False)]


# 2. The Config Wrapper
class Config:
    DB_PATH = ConfigManager.DB_PATH
    
    _data = ConfigManager.load_main_config()
    
    # --- THE FIX ---
    # Read the new 'interval_minutes' (fallback to 60 if missing)
    INTERVAL_MINUTES = _data["app_settings"].get("interval_minutes", 60)
    
    # Automatically convert to milliseconds for Qt Timers!
    # This prevents the rest of your app from crashing.
    INTERVAL_MS = INTERVAL_MINUTES * 60 * 1000 
    
    POLLING_RATE_SECONDS = _data["app_settings"]["polling_rate_seconds"]
    
    DAILY_WATER_TARGET_ML = _data["targets"]["daily_water_target_ml"]
    TREK_DAY_WATER_TARGET_ML = _data["targets"]["trek_day_water_target_ml"]
    WATER_PER_INTERVAL_ML = _data["targets"]["water_per_interval_ml"]
    
    BMC_TARGET_DATE = _data["targets"]["bmc_target_date"]
    BMC_LOCATION = _data["targets"]["bmc_location"]
    
    @staticmethod
    def get_exercises():
        return ConfigManager.get_exercises()
        
    @staticmethod
    def save_exercises(exercise_list):
        ConfigManager.save_exercises(exercise_list)

    @staticmethod
    def get_active_exercises():
        return ConfigManager.get_active_exercises()
        
    @staticmethod
    def get_days_to_bmc():
        """Calculates the days remaining until the BMC start date."""
        from datetime import datetime
        try:
            target = datetime.strptime(Config.BMC_TARGET_DATE, "%Y-%m-%d")
            today = datetime.now()
            delta = target - today
            return max(0, delta.days)
        except ValueError:
            return 0

    @staticmethod
    def reload():
        """Call this if you want the app to re-read the config.json while running."""
        Config._data = ConfigManager.load_main_config()
        Config.INTERVAL_MINUTES = Config._data["app_settings"].get("interval_minutes", 60)
        Config.INTERVAL_MS = Config.INTERVAL_MINUTES * 60 * 1000 # Update the ms variable too
        Config.DAILY_WATER_TARGET_ML = Config._data["targets"]["daily_water_target_ml"]
        Config.WATER_PER_INTERVAL_ML = Config._data["targets"]["water_per_interval_ml"]