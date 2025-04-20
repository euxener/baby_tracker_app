# models/feeding_log.py

from models.daily_log import DailyLog

class FeedingLog(DailyLog):
    def __init__(self, baby_id, date, time, feeding_type, amount = None, duration = None, notes = None):
        """
        Initialize a new FeedingLog.

        Args:
            baby_id (str): UUID of baby
            date (datetime): Date of feeding
            time (datetime): Time of feeding
            feeding_type (str): Type of feeding ('breast', 'bottle', 'solid')
            amount (float, optional): Amount in oz or ml (for bottle) or g (for solid). Defaults to None.
            duration (int, optional): Duration of feeding in minutes. Defaults to None.
            notes (str, optional): Additional notes. Defaults to None.
        """
        super().__init__(baby_id, date, time, "feeding", notes)
        self.feeding_type = feeding_type
        self.amount = amount
        self.duration = duration
        
    def to_dict(self):
        
        log_dict = super().to_dict()
        log_dict.update({
            "feeding_type": self.feeding_type,
            "amount": self.amount,
            "duration": self.duration
        })
        return log_dict