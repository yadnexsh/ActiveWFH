import sqlite3
import logging
from datetime import date
from config import Config

logger = logging.getLogger("Basecamp.Database")

class DatabaseManager:
    def __init__(self, db_path=Config.DB_PATH):
        self.db_path = db_path
        self.initialize_tables()

    def _get_connection(self):
        """Creates a fresh connection for thread safety."""
        return sqlite3.connect(self.db_path)

    def initialize_tables(self):
        """Creates the schema if it doesn't exist."""
        query = """
        CREATE TABLE IF NOT EXISTS daily_logs (
            log_date TEXT PRIMARY KEY,
            water_ml INTEGER DEFAULT 0,
            screen_time_sec INTEGER DEFAULT 0,
            exercises_completed INTEGER DEFAULT 0
        )
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query)
                conn.commit()
            logger.info("Database schema initialized.")
        except sqlite3.Error as e:
            logger.error(f"Database initialization failed: {e}")

    def _ensure_today_exists(self):
        """Ensures a row exists for the current date before updating."""
        today = date.today().isoformat()
        query = """
        INSERT OR IGNORE INTO daily_logs (log_date)
        VALUES (?)
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (today,))
            conn.commit()
        return today

    def get_today_stats(self):
        """Retrieves today's current totals for the UI."""
        today = self._ensure_today_exists()
        query = "SELECT water_ml, screen_time_sec, exercises_completed FROM daily_logs WHERE log_date = ?"
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (today,))
            row = cursor.fetchone()
            
        return {
            "water_ml": row[0],
            "screen_time_sec": row[1],
            "exercises_completed": row[2]
        }

    def add_water(self, amount_ml):
        """Adds water volume to today's log."""
        today = self._ensure_today_exists()
        query = "UPDATE daily_logs SET water_ml = water_ml + ? WHERE log_date = ?"
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (amount_ml, today))
            conn.commit()
        logger.info(f"Logged +{amount_ml}ml water.")

    def add_screen_time(self, seconds):
        """Appends active screen time (Called by the telemetry background worker)."""
        today = self._ensure_today_exists()
        query = "UPDATE daily_logs SET screen_time_sec = screen_time_sec + ? WHERE log_date = ?"
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (seconds, today))
            conn.commit()

    def increment_exercise(self):
        """Logs a completed movement intervention."""
        today = self._ensure_today_exists()
        query = "UPDATE daily_logs SET exercises_completed = exercises_completed + 1 WHERE log_date = ?"
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (today,))
            conn.commit()
        logger.info("Logged 1 completed exercise routine.")

    def get_stats_for_date(self, target_date_str):
            """Retrieves stats for a specific historical date (YYYY-MM-DD)."""
            query = "SELECT water_ml, screen_time_sec, exercises_completed FROM daily_logs WHERE log_date = ?"
            
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (target_date_str,))
                row = cursor.fetchone()
                
            if row:
                return {
                    "water_ml": row[0],
                    "screen_time_sec": row[1],
                    "exercises_completed": row[2]
                }
            return None