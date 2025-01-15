import mysql.connector
from mysql.connector import Error
from typing import Dict, List, Optional, Any
import os
from dotenv import load_dotenv

load_dotenv()


class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance.connection = None
        return cls._instance

    def connect(self):
        try:
            if not self.connection or not self.connection.is_connected():
                self.connection = mysql.connector.connect(
                    host=os.getenv('DB_HOST'),
                    database=os.getenv('DB_NAME'),
                    user=os.getenv('DB_USER'),
                    password=os.getenv('DB_PASSWORD')
                )
        except Error as e:
            raise Exception(f"Error connecting to MySQL database: {e}")

    def execute_query(self, query: str, params: tuple = None) -> Optional[List[Dict[str, Any]]]:
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
    def __init__(self):
        self.db = DatabaseConnection()

    # User operations
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
        result = self.db.execute_query(query, params)
        return result[0]['last_insert_id']

    def get_user_by_email(self, email: str) -> Optional[Dict]:
        query = "SELECT * FROM users WHERE email = %s"
        result = self.db.execute_query(query, (email,))
        return result[0] if result else None

    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        query = "SELECT * FROM users WHERE user_id = %s"
        result = self.db.execute_query(query, (user_id,))
        return result[0] if result else None

    # Vacation operations
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
        result = self.db.execute_query(query, params)
        return result[0]['last_insert_id']

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
        self.db.execute_query(query, params)

    def delete_vacation(self, vacation_id: int) -> None:
        query = "DELETE FROM vacations WHERE vacation_id = %s"
        self.db.execute_query(query, (vacation_id,))

    def get_all_vacations(self) -> List[Dict]:
        query = """
        SELECT v.*, c.country_name, COUNT(l.like_id) as total_likes 
        FROM vacations v 
        LEFT JOIN likes l ON v.vacation_id = l.vacation_id 
        JOIN countries c ON v.country = c.country_id 
        GROUP BY v.vacation_id
        """
        return self.db.execute_query(query)

    def get_vacation_by_id(self, vacation_id: int) -> Optional[Dict]:
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
    def add_like(self, user_id: int, vacation_id: int) -> None:
        query = "INSERT INTO likes (user_id, vacation_id) VALUES (%s, %s)"
        self.db.execute_query(query, (user_id, vacation_id))

    def remove_like(self, user_id: int, vacation_id: int) -> None:
        query = "DELETE FROM likes WHERE user_id = %s AND vacation_id = %s"
        self.db.execute_query(query, (user_id, vacation_id))

    def get_user_likes(self, user_id: int) -> List[Dict]:
        query = """
        SELECT v.*, c.country_name
        FROM vacations v
        JOIN likes l ON v.vacation_id = l.vacation_id
        JOIN countries c ON v.country = c.country_id
        WHERE l.user_id = %s
        """
        return self.db.execute_query(query, (user_id,))

    def check_like_exists(self, user_id: int, vacation_id: int) -> bool:
        query = "SELECT * FROM likes WHERE user_id = %s AND vacation_id = %s"
        result = self.db.execute_query(query, (user_id, vacation_id))
        return bool(result)

    # Country operations
    def get_all_countries(self) -> List[Dict]:
        query = "SELECT * FROM countries"
        return self.db.execute_query(query)

    def get_country_by_id(self, country_id: int) -> Optional[Dict]:
        query = "SELECT * FROM countries WHERE country_id = %s"
        result = self.db.execute_query(query, (country_id,))
        return result[0] if result else None