# views/cli_view.py

import datetime

class CLIView:
    def __init__(self, baby_controller):
        """_summary_

        Args:
            baby_controller (_type_): _description_
            growth_controller (_type_): _description_
        """
        self.baby_controller = baby_controller
        # self.growth_controller = growth_controller
    
    def display_main_menu(self):
        """Display the main menu and get user choice"""
        print("\n===== Baby Tracker =====")
        print("1. Manage Babies")
        print("2. Track Growth")
        print("3. Track Milestones")
        print("4. Daily Logs")
        print("5. Reports")
        print("0. Exit")
        
        choice = input("\nEnter your choice: ")
        return choice
    
    def run(self):
        """Run the CLI application."""
        while True:
            choice = self.display_main_menu()
            
            if choice == '1':
                self.manage_babies_menu()
            elif choice == '2':
                self.track_growth_menu()
            elif choice == '3':
                print("Milestone tracking not implemented yet.")
            elif choice == '4':
                print("Daily logs not implemented yet.")
            elif choice == '5':
                print("Reports not implemented yet.")
            elif choice == '0':
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
                
    def manage_babies_menu(self):
        """Displays baby management menu"""
        while True:
            print("\n===== Manage Babies =====")
            print("1. Add New Baby")
            print("2. View All Babies")
            print("3. View Baby Details")
            print("4. Update Baby Information")
            print("5. Delete Baby")
            print("0. Back to Main Menu")
            
            choice = input("\nEnter your choice: ")
            
            if choice == '1':
                self.add_baby()
            elif choice == '2':
                #self.list_babies()
                print("Not implemented yet.")
            elif choice == '3':
                #self.view_baby_details()
                print("Not implemented yet.")
            elif choice == '4':
                #self.update_baby()
                print("Not implemented yet.")
            elif choice == '5':
                #self.delete_baby()
                print("Not implemented yet.")
            elif choice == '0':
                break
            else:
                print("Invalid choice. Please try again.")
    
    def add_baby(self):
        """Add a new baby."""
        print("\n===== Add New Baby =====")
        name = input("Name: ")
        
        while True:
            birthdate_str = input("Birthdate (YYYY-MM-DD): ")
            try:
                birthdate = datetime.datetime.strptime(birthdate_str, "%Y-%m-%d")
                break
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")
        
        gender = input("Gender (optional): ")
        notes = input("Notes (optional): ")
        
        baby = self.baby_controller.create_baby(name, birthdate, gender, notes)
        print(f"\nBaby '{baby.name}' added successfully with ID: {baby.id}")
    
    # Include additional methods here...
    
    def track_growth_menu(self):
        pass