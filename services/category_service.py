import os
from sqlalchemy import create_engine, text, Column, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

load_dotenv()

SQL_MYKOLA_PASSWORD = os.getenv('SQL_MYKOLA_PASSWORD')

engine = create_engine(f'mysql+mysqlconnector://mykola:{SQL_MYKOLA_PASSWORD}@localhost/EXPENSE_TRACKER?charset=utf8mb4&collation=utf8mb4_general_ci', echo=True)
Session = sessionmaker(bind=engine)

Base = declarative_base()


class Category(Base):
    __tablename__ = 'CATEGORIES'
    name = Column(String, primary_key=True)


def add_category(name: str):
    with engine.connect() as connection:
        query = text(f'INSERT IGNORE INTO CATEGORIES (NAME) VALUES ({name.upper()})')
        connection.execute(query)
        connection.commit()
        print(f'Category {name.upper()} has been added successfully.')
    view_categories()

def edit_category(initial_name: str, needed_name:str):
    """ Edit name of the category """
    session = Session()
    try:
        # Fetch the category
        category = session.query(Category).filter_by(name=initial_name).one()
        
        # Update the name
        category.name = needed_name
        session.commit()
        
        # Refresh the object to ensure it has the latest state
        session.refresh(category)
        print(f"Updated category: {category.name}")
    except NoResultFound:
        print("Category not found.")
    finally:
        session.close()
       
    view_categories()

def view_categories():
    print("All categories listed here:")
    with engine.connect() as connection:
        query = text('SELECT NAME FROM CATEGORIES')
        output = connection.execute(query)
        for el in output:
            print(el[0])