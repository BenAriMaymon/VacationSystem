from datetime import datetime


class VacationLogic:
    def __init__(self, dal):
        self.dal = dal

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

    def create_vacation(self, vacation_data):
        self.validate_vacation_data(vacation_data)
        return self.dal.create_vacation(vacation_data)

    def update_vacation(self, vacation_id, vacation_data):
        self.validate_vacation_data(vacation_data)
        existing_vacation = self.dal.get_vacation_by_id(vacation_id)
        if not existing_vacation:
            raise ValueError("Vacation not found")
        self.dal.update_vacation(vacation_id, vacation_data)

    def delete_vacation(self, vacation_id):
        existing_vacation = self.dal.get_vacation_by_id(vacation_id)
        if not existing_vacation:
            raise ValueError("Vacation not found")
        self.dal.delete_vacation(vacation_id)

    def get_all_vacations(self):
        return self.dal.get_all_vacations()

    def get_vacation_by_id(self, vacation_id):
        return self.dal.get_vacation_by_id(vacation_id)