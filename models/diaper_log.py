# models/diaper_log

from models.daily_log import DailyLog

class DiaperLog(DailyLog):
    def __init__(self, baby_id, date, time, diaper_type, notes=None):
        """
        Initialize a new DiaperLog

        Args:
            baby_id (str): UUID of baby
            date (datetime): Date of diaper change
            time (datetime): Time of diaper change
            diaper_type (str): Type of diaper ('wet', 'soiled', 'both')
            notes (str, optional): Additional notes. Defaults to None.
        """
        super().__init__(baby_id, date, time, "diaper", notes)
        self.diaper_type = diaper_type
        
    def to_dict(self):
        """
        Convert DiaperLog instance to dictionary for serialization.

        Returns:
            dict: Dictionary representation of DiaperLog
        """
        log_dict = super().to_dict()
        log_dict.update({
            "diaper_type": self.diaper_type
        })
        
        return log_dict