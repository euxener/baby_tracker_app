# models/daily_log.py

import uuid
from datetime import datetime

class DailyLog:
    def __init__(self, baby_id, date, time, log_type, notes = None):
        """
        Initialize a new DailyLog.

        Args:
            baby_id (str): UUID of baby
            date (datetime): Date of log
            time (datetime): Time of log
            log_type (str): Type of log (e.g., 'feeding', 'sleep', 'diaper')
            notes (str, optional): Additional notes. Defaults to None.
        """
        self.id = str(uuid.uuid4())
        self.baby_id = baby_id
        self.date = date
        self.time = time
        self.log_type = log_type
        self.notes = notes
        
    def to_dict(self):
        """
        Converts DailyLog instance to dictionary for serialization.

        Returns:
            dict: Dictionary representation of DailyLog
        """
        return {
            "id": self.id,
            "baby_id": self.baby_id,
            "date": self.date.isoformat(),
            "time": self.time.isoformat(),
            "log_type": self.log_type,
            "notes": self.notes
        }