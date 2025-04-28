# controllers/milestone_controller.py

from datetime import datetime
from models.milestone import Milestone

class MilestoneController:
    def __init__(self, data_service):
        """
        Initialize the Milestone Controller.
        
        Args:
            data_service: Service for data persistence
        """
        
        self.data_service = data_service
        
        # TODO: Do research of worldwide standard / approved milestones for babies (WHO/UN?)
        # TODO: Evaluate if standard_milestones data should be kept in data service and not directly in controller
        self.standard_milestones = {
                "physical": [
                {"name": "Holds head up", "min_months": 1, "max_months": 4},
                {"name": "Rolls over", "min_months": 3, "max_months": 7},
                {"name": "Sits without support", "min_months": 5, "max_months": 8},
                {"name": "Crawls", "min_months": 6, "max_months": 10},
                {"name": "Pulls to stand", "min_months": 8, "max_months": 12},
                {"name": "Walks alone", "min_months": 9, "max_months": 18},
                {"name": "Climbs stairs", "min_months": 12, "max_months": 18},
                {"name": "Kicks a ball", "min_months": 18, "max_months": 24},
            ],
            "social": [
                {"name": "Smiles", "min_months": 1, "max_months": 3},
                {"name": "Laughs", "min_months": 3, "max_months": 6},
                {"name": "Recognizes familiar people", "min_months": 3, "max_months": 6},
                {"name": "Stranger anxiety", "min_months": 6, "max_months": 12},
                {"name": "Plays peek-a-boo", "min_months": 6, "max_months": 12},
                {"name": "Waves bye-bye", "min_months": 8, "max_months": 12},
                {"name": "Plays with others", "min_months": 12, "max_months": 24},
                {"name": "Shows empathy", "min_months": 18, "max_months": 36},
            ],
            "language": [
                {"name": "Coos", "min_months": 1, "max_months": 4},
                {"name": "Babbles", "min_months": 4, "max_months": 8},
                {"name": "Says first word", "min_months": 8, "max_months": 14},
                {"name": "Says 2-3 words", "min_months": 12, "max_months": 18},
                {"name": "Points to objects", "min_months": 12, "max_months": 18},
                {"name": "Follows simple instructions", "min_months": 12, "max_months": 24},
                {"name": "Speaks in 2-word phrases", "min_months": 18, "max_months": 24},
                {"name": "Uses 3-word sentences", "min_months": 24, "max_months": 36},
            ],
            "cognitive": [
                {"name": "Follows moving objects", "min_months": 1, "max_months": 3},
                {"name": "Recognizes familiar objects", "min_months": 3, "max_months": 6},
                {"name": "Finds hidden objects", "min_months": 6, "max_months": 12},
                {"name": "Explores objects", "min_months": 6, "max_months": 12},
                {"name": "Scribbles", "min_months": 12, "max_months": 18},
                {"name": "Sorts shapes", "min_months": 18, "max_months": 24},
                {"name": "Follows 2-step commands", "min_months": 18, "max_months": 24},
                {"name": "Engages in pretend play", "min_months": 24, "max_months": 36},
            ]
        }
        
    def add_milestone(self, baby_id, name, category, achieved_date = None, expected_range = None, notes = None):
        """
        Add a new milestone for a baby.

        Args:
            baby_id (str): UUID of baby
            name (str): Name of milestone
            category (str): Category of milestone
            achieved_date (datetime or str, optional): Date when milestone was achieved. Defaults to None.
            expected_range (dict, optional): Expected age range for milestone. Defaults to None.
            notes (str, optional): Additional notes. Defaults to None.
        
        Returns:
            Milestone: Create milestone or None if baby not found
        """
        
        # Convert string date to datetime if provided
        if isinstance(achieved_date, str) and achieved_date:
            achieved_date = datetime.strptime(achieved_date, '%Y-%m-%d')
            
        # Get baby
        baby = self.data_service.load_baby(baby_id)
        if not baby:
            return None
        
        # Create milestone
        milestone = Milestone(
            baby_id,
            name,
            category,
            achieved_date,
            expected_range,
            notes
        )
    
        # Add to baby and save
        if not hasattr(baby, 'milestones'):
            baby.milestones = []
        baby.milestones.append(milestone)
        self.data_service.save_baby(baby)
        
        return milestone
        
    def get_milestones(self, baby_id):
        """
        Get all milestone for baby.

        Args:
            baby_id (str): UUID of baby
            
        Returns:
            list: List of milestone or None if baby not found
        """
        
        baby = self.data_service.load_baby(baby_id)
        if not baby:
            return None
        
        # Ensure milestone attribute exists
        if not hasattr(baby, 'milestones'):
            baby.milestones = []
            
        return sorted(baby.milestones, key = lambda m: (m.achieved_date or datetime.max, m.name))
    
    def update_milestone(self, baby_id, milestone_id, **kwargs):
        """
        Update a milestone.

        Args:
            baby_id (str): UUID of baby
            milestone_id (str): UUID of milestone
            **kwargs: Fields to update
            
        Returns:
            Milestone: Update milestone or None if not found
        """
        baby = self.data_service.load_baby(baby_id)
        if not baby:
            return None
        
        # Ensure milestones attribute exists
        if not hasattr(baby, 'milestones'):
            baby.milestones = []
            
        # Find milestone
        # TODO: Understand functionality of line below
        milestone = next((m for m in baby.milestones if m.id == milestone_id), None)
        if not milestone:
            return None
        
        # Update fields
        for key, value in kwargs.items():
            if hasattr(milestone, key):
                setattr(milestone, key, value)
                
        # Save changes
        self.data_service.save_baby(baby)
        
        return milestone
    
    def delete_milestone(self, baby_id, milestone_id):
        """
        Delete a milestone.

        Args:
            baby_id (str): UUID of baby
            milestone_id (str): UUID of milestone

        Returns:
            bool: True if successful, False otherwise
        """
        baby = self.data_service.load_baby(baby_id)
        if not baby:
            return False
        
        # Ensure milestone attribute exists
        if not hasattr(baby, 'milestones'):
            baby.milestones = []
            
        # Find and remove milestone
        initial_count = len(baby.milestones)
        
        # TODO: Understand functionality of line below
        baby.milestones = [m for m in baby.milestones if m.id != milestone_id]
        
        if len(baby.milestones) == initial_count:
            return False # Milestone not found
        
        # Save changes
        self.data_service.save_baby(baby)
        
        return True
        
    def get_milestone_suggestions(self, baby_age_months):
        suggestions = {}
        
        # Get milestones appropriate for baby's age
        for category, milestones in self.standard_milestones.items():
            category_suggestions = []
        
            for milestone in milestones:
                # Include milestones that baby might achieve soon (within next 3 months)
                if milestone['min_months'] <= baby_age_months + 3 and milestone['max_months'] >= baby_age_months:
                    category_suggestions.append({
                        "name": milestone["name"],
                        "expected_range": {
                            'min_months': milestone['min_months'],
                            'max_months': milestone['max_months']
                        }
                    })
            
            if category_suggestions:
                suggestions[category] = category_suggestions
        
        return suggestions