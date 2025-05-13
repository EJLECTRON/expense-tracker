from os import getenv
from dotenv import load_dotenv
from datetime import datetime

from sqlalchemy import (
    create_engine
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

    if category is not None:
        category = category.upper()

    assert isinstance(amount, int) and amount > 0, "Input error: amount must be a positive integer"

    session = Session()
    
    try:
        query = session.query(Expense)

        if category:
            query = query.filter(Expense.category == category)

        results = query.limit(amount).all()

        logging.info("All requested expenses are listed here:")
        for expense in results:
            print(expense)

    except Exception as e:
        logging.exception(f"An unexpected error occurred while deleting expense. Error:{e}")
        session.rollback()

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

    assert name and isinstance(name, str), logging.error("Missing or invalid 'name'")
    assert isinstance(amount, (int, float)) and amount > 0, logging.error("'amount' must be a positive number")
    assert category and isinstance(category, str), logging.error("Missing or invalid 'category'")

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

    except Exception as e:
        logging.exception(f"An unexpected error occurred while adding expense. Error:{e}")
        session.rollback()

    finally:
        session.close()


def edit_expense(**kwargs):
    """
    Edit expense (search for a record using its ID).

    Keyword arguments:
        - title (str, required): Title that represents record to edit.
        - new_title (str, optional): New name of the record.
        - amount (positive float, optional): New amount of the record.
        - category (str, optional): New category (must exist in CATEGORIES).
        - description (str, optional): New description.
    """
    title = kwargs.get("title")
    new_title = kwargs.get("new_title")
    amount = kwargs.get("amount")
    category = kwargs.get("category")
    description = kwargs.get("description")
    
    if title is not None:
        assert isinstance(title, str), logging.error("'title' must be a string")

    if new_title is not None:
        assert isinstance(new_title, str), logging.error("'new_title' must be a string")

    if category is not None:
        assert isinstance(category, str), logging.error("'category' must be a string")
        category = category.upper()

    if amount is not None:
        assert isinstance(amount, (int, float)) and amount > 0, logging.error("'amount' must be a positive number")
    
    if description is not None:
        assert isinstance(description, str), logging.error("'description' must be a string")

    session = Session()

    try:
        expense = session.query(Expense).filter_by(title=title).one()

        if new_title is not None:
            expense.title = new_title

        if amount is not None:
            expense.amount = amount

        if category is not None:
            try:
                session.query(Category).filter_by(name=category).one() # Validate that the new category exists
            except NoResultFound:
                logging.error(f"No category found for category '{category}'")
            expense.category = category

        if description is not None:
            expense.description = description

        session.commit()
        logging.info(f"Expense with title {title} has been updated successfully.")

    except NoResultFound:
        logging.error(f"No expense found for title '{title}'.")
        session.rollback()

    except IntegrityError as e:
        logging.error(f"Database integrity error occurred: {str(e)}")
        session.rollback()
    
    except Exception as e:
        logging.exception(f"An unexpected error occurred while editing expense. Error:{e}")
        session.rollback()

    finally:
        session.close()


def delete_expense(**kwargs):
    """
    Delete an expense by title.

    Keyword arguments:
        - title (str, required): Title of the record to be deleted.
    """
    title = kwargs.get("title")

    if title is None:
        logging.error("'title' is required to delete an expense.")
        return

    assert isinstance(title, str), logging.error("'title' must be a string")

    session = Session()

    try:
        expense = session.query(Expense).filter_by(title=title).one()
        session.delete(expense)
        session.commit()
        logging.info(f"Expense with title '{title}' has been deleted successfully.")

    except NoResultFound:
        logging.error(f"No expense found for title '{title}'.")
        session.rollback()

    except IntegrityError as e:
        logging.error(f"Database integrity error occurred during deletion: {str(e)}")
        session.rollback()

    except Exception as e:
        logging.exception(f"An unexpected error occurred while deleting expense. Error:{e}")
        session.rollback()

    finally:
        session.close()
