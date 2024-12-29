import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

SQL_MYKOLA_PASSWORD = os.getenv('SQL_MYKOLA_PASSWORD')

engine = create_engine(f'mysql+mysqlconnector://mykola:{SQL_MYKOLA_PASSWORD}@localhost/EXPENSE_TRACKER?charset=utf8mb4&collation=utf8mb4_general_ci', echo=True)


def add_category(name: str):
    with engine.connect() as connection:
        query = text(f'INSERT IGNORE INTO CATEGORIES (NAME) VALUES ({name.upper()})')
        connection.execute(query)
        connection.commit()
        print(f'Category {name.upper()} has been added successfully.')
        view_categories()


def view_categories():
    print("All categories listed here:")
    with engine.connect() as connection:
        query = text("SELECT NAME FROM CATEGORIES")
        output = connection.execute(query)
        for el in output:
            print(el[0])