"""
database.py

Defines the database connection and database related functions
"""
from sqlmodel import SQLModel, create_engine, Session


sqlite_file_name = "batch_inv.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    """
    Creates the database and all the tables based on models
    """
    SQLModel.metadata.create_all(engine)


def get_session():
    """
    Provides a database session to interact with the database.
    """
    with Session(engine) as session:
        yield session
