import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

SQL_MYKOLA_PASSWORD = os.getenv('SQL_MYKOLA_PASSWORD')

engine = create_engine(f'mysql+mysqlconnector://mykola:{SQL_MYKOLA_PASSWORD}@localhost/EXPENSE_TRACKER?charset=utf8mb4&collation=utf8mb4_general_ci', echo=True)

def add_expense(name: str, amount: float, category: str, description: str) -> str:
    with engine.connect() as connection:
        query = text(f'INSERT INTO EXPENSES (TITLE, AMOUNT, TIME_OF_TRANSACTION, CATEGORY, DESCRIPTION) VALUES ("{name}", {amount}, "{datetime.now().strftime('%Y-%m-%d')}", "{category}", "{description}")')
        connection.execute(query)
        connection.commit()


def view_expenses(number, category):
    with engine.connect() as connection:
        query = text(f'SELECT * FROM EXPENSES WHERE CATEGORY=\'{category}\' LIMIT {number}')
        output = connection.execute(query)
        print(output.fetchall())