import sqlite3
from contextlib import contextmanager
from datetime import datetime, timedelta

class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self._init_db()

    @contextmanager
    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
        finally:
            conn.commit()
            conn.close()

    def _init_db(self):
        query = """
        CREATE TABLE IF NOT EXISTS daily_logs (
            log_date TEXT PRIMARY KEY,
            water_ml INTEGER DEFAULT 0,
            screen_time_sec INTEGER DEFAULT 0,
            exercises_completed INTEGER DEFAULT 0
        )
        """
        with self._get_connection() as conn:
            conn.execute(query)

    def _ensure_date_exists(self, cursor, date_str):
        cursor.execute("INSERT OR IGNORE INTO daily_logs (log_date) VALUES (?)", (date_str,))

    def add_water(self, amount_ml, date_str):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            self._ensure_date_exists(cursor, date_str)
            cursor.execute("UPDATE daily_logs SET water_ml = water_ml + ? WHERE log_date = ?", (amount_ml, date_str))

    def add_screen_time(self, seconds, date_str):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            self._ensure_date_exists(cursor, date_str)
            cursor.execute("UPDATE daily_logs SET screen_time_sec = screen_time_sec + ? WHERE log_date = ?", (seconds, date_str))

    def add_exercise(self, date_str):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            self._ensure_date_exists(cursor, date_str)
            cursor.execute("UPDATE daily_logs SET exercises_completed = exercises_completed + 1 WHERE log_date = ?", (date_str,))

    def get_stats_for_date(self, target_date_str):
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

    def get_graph_data(self, limit=7):
        """Generates a continuous timeline, fetching DB data and filling empty days with zeros."""
        today = datetime.now()
        
        # Generate a list of dates from oldest to newest (e.g., 7 days ago up to today)
        date_list = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(limit-1, -1, -1)]
        
        placeholders = ','.join(['?'] * limit)
        query = f"""
            SELECT log_date, water_ml, screen_time_sec, exercises_completed 
            FROM daily_logs 
            WHERE log_date IN ({placeholders})
        """
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, date_list)
            rows = cursor.fetchall()
            
        # Map the DB rows for quick lookup
        db_map = {row[0]: row for row in rows}
        
        results = []
        for d_str in date_list:
            dt_obj = datetime.strptime(d_str, "%Y-%m-%d")
            
            # Format outputs as DD-MM-YY and short DD-MM
            dd_mm_yy = dt_obj.strftime("%d-%m-%y")
            dd_mm = dt_obj.strftime("%d-%m")
            
            if d_str in db_map:
                row = db_map[d_str]
                results.append({
                    "full_date": dd_mm_yy,
                    "date": dd_mm,
                    "water_ml": row[1],
                    "screen_min": row[2] // 60,
                    "exercises": row[3]
                })
            else:
                # Inject a blank log if the user didn't record anything that day
                results.append({
                    "full_date": dd_mm_yy,
                    "date": dd_mm,
                    "water_ml": 0,
                    "screen_min": 0,
                    "exercises": 0
                })
                
        return results