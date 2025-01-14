from datetime import datetime
from dateutil.relativedelta import relativedelta


class UserLogic:
    def __init__(self, dal):
        self.dal = dal

    """"ולידציה של סיסמא
    הפונקציה בודקת אם קיים בסיסמא שהתקבלה לפחות 6 תווים
    לפחות אות אחת גדולה
    לפחות אות אחת קטנה
    לפחות מספר אחד
    לפחות תו אחד מיוחד

    Password validation:
    At least 6 characters
    At least one of:
    Uppercase letter
    Lowercase letter
    Number
    Special character
    
"""
    def validate_password(self, password):

        special_characters = "!@#$%^&*()_+-=\|?><~"

        if len(password) < 6:
            raise ValueError("Password must be at least 6 characters long")

        if not any(char.isupper() for char in password):
            raise ValueError("Password must contain at least one uppercase letter")

        if not any(char.islower() for char in password):
            raise ValueError("Password must contain at least one lowercase letter")

        if not any(char.isdigit() for char in password):
            raise ValueError("Password must contain at least one number")

        if not any(char in special_characters for char in password):
            raise ValueError(f"Password must contain at least one special character ({special_characters})")

        return True

        """"ולידציה של מייל
        הפונקציה בודקת
        אם המייל מכיל @
        אם התחלת המייל לא מכילה אותיות לא חוקיות
        אם יש נקודה בסיומת
        ואם הסיומת חוקית
        
        Email validation:
        Presence of @ symbol
        local part contains only valid characters
        domain part has at least 2 characters long and be alphanumeric

    """
    def validate_email(self, email):
        if "@" not in email or email.count("@") != 1:
            raise ValueError("Invalid email format: missing or multiple '@' symbols")

        local_part, domain = email.split("@", 1)

        if not local_part or any(
                char not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._%+-" for char in
                local_part):
            raise ValueError("Invalid email format: invalid characters in the local part")

        if "." not in domain or domain.startswith(".") or domain.endswith("."):
            raise ValueError("Invalid email format: invalid domain structure")

        domain_parts = domain.split(".")
        if any(not part.isalnum() or not part for part in domain_parts):
            raise ValueError("Invalid email format: invalid characters in the domain")

        if len(domain_parts[-1]) < 2:
            raise ValueError("Invalid email format: domain suffix must be at least 2 characters long")

        return True

    """
    ולידציה של תאריך לידה
    הפונקציה בודקת
     אם הפורמט של תאריך הלידה תקין (YYYY-MM-DD)
     אם תאריך הלידה חוקי ואינו גורם לשגיאה
     אם גיל המשתמש לפחות 18 שנים

    Date of Birth Validation:
    Validates the format of the date of birth (YYYY-MM-DD)
    Checks if the date is valid
    Ensures the user is at least 18 years old
    """

    def validate_date_of_birth(self, date_of_birth):
        try:
            dob = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
            age = relativedelta(datetime.now().date(), dob).years
            if age < 18:
                raise ValueError("User must be at least 18 years old")
            return True
        except ValueError as e:
            if "must be at least 18 years old" in str(e):
                raise
            raise ValueError("Invalid date format. Use YYYY-MM-DD")

    """
    ולידציה של נתוני משתמש
     שכל השדות החיוניים קיימים ואינם ריקים
     אם כתובת האימייל תקינה באמצעות הפונקציה validate_email
     אם הסיסמה עומדת בדרישות באמצעות הפונקציה validate_password
     אם תאריך הלידה תקין ועומד בדרישות גיל באמצעות הפונקציה validate_date_of_birth

    User Data Validation:
    Ensures all required fields are present and not empty
    Validates email using the validate_email function
    Validates password using the validate_password function
    Validates date of birth using the validate_date_of_birth function
    """

    def validate_user_data(self, user_data):
        required_fields = ['firstname', 'lastname', 'email', 'password', 'date_of_birth']
        for field in required_fields:
            if field not in user_data or not user_data[field]:
                raise ValueError(f"{field} is required")
        self.validate_email(user_data['email'])
        self.validate_password(user_data['password'])
        self.validate_date_of_birth(user_data['date_of_birth'])
        return True