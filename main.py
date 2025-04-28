
from controllers.baby_controller import BabyController
from controllers.growth_controller import GrowthController
from controllers.milestone_controller import MilestoneController
from controllers.daily_log_controller import DailyLogController
from services.data_service import DataService
from views.cli_view import CLIView

def main():
    """
    Main entry point for the Baby Tracker application.
    """
    # Initialize services
    data_service = DataService()
    
    # Initialize controllers
    baby_controller = BabyController(data_service)
    growth_controller = GrowthController(data_service)
    milestone_controller = MilestoneController(data_service)
    daily_log_controller = DailyLogController(data_service)
    
    # Initialize view
    cli_view = CLIView(baby_controller, growth_controller, milestone_controller, daily_log_controller)
    
    # Run the application
    cli_view.run()

if __name__ == "__main__":
    main()