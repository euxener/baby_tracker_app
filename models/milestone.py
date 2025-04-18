# models/milestone.py

import uuid
from datetime import datetime

class Milestone:
    def __init__(self, baby_id, name, category, achieved_date = None, expected_range = None, notes = None):
        """
        Initialize a new Milestone.

        Args:
            baby_id (str): UUID of baby this milestone belongs to
            name (str): Name of milestone
            category (str): Category of milestone (e.g., physical, social)
            achieved_date (datetime, optional): Date of milestone was achieved. Defaults to None.
            expected_range (dict, optional): Expected age range for milestone (e.g., {"min_months": 3, "max_months": 6}). Defaults to None.
            notes (str, optional): Additional notes about the milestone. Defaults to None.
        """
        self.id = str(uuid.uuid4())
        self.baby_id = baby_id
        self.name = name
        self.category = category
        self.achieved_date = achieved_date
        self.expected_range = expected_range
        self.notes = notes
        
    def is_achieved(self):
        """Check if milestone has been achieved."""
        return self.achieved_date is not None
        
    def achieved_on_time(self, baby_birthdate):
        """
        Check if milestone was achieved within the expected range.

        Args:
            baby_birthdate (datetime): Baby's birthdate
            
        Returns:
            bool or None: True if on time, False if late/early, None if no expected range or not achieved
        """
        if not self.is_achieved() or not self.expected_range:
            return None
        
        # Calculate age in months when milestone is achieved
        delta = self.achieved_date - baby_birthdate
        months_age = delta.days // 30
        
        min_months = self.expected_range.get("min_months")
        max_months = self.expected_range.get("max_months")
        
        if min_months is not None and max_months is not None:
            return min_months <= months_age <= max_months
        
        return None
    
    def to_dict(self):
        """
        Convert Milestone instance to dictionary for serialization
        
        Returns:
            dict: Dictionary representation of the Milestone
        """
        return {
            "id": self.id,
            "baby_id": self.baby_id,
            "name": self.name,
            "category": self.category,
            "achieved_date": self.achieved_date.isoformat() if self.achieved_date else None,
            "expected_range": self.expected_range,
            "notes": self.notes
        }        