# models/growth_record.py

from datetime import datetime
import uuid

class GrowthRecord:
    def __init__(self, baby_id, date, weight = None, height = None, head_circumference = None, notes = None) -> None:
        """
        Initialize a new GrowthRecord.

        Args:
            baby_id (str): UUID of the baby this record belongs to 
            date (datetime): Date of the measurement
            weight (float, optional): Weight in kilograms. Defaults to None.
            height (float, optional): Height in centimeters. Defaults to None.
            head_circumference (float, optional): Head circumference in centimeters. Defaults to None.
            notes (str, optional): Additional notes about the measurement. Defaults to None.
        """
        self.id = str(uuid.uuid4())
        self.baby_id = baby_id
        self.date = date
        self.weight = weight
        self.height = height
        self.head_circumference = head_circumference
        self.notes = notes
        
    def to_dict(self):
        """
        Convert GrowthRecord instance to dictionary for serialization.
        
        Returns:
            dict: dictionary representation of the GrowthRecord
        """
        return {
            "id": self.id,
            "baby_id": self.baby_id,
            "date": self.date.isoformat(),
            "weight": self.weight,
            "height": self.height,
            "head_circumference": self.head_circumference,
            "notes": self.notes
        }