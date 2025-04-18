# controllers/growth_controller.py

from datetime import datetime
from models.growth_record import GrowthRecord

class GrowthController:
    def __init__(self, data_service):
        """
        Initialize the Growth Controller.

        Args:
            data_service: Service for data persistence
        """
        self.data_service = data_service
    
    def add_growth_record(self, baby_id, date, weight = None, height = None, head_circumference = None, notes = None):
        """
        Add a new growth record for baby

        Args:
            baby_id (str): UUID of baby
            date (datetime or str): Date of measurement
            weight (float, optional): Weight in kg. Defaults to None.
            height (float, optional): Heihgt in cm. Defaults to None.
            head_circumference (float, optional): Head circumference in cm. Defaults to None.
            notes (str, optional): Additional notes. Defaults to None.
        
        Returns:
            GrowthRecord: The created growth record or None if baby not found.
        """
        
        # Convert string date to datetime
        if isinstance(date, str):
            date = datetime.strptime(date, "%Y-%m-%d")
        
        # Get the baby
        baby = self.data_service.load_baby(baby_id)
        if not baby:
            return None
        
        # Create growth record
        growth_record = GrowthRecord(
            baby_id,
            date,
            weight,
            height,
            head_circumference,
            notes
        )
        
        # Add to baby and save
        baby.add_growth_record(growth_record)
        self.data_service.save_baby(baby)
        
        return growth_record
    
    def get_growth_records(self, baby_id):
        """
        Get all growth records for baby.

        Args:
            baby_id (str): UUID of baby
            
        Returns:
            list: List of growth records or None if baby not found
        """
        baby = self.data_service.load_baby(baby_id)
        if not baby:
            return None
        
        return sorted(baby.growth_records, key = lambda r: r.date)
    
    def update_growth_record(self, baby_id, record_id, **kwargs):
        """
        Update a growth record.

        Args:
            baby_id (str): UUID of baby
            record_id (str): UUID of growth record
            **kwargs: Fields to update
            
        Returns:
            GrowthRecord: Updated record or None if not found
        """
        
        baby = self.data_service.load_baby(baby_id)
        if not baby:
            return None
        
        # Find the record
        record = next((r for r in baby.growth_records if r.id == record_id), None)
        if not record:
            return None
        
        # Update fields
        for key, value in kwargs.items():
            if hasattr(record, key):
                setattr(record, key, value)
                
        # Save changes
        self.data_service.save_baby(baby)
        
        return record
    
    def delete_growth_record(self, baby_id, record_id):
        """
        Delete a growth record.
        
        Args:
            baby_id (str): UUID of baby
            record_id (str): UUID of growth record
            
        Returns:
            bool: True if sucessful, False otherwise
        """
        baby = self.data_service.load_baby(baby_id)
        if not baby:
            return False
        
        # Find and remove record
        initial_count = len(baby.growth_records)
        baby.growth_records = [r for r in baby.growth_records if r.id != record_id]
        
        if len(baby.growth_records) == initial_count:
            return False # Record not found
        
        # Save changes
        self.data_service.save_baby(baby)
        
        return True