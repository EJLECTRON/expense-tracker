import os
from sqlalchemy import create_engine, text, Column, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

from expense_tracker.services.logger import get_custom_logger


logging = get_custom_logger()

load_dotenv()

SQL_MYKOLA_PASSWORD = os.getenv('SQL_MYKOLA_PASSWORD')

engine = create_engine(f'mysql+mysqlconnector://mykola:{SQL_MYKOLA_PASSWORD}@localhost/EXPENSE_TRACKER?charset=utf8mb4&collation=utf8mb4_general_ci')
Session = sessionmaker(bind=engine)

Base = declarative_base()


class Category:
    __tablename__ = 'CATEGORIES'
    name = Column(String, primary_key=True)


def view_categories():
    logging.info("All categories listed here:")
    session = Session()
    try:
        categories = session.query(Category).all()
        for category in categories:
            print(category.name)
    finally:
        session.close()


def add_category(name: str):
    name = name.upper()
    session = Session()
    try:
        exists = session.query(Category).filter_by(name=name).first()
        if not exists:
            new_category = Category()
            new_category.name = Column(name, primary_key=True)

            session.add(new_category)
            session.commit()

            logging.info(f'Category {name} has been added successfully.')
        else:
            logging.info(f'Category {name} already exists. Skipping insert.')
    finally:
        session.close()


def edit_category(initial_name: str, needed_name:str):
    """ Edit name of the category """
    initial_name, needed_name = initial_name.upper(), needed_name.upper()
    session = Session()

    try:
        category = session.query(Category).filter_by(name=initial_name).one()
        category.name = Column(needed_name, primary_key=True)

        session.commit()
        session.refresh(category)

        logging.info(f"Category {category.name} has been updated successfully.")
    except NoResultFound:
        logging.error("Category not found.")
    finally:
        session.close()


def delete_category(name: str):
    """ Delete category """
    name = name.upper()
    session = Session()

    try:
        category = session.query(Category).filter_by(name=name).one()
        session.delete(category)
        session.commit()

        logging.info(f"Category {category.name} has been deleted successfully.")
    except NoResultFound:
        logging.error("Category not found.")
    finally:
        session.close()
