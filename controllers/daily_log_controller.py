# controllers/daily_log_controller.py

from datetime import datetime
from models.daily_log import DailyLog
from models.feeding_log import FeedingLog
from models.sleep_log import SleepLog
from models.diaper_log import DiaperLog

class DailyLogController:
    def __init__(self, data_service):
        """
        Initialize DailyLogController

        Args:
            data_service: Service for data persistence
        """
        self.data_service = data_service
        
    def add_feeding_log(self, baby_id, date, time, feeding_type, amount = None, duration = None, notes = None):
        """
        Add a new feeding log to baby

        Args:
            baby_id (str): UUID of baby
            date (datetime): Date of feeding
            time (datetime): Time of feeding
            feeding_type (str): Type of feeding ('breast', 'bottle', 'solid')
            amount (float, optional): Amount in oz or ml (for bottle) or g (for solid). Defaults to None.
            duration (int, optional): Duration of feeding in minutes. Defaults to None.
            notes (str, optional): Additional notes. Defaults to None.

        Returns:
            FeedingLog: Created feeding log or None if baby not found
        """
        
        # Convert string dates/time to datetime if needed
        date, time = self._parse_date_time(date, time)
        
        # Get baby
        baby = self.data_service.load_baby(baby_id)
        
        if not baby:
            return None
        
        # Create log
        log = FeedingLog(
            baby_id,
            date,
            time,
            feeding_type,
            amount,
            duration,
            notes
        )

        # Add to baby and save
        if not hasattr(baby, 'daily_logs'):
            baby.daily_logs = []
        baby.daily_logs.append(log)
        self.data_service.save_baby(baby)
        
        return log
    
    # Add sleep log
    def add_sleep_log(self, baby_id, date, start_time, end_time = None, quality = None, notes = None):
        """
        Add a new sleep log to baby

        Args:
            baby_id (str): UUID of baby
            date (datetime): Date of sleep start
            start_time (datetime): Time of sleep start
            end_time (datetime, optional): Time of sleep ended. Defaults to None.
            quality (str, optional): Sleep quality ('good', 'fair', 'poor'). Defaults to None.
            notes (str, optional): Additional notes. Defaults to None.
            
        Returns:
            SleepLog: Created sleep log or None if baby not found
        """
        # Convert string dates/times to datetime if needed
        date, start_time = self._parse_date_time(date, start_time)
        # TODO: Understand functionality of couple of lines below
        if end_time:
            _, end_time = self._parse_date_time(date, end_time)
        
        # Get baby
        baby = self.data_service.load_baby(baby_id)
        if not baby:
            return None
        
        # Create sleep log
        log = SleepLog(
            baby_id,
            date,
            start_time,
            end_time,
            quality,
            notes
        )
        
        # Add to baby and save
        if not hasattr(baby, 'daily_logs'):
            baby.daily_logs = []
        baby.daily_logs.append(log)
        self.data_service.save_baby(baby)
        
        return log
    
    # Add diaper log
    def add_diaper_log(self, baby_id, date, time, diaper_type, notes = None):
        """
        Add a new diaper log for a baby

        Args:
            baby_id (str): UUID of baby
            date (datetime): Date of diaper change
            time (datetime): Time of diaper change
            diaper_type (str): Type of diaper ('wet', 'soiled', 'both')
            notes (str, optional): Additional notes. Defaults to None.

        Returns:
            DiaperLog: Created diaper log or None if baby not found
        """
        # Convert string dates/times to datetime if needed
        date, time = self._parse_date_time(date, time)
        
        # Get baby
        baby = self.data_service.load_baby(baby_id)
        if not baby:
            return None
        
        # Create log
        log = DiaperLog(
            baby_id,
            date,
            time,
            diaper_type,
            notes
        )
        
        # Add to baby and save
        if not hasattr(baby, 'daily_logs'):
            baby.daily_logs = []
        baby.daily_logs.append(log)
        self.data_service.save_baby(baby)
        
        return log
    
    # Helper method to parse date/time strings
    def _parse_date_time(self, date, time):
        """
        Parse date and time strings to datetime objects.
        
        Args:
            date (datetime or str): Date
            time (datetime or str): Time

        Returns:
            tuple: (datetime.date, datetime.time)
        """
        if isinstance(date, str):
            date = datetime.strptime(date, "%Y-%m-%d").date()
        elif isinstance(date, datetime):
            date = date.date()
        
        if isinstance(time, str):
            time = datetime.strptime(time, "%H:%M").time()
        elif isinstance(time, datetime):
            time = time.time()
        
        return date, time