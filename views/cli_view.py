# views/cli_view.py

import datetime

class CLIView:
    def __init__(self, baby_controller, growth_controller):
        """_summary_

        Args:
            baby_controller (_type_): _description_
            growth_controller (_type_): _description_
        """
        self.baby_controller = baby_controller
        self.growth_controller = growth_controller

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
        
        birthdate_str = input(f"Birthdate [{baby.birthdate.strftime("%Y-%m-%d")}]: ")
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
        date_str = input(f"Date [{record.date.strftime("%Y-%m-%d")}]: ")
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
                    
                    confirm = input(f"Are you sure you want to delete growth record from {record.date.strftime("%Y-%m-%d")}? (y/n): ")
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