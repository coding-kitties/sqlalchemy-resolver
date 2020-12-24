class SQLAlchemyWrapperException(Exception):

    def __init__(self, message: str = None):
        super(SQLAlchemyWrapperException, self).__init__(message)
