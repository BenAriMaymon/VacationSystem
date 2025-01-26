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
                print("1. View All Vacations")
                print("2. Add Vacation")
                print("3. Edit Vacation")
                print("4. Delete Vacation")
                print("5. Logout")
            else:
                print("1. View All Vacations")
                print("2. View My Liked Vacations")
                print("3. Like/Unlike Vacation")
                print("4. Logout")

    def register(self):
        print("\n- Register New User -")
        try:
            while True:
                firstname = input("Enter first name: ").strip()
                if not firstname:
                    print("Error: First name cannot be empty")
                    continue
                break

            while True:
                lastname = input("Enter last name: ").strip()
                if not lastname:
                    print("Error: Last name cannot be empty")
                    continue
                break

            while True:
                email = input("Enter email: ").strip()
                try:
                    self.facade.validate_email(email)
                    break
                except ValueError as e:
                    print(f"Error: {e}")

            while True:
                password = input("Enter password: ").strip()
                try:
                    self.facade.validate_password(password)
                    break
                except ValueError as e:
                    print(f"Error: {e}")

            while True:
                date_of_birth = input("Enter date of birth (YYYY-MM-DD): ").strip()
                try:
                    self.facade.validate_date_of_birth(date_of_birth)
                    break
                except ValueError as e:
                    print(f"Error: {e}")

            user_data = {
                'firstname': firstname,
                'lastname': lastname,
                'email': email,
                'password': password,
                'date_of_birth': date_of_birth,
                'role': 1
            }
            self.facade.register_user(user_data)
            print("Registration successful! Please login.")
        except ValueError as e:
            print(f"Error: {e}")

    def login(self):
        print("\n- Login -")
        while True:
            email = input("Enter email: ").strip()
            try:
                self.facade.validate_email(email)
                break
            except ValueError as e:
                print(f"Error: {e}")

        password = input("Enter password: ")
        try:
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

            while True:
                title = input("Enter vacation title: ").strip()
                if not title:
                    print("Error: Title cannot be empty")
                    continue
                break

            while True:
                try:
                    country = int(input("Enter country ID: "))
                    if not any(c['country_id'] == country for c in countries):
                        print("Error: Invalid country ID")
                        continue
                    break
                except ValueError:
                    print("Error: Please enter a valid number")

            while True:
                start_date = input("Enter start date (YYYY-MM-DD): ").strip()
                end_date = input("Enter end date (YYYY-MM-DD): ").strip()
                try:
                    self.facade.validate_dates(start_date, end_date)
                    break
                except ValueError as e:
                    print(f"Error: {e}")

            while True:
                try:
                    price = float(input("Enter price: "))
                    self.facade.validate_price(price)
                    break
                except ValueError as e:
                    print(f"Error: {e}")

            img_url = input("Enter image URL (optional): ") or None

            vacation_data = {
                'vacation_title': title,
                'country': country,
                'start_date': start_date,
                'end_date': end_date,
                'price': price,
                'img_url': img_url
            }
            self.facade.create_vacation(vacation_data)
            print("Vacation added successfully!")
        except ValueError as e:
            print(f"Error: {e}")
    def edit_vacation(self):
        print("\n- Edit Vacation -")
        try:
            while True:
                try:
                    vacation_id = int(input("Enter vacation ID to edit: "))
                    vacation = self.facade.get_vacation_by_id(vacation_id)
                    if not vacation:
                        print("Error: Vacation not found")
                        continue
                    break
                except ValueError:
                    print("Error: Please enter a valid number")

            countries = self.facade.get_all_countries()
            print("\nAvailable Countries:")
            for country in countries:
                print(f"{country['country_id']}. {country['country_name']}")

            title = input(f"Enter new title ({vacation['vacation_title']}): ").strip()
            if not title:
                title = vacation['vacation_title']

            country = vacation['country']
            country_input = input(f"Enter new country ID ({vacation['country']}): ").strip()
            if country_input:
                try:
                    country = int(country_input)
                    if not any(c['country_id'] == country for c in countries):
                        print("Warning: Invalid country ID, keeping original value")
                        country = vacation['country']
                except ValueError:
                    print("Warning: Invalid country ID, keeping original value")

            start_date = input(f"Enter new start date ({vacation['start_date']}): ").strip() or str(
                vacation['start_date'])
            end_date = input(f"Enter new end date ({vacation['end_date']}): ").strip() or str(vacation['end_date'])

            try:
                self.facade.validate_dates(start_date, end_date)
            except ValueError as e:
                print(f"Warning: {e}, keeping original dates")
                start_date = str(vacation['start_date'])
                end_date = str(vacation['end_date'])

            price = vacation['price']
            price_input = input(f"Enter new price ({vacation['price']}): ").strip()
            if price_input:
                try:
                    price = float(price_input)
                    self.facade.validate_price(price)
                except ValueError as e:
                    print(f"Warning: {e}, keeping original value")
                    price = vacation['price']

            img_url = input(f"Enter new image URL ({vacation['img_url']}): ").strip() or vacation['img_url']

            vacation_data = {
                'vacation_title': title,
                'country': country,
                'start_date': start_date,
                'end_date': end_date,
                'price': price,
                'img_url': img_url
            }
            self.facade.update_vacation(vacation_id, vacation_data)
            print("Vacation updated successfully!")
        except ValueError as e:
            print(f"Error: {e}")
    def delete_vacation(self):
        print("\n- Delete Vacation -")
        try:
            while True:
                try:
                    vacation_id = int(input("Enter vacation ID to delete: "))
                    if not self.facade.get_vacation_by_id(vacation_id):
                        print("Error: Vacation not found")
                        continue
                    break
                except ValueError:
                    print("Error: Please enter a valid number")

            while True:
                confirm = input("Are you sure you want to delete this vacation? (yes/no): ").lower()
                if confirm not in ['yes', 'no']:
                    print("Error: Please enter 'yes' or 'no'")
                    continue
                break

            if confirm == 'yes':
                self.facade.delete_vacation(vacation_id)
                print("Vacation deleted successfully!")
            else:
                print("Deletion cancelled")
        except ValueError as e:
            print(f"Error: {e}")

    def handle_likes(self):
        print("\n- Like/Unlike Vacation -")
        try:
            while True:
                try:
                    vacation_id = int(input("Enter vacation ID: "))
                    if not self.facade.get_vacation_by_id(vacation_id):
                        print("Error: Vacation not found")
                        continue
                    break
                except ValueError:
                    print("Error: Please enter a valid number")

            while True:
                action = input("Enter 'like' or 'unlike': ").lower()
                if action not in ['like', 'unlike']:
                    print("Error: Please enter 'like' or 'unlike'")
                    continue
                break

            if action == 'like':
                self.facade.like_vacation(vacation_id)
                print("Vacation liked successfully!")
            else:
                self.facade.unlike_vacation(vacation_id)
                print("Vacation unliked successfully!")
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

    def run(self):
        while True:
            self.display_menu()
            choice = input("\nEnter your choice: ")
            if not choice.isdigit():
                print("Error: Please enter a valid number")
                continue

            if not self.facade.current_user:
                if choice == '1':
                    self.login()
                elif choice == '2':
                    self.register()
                elif choice == '3':
                    print("Goodbye!")
                    break
                else:
                    print("Invalid choice")
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
                    else:
                        print("Invalid choice")
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
                    else:
                        print("Invalid choice")

if __name__ == "__main__":
    system = VacationManagementSystem()
    system.run()