import pytest, os, subprocess
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

from expense_tracker.services.category_service import view_categories, add_category, edit_category, delete_category
from expense_tracker.services.expense_service import view_expenses, add_expense, edit_expense, delete_expense



load_dotenv()
SQL_MYKOLA_PASSWORD = os.getenv('SQL_MYKOLA_PASSWORD')

engine = create_engine(f'mysql+mysqlconnector://mykola:{SQL_MYKOLA_PASSWORD}@localhost/EXPENSE_TRACKER?charset=utf8mb4&collation=utf8mb4_general_ci')


def test_view_category():
    pass


def test_add_category():
    pass


def test_edit_category():
    pass


def test_delete_category():
    pass


def test_view_expense():
    pass


def test_add_expense():
    pass


def test_edit_expense():
    pass


def test_delete_expense():
    pass
