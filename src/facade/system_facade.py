
import bcrypt

class SystemFacade:
    def __init__(self, user_logic, vacation_logic, like_logic, dal):
        self.user_logic = user_logic
        self.vacation_logic = vacation_logic
        self.like_logic = like_logic
        self.dal = dal
        self._current_user = None
        "מאתחל את המשתנים"

    @property
    def current_user(self):
        return self._current_user
    "current user= user"

    def _require_authentication(self):
        if not self._current_user:
            raise ValueError("Authentication required")
        "דרישת התחברות מהמשתמש "

    def _require_admin(self):
        self._require_authentication()
        if self._current_user.get('role') != 2:
            raise ValueError("Unauthorized: Admin access required")
        "בודק האם המשתמש מנהל "
    def validate_email(self,email):
        return self.user_logic.validate_email(email)

    def validate_password(self,password):
        return self.user_logic.validate_password(password)

    def validate_date_of_birth(self, date_of_birth):
        return self.user_logic.validate_date_of_birth(date_of_birth)

    def validate_dates(self, start_date, end_date):
        return self.vacation_logic.validate_dates(start_date, end_date)

    def validate_price(self, price):
        return self.vacation_logic.validate_price(price)

    def register_user(self, user_data):
        self.user_logic.validate_user_data(user_data)
        user_data['password'] = bcrypt.hashpw(user_data['password'].encode('utf-8'), bcrypt.gensalt())
        return self.dal.create_user(user_data)
    "check with the logic if its valid and than take the user data and sent it to the dal to create user "
    "בודק תקינות עם הלוגיק ואם כן שולח לדל להקים משתמש"
    def login(self, email, password):
        user = self.dal.get_user_by_email(email)
        if not user or not bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            raise ValueError("Invalid email or password")
        self._current_user = user
        return user
    "check if the password and the email valid and match if it does its change the current user "
    "בודק האם הסיסמה והמייל תיקנים ותואמים אם כן מעדכן את המשתמש הנוכחי אם לא מעלה הודעה"

    def logout(self):
        self._current_user = None
        "logout from current user account"
        "משנה את המשתמש הנוכחי לכלום "

    def create_vacation(self, vacation_data):
        self._require_admin()
        return self.vacation_logic.create_vacation(vacation_data)
    "allows admin to create vacation"
    "נדרש שהמשתמש יהיה מנהל במידה וכן נותן לו ליצור חופשה "


    def update_vacation(self, vacation_id, vacation_data):
        self._require_admin()
        self.vacation_logic.update_vacation(vacation_id, vacation_data)
        "allows admin to update existing vacation "
        "נדרש שהמשתמש יהיה מנהל במידה וכן נותן לו לעדכן חופשה קיימת"

    def delete_vacation(self, vacation_id):
        self._require_admin()
        self.vacation_logic.delete_vacation(vacation_id)
        "check if the user is admin if it does allows him to delete existing vacation "

    def get_all_vacations(self):
        self._require_authentication()
        return self.vacation_logic.get_all_vacations()
    "if the user connected allows him to see all the vac"

    def like_vacation(self, vacation_id):
        self._require_authentication()
        self.like_logic.add_like(self._current_user['user_id'], vacation_id)
        "if the user connected allows him to like existing vac"

    def unlike_vacation(self, vacation_id):
        self._require_authentication()
        self.like_logic.remove_like(self._current_user['user_id'], vacation_id)
        "if the user connected allows him to unlike the vac"

    def get_user_likes(self):
        self._require_authentication()
        return self.like_logic.get_user_likes(self._current_user['user_id'])
    "if the user connected allows him to see the user likes"
    def get_all_countries(self):
        return self.dal.get_all_countries()
    "get all the countries from the dal"
    def get_vacation_by_id(self, vacation_id):
        self._require_authentication()
        return self.vacation_logic.get_vacation_by_id(vacation_id)
    "if the user connected allows him to get the vac if from vacation_id"

