from os import getenv
from dotenv import load_dotenv

from sqlalchemy import (
    create_engine
)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import NoResultFound

from expense_tracker.services import Category
from expense_tracker.services.logger import get_custom_logger


load_dotenv()
SQL_MYKOLA_PASSWORD = getenv('SQL_MYKOLA_PASSWORD')
engine = create_engine(f'mysql+mysqlconnector://mykola:{SQL_MYKOLA_PASSWORD}@localhost/EXPENSE_TRACKER?charset=utf8mb4&collation=utf8mb4_general_ci')

logging, Session = get_custom_logger(), sessionmaker(bind=engine)


def view_categories():
    session = Session()

    try:
        categories = session.query(Category).all()

        logging.info("All categories listed here:")
        for category in categories:
            print(category.name)

    finally:
        session.close()


def add_category(name: str):
    """
    Keyword arguments:
        - name (str, required): Name of the record.
    """
    if name is not None:
        assert name and isinstance(name, str), logging.error("Missing or invalid 'name'")
        name = name.upper()

    session = Session()

    try:
        exists = session.query(Category).filter_by(name=name).first()

        if not exists:
            new_category = Category()
            new_category.name = name

            session.add(new_category)
            session.commit()

            logging.info(f'Category {name} has been added successfully.')
        else:
            logging.info(f'Category {name} already exists. Skipping insert.')

    finally:
        session.close()


def edit_category(initial_name: str, needed_name: str):
    """
    Keyword arguments:
        - initial_name (str, required): Name of the record to edit.
        - needed_name (str, required): New name of the record.
    """
    if initial_name is not None:
        assert initial_name and isinstance(initial_name, str), logging.error("Missing or invalid 'initial_name'")
        initial_name = initial_name.upper()

    if needed_name is not None:
        assert needed_name and isinstance(needed_name, str), logging.error("Missing or invalid 'needed_name'")
        needed_name = needed_name.upper()

    session = Session()

    try:
        category = session.query(Category).filter_by(name=initial_name).one()
        category.name = needed_name

        session.commit()
        session.refresh(category)

        logging.info(f"Category {category.name} has been updated successfully.")

    except NoResultFound:
        logging.error(
            f"No such category '{initial_name}' found. Use 'view_categories()' to list available categories."
        )
        session.rollback()

    finally:
        session.close()


def delete_category(name: str):
    """
    Keyword arguments:
        - name (str, required): Name of the record.
    """
    if name is not None:
        assert name and isinstance(name, str), logging.error("Missing or invalid 'name'")
        name = name.upper()

    session = Session()

    try:
        category = session.query(Category).filter_by(name=name).one()
        session.delete(category)
        session.commit()

        logging.info(f"Category {category.name} has been deleted successfully.")

    except NoResultFound:
        logging.error(
            f"No such category '{name}' found. Use 'view_categories()' to list available categories."
        )
        session.rollback()

    finally:
        session.close()
