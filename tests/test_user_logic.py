import pytest
from datetime import datetime, timedelta
from src.logic.user_logic import UserLogic
from unittest.mock import Mock

@pytest.fixture
def mock_dal():
    return Mock()

@pytest.fixture
def user_logic(mock_dal):
    return UserLogic(mock_dal)

def test_validate_password_valid(user_logic):
    assert user_logic.validate_password("Test123!") == True

def test_validate_password_too_short(user_logic):
    with pytest.raises(ValueError, match="Password must be at least 6 characters long"):
        user_logic.validate_password("Test1")

def test_validate_password_no_uppercase(user_logic):
    with pytest.raises(ValueError, match="Password must contain at least one uppercase letter"):
        user_logic.validate_password("test123")

def test_validate_password_no_lowercase(user_logic):
    with pytest.raises(ValueError, match="Password must contain at least one lowercase letter"):
        user_logic.validate_password("TEST123")

def test_validate_password_no_number(user_logic):
    with pytest.raises(ValueError, match="Password must contain at least one number"):
        user_logic.validate_password("TestTest")

def test_validate_password_no_number(user_logic):
    with pytest.raises(ValueError, match="Password must contain at least one special character"):
        user_logic.validate_password("TestTest123")

def test_validate_email_valid(user_logic):
    assert user_logic.validate_email("test@example.com") == True

def test_validate_email_invalid(user_logic):
    with pytest.raises(ValueError, match="Invalid email format"):
        user_logic.validate_email("invalid_email")

def test_validate_date_of_birth_valid(user_logic):
    valid_date = (datetime.now() - timedelta(days=365*20)).strftime('%Y-%m-%d')
    assert user_logic.validate_date_of_birth(valid_date) == True

def test_validate_date_of_birth_underage(user_logic):
    underage_date = (datetime.now() - timedelta(days=365*17)).strftime('%Y-%m-%d')
    with pytest.raises(ValueError, match="User must be at least 18 years old"):
        user_logic.validate_date_of_birth(underage_date)

def test_validate_user_data_valid(user_logic):
    valid_data = {
        'firstname': 'Test',
        'lastname': 'User',
        'email': 'test@example.com',
        'password': 'Test123!',
        'date_of_birth': (datetime.now() - timedelta(days=365*20)).strftime('%Y-%m-%d')
    }
    assert user_logic.validate_user_data(valid_data) == True

def test_validate_user_data_missing_field(user_logic):
    invalid_data = {
        'firstname': 'Test',
        'lastname': 'User',
        'email': 'test@example.com',
        'password': 'Test123!'
        # missing date_of_birth
    }
    with pytest.raises(ValueError, match="date_of_birth is required"):
        user_logic.validate_user_data(invalid_data)