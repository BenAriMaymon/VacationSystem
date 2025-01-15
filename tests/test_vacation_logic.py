import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock
from src.logic.vacation_logic import VacationLogic

@pytest.fixture
def setup_logic():
    dal = Mock()
    dal.get_country_by_id.return_value = {"id": 1, "name": "Mock Country"}
    dal.get_vacation_by_id.return_value = {"id": 1, "title": "Mock Vacation"}
    return VacationLogic(dal)


def test_validate_dates_valid(setup_logic):
    logic = setup_logic
    start_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    end_date = (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d')
    assert logic.validate_dates(start_date, end_date)


def test_validate_dates_start_in_past(setup_logic):
    logic = setup_logic
    start_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    end_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    with pytest.raises(ValueError):
        logic.validate_dates(start_date, end_date)


def test_validate_price_valid(setup_logic):
    logic = setup_logic
    assert logic.validate_price(2000)


def test_validate_price_out_of_range(setup_logic):
    logic = setup_logic
    with pytest.raises(ValueError):
        logic.validate_price(999)
    with pytest.raises(ValueError):
        logic.validate_price(10001)


def test_validate_vacation_data_complete(setup_logic):
    logic = setup_logic
    vacation_data = {
        "vacation_title": "Test Vacation",
        "country": 1,
        "start_date": (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'),
        "end_date": (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d'),
        "price": "3000",
    }
    assert logic.validate_vacation_data(vacation_data)


def test_create_vacation(setup_logic):
    logic = setup_logic
    vacation_data = {
        "vacation_title": "Test Vacation",
        "country": 1,
        "start_date": (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'),
        "end_date": (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d'),
        "price": "3000",
    }
    logic.create_vacation(vacation_data)
    logic.dal.create_vacation.assert_called_once_with(vacation_data)


def test_delete_vacation(setup_logic):
    logic = setup_logic
    logic.delete_vacation(1)
    logic.dal.delete_vacation.assert_called_once_with(1)