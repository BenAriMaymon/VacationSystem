import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()


class DatabaseConnection:
    _instance = None
    """
    מחלקת חיבור למסד הנתונים המיישמת תבנית Singleton
    מבטיחה שרק מופע אחד של החיבור למסד הנתונים קיים בכל זמן נתון

    Database Connection class implementing Singleton pattern
    Ensures only one database connection instance exists at any time
    """

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance.connection = None
        return cls._instance

    def connect(self):
        """
        יצירת חיבור למסד הנתונים MySQL
        משתמש במשתני סביבה לפרטי ההתחברות
        מעלה חריגה במקרה של שגיאת התחברות

        Establishes connection to MySQL database
        Uses environment variables for connection details
        Raises exception if connection fails
        """
        try:
            if not self.connection or not self.connection.is_connected():
                self.connection = mysql.connector.connect(
                    host=os.getenv('DB_HOST', 'localhost'),
                    database=os.getenv('DB_NAME', 'vacation_system'),
                    user=os.getenv('DB_USER', 'root'),
                    password=os.getenv('DB_PASSWORD', '')
                )
        except Error as e:
            raise Exception(f"Error connecting to MySQL database: {e}")

    def execute_query(self, query, params=None):
        """
        ביצוע שאילתת SQL במסד הנתונים
        תומך בשאילתות SELECT ושאילתות עדכון
        מחזיר תוצאות עבור שאילתות SELECT ומזהה הכנסה אחרון עבור הכנסות

        Executes SQL query on the database
        Supports both SELECT and modification queries
        Returns results for SELECT queries and last insert ID for insertions
        """
        self.connect()
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params)

            if query.strip().upper().startswith('SELECT'):
                result = cursor.fetchall()
            else:
                self.connection.commit()
                result = [{"last_insert_id": cursor.lastrowid}] if cursor.lastrowid else []

            return result
        except Error as e:
            self.connection.rollback()
            raise Exception(f"Database error: {e}")
        finally:
            cursor.close()


class DAL:
    """
    שכבת גישה לנתונים (DAL) המספקת ממשק לביצוע פעולות במסד הנתונים
    מכילה פונקציות לניהול משתמשים, חופשות, לייקים ומדינות

    Data Access Layer (DAL) providing interface for database operations
    Contains functions for managing users, vacations, likes, and countries
    """

    def __init__(self):
        self.db = DatabaseConnection()

    # User operations
    def create_user(self, user_data):
        """
        יצירת משתמש חדש במערכת
        מקבל מילון עם פרטי המשתמש
        מחזיר את המזהה של המשתמש החדש

        Creates a new user in the system
        Accepts dictionary with user details
        Returns the new user's ID
        """
        query = """
        INSERT INTO users (firstname, lastname, email, password, date_of_birth, role)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (
            user_data['firstname'],
            user_data['lastname'],
            user_data['email'],
            user_data['password'],
            user_data['date_of_birth'],
            user_data.get('role', 1)
        )
        result = self.db.execute_query(query, params)
        return result[0]['last_insert_id']

    def get_user_by_email(self, email):
        """
        שליפת משתמש לפי כתובת אימייל
        מחזיר את פרטי המשתמש או None אם לא נמצא

        Retrieves user by email address
        Returns user details or None if not found
        """
        query = "SELECT * FROM users WHERE email = %s"
        result = self.db.execute_query(query, (email,))
        return result[0] if result else None

    def get_user_by_id(self, user_id):
        """
        שליפת משתמש לפי מזהה
        מחזיר את פרטי המשתמש או None אם לא נמצא

        Retrieves user by ID
        Returns user details or None if not found
        """
        query = "SELECT * FROM users WHERE user_id = %s"
        result = self.db.execute_query(query, (user_id,))
        return result[0] if result else None

    # Vacation operations
    def create_vacation(self, vacation_data):
        """
        יצירת חופשה חדשה במערכת
        מקבל מילון עם פרטי החופשה
        מחזיר את המזהה של החופשה החדשה

        Creates a new vacation in the system
        Accepts dictionary with vacation details
        Returns the new vacation's ID
        """
        query = """
        INSERT INTO vacations (vacation_title, country, start_date, end_date, price, img_url)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (
            vacation_data['vacation_title'],
            vacation_data['country'],
            vacation_data['start_date'],
            vacation_data['end_date'],
            vacation_data['price'],
            vacation_data.get('img_url')
        )
        result = self.db.execute_query(query, params)
        return result[0]['last_insert_id']

    def update_vacation(self, vacation_id, vacation_data):
        """
        עדכון פרטי חופשה קיימת
        מקבל מזהה חופשה ומילון עם הפרטים המעודכנים

        Updates existing vacation details
        Accepts vacation ID and dictionary with updated details
        """
        query = """
        UPDATE vacations
        SET vacation_title = %s, country = %s, start_date = %s, end_date = %s, 
            price = %s, img_url = %s
        WHERE vacation_id = %s
        """
        params = (
            vacation_data['vacation_title'],
            vacation_data['country'],
            vacation_data['start_date'],
            vacation_data['end_date'],
            vacation_data['price'],
            vacation_data.get('img_url'),
            vacation_id
        )
        self.db.execute_query(query, params)

    def delete_vacation(self, vacation_id):
        """
        מחיקת חופשה מהמערכת
        מקבל מזהה חופשה למחיקה

        Deletes vacation from the system
        Accepts vacation ID to delete
        """
        query = "DELETE FROM vacations WHERE vacation_id = %s"
        self.db.execute_query(query, (vacation_id,))

    def get_all_vacations(self):
        """
        שליפת כל החופשות מהמערכת
        כולל שם המדינה ומספר הלייקים

        Retrieves all vacations from the system
        Includes country name and number of likes
        """
        query = """
        SELECT v.*, c.country_name, COUNT(l.like_id) as total_likes 
        FROM vacations v 
        LEFT JOIN likes l ON v.vacation_id = l.vacation_id 
        JOIN countries c ON v.country = c.country_id 
        GROUP BY v.vacation_id
        """
        return self.db.execute_query(query)

    def get_vacation_by_id(self, vacation_id):
        """
        שליפת חופשה לפי מזהה
        כולל שם המדינה ומספר הלייקים

        Retrieves vacation by ID
        Includes country name and number of likes
        """
        query = """
        SELECT v.*, c.country_name, COUNT(l.like_id) as total_likes 
        FROM vacations v 
        LEFT JOIN likes l ON v.vacation_id = l.vacation_id 
        JOIN countries c ON v.country = c.country_id 
        WHERE v.vacation_id = %s
        GROUP BY v.vacation_id
        """
        result = self.db.execute_query(query, (vacation_id,))
        return result[0] if result else None

    # Like operations
    def add_like(self, user_id, vacation_id):
        """
        הוספת לייק לחופשה
        מקבל מזהה משתמש ומזהה חופשה

        Adds a like to a vacation
        Accepts user ID and vacation ID
        """
        query = "INSERT INTO likes (user_id, vacation_id) VALUES (%s, %s)"
        self.db.execute_query(query, (user_id, vacation_id))

    def remove_like(self, user_id, vacation_id):
        """
        הסרת לייק מחופשה
        מקבל מזהה משתמש ומזהה חופשה

        Removes a like from a vacation
        Accepts user ID and vacation ID
        """
        query = "DELETE FROM likes WHERE user_id = %s AND vacation_id = %s"
        self.db.execute_query(query, (user_id, vacation_id))

    def get_user_likes(self, user_id):
        """
        שליפת כל החופשות שמשתמש מסוים סימן בלייק
        מחזיר רשימה של חופשות כולל שם המדינה

        Retrieves all vacations liked by a specific user
        Returns list of vacations including country name
        """
        query = """
        SELECT v.*, c.country_name
        FROM vacations v
        JOIN likes l ON v.vacation_id = l.vacation_id
        JOIN countries c ON v.country = c.country_id
        WHERE l.user_id = %s
        """
        return self.db.execute_query(query, (user_id,))

    def check_like_exists(self, user_id, vacation_id):
        """
        בדיקה האם קיים לייק של משתמש מסוים לחופשה מסוימת
        מחזיר True אם קיים לייק, אחרת False

        Checks if a specific user has liked a specific vacation
        Returns True if like exists, False otherwise
        """
        query = "SELECT * FROM likes WHERE user_id = %s AND vacation_id = %s"
        result = self.db.execute_query(query, (user_id, vacation_id))
        return bool(result)

    # Country operations
    def get_all_countries(self):
        """
        שליפת כל המדינות מהמערכת
        מחזיר רשימה של כל המדינות הזמינות

        Retrieves all countries from the system
        Returns list of all available countries
        """
        query = "SELECT * FROM countries"
        return self.db.execute_query(query)

    def get_country_by_id(self, country_id):
        """
        שליפת מדינה לפי מזהה
        מחזיר את פרטי המדינה או None אם לא נמצאה

        Retrieves country by ID
        Returns country details or None if not found
        """
        query = "SELECT * FROM countries WHERE country_id = %s"
        result = self.db.execute_query(query, (country_id,))
        return result[0] if result else None