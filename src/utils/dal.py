import mysql.connector
from mysql.connector import Error
from typing import Dict, List, Optional, Any
import os
from dotenv import load_dotenv

load_dotenv()


class DAL:
    """
    מחלקת DAL (Data Access Layer) - שכבת גישה לנתונים
    מספקת ממשק מאובטח ומאורגן לביצוע פעולות מול בסיס הנתונים
    """

    def __init__(self):
        """
        יצירת התחברות לבסיס הנתונים
        במקרה של שגיאה, מדפיסה הודעת שגיאה ומאפסת את החיבור
        """
        try:
            self.connection = mysql.connector.connect(
                host=os.getenv('DB_HOST', 'localhost'),
                database=os.getenv('DB_NAME', 'vacation_system'),
                user=os.getenv('DB_USER', 'root'),
                password=os.getenv('DB_PASSWORD', '036320884'),
                autocommit=True
            )
        except mysql.connector.Error as err:
            print(f"Error connecting to database: {err}")
            self.connection = None

    def _validate_query_params(self, query, params):
        """
        בדיקת תקינות הפרמטרים של השאילתה
        """
        if not isinstance(query, str):
            raise ValueError("Query must be a string.")
        if params is not None and not isinstance(params, tuple):
            raise ValueError("Params must be a tuple or None.")

    def _execute_query(self, query: str, params: tuple = None, fetchall: bool = False, fetchone: bool = False):
        """
        הרצת שאילתה עם אפשרויות שונות לקבלת התוצאות
        """
        self._validate_query_params(query, params)
        if self.connection:
            try:
                with self.connection.cursor(dictionary=True) as cursor:
                    cursor.execute(query, params)
                    if fetchall:
                        return cursor.fetchall()
                    elif fetchone:
                        return cursor.fetchone()
                    else:
                        return cursor.rowcount
            except mysql.connector.Error as err:
                print(f"Error executing query: {err}")
        return None

    def get_table(self, query: str, params: tuple = None) -> List[Dict[str, Any]]:
        """שליפת כל השורות מטבלה"""
        return self._execute_query(query, params, fetchall=True)

    def get_scalar(self, query: str, params: tuple = None) -> Any:
        """שליפת ערך בודד (שורה אחת)"""
        return self._execute_query(query, params, fetchone=True)

    def insert(self, query: str, params: tuple = None):
        """הוספת נתונים לטבלה"""
        return self._execute_query(query, params)

    def update(self, query: str, params: tuple = None):
        """עדכון נתונים בטבלה"""
        return self._execute_query(query, params)

    def delete(self, query: str, params: tuple = None):
        """מחיקת נתונים מטבלה"""
        return self._execute_query(query, params)

    def close(self):
        """סגירת החיבור לבסיס הנתונים"""
        if self.connection:
            self.connection.close()

    def __enter__(self):
        """בלוק ה-with"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """סיום בלוק ה-with"""
        if self.connection:
            self.close()
            print("Connection Closed!")


# User operations
class UserDAL(DAL):

    def create_user(self, user_data: Dict) -> int:
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
            user_data.get('role', 1)  # Default to regular user role
        )
        return self.insert(query, params)

    def get_user_by_email(self, email: str) -> Optional[Dict]:
        query = "SELECT * FROM users WHERE email = %s"
        result = self.get_scalar(query, (email,))
        return result

    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        query = "SELECT * FROM users WHERE user_id = %s"
        result = self.get_scalar(query, (user_id,))
        return result


# Vacation operations
class VacationDAL(DAL):

    def create_vacation(self, vacation_data: Dict) -> int:
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
        return self.insert(query, params)

    def update_vacation(self, vacation_id: int, vacation_data: Dict) -> None:
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
        self.update(query, params)

    def delete_vacation(self, vacation_id: int) -> None:
        query = "DELETE FROM vacations WHERE vacation_id = %s"
        self.delete(query, (vacation_id,))

    def get_all_vacations(self) -> List[Dict]:
        query = """
        SELECT v.*, c.country_name, COUNT(l.like_id) as total_likes 
        FROM vacations v 
        LEFT JOIN likes l ON v.vacation_id = l.vacation_id 
        JOIN countries c ON v.country = c.country_id 
        GROUP BY v.vacation_id
        """
        return self.get_table(query)

    def get_vacation_by_id(self, vacation_id: int) -> Optional[Dict]:
        query = """
        SELECT v.*, c.country_name, COUNT(l.like_id) as total_likes 
        FROM vacations v 
        LEFT JOIN likes l ON v.vacation_id = l.vacation_id 
        JOIN countries c ON v.country = c.country_id 
        WHERE v.vacation_id = %s
        GROUP BY v.vacation_id
        """
        result = self.get_scalar(query, (vacation_id,))
        return result


# Example Usage
if __name__ == '__main__':
    with DAL() as dal:
        # Example for vacation CRUD
        vacation_data = {
            'vacation_title': 'Beach Paradise',
            'country': 1,  # Country ID
            'start_date': '2025-01-01',
            'end_date': '2025-01-14',
            'price': 1000
        }
        vacation_id = dal.create_vacation(vacation_data)
        print(f"Vacation created with ID: {vacation_id}")

        vacations = dal.get_all_vacations()
        for vacation in vacations:
            print(f"Vacation title: {vacation['vacation_title']}, Country: {vacation['country_name']}")

        # User operations
        user_data = {
            'firstname': 'John',
            'lastname': 'Doe',
            'email': 'john.doe@example.com',
            'password': 'password123',
            'date_of_birth': '1990-01-01'
        }
        user_dal = UserDAL()
        user_id = user_dal.create_user(user_data)
        print(f"User created with ID: {user_id}")
