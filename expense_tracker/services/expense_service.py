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

#TODO case when name is more than 1 word isn't counted
def edit_expense(**kwargs):
    """
    Edit expense (search for a record available only using id)
    Keyword arguments:
        - searched_id (str, required): Id of the record to update.
        - title (str, optional): New name of the record (default: (default: "")
        - amount (positive float, optional): New amount of the record (default: 0.0)
        - category (str, optional): New category of the record (default: "")
        - description (str, optional): New description of the record (default: "")
    """
    query, is_any_key_params = 'UPDATE EXPENSES SET', False

    for el in kwargs:
        if kwargs[el] != None and el != "searched_id":
            is_any_key_params = True
            query += f' {el.upper()} = \'{kwargs[el]}\','

    if is_any_key_params:
        query = query[:-1]
        query += f' WHERE ID = {kwargs["searched_id"]};'

        with engine.connect() as connection:
            query = text(query)
            connection.execute(query)
            connection.commit()
        logging.info("Updated successfully.")
    else:
        logging.error("None parameters were given, try again.")


#TODO case when name is more than 1 word isn't counted
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
                query += f' {el}={kwargs[el]} AND' # adds key param to query
            except NameError:
                pass

    query = query[:len(query) - 3] + ';' # join semicolon to the end of query

    if is_any_key_params:
        with engine.connect() as connection:
            query = text(query)
            connection.execute(query)
            connection.commit()
        logging.info("Deleted successfully.")
    else:
        logging.error("None parameters were given, try again.")
