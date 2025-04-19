# services/data_service.py

import json
import os
from models.baby import Baby
from models.growth_record import GrowthRecord
from models.milestone import Milestone
from datetime import datetime

class DataService:
    def __init__(self, data_dir = "data"):
        """
        Initialize the DataService

        Args:
            data_dir (str): Directory where data will be stored. Defaults to "data".
        """
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok = True)
        
    def _get_baby_file_path(self, baby_id):
        """Get the file path for a baby's data"""
        return os.path.join(self.data_dir, f"baby_{baby_id}.json")
    
    def save_baby(self, baby):
        """
        Save a baby instance to persistent storage

        Args:
            baby (Baby): Baby instance to save

        Returns:
            bool: True if successful
        """
        
        # Convert to serializable format
        baby_dict = baby.to_dict()
        
        # Add serialized related objects
        baby_dict["growth_records"] = [
            record.to_dict() for record in baby.growth_records
        ]
        
        # TODO: Implement saving of milestones
        if hasattr(baby, 'milestones') and baby.milestones:
            baby_dict["milestones"] = [
                milestone.to_dict() for milestone in baby.milestones
            ]
        else:
            baby_dict['milestones'] = []
            
        # TODO: Implement saving of daily logs
        if hasattr(baby, 'daily_logs') and baby.daily_logs:
            baby_dict["daily_logs"] = [
                daily_log.to_dict() for daily_log in baby.daily_logs
            ]
        else:
            baby_dict['daily_logs'] = []
                    
        # Save to file
        with open(self._get_baby_file_path(baby.id), 'w') as f:
            json.dump(baby_dict, f, indent = 2, default = str)
        
        return True
    
    def load_baby(self, baby_id):
        """
        Load a baby from persistent storage

        Args:
            baby_id (str): UUID of baby to load

        Returns:
            Baby: Loaded baby instance or None if not found
        """
        file_path = self._get_baby_file_path(baby_id)
        
        if not os.path.exists(file_path):
            return None
        
        with open(file_path, 'r') as f:
            baby_dict = json.load(f)
            
        # Create baby instance
        birthdate = datetime.fromisoformat(baby_dict["birthdate"])
        
        baby = Baby(
            baby_dict["name"],
            birthdate,
            baby_dict["gender"],
            baby_dict["notes"]
        )
        
        baby.id = baby_dict["id"] # Use saved ID
        
        # Load growths records
        if "growth_records" in baby_dict:
            for record_dict in baby_dict["growth_records"]:
                date = datetime.fromisoformat(record_dict["date"])
                record = GrowthRecord(
                    record_dict["baby_id"],
                    date,
                    record_dict["weight"],
                    record_dict["height"],
                    record_dict["head_circumference"],
                    record_dict["notes"]
                )
                record.id = record_dict["id"] # Saved ID
                baby.growth_records.append(record)
                
        # Load milestones
        if "milestones" in baby_dict:
            for milestone_dict in baby_dict["milestones"]:
                achieved_date = None
                if milestone_dict['achieved_date']:
                    achieved_date = datetime.fromisoformat(milestone_dict["achieved_date"])
                milestone = Milestone(
                    milestone_dict['baby_id'],
                    milestone_dict['name'],
                    milestone_dict['category'],
                    achieved_date,
                    milestone_dict['expected_range'],
                    milestone_dict['notes']
                )
                milestone.id = milestone_dict["id"] # Saved ID
                baby.milestones.append(milestone)
                
        # TODO: Implement loading of daily logs
        # Load daily logs
        
        return baby
    
    def load_all_babies(self):
        """
        Load all babies from persistent storage
        
        Returns:
            list: List of all Baby instances
        """
        babies = []
        
        for filename in os.listdir(self.data_dir):
            if filename.startswith("baby_") and filename.endswith(".json"):
                baby_id = filename[5:-5]
                baby = self.load_baby(baby_id)
                if baby:
                    babies.append(baby)
        
        return babies
    
    def delete_baby(self, baby_id):
        """
        Delete a baby from persistent storage

        Args:
            baby_id (str): UUID of baby to delete
        
        Returns:
            bool: True if successful, False if not found
        """
        file_path = self._get_baby_file_path(baby_id)
        
        if not os.path.exists(file_path):
            return False
        
        os.remove(file_path)
        return True