# models/sleep_log.py

from models.daily_log import DailyLog
from datetime import datetime, timedelta

class SleepLog(DailyLog):
    def __init__(self, baby_id, date, start_time, end_time = None, quality = None, notes = None):
        """
        Initialize a new SleepLog

        Args:
            baby_id (str): UUID of baby
            date (datetime): Date of sleep start
            start_time (datetime): Time of sleep start
            end_time (datetime, optional): Time of sleep ended. Defaults to None.
            quality (str, optional): Sleep quality ('good', 'fair', 'poor'). Defaults to None.
            notes (str, optional): Additional notes. Defaults to None.
        """
        super().__init__(baby_id, date, start_time, "sleep", notes)
        self.start_time = start_time
        self.end_time = end_time
        self.quality = quality
    
    # TODO: Understand why is the @property decorator used here
    @property
    def duration(self):
        """Calculate sleep duration in minutes."""
        if not self.end_time:
            return None
        
        delta = self.end_time - self.start_time
        return delta.total_seconds() / 60
    
    def to_dict(self):
        log_dict = super().to_dict()
        log_dict.update({
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "quality": self.quality
        })
        return log_dict