# views/cli_view.py

import datetime

class CLIView:
    def __init__(self, baby_controller, growth_controller, milestone_controller, daily_log_controller):
        """
        Initialize CLI view.
        
        Args:
            baby_controller (BabyController): Controller for baby operations
            growth_controller (GrowthController): Controller for growth records operations
            milestone_controller (MilestoneController): Controller for milestone operations
            daily_log_controller (DailyLogController): Controller for log operations
        """
        self.baby_controller = baby_controller
        self.growth_controller = growth_controller
        self.milestone_controller = milestone_controller
        self.daily_log_controller = daily_log_controller

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
                self.track_milestones_menu()
            elif choice == '4':
                self.daily_logs_menu()
            elif choice == '5':
                print("Reports not implemented yet.")
            elif choice == '0':
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

################## Babies menu ################## 

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
                self.list_babies()
            elif choice == '3':
                self.view_baby_details()
            elif choice == '4':
                self.update_baby()
            elif choice == '5':
                self.delete_baby()
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

    def list_babies(self):
        """List all babies."""
        print("\n===== All Babies =====")
        babies = self.baby_controller.get_all_babies()
        
        if not babies:
            print("No babies found.")
            return

        for i, baby in enumerate(babies, 1):
            age_info = baby.calculate_age()
            age_str = ""
            if age_info["years"] > 0:
                age_str += f"{age_info['years']} year(s) "
            if age_info["months"] > 0:
                age_str += f"{age_info['months']} month(s) "
            if age_info["days"] > 0:
                age_str += f"{age_info['days']} day(s)"
            
            print(f"{i}. {baby.name} - Born: {baby.birthdate.strftime('%Y-%m-%d')} - Age: {age_str.strip()}")
        print()

    def view_baby_details(self):
        """View details of a specific baby."""
        babies = self.baby_controller.get_all_babies()
        
        if not babies:
            print("\nNo babies found.")
            return
        
        self.list_babies()
        
        try:
            choice = int(input("\nEnter the number of the baby to view (0 to cancel): "))
            if choice == 0:
                return
            if 1 <= choice <= len(babies):
                baby = babies[choice - 1]
                self._display_baby_details(baby)
            else:
                print("Invalid selection.")
        except ValueError:
            print("Please enter a valid number.")

    def _display_baby_details(self, baby):
        """Display detailed information about a baby."""
        print(f"\n===== {baby.name} =====")
        print(f"ID: {baby.id}")
        print(f"Birthdate: {baby.birthdate.strftime('%Y-%m-%d')}")
        
        age_info = baby.calculate_age()
        age_str = ""
        
        if age_info["years"] > 0:
            age_str += f"{age_info['years']} year(s) "
        if age_info["months"] > 0:
            age_str += f"{age_info['months']} month(s) "
        if age_info["days"] > 0:
            age_str += f"{age_info['days']} day(s)"
            
        print(f"Age: {age_str.strip()}")
        
        if baby.gender:
            print(f"Gender: {baby.gender}")
        
        if baby.notes:
            print(f"Notes: {baby.notes}")
            
        if baby.growth_records:
            print("\nGrowth Records:")
            for i, record in enumerate(sorted(baby.growth_records, key = lambda r: r.date), 1):
                print(f"{i}. Date: {record.date.strftime('%Y-%m-%d')}")
                if record.weight:
                    print(f"   Weight: {record.weight} kg")
                if record.height:
                    print(f"   Height: {record.height} cm")
                if record.head_circumference:
                    print(f"   Head circumference: {record.head_circumference} cm")
                if record.notes:
                    print(f"   Notes: {record.notes}")
        
        input("\nPress Enter to continue...")
        
    def update_baby(self):
        """Update baby's information"""
        babies = self.baby_controller.get_all_babies()
        
        if not babies:
            print("\nNo babies found.")
            return
        
        self.list_babies()
        
        try:
            choice = int(input("\nEnter the number of baby to update (0 to cancel): "))
            if choice == 0:
                return
            
            if 1 <= choice <= len(babies):
                baby = babies[choice - 1]
                self._update_baby_form(baby)
            else:
                print("Invalid selection.")
        
        except ValueError:
            print("Please enter a valid number.")

    def _update_baby_form(self, baby):
        """Form for updating baby information."""
        print(f"\n===== Update {baby.name} =====")
        print("Leave fields blank to keep current values.")
        
        name = input(f"Name [{baby.name}]")
        name = name if name else baby.name
        
        birthdate_str = input(f"Birthdate [{baby.birthdate.strftime('%Y-%m-%d')}]: ")
        if birthdate_str:
            try:
                birthdate = datetime.datetime.strptime(birthdate_str, "%Y-%m-%d")
            except:
                print("Invalid date format. Keeping current birthdate.")
                birthdate = baby.birthdate
        else:
            birthdate = baby.birthdate
            
        gender = input(f"Gender [{baby.gender or ''}]: ")
        gender = gender if gender else baby.gender
        
        notes = input(f"Notes [{baby.notes or ''}]: ")
        notes = notes if notes else baby.notes
        
        updated_baby = self.baby_controller.update_baby(
            baby.id,
            name = name,
            birthdate = birthdate,
            gender = gender,
            notes = notes
        )
        
        if updated_baby:
            print(f"\nBaby '{updated_baby.name}' updated successfully.")
        else:
            print("\nFailed to update baby information.")
    
    def delete_baby(self):
        """Delete a baby."""
        babies = self.baby_controller.get_all_babies()
        
        if not babies:
            print("\nNo babies found.")
            return
        
        self.list_babies()
        
        try:
            choice = int(input("\nEnter the number of baby to delete (0 to cancel): "))
            if choice == 0:
                return

            if 1 <= choice <= len(babies):
                baby = babies[choice - 1]
                confirm = input(f"Are you sure you want to delete '{baby.name}'? (y/n): ")
                
                if confirm.lower() == 'y':
                    if self.baby_controller.delete_baby(baby.id):
                        print(f"\nBaby '{baby.name}' deleted successfully.")
                    else:
                        print("\nFailed to delete baby.")
                else:
                    print("\nDeletion cancelled.")
            else:
                print("Invalid selection.")
        except ValueError:
            print("Print enter a valid number.")

################## Growth menu ##################

    def track_growth_menu(self):
        """Display growth tracking menu."""
        while True:
            print("\n===== Track Growth =====")
            print("1. Add Growth Record")
            print("2. View Growth Records")
            print("3. Update Growth Record")
            print("4. Delete Growth Record")
            print("0. Back to Main Menu")
            
            choice = input("\nEnter your choice: ")
            
            if choice == '1':
                self.add_growth_record()
            elif choice == '2':
                self.view_growth_records()
            elif choice == '3':
                self.update_growth_record()
            elif choice == '4':
                self.delete_growth_record()
            elif choice == '0':
                break
            else:
                print("Invalid choice. Please try again.")

    def add_growth_record(self):
        """Add a new growth record"""
        
        # Get the baby first
        babies = self.baby_controller.get_all_babies()
        
        if not babies:
            print("\nNo babies found.")
            return
        
        self.list_babies()
        
        try:
            choice = int(input("\nEnter the number of baby (0 to cancel): "))
            if choice == 0:
                return
            
            if 1 <= choice <= len(babies):
                baby = babies[choice - 1]
                self._add_growth_record_form(baby)
            else:
                print("Invalid selection.")
        except ValueError:
            print("Please enter a valid number.")
            
    def _add_growth_record_form(self, baby):
        """Form for adding a growth record."""
        print(f"\n===== Add Growth Record for {baby.name} =====")
        
        # Get date
        while True:
            date_str = input("Date (YYYY-MM-DD) [today]: ")
            if not date_str:
                date = datetime.datetime.now()
                break
            
            try:
                date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
                break
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")
        
        # Get measurements
        try:
            weight_str = input("Weight in kg (leave blank if not measured): ")
            weight = float(weight_str) if weight_str else None
        except ValueError:
            print("Invalid weight. Setting to None.")
            weight = None
        
        try:
            height_str = input("Height in cm (leave blank if not measured): ")
            height = float(height_str) if height_str else None
        except ValueError:
            print("Invalid height. Setting to None.")
            height = None
            
        try:
            hc_str = input("Head circumference in cm (leave blank if not measured): ")
            head_circumference = float(hc_str) if hc_str else None
        except ValueError:
            print("Invalid head circumference. Setting to None.")
            head_circumference = None
        
        notes = input("Notes (optional): ")
        
        # Create the record
        record = self.growth_controller.add_growth_record(
            baby.id,
            date,
            weight,
            height,
            head_circumference,
            notes
        )
        
        if record:
            print("\nGrowth record added successfully.")
        else:
            print("\nFailed to add growth record.")
            
    def view_growth_records(self):
        """View growth records for a baby."""
        # Get the baby first
        babies = self.baby_controller.get_all_babies()
        
        if not babies:
            print("\nNo babies found.")
            return
        
        self.list_babies()
        
        try:
            choice = int(input("\nEnter the number of baby (0 to cancel): "))
            if choice == 0:
                return
            
            if 1 <= choice <= len(babies):
                baby = babies[choice - 1]
                self._display_growth_records(baby)
            else:
                print("Invalid selection.")            
        except ValueError:
            print("Please enter a valid number.")

    def _display_growth_records(self, baby):
        """Display growth record for baby."""
        records = self.growth_controller.get_growth_records(baby.id)
        
        if not records:
            print(f"\n{baby.name} has no growth records.")
            return
        
        print(f"\n===== Growth Records for {baby.name} =====")
        
        # Display as table
        print("\nDate       | Weight (kg) | Height (cm) | Head Circ. (cm) | Notes")
        print("-" * 75)
        
        for record in records:
            date_str = record.date.strftime("%Y-%m-%d")
            weight_str = f"{record.weight:.2f}" if record.weight is not None else "N/A"
            height_str = f"{record.height:.2f}" if record.height is not None else "N/A"
            hc_str = f"{record.head_circumference:.1f}" if record.head_circumference is not None else "N/A"
            notes_str = record.notes if record.notes else ""
            
            print(f"{date_str} | {weight_str:^11} | {height_str:^11} | {hc_str:^15} | {notes_str}")
            
        input("\nPress Enter to continue...")
        
    
    def update_growth_record(self):
        """Update a growth record"""
        
        # Get the baby first
        babies = self.baby_controller.get_all_babies()
        
        if not babies:
            print("\nNo babies found.")
            return
        
        self.list_babies()
        
        try:
            baby_choice = int(input("\nEnter the number of baby (0 to cancel): "))
            if baby_choice == 0:
                return

            if 1 <= baby_choice <= len(babies):
                baby = babies[baby_choice - 1]
                
                # Get the baby's growth records
                records = self.growth_controller.get_growth_records(baby.id)
                
                if not records:
                    print(f"\n{baby.name} has no growth records.")
                    return

                # Display records
                print(f"\n===== Growth Records for {baby.name} =====")
                for i, record in enumerate(records, 1):
                    date_str = record.date.strftime("%Y-%m-%d")
                    weight_str = f"{record.weight} kg" if record.weight is not None else "not recorded"
                    height_str = f"{record.height} kg" if record.height is not None else "not recorded"
                    hc_str = f"{record.head_circumference} cm" if record.head_circumference is not None else "not recorded"
                    
                    print(f"{i}. Date: {date_str}, Weight: {weight_str}, Height: {height_str}, Head: {hc_str}")
                
                # Get the record to update
                record_choice = int(input("\nEnter the number of record to update (0 to cancel): "))
                if record_choice == 0:
                    return
                
                if 1 <= record_choice <= len(records):
                    record = records[record_choice - 1]
                    self._update_growth_record_form(baby, record)
                else:
                    print("Invalid selection.")
            else:
                print("Invalid selection.")
        except ValueError:
            print("Please enter a valid number.")

    def _update_growth_record_form(self, baby, record):
        """Form for updating a growth record."""
        print(f"\n===== Update Growth Record for {baby.name} =====")
        print("Leave fields blank to keep current values.")
        
        # Date
        date_str = input(f"Date [{record.date.strftime('%Y-%m-%d')}]: ")
        if date_str:
            try:
                date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                print("Invalid date format. Keeping current date.")
                date = record.date
        else:
            date = record.date
        
        # Weight
        try:
            current_weight = f"{record.weight}" if record.weight is not None else ""
            weight_str = input(f"Weight in kg [{current_weight}]: ")
            weight = float(weight_str) if weight_str else record.weight
        except ValueError:
            print("Invalid weight. Keeping current value.")
            weight = record.weight
            
        # Height
        try:
            current_height = f"{record.height}" if record.height is not None else ""
            height_str = input(f"height in cm [{current_height}]: ")
            height = float(height_str) if height_str else record.height
        except ValueError:
            print("Invalid height. Keeping current value.")
            height = record.height
            
        # Head circumference
        try:
            current_hc = f"{record.head_circumference}" if record.head_circumference is not None else ""
            hc_str = input(f"Head circumference in cm [{current_hc}]: ")
            head_circumference = float(hc_str) if hc_str else record.head_circumference
        except ValueError:
            print("Invalid head circumference. Keeping current value.")
            head_circumference = record.head_circumference
        
        # Notes
        current_notes = record.notes if record.notes else ""
        notes = input(f"Notes [{current_notes}]: ")
        notes = notes if notes else record.notes
        
        # Update record
        updated_record = self.growth_controller.update_growth_record(
            baby.id,
            record.id,
            date = date,
            weight = weight,
            height = height,
            head_circumference = head_circumference,
            notes = notes
        )
        
        if updated_record:
            print("\nGrowth record updated successfully.")
        else:
            print("\nFailed to update growth record.")
        
    def delete_growth_record(self):
        """Delete a growth record."""
        # Get baby
        babies = self.baby_controller.get_all_babies()
        
        if not babies:
            print("\nNo babies found.")
            return
        
        self.list_babies()
        
        try:
            baby_choice = int(input("\nEnter the number of baby (0 to cancel): "))
            if baby_choice == 0:
                return
            
            if 1 <= baby_choice <= len(babies):
                baby = babies[baby_choice - 1]
                
                # Get baby's growth records
                records = self.growth_controller.get_growth_records(baby.id)
                
                if not records:
                    print(f"\n{baby.name} has no growth records.")
                    return
                
                # Display records
                print(f"\n===== Growth Records for {baby.name} =====")
                for i, record in enumerate(records, 1):
                    date_str = record.date.strftime("%Y-%m-%d")
                    weight_str = f"{record.weight} kg" if record.weight is not None else "not recorded"
                    height_str = f"{record.height} kg" if record.height is not None else "not recorded"
                    hc_str = f"{record.head_circumference} cm" if record.head_circumference is not None else "not recorded"
                    
                    print(f"{i}. Date: {date_str}, Weight: {weight_str}, Height: {height_str}, Head: {hc_str}")
                
                # Get the record to delete
                record_choice = int(input("\nEnter the number of record to delete (0 to cancel): "))
                if record_choice == 0:
                    return
                
                if 1 <= record_choice <= len(records):
                    record = records[record_choice - 1]
                    
                    confirm = input(f"Are you sure you want to delete growth record from {record.date.strftime('%Y-%m-%d')}? (y/n): ")
                    if confirm.lower() == "y":
                        if self.growth_controller.delete_growth_record(baby.id, record.id):
                            print("\nGrowth record deleted successfully.")
                        else:
                            print("\nFailed to delete growth record.")
                    else:
                        print("\nDeletion cancelled.")
                else:
                    print("Invalid selection.")
            else:
                print("Invalid selection.")
        except ValueError:
            print("Please enter a valid number.")

################## Milestone menu ##################

    def track_milestones_menu(self):
        """Display milestone tracking menu."""
        while True:
            print("\n===== Track Milestones =====")
            print("1. Add Milestone")
            print("2. View Milestones")
            print("3. Update Milestone")
            print("4. Delete Milestone")
            print("5. Get Milestone Suggestions")
            print("0. Back to Main Menu")
            
            choice = input("\nEnter your choice: ")
            
            if choice == '1':
                self.add_milestone()
            elif choice == '2':
                self.view_milestone()
            elif choice == '3':
                self.update_milestone()
            elif choice == '4':
                self.delete_milestone()
            elif choice == '5':
                self.get_milestone_suggestions()
            elif choice == '0':
                break
            else:
                print('Invalid choice. Please try again.')
        
    def add_milestone(self):
        """Add a new milestone."""
        #Get baby
        babies = self.baby_controller.get_all_babies()
        
        if not babies:
            print("\nNo babies found.")
            
        self.list_babies()
        
        try:
            choice = int(input('\nEnter the number of baby (0 to cancel): '))
            if choice == 0:
                return
            
            if 1 <= choice <= len(babies):
                baby = babies[choice - 1]
                self._add_milestone_form(baby)
            else:
                print('Invalid selection.')
        except ValueError:
            print('Please enter a valid number.')
    
    def _add_milestone_form(self, baby):
        """Form for adding milestone."""
        print(f"\n===== Add Milestone for {baby.name} =====")
        
        name = input("Milestone name: ")
        if not name:
            print("Milestone name cannot be empty.")
            return
        
        # Category selection
        print("\nCategories:")
        print("1. Physical")
        print("2. Social")
        print("3. Language")
        print("4. Cognitive")
        print("5. Other")
        
        try:
            category_choice = int(input("\nSelect category: "))
            if 1 <= category_choice <= 5:
                categories = ['physical', 'social', 'language', 'cognitive', 'other']
                category = categories[category_choice - 1]
            else:
                print("Invalid category. Using 'other'.")
                category = 'other'
        except ValueError:
            print("Invalid choice. Using 'other'.")
            category = 'other'
            
        # Achievement date
        achieved = input("Has this milestone been achieved? (y/n): ")
        achieved_date = None
        
        if achieved.lower() == 'y':
            while True:
                date_str = input(f"Date achieved (YYYY-MM-DD) [today]: ")
                if not date_str:
                    achieved_date = datetime.datetime.now()
                    break
                
                try:
                    achieved_date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
                    break
                except ValueError:
                    print("Invalid date format. Please use YYYY-MM-DD.")
                    
        # Expected age range
        expected_range = None
        if category != 'other':
            try:
                min_months = int(input("Expected minimum age in months(optional): "))
                max_months = int(input("Expected maximum age in months(optional): "))
                expected_range = {
                    "min_months": min_months,
                    "max_months": max_months
                }
            except ValueError:
                print("Invalid input for expected age range. Leaving blank.")
        
        notes = input("Notes (optional): ")
        
        # Create milestone
        milestone = self.milestone_controller.add_milestone(
            baby.id,
            name,
            category,
            achieved_date,
            expected_range,
            notes
        )
        
        if milestone:
            print("\nMilestone added successfully.")
        else:
            print("\nFailed to add milestone.")
            
    def view_milestone(self):
        """View milestones for a baby."""
        
        # Get baby
        babies = self.baby_controller.get_all_babies()
        
        if not babies:
            print("\nNo babies found.")
            return
        
        self.list_babies()
        
        try:
            choice = int(input("\nEnter the number of baby (0 to cancel): "))
            if choice == 0:
                return
            
            if 1 <= choice <= len(babies):
                baby = babies[choice - 1]
                self._display_milestones(baby)
            else:
                print("Invalid selection.")
        except ValueError:
            print("Please enter a valid number.")
        
    def _display_milestones(self, baby):
        """Display milestones for a baby."""
        milestones = self.milestone_controller.get_milestones(baby.id)
        
        if not milestones:
            print(f"\n{baby.name} has no recorded milestones.")
            return
        
        print(f"\n===== Milestones for {baby.name} =====")
        
        # Group by category
        categories = {}
        for milestone in milestones:
            if milestone.category not in categories:
                categories[milestone.category] = []
            categories[milestone.category].append(milestone)
            
        # Display by category
        for category, cat_milestones in categories.items():
            print(f"\n## {category.capitalize()} ##")
            for i, milestone in enumerate(cat_milestones, 1):
                status = "✓ Achieved" if milestone.is_achieved() else "○ Not achieved"
                date_str = milestone.achieved_date.strftime("%Y-%m-%d") if milestone.achieved_date else "N/A"
                
                print(f"{i}. {milestone.name} - {status}")
                if milestone.achieved_date:
                    print(f"   Date achieved: {date_str}")

                if milestone.expected_range:
                    min_months = milestone.expected_range.get("min_months", "?")
                    max_months = milestone.expected_range.get("max_months", "?")
                    print(f"   Expected age: {min_months}-{max_months} months")
                
                if milestone.notes:
                    print(f"   Notes: {milestone.notes}")
                    
        input("\nPress Enter to continue...")

    def update_milestone(self):
        """Update a milestone."""
        
        # Get baby
        babies = self.baby_controller.get_all_babies()
        
        if not babies:
            print("\nNo babies found.")
            return
        
        self.list_babies()
        
        try:
            baby_choice = int(input("\nEnter the number of baby (0 to cancel): "))
            
            if baby_choice == 0:
                return
            
            if 1 <= baby_choice <= len(babies):
                baby = babies[baby_choice - 1]
                
                # Get baby's milestones
                milestones = self.milestone_controller.get_milestones(baby.id)
                                
                if not milestones:
                    print(f"\n{baby.name} has no recorded milestones.")
                    return
                
                # Display milestones
                print(f"\n===== Milestones for {baby.name} =====")
                for i, milestone in enumerate(milestones, 1):
                    status = "Achieved" if milestone.is_achieved() else "Not achieved"
                    print(f"{i}. {milestone.name} - {status} - Category: {milestone.category}")
                
                # Get milestone to update
                milestone_choice = int(input("\nEnter the number of milestone to update (0 to cancel): "))
                if milestone_choice == 0:
                    return
                
                if 1 <= milestone_choice <= len(milestones):
                    milestone = milestones[milestone_choice - 1]
                    self._update_milestone_form(baby, milestone)
                else:
                    print("Invalid selection.")
            else:
                print("Invalid selection.")
        except ValueError:
            print("Please enter a valid number.")
            
    def _update_milestone_form(self, baby, milestone):
        """Form for updating a milestone."""
        print(f"\n===== Update Milestone for {baby.name} =====")
        print("Leave fields blank to keep current values.")
        
        name = input(f"Name [{milestone.name}]: ")
        name = name if name else milestone.name
        
        # Category selection
        print("\nCategories:")
        print("1. Physical")
        print("2. Social")
        print("3. Language")
        print("4. Cognitive")
        print("5. Other")
        print(f"Current category: {milestone.category}")
        
        try:
            category_choice = input("\nSelect new category (or press Enter to keep current): ")
            if category_choice:
                category_choice = int(category_choice)
                if 1 <= category_choice <= 5:
                    categories = ["physical", "social", "language", "cognitive", "other"]
                    category = categories[category_choice - 1]
                else:
                    print("Invalid category. Keeping current.")
                    category = milestone.category
            else:
                category = milestone.category
        
        except ValueError:
            print("Invalid choice. Keeping current category.")
            category = milestone.category
            
        # Achievement status
        current_status = "achieved" if milestone.is_achieved() else "not achieved"
        status_change = input(f"Current status: {current_status}. Change? (y/n): ")
        
        achieved_date = milestone.achieved_date
        if status_change.lower() == 'y':
            if milestone.is_achieved():
                # If currently achieved, ask if they want to mark as not achieved
                unachieve = input("Mark as not achieved? (y/n): ")
                if unachieve.lower() == 'y':
                    achieved_date = None
            else:
                # If not achieved, ask for achievement date
                achieve = input("Mark as achieved? (y/n): ")
                if achieve.lower() == 'y':
                    while True:
                        date_str = input(f"Date achieved  (YYYY-MM-DD) [Press Enter for today]: ")
                        if not date_str:
                            achieved_date = datetime.datetime.now()
                            break
                        
                        try:
                            achieved_date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
                            break
                        except ValueError:
                            print("Invalid date format. Please use YYYY-MM-DD.")
                            
        # Expected age range
        expected_range = milestone.expected_range
        if category != "other":
            update_range = input("Update expected age range? (y/n): ")
            if update_range.lower() == 'y':
                try:
                    current_min = ""
                    current_max = ""
                    if expected_range:
                        current_min = expected_range.get("min_months", "")
                        current_max = expected_range.get("max_months", "")
                        
                    min_str = input(f"Expected minimum age in months [{current_min}]: ")
                    max_str = input(f"Expected maximum age in months [{current_max}]: ")
                    
                    min_months = int(min_str) if min_str else (expected_range.get("min_months") if expected_range else None)
                    max_months = int(max_str) if max_str else (expected_range.get("max_months") if expected_range else None)
                    
                    if min_months is not None and max_months is not None:
                        expected_range = {
                            "min_months": min_months,
                            "max_months": max_months
                        }
                except ValueError:
                    print("Invalid input for expected range. Keeping current values.")
        
        # Notes
        current_notes = milestone.notes if milestone.notes else ""
        notes = input(f"Notes [{current_notes}]: ")
        notes = notes if notes else milestone.notes
        
        # Update milestone
        updated_milestone = self.milestone_controller.update_milestone(
            baby.id,
            milestone.id,
            name = name,
            category = category,
            achieved_date = achieved_date,
            expected_range = expected_range,
            notes = notes
        )
        
        if updated_milestone:
            print("\nMilestone updated successfully.")
        else:
            print("\nFailed to update milestone.")
        
    def delete_milestone(self):
        """Delete a milestone."""
        
        # Get baby first
        babies = self.baby_controller.get_all_babies()
        
        if not babies:
            print("\nNo babies found.")
        
        self.list_babies()
        
        try:
            baby_choice = int(input("\nEnter the number of baby (0 to cancel): "))
            if baby_choice == 0:
                return
            
            if 1 <= baby_choice <= len(babies):
                baby = babies[baby_choice - 1]
                
                # Get baby milestones
                milestones = self.milestone_controller.get_milestones(baby.id)
                
                if not milestones:
                    print(f"\n{baby.name} has no recorded milestones.")
                    return
                
                # Display milestones
                print(f"\n====== Milestone for {baby.name} =====")
                for i, milestone in enumerate(milestones, 1):
                    status = "Achieved" if milestone.is_achieved() else "Not achieved"
                    print(f"{i}. {milestone.name} - {status} - Category: {milestone.category}")
                
                # Get milestone to delete
                milestone_choice = int(input("\nEnter the number of milestone to delete (0 to cancel): "))
                if milestone_choice == 0:
                    return
                
                if 1 <= milestone_choice <= len(milestones):
                    milestone = milestones[milestone_choice - 1]
                    
                    confirm = input(f"Are you sure you want to delete the milestone '{milestone.name}'? (y/n): ")
                    if confirm.lower() == 'y':
                        if self.milestone_controller.delete_milestone(baby.id, milestone.id):
                            print("\nMilestone deleted successfully.")
                        else:
                            print("\nFailed to delete milestone.")
                    else:
                        print("\nDeletion cancelled.")
                else:
                    print("Invalid selection.")
            else:
                print("Invalid selection.")
        except ValueError:
            print("PLease enter a valid number.")
        
    def get_milestone_suggestions(self):
        """Get milestone suggestions for baby."""
        
        # Get baby
        babies = self.baby_controller.get_all_babies()
        
        if not babies:
            print("\nNo babies found.")
            return
        
        self.list_babies()
        
        try:
            choice = int(input("\nEnter the number of baby (0 to cancel): "))
            if choice == 0:
                return
            
            if 1 <= choice <= len(babies):
                baby = babies[choice - 1]
                
                # Calculate baby's age in months
                age_info = baby.calculate_age()
                months_age = age_info["years"] * 12 + age_info["months"]
                
                # Get milestones suggestions
                suggestions = self.milestone_controller.get_milestone_suggestions(months_age)
                
                if not suggestions:
                    print(f"\nNo milestone suggestions found for {baby.name}'s age ({months_age} months).")
                    return
                
                print(f"f\n===== Milestone Suggestions for {baby.name} =====")
                print(f"Age: {months_age} months\n")
                
                for category, milestones in suggestions.items():
                    print(f"## {category.capitalize()} ##")
                    for i, milestone in enumerate(milestones, 1):
                        min_months = milestone["expected_range"]["min_months"]
                        max_months = milestone["expected_range"]["max_months"]
                        print(f"{i}. {milestone['name']} (typically achieved between {min_months}-{max_months} months)")
                    print()
                
                # Ask if user wants to add any of these milestones
                add_milestone = input("Would you like to add any of these milestones? (y/n): ")
                if add_milestone.lower() == 'y':
                    self._add_milestone_form(baby)
            
            else:
                print("Invalid selection.")
        except ValueError:
            print("Please enter a valid number.")


# TODO: Implement daily logs menu functions
################## Daily logs menu ##################
    def daily_logs_menu(self):
        """Display daily logs menu."""
        while True:
            print("\n===== Daily Logs =====")
            print("1. Add Feeding Log")
            print("2. Add Sleep Log")
            print("3. Add Diaper Log")
            print("4. View Logs")
            print("0. Back to Main Menu")
            
            choice = input("\nEnter your choice: ")
            
            if choice == '1':
                self.add_feeding_log()
            elif choice == '2':
                self.add_sleep_log()
            elif choice == '3':
                self.add_diaper_log()
            elif choice == '4':
                self.view_daily_logs()
            elif choice == '0':
                break
            else:
                print("Invalid choice. Please try again.")
    
    # TODO: Implement add methods for feeding, sleep, diaper logs and view logs method
    def add_feeding_log(self):
        """Add a new feeding log."""
        pass
    
    def add_sleep_log(self):
        """Add a new sleep log"""
        pass
    
    def add_diaper_log(self):
        """Add a new diaper log"""
        pass
    
    def view_daily_logs(self):
        """View daily logs for a baby."""
        pass