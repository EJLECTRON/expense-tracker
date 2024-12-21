import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

SQL_ROOT_PASSWORD = os.getenv('SQL_ROOT_PASSWORD')

engine = create_engine(f"mysql+mysqlconnector://mykola:{SQL_ROOT_PASSWORD}@localhost/EXPENSE_TRACKER?charset=utf8mb4&collation=utf8mb4_general_ci", echo=True)


def add_category(name: str, datatype: str):
    print("add_category")


def view_categories():
    print("All categories listed here:")
    with engine.connect() as connection:
        output = connection.execute(text("SELECT NAME FROM CATEGORIES"))
        for el in output:
            print(el[0])