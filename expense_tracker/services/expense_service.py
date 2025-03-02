import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

SQL_MYKOLA_PASSWORD = os.getenv('SQL_MYKOLA_PASSWORD')

engine = create_engine(f'mysql+mysqlconnector://mykola:{SQL_MYKOLA_PASSWORD}@localhost/EXPENSE_TRACKER?charset=utf8mb4&collation=utf8mb4_general_ci', echo=True)


def add_expense(**kwargs):
    """
    Keyword arguments:
        - name (str, required): Name of the record.
        - amount (float, required): Amount of the record (pieces, grams, mililiters, etc.).
        - category (str, required): category of the record from CATEGORIES table.
        - description (str, optional): Description of the record. Defaults to ''.
    """
    category = kwargs.get("category").upper()
    description = kwargs.get("description", "")

    with engine.connect() as connection:
        query = text(f'INSERT INTO EXPENSES (TITLE, AMOUNT, TIME_OF_TRANSACTION, CATEGORY, DESCRIPTION) VALUES ' + \
                    f'("{kwargs["name"]}", {kwargs["amount"]}, "{str(datetime.now().strftime('%Y-%m-%d'))}", ' + \
                    f'"{category}", "{description}")')
        connection.execute(query)
        connection.commit()


def view_expenses(number: str, category:str):
    category = category.upper()
    with engine.connect() as connection:
        query = text(f'SELECT * FROM EXPENSES WHERE CATEGORY=\'{category}\' LIMIT {number}')
        output = connection.execute(query)
        print(output.fetchall())


def edit_expense():
    pass


def delete_expense(**kwargs):
    """
    Keyword arguments:
        - id (int, optional): Id of the record (default. (default: 0; non-existent value in database).
        - name (str, optional): Name of the record/s (default. (default: "")
        - amount (float, optional): Amount of the record/s (default: 0.0)
        - time_of_transaction (str, optional): Time of the record/s (default: "")
        - category (str, optional): Category of the record/s (default: "")
        - description (str, optional): Description of the record/s (default: "")
    """
    query, is_any_key_params = "DELETE FROM EXPENSES WHERE", False

    for index, el in enumerate(kwargs):
        if kwargs[el] != None: # checks if element was given by user
            is_any_key_params = True
            try:
                query = query + f' {el}={kwargs[el]}' # adds key param to query
                query += " AND"
            except NameError:
                pass

    query = query[:len(query) - 3] + ';' # join semicolon to the end of query

    if is_any_key_params:
        with engine.connect() as connection:
            query = text(query)
            connection.execute(query)
            connection.commit()
        print("Deleted successfully.")
    else:
        print("None parameters were given, try again.")
