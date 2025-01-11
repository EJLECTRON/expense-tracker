import pytest, os, subprocess
from sqlalchemy import create_engine, text
from dotenv import load_dotenv


def test_install():
    subprocess.run(["/home/ejlectron/Programming/projects/expense-tracker/install_scripts/install.sh"], shell=True)
        
    try:
        load_dotenv()
        SQL_MYKOLA_PASSWORD = os.getenv('SQL_MYKOLA_PASSWORD')

        engine = create_engine(f'mysql+mysqlconnector://mykola:{SQL_MYKOLA_PASSWORD}@localhost/EXPENSE_TRACKER?charset=utf8mb4&collation=utf8mb4_general_ci', echo=True)
    except Exception as e:
        print(f"Failed to connect: {e}")
    user_creation(engine)
    database_creation(engine)


def user_creation(engine):
    with engine.connect() as connection:
        assert engine.dialect.do_ping(connection.connection), "Something wrong with connection using user mykola"


def database_creation(engine):
    """Test that the database was created."""
    response = None

    with engine.connect() as connection:
        query = text("SHOW DATABASES")
        output = connection.execute(query)
        response = output.fetchall()

    for i in range(len(response)):
        response[i] = response[i][0]

    assert 'EXPENSE_TRACKER' in response, "Database 'EXPENSE_TRACKER' should exist."

if __name__ == "__main__":
    test_install()