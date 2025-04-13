# setup.py

from setuptools import setup, find_packages

setup(
    name="expense_tracker",
    version="0.1",
    author="Mykola Ishchenko",
    author_email="ish.myk0la@gmail.com",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "expense-tracker = expense_tracker.__main__:main",  # Entry point for the CLI
        ],
    },
    install_requires=[
        "sqlalchemy",
        "mysql-connector-python",
        "argparse",
    ]
)

