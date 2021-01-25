import os
from unittest import TestCase

from sqlalchemy_resolver.wrappers import SQLAlchemyWrapper
from sqlalchemy_resolver.constants import DATABASE_PATH, DATABASE_NAME


def create_config():
    return {
        DATABASE_NAME: 'test_db',
        DATABASE_PATH: database_directory,
    }


database_directory = os.path.join(
    os.path.abspath(os.path.join(os.getcwd(), os.pardir)),
    'resources/'
)

db = SQLAlchemyWrapper()


class SQLiteTestBase(TestCase):

    def setUp(self) -> None:
        db.connect_sqlite(create_config())
        db.initialize_tables()

    def tearDown(self):
        db.session.close()
        database_path = db.config[DATABASE_PATH]

        if os.path.isfile(database_path):
            os.remove(database_path)
