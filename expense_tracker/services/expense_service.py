import os
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError
from dotenv import load_dotenv
from datetime import datetime

from expense_tracker.services.logger import get_custom_logger


logging = get_custom_logger()

load_dotenv()

SQL_MYKOLA_PASSWORD = os.getenv('SQL_MYKOLA_PASSWORD')

engine = create_engine(f'mysql+mysqlconnector://mykola:{SQL_MYKOLA_PASSWORD}@localhost/EXPENSE_TRACKER?charset=utf8mb4&collation=utf8mb4_general_ci')


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
        try:
            query = text(f'INSERT INTO EXPENSES (TITLE, AMOUNT, TIME_OF_TRANSACTION, CATEGORY, DESCRIPTION) VALUES ' + \
                        f'("{kwargs["name"]}", {kwargs["amount"]}, "{str(datetime.now().strftime('%Y-%m-%d'))}", ' + \
                        f'"{category}", "{description}")')
            connection.execute(query)
            connection.commit()
        except IntegrityError:
            logging.error(f'There is no such category as {category}, please view list of available categories using show-categories')

def view_expenses(**kwargs):
    """
    Keyword arguments:
        - amount (positive float, optional): Amount of the record/s user wants (default: 7)
        - category (str, required): Category of the record/s user wants
    """
    category = kwargs.get("category").upper()
    amount = kwargs.get("amount", 7)

    assert amount > 0, "Input error: amount should be more than 0"

    with engine.connect() as connection:
        query = text(f'SELECT * FROM EXPENSES WHERE CATEGORY=\'{category}\' LIMIT {amount}')
        output = connection.execute(query)
        print(output.fetchall())


def edit_expense():
    pass


def delete_expense(**kwargs):
    """
    Keyword arguments:
        - id (int, optional): Id of the record (default. (default: 0; non-existent value in database).
        - name (str, optional): Name of the record/s (default. (default: "")
        - amount (positive float, optional): Amount of the record/s (default: 0.0)
        - time_of_transaction (str, optional): Time of the record/s (default: "")
        - category (str, optional): Category of the record/s (default: "")
        - description (str, optional): Description of the record/s (default: "")
    """
    query, is_any_key_params = "DELETE FROM EXPENSES WHERE", False

    assert kwargs['amount'] > 0, "Input error: amount should be more than 0"

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
