from click import echo
from flask import session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

from app import TestTable


connection_string = "postgresql://hints:password@localhost/hints?connect_timeout=5"


def get_engine(connection_string):
    if not database_exists(connection_string):
        create_database(connection_string)
    return create_engine(connection_string, echo=True)



engine = get_engine(connection_string)
Session = sessionmaker(engine)

with Session() as session:
    new_data = TestTable(vacancy_name="test")
    session.add(new_data)
    session.commit()