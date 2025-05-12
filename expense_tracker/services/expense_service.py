from os import getenv
from dotenv import load_dotenv
from datetime import datetime

from sqlalchemy import (
    create_engine, text
)
from sqlalchemy.exc import IntegrityError, NoResultFound

from sqlalchemy.orm import sessionmaker
from expense_tracker.services import Category, Expense
from expense_tracker.services.logger import get_custom_logger


load_dotenv()
SQL_MYKOLA_PASSWORD = getenv('SQL_MYKOLA_PASSWORD')
engine = create_engine(f'mysql+mysqlconnector://mykola:{SQL_MYKOLA_PASSWORD}@localhost/EXPENSE_TRACKER?charset=utf8mb4&collation=utf8mb4_general_ci')

logging, Session = get_custom_logger(), sessionmaker(bind=engine)


def view_expenses(**kwargs):
    """
    Keyword arguments:
        - amount (positive int, optional): Number of records to fetch (default: 7)
        - category (str, optional): Filter by category if provided
    """
    amount = kwargs.get("amount", 7)
    category = kwargs.get("category")
    
    category = category.upper() if category else None

    assert isinstance(amount, int) and amount > 0, "Input error: amount must be a positive integer"

    session = Session()
    
    try:
        query = session.query(Expense)

        if category:
            category = category.upper()
            query = query.filter(Expense.category == category)

        results = query.limit(amount).all()

        logging.info("All requested expenses are listed here:")
        for expense in results:
            print(expense)
    finally:
        session.close()


def add_expense(**kwargs):
    """
    Keyword arguments:
        - name (str, required): Name of the record.
        - amount (float, required): Amount of the record (pieces, grams, milliliters, etc.).
        - category (str, required): Category of the record from CATEGORIES table.
        - description (str, optional): Description of the record. Defaults to ''.
    """
    name = kwargs.get("name")
    amount = kwargs.get("amount")
    category = kwargs.get("category")
    description = kwargs.get("description", "")

    assert name and isinstance(name, str), "Missing or invalid 'name'"
    assert isinstance(amount, (int, float)) and amount > 0, "'amount' must be a positive number"
    assert category and isinstance(category, str), "Missing or invalid 'category'"

    category = category.upper()

    session = Session()

    try:
        session.query(Category).filter_by(name=category).one() #raises NoResultFound if it not found

        new_expense = Expense(
            title=name,
            amount=amount,
            time_of_transaction=datetime.now(),
            category=category,
            description=description
        )

        session.add(new_expense)
        session.commit()
        logging.info(f"Expense '{name}' has been successfully added under category '{category}'.")

    except NoResultFound:
        logging.error(
            f"No such category '{category}' found. Use 'view_categories()' to list available categories."
        )
        session.rollback()

    except IntegrityError as e:
        logging.error(f"Database integrity error occurred: {str(e)}")
        session.rollback()

    finally:
        session.close()



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
        if kwargs[el] is not None and el != "searched_id":
            is_any_key_params = True
            if type(kwargs[el] is str):
                query += f' {el.upper()} = \'{kwargs[el]}\','
            else:
                query += f' {el.upper()} = {kwargs[el]},'

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
        - title (str, optional): Name of the record/s (default. (default: "")
        - amount (positive float, optional): Amount of the record/s (default: 0.0)
        - time_of_transaction (str, optional): Time of the record/s (default: "")
        - category (str, optional): Category of the record/s (default: "")
        - description (str, optional): Description of the record/s (default: "")
    """
    query, is_any_key_params = "DELETE FROM EXPENSES WHERE", False

    if kwargs['amount'] is not None:
        assert kwargs['amount'] > 0, "Input error: amount should be more than 0"

    for index, el in enumerate(kwargs):
        if kwargs[el] is not None: # checks if element was given by user
            is_any_key_params = True
            try:
                if type(kwargs[el] is str):
                    query += f' {el.upper()}=\'{kwargs[el]}\' AND' # adds key param to query
                else:
                    query += f' {el.upper()}={kwargs[el]} AND'
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
