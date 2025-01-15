from utils.dal import DAL
from logic.user_logic import UserLogic
from logic.vacation_logic import VacationLogic
from logic.like_logic import LikeLogic
from facade.system_facade import SystemFacade
class VacationManagementSystem:
    def __init__(self):
        self.dal = DAL()
        self.user_logic = UserLogic(self.dal)
        self.vacation_logic = VacationLogic(self.dal)
        self.like_logic = LikeLogic(self.dal)
        self.facade = SystemFacade(self.user_logic, self.vacation_logic, self.like_logic, self.dal)
    def display_menu(self):
        if not self.facade.current_user:
            print("\n- Vacation Management System -")
            print("1. Login")
            print("2. Register")
            print("3. Exit")
        else:
            print(f"\n- Welcome {self.facade.current_user['firstname']} -")
            if self.facade.current_user['role'] == 2:
                #admin features
                print("1. View All Vacations")
                print("2. Add Vacation")
                print("3. Edit Vacation")
                print("4. Delete Vacation")
                print("5. Logout")
            else:
                #user features
                print("1. View All Vacations")
                print("2. View My Liked Vacations")
                print("3. Like/Unlike Vacation")
                print("4. Logout")
    def register(self):
        print("\n- Register New User -")
        try:
            user_data = {
                'firstname': input("Enter first name: "),
                'lastname': input("Enter last name: "),
                'email': input("Enter email: "),
                'password': input("Enter password: "),
                'date_of_birth': input("Enter date of birth (YYYY-MM-DD): "),
                'role': 1 #everybody is a user
            }
            self.facade.register_user(user_data)
            print("Registration successful! Please login.")
        except ValueError as e:
            print(f"Error: {e}")
    def login(self):
        print("\n- Login -")
        try:
            email = input("Enter email: ")
            password = input("Enter password: ")
            self.facade.login(email, password)
            print("Login successful!")
        except ValueError as e:
            print(f"Error: {e}")
    def add_vacation(self):
        print("\n- Add New Vacation -")
        try:
            countries = self.facade.get_all_countries()
            print("\nAvailable Countries:")
            for country in countries:
                print(f"{country['country_id']}. {country['country_name']}")

            vacation_data = {
                'vacation_title': input("Enter vacation title: "),
                'country': int(input("Enter country ID: ")),
                'start_date': input("Enter start date (YYYY-MM-DD): "),
                'end_date': input("Enter end date (YYYY-MM-DD): "),
                'price': float(input("Enter price: ")),
                'img_url': input("Enter image URL (optional): ") or None
            }
            self.facade.create_vacation(vacation_data)
            print("Vacation added successfully!")
        except ValueError as e:
            print(f"Error: {e}")
    def view_vacations(self):
        print("\n- All Vacations -")
        try:
            vacations = self.facade.get_all_vacations()
            for vacation in vacations:
                print(f"\nID: {vacation['vacation_id']}")
                print(f"Title: {vacation['vacation_title']}")
                print(f"Country: {vacation['country_name']}")
                print(f"Dates: {vacation['start_date']} to {vacation['end_date']}")
                print(f"Price: ${vacation['price']}")
                print(f"Likes: {vacation['total_likes']}")
        except ValueError as e:
            print(f"Error: {e}")
    def handle_likes(self):
        print("\n- Like/Unlike Vacation -")
        try:
            vacation_id = int(input("Enter vacation ID: "))
            action = input("Enter 'like' or 'unlike': ").lower()
            if action == 'like':
                self.facade.like_vacation(vacation_id)
                print("Vacation liked successfully!")
            elif action == 'unlike':
                self.facade.unlike_vacation(vacation_id)
                print("Vacation unliked successfully!")
            else:
                print("Invalid action")
        except ValueError as e:
            print(f"Error: {e}")
    def view_liked_vacations(self):
        print("\n- My Liked Vacations -")
        try:
            liked_vacations = self.facade.get_user_likes()
            if not liked_vacations:
                print("You haven't liked any vacations yet.")
            for vacation in liked_vacations:
                print(f"\nID: {vacation['vacation_id']}")
                print(f"Title: {vacation['vacation_title']}")
                print(f"Country: {vacation['country_name']}")
                print(f"Dates: {vacation['start_date']} to {vacation['end_date']}")
                print(f"Price: ${vacation['price']}")
        except ValueError as e:
            print(f"Error: {e}")
    def edit_vacation(self):
        print("\n- Edit Vacation -")
        try:
            vacation_id = int(input("Enter vacation ID to edit: "))
            vacation = self.facade.get_vacation_by_id(vacation_id)
            if not vacation:
                print("Vacation not found")
                return

            countries = self.facade.get_all_countries()
            print("\nAvailable Countries:")
            for country in countries:
                print(f"{country['country_id']}. {country['country_name']}")

            vacation_data = {
                'vacation_title': input(f"Enter new title ({vacation['vacation_title']}): ") or vacation[
                    'vacation_title'],
                'country': int(input(f"Enter new country ID ({vacation['country']}): ") or vacation['country']),
                'start_date': input(f"Enter new start date ({vacation['start_date']}): ") or str(
                    vacation['start_date']),
                'end_date': input(f"Enter new end date ({vacation['end_date']}): ") or str(vacation['end_date']),
                'price': float(input(f"Enter new price ({vacation['price']}): ") or vacation['price']),
                'img_url': input(f"Enter new image URL ({vacation['img_url']}): ") or vacation['img_url']
            }
            self.facade.update_vacation(vacation_id, vacation_data)
            print("Vacation updated successfully!")
        except ValueError as e:
            print(f"Error: {e}")
    def delete_vacation(self):
        print("\n- Delete Vacation -")
        try:
            vacation_id = int(input("Enter vacation ID to delete: "))
            confirm = input("Are you sure you want to delete this vacation? (yes/no): ")
            if confirm.lower() == 'yes':
                self.facade.delete_vacation(vacation_id)
                print("Vacation deleted successfully!")
            else:
                print("Deletion cancelled")
        except ValueError as e:
            print(f"Error: {e}")
    def run(self):
        while True:
            self.display_menu()
            choice = input("\nEnter your choice: ")

            if not self.facade.current_user:
                if choice == '1':
                    self.login()
                elif choice == '2':
                    self.register()
                elif choice == '3':
                    print("Goodbye!")
                    break
            else:
                if self.facade.current_user['role'] == 2:  # admin selections
                    if choice == '1':
                        self.view_vacations()
                    elif choice == '2':
                        self.add_vacation()
                    elif choice == '3':
                        self.edit_vacation()
                    elif choice == '4':
                        self.delete_vacation()
                    elif choice == '5':
                        self.facade.logout()
                        print("Logged out successfully!")
                else:  # user selections
                    if choice == '1':
                        self.view_vacations()
                    elif choice == '2':
                        self.view_liked_vacations()
                    elif choice == '3':
                        self.handle_likes()
                    elif choice == '4':
                        self.facade.logout()
                        print("Logged out successfully!")
if __name__ == "__main__":
    system = VacationManagementSystem()
    system.run()
