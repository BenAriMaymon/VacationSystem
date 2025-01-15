from datetime import datetime


class VacationLogic:
    def __init__(self, dal):
        self.dal = dal

    """
        ולידציה של תאריכי החופשה
         אם הפורמט של התאריכים תקין (YYYY MM DD)
         אם תאריך ההתחלה נמצא בעתיד
         אם תאריך הסיום מאוחר מתאריך ההתחלה

        Vacation Dates Validation:
        Validates the format of start and end dates (YYYY MM DD)
        Ensures the start date is in the future
        Ensures the end date is after the start date
        """

    def validate_dates(self, start_date, end_date):
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d').date()
            end = datetime.strptime(end_date, '%Y-%m-%d').date()
            today = datetime.now().date()

            if start <= today:
                raise ValueError("Start date must be in the future")
            if end <= start:
                raise ValueError("End date must be after start date")
            return True
        except ValueError as e:
            if str(e) in ["Start date must be in the future", "End date must be after start date"]:
                raise
            raise ValueError("Invalid date format. Use YYYY-MM-DD")

    """
    ולידציה של מחיר החופשה
     אם המחיר הוא ערך מספרי חוקי
     אם המחיר הוא בטווח שבין 1000 ל10000 

    Vacation Price Validation:
    Validates if the price is a valid numeric value
    Ensures the price is between one thousand and ten thousand dollars
    """

    def validate_price(self, price):
        try:
            price_float = float(price)
            if not 1000 <= price_float <= 10000:
                raise ValueError("Price must be between $1,000 and $10,000")
            return True
        except ValueError as e:
            if "Price must be between" in str(e):
                raise
            raise ValueError("Invalid price format")

    """
        ולידציה של נתוני החופשה
         שכל השדות החיוניים קיימים ואינם ריקים
         אם תאריכי החופשה תקינים באמצעות הפונקציה validate_dates
         אם המחיר תקין ועומד בדרישות באמצעות הפונקציה validate_price
         אם הקוד של המדינה תקין על ידי בדיקה מול בסיס הנתונים

        Vacation Data Validation:
        Ensures all required fields are present and not empty
        Validates dates using the validate_dates function
        Validates price using the validate_price function
        Validates the country code by checking the database
        """

    def validate_vacation_data(self, vacation_data):
        required_fields = ['vacation_title', 'country', 'start_date', 'end_date', 'price']
        for field in required_fields:
            if field not in vacation_data or not vacation_data[field]:
                raise ValueError(f"{field} is required")

        self.validate_dates(vacation_data['start_date'], vacation_data['end_date'])
        self.validate_price(vacation_data['price'])

        country = self.dal.get_country_by_id(vacation_data['country'])
        if not country:
            raise ValueError("Invalid country selection")

        return True
    """
    יצירת חופשה חדשה
    הפונקציה בודקת את נתוני החופשה באמצעות הפונקציה validate_vacation_data
    ולאחר מכן יוצרת חופשה חדשה בבסיס הנתונים

    Create Vacation:
    Validates vacation data using the validate_vacation_data function
    Creates a new vacation in the database
    """
    def create_vacation(self, vacation_data):
        self.validate_vacation_data(vacation_data)
        return self.dal.create_vacation(vacation_data)
    """
    עדכון חופשה קיימת
    הפונקציה בודקת את נתוני החופשה באמצעות הפונקציה validate_vacation_data
    ולאחר מכן מעדכנת חופשה קיימת בבסיס הנתונים

    Update Vacation:
    Validates vacation data using the validate_vacation_data function
    Updates an existing vacation in the database
    """
    def update_vacation(self, vacation_id, vacation_data):
        self.validate_vacation_data(vacation_data)
        existing_vacation = self.dal.get_vacation_by_id(vacation_id)
        if not existing_vacation:
            raise ValueError("Vacation not found")
        self.dal.update_vacation(vacation_id, vacation_data)
    """
    מחיקת חופשה
    הפונקציה בודקת אם החופשה קיימת בבסיס הנתונים
    ואם כן, מוחקת אותה

    Delete Vacation:
    Checks if the vacation exists in the database
    Deletes the vacation if it exists
    """
    def delete_vacation(self, vacation_id):
        existing_vacation = self.dal.get_vacation_by_id(vacation_id)
        if not existing_vacation:
            raise ValueError("Vacation not found")
        self.dal.delete_vacation(vacation_id)
    """
    שליפת כל החופשות
    הפונקציה מחזירה את כל רשומות החופשות הקיימות בבסיס הנתונים

    Get All Vacations:
    Retrieves all vacation records from the database
    """
    def get_all_vacations(self):
        return self.dal.get_all_vacations()
    """
    שליפת חופשה לפי מזהה
    הפונקציה מחזירה חופשה מסוימת לפי מזהה החופשה

    Get Vacation By ID:
    Retrieves a specific vacation by its ID
    """
    def get_vacation_by_id(self, vacation_id):
        return self.dal.get_vacation_by_id(vacation_id)