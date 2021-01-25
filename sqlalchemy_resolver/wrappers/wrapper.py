import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Query, class_mapper, sessionmaker, scoped_session, \
    Session
from sqlalchemy.orm.exc import UnmappedClassError
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy_resolver.base_model import Model
from sqlalchemy_resolver.configuration import Config
from sqlalchemy_resolver.exceptions import SQLAlchemyWrapperException
from sqlalchemy_resolver.constants import DATABASE_HOST, DATABASE_PASSWORD, \
    DATABASE_TYPE, DATABASE_URL, DATABASE_NAME, DATABASE_USERNAME, \
    DATABASE_PATH
from sqlalchemy_resolver.database_type import DatabaseType


class _SessionProperty:
    """
    Wrapper for session property of a Model
    To make sure that each thread gets an scoped session, a new scoped
    session is created if a new thread accesses the session property of
    a Model.
    """
    def __init__(self, db):
        self.db = db

    def __get__(self, instance, owner):
        return self.db.session


class _QueryProperty:
    """
    Wrapper for query property of a Model
    This wrapper makes sure that each model gets a Query object with a
    correct session corresponding to its thread.
    """
    def __init__(self, db):
        self.db = db

    def __get__(self, instance, owner):

        try:
            mapper = class_mapper(owner)
            if mapper:
                return owner.query_class(mapper, session=self.db.session)

        except UnmappedClassError:
            return None


class SQLAlchemyWrapper:

    def __init__(
            self, config=None, query_class=Query, model_class=Model
    ) -> None:
        self._configured = False
        self.Query = query_class
        self.engine = None
        self.session_factory = None
        self.Session = None
        self._model = self.make_declarative_base(model_class)
        self.config = config

    @staticmethod
    def make_declarative_base(model_class):
        """
        Creates the declarative base that all models will inherit from.
        """

        return declarative_base(cls=model_class)

    @property
    def session(self) -> Session:
        """
        Returns scoped session of an Session object
        """
        return self.Session()

    @property
    def Model(self):
        return self._model

    def initialize_tables(self):
        self._model.metadata.create_all(self.engine)

    def set_config(self, config: Config):
        self.config = config

    # def initialize_migrations(self, raise_exception: bool = True):
    #
    #     if MIGRATIONS_DIRECTORY not in self.config:
    #         raise SQLAlchemyWrapperException(
    #             "migrations directory is not specified in the config"
    #         )
    #
    #     migration_directory = self.config[MIGRATIONS_DIRECTORY]
    #     destination_dir = os.path.join(migration_directory, 'alembic')
    #
    #     if os.path.isdir(destination_dir) and raise_exception:
    #         raise SQLAlchemyWrapperException(
    #             "Migration directory already exists"
    #         )
    #
    #     if not os.path.isdir(destination_dir):
    #         os.makedirs(migration_directory)
    #
    #     if DATABASE_URL not in self.config:
    #         raise SQLAlchemyWrapperException(
    #             "Database wrapper is not configured"
    #         )
    #
    #     init_migrations(migration_directory, self.config[DATABASE_URL])
    #
    # def perform_auto_migration(self, migration_id: str = None):
    #     migration_directory = self.config[MIGRATIONS_DIRECTORY]
    #     perform_auto_migration(migration_directory, migration_id)

    def connect_postgresql(
            self,
            config: Config,
            ssl_require: bool = False,
            connection_url: str = None
    ):

        if connection_url:

            if config is None:
                self.config = Config()
                self.config[DATABASE_URL] = connection_url
        else:
            if config:
                self.config = config

            if not self.config:
                raise SQLAlchemyWrapperException("Config is not defined")

            # Try to get all required configuration properties
            try:
                self.config[DATABASE_URL] = 'postgresql://{}:{}@{}/{}'.format(
                    self.config[DATABASE_USERNAME],
                    self.config[DATABASE_PASSWORD],
                    self.config[DATABASE_HOST],
                    self.config[DATABASE_NAME]
                )
                self.config[DATABASE_TYPE] = DatabaseType.POSTGRESQL.value
            except Exception:
                raise SQLAlchemyWrapperException(
                    "Missing configuration: DATABASE_USERNAME, "
                    "DATABASE_PASSWORD, DATABASE_HOST and DATABASE_NAME"
                 )

        self.initialize_engine(
            self.config[DATABASE_URL], ssl_require=ssl_require
        )
        self.initialize_session()
        self.initialize_model()

    def connect_sqlite(self, config, connection_url: str = None):

        if connection_url:

            if config is None:
                self.config = Config()
                self.config[DATABASE_URL] = connection_url
        else:
            if config:
                self.config = config

            if not self.config:
                raise SQLAlchemyWrapperException("Config is not defined")

        try:
            data_base_path = self.config[DATABASE_PATH]

            if not os.path.isdir(data_base_path):
                raise SQLAlchemyWrapperException(
                    "Database path is not a directory"
                )

            if not config[DATABASE_PATH].endswith(".sqlite3"):
                data_base_name = self.config[DATABASE_NAME]
                database_path = os.path.join(
                    data_base_path, data_base_name
                )
                database_path += ".sqlite3"
                self.config[DATABASE_PATH] = database_path
        except Exception as e:
            raise SQLAlchemyWrapperException(
                "Missing configuration settings for sqlite3. For sqlite3 the "
                "following attributes are needed: DATABASE_PATH, DATABASE_NAME"
            )

        if not os.path.isfile(self.config[DATABASE_PATH]):
            print()
            os.mknod(self.config[DATABASE_PATH])

        self.config[DATABASE_URL] = 'sqlite:////{}'.format(
            config[DATABASE_PATH]
        )
        self.config[DATABASE_TYPE] = DatabaseType.SQLITE3.value

        self.initialize_engine(self.config[DATABASE_URL])
        self.initialize_session()
        self.initialize_model()

    def initialize_engine(self, database_url, ssl_require: bool = False):

        if ssl_require:
            self.engine = create_engine(
                database_url, connect_args={'sslmode': 'require'}
            )
        else:
            self.engine = create_engine(database_url)

    def initialize_session(self):
        self.session_factory = sessionmaker(bind=self.engine)
        self.Session = scoped_session(self.session_factory)

    def initialize_model(self):
        if self._model is None:
            raise SQLAlchemyWrapperException("Model is not defined")

        self._model.session = _SessionProperty(self)

        if not getattr(self._model, 'query_class', None):
            self._model.query_class = self.Query

        self._model.query = _QueryProperty(self)

    @property
    def metadata(self):
        return self.Model.metadata
