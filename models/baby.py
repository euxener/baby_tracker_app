# models/baby.py

from datetime import datetime
import re
import uuid

class Baby:
    def __init__(self, name, birthdate, gender = None, notes = None) -> None:
        """
        Initialize a new Baby instance.
        
        Args:
            name (str): The baby's name
            birthdate (datetime): The baby's date of birth
            gender (str, optional): Baby's gender
            notes (str, optional): Additional notes about baby
        """
        self.id = str(uuid.uuid4())
        self.name = name
        self.birthdate = birthdate
        self.gender = gender
        self.notes = notes
        self.growth_records = []
        self.daily_logs = []
        
    def calculate_age(self, as_of_date = None):
        """
        Calculate baby's age
        
        Args:
            as_of_date (datetime, optional): Date to calculate age as of.
                Defaults to current date.
        Returns:
            dict: Contains years, months, days. 
        """
        if as_of_date is None:
            as_of_date = datetime.now()
        
        delta = as_of_date - self.birthdate
        years = delta.days // 365
        remaining_days = delta.days % 365
        months = remaining_days // 30
        days = remaining_days % 30
        
        return {
            "years": years,
            "months": months,
            "days": days,
            "total_days": delta.days
        }
        
    def add_growth_record(self, growth_record) -> None:
        """
        Add a growth record to this baby's history

        Args:
            growth_record (GrowthRecord): Growth record to add
        """
        self.growth_records.append(growth_record)
        
    def to_dict(self):
        """
        Convert baby instance to dictionary for serialization
        
        Returns:
            dict: Dictionary representation of Baby instance
        """
        return {
            "id": self.id,
            "name": self.name,
            "birthdate": self.birthdate,
            "gender": self.gender,
            "notes": self.notes
        }