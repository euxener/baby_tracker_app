from controllers import baby_controller
from controllers.baby_controller import BabyController
# from controllers.growth_controller import GrowthController
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
    #growth_controller = GrowthController(data_service)
    
    # Initialize view
    cli_view = CLIView(baby_controller)
    
    # Run the application
    cli_view.run()

if __name__ == "__main__":
    main()
