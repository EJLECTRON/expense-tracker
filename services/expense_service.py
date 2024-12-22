import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

SQL_ROOT_PASSWORD = os.getenv('SQL_ROOT_PASSWORD')

engine = create_engine(f"mysql+mysqlconnector://mykola:{SQL_ROOT_PASSWORD}@localhost/EXPENSE_TRACKER?charset=utf8mb4&collation=utf8mb4_general_ci", echo=True)

def add_expense(name: str, datatype: str, amount: float) -> str:
    with engine.connect() as connection:
        query = f"INSERT INTO EXPENSES (A) VALUES ({name})"
        connection.execute(query)


def view_expenses(number=1, category="ENTERTAINMENT"):
    with engine.connect() as connection:
        query = f"SELECT * FROM EXPENSES WHERE CATEGORY = {category} LIMIT {number}"
        connection.execute(query)