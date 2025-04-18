# controllers/baby_controller.py

from datetime import datetime
from models.baby import Baby

class BabyController:
    def __init__(self, data_service) -> None:
        """
        Initialize the Baby Controller.

        Args:
            data_service: Service for data persistence
        """
        self.data_service = data_service
    
    def create_baby(self, name, birthdate, gender = None, notes = None):
        """
        Create a new baby profile.

        Args:
            name (str): Baby's name
            birthdate (str): Baby's birthdate (YYYY-MM-DD)
            gender (str, optional): Baby's gender. Defaults to None.
            notes (str, optional): Additional notes. Defaults to None.

        Returns:
            Baby: Created Baby instance
        """
        
        # Convert string date to datetime
        if isinstance(birthdate, str):
            birthdate = datetime.strptime(birthdate, "%Y-%m-%d")
        
        baby = Baby(name, birthdate, gender, notes)
        
        self.data_service.save_baby(baby)
        
        return baby
    
    def get_baby_by_id(self, baby_id):
        """
        Retrieve a baby by ID.

        Args:
            baby_id (str): UUID of baby to retrieve

        Returns:
            Baby: Retrieved Baby instance or None if not found
        """
        return self.data_service.load_baby(baby_id)
    
    def get_all_babies(self):
        """
        Retrieve all babies.
        
        Returns:
            list: List of all Baby instances
        """
        return self.data_service.load_all_babies()
    
    def update_baby(self, baby_id, **kwargs):
        """
        Update baby's information

        Args:
            baby_id (str): UUID of baby to update
            **kwargs: Fields to update (name, notes, etc.)

        Returns:
            Baby: Updated Baby instance or None if not found
        """
        baby = self.get_baby_by_id(baby_id)
        if not baby:
            return None
        
        # Update fields
        for key, value in kwargs.items():
            if hasattr(baby, key):
                setattr(baby, key, value)
        
        # Save changes
        self.data_service.save_baby(baby)
        
        return baby
    
    def delete_baby(self, baby_id):
        """
        Delete a baby profile

        Args:
            baby_id (str): UUID of baby to delete

        Returns:
            bool: True if successful, False otherwise
        """
        return self.data_service.delete_baby(baby_id)