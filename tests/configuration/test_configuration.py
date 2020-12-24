from unittest import TestCase
from sqlalchemy_resolver.configuration import Config
from sqlalchemy_resolver.database_type import DatabaseType
from tests.utils import random_string


class TestConfiguration(TestCase):

    def setUp(self) -> None:
        self.config = Config()
        self.config.DATABASE_TYPE = DatabaseType.SQLITE3
        self.config.DATABASE_NAME = random_string(10)
        self.config.DATABASE_PASSWORD = random_string(10)
        self.config.DATABASE_URL = random_string(10)
        self.config.DATABASE_USERNAME = random_string(10)

    def test(self):
        self.assertIsNotNone(self.config.DATABASE_TYPE)
        self.assertIsNotNone(self.config.DATABASE_URL)
        self.assertIsNotNone(self.config.DATABASE_USERNAME)
        self.assertIsNotNone(self.config.DATABASE_PASSWORD)
        self.assertIsNotNone(self.config.DATABASE_NAME)
