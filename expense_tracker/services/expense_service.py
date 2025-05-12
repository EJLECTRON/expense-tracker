from os import getenv
from dotenv import load_dotenv
from datetime import datetime

from sqlalchemy import (
    Column, Integer, String, DateTime, ForeignKey,
    create_engine, text, func
)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import relationship, DeclarativeBase

from expense_tracker.services.logger import get_custom_logger


logging = get_custom_logger()

load_dotenv()

SQL_MYKOLA_PASSWORD = getenv('SQL_MYKOLA_PASSWORD')

engine = create_engine(f'mysql+mysqlconnector://mykola:{SQL_MYKOLA_PASSWORD}@localhost/EXPENSE_TRACKER?charset=utf8mb4&collation=utf8mb4_general_ci')


class Expense(DeclarativeBase):
    __tablename__ = 'EXPENSES'

    id = Column('ID', Integer, primary_key=True, autoincrement=True, unique=True)
    title = Column('TITLE', String(20), nullable=False)
    amount = Column('AMOUNT', Integer, nullable=False)
    time_of_transaction = Column('TIME_OF_TRANSACTION', DateTime, nullable=False, default=func.now())
    category = Column('CATEGORY', String(50), ForeignKey('CATEGORIES.NAME', onupdate="CASCADE", ondelete="SET DEFAULT"), nullable=False)
    description = Column('DESCRIPTION', String(511))

    category_obj = relationship('Category', back_populates='expenses')

    def __repr__(self):
        return f"<Expense(title='{self.title}', amount={self.amount}, category='{self.category}')>"



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
            query = text('INSERT INTO EXPENSES (TITLE, AMOUNT, TIME_OF_TRANSACTION, CATEGORY, DESCRIPTION) VALUES ' + \
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
