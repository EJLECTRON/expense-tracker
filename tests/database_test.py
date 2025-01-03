import pytest, os 
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()
SQL_ROOT_PASSWORD = os.getenv('SQL_ROOT_PASSWORD')

engine = create_engine(f'mysql+mysqlconnector://root:{SQL_ROOT_PASSWORD}@localhost/mysql?charset=utf8mb4&collation=utf8mb4_general_ci', echo=True)

# Database connection details
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": SQL_ROOT_PASSWORD,  # Replace with your root password
    "database": "mysql",  # Default MySQL database
    "auth_plugin": "mysql_native_password",
}


def test_database_creation():
    """Test that the database was created."""
    response = None
    
    with engine.connect() as connection:
        with open("../install_scripts/set_up_database.sql") as file:
            query = text(file.read())
            connection.execute(query)
            connection.commit()
            response = connection.execute(text("SHOW DATABASES"))
            
    assert "EXPENSE_TRACKER" in response, "Database 'EXPENSE_TRACKER' should exist."

if __name__ == "__main__":
    test_database_creation()