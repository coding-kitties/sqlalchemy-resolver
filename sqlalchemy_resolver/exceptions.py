class SQLAlchemyWrapperException(Exception):

    def __init__(self, message: str = None):
        super(SQLAlchemyWrapperException, self).__init__(message)


class SQLAlchemyResolverFlaskException(Exception):

    def __init__(self, message: str = None, status_code: int = 400):
        super(Exception, self).__init__(message)
        self._message = message
        self._status_code = status_code

    @property
    def error_message(self):

        if self._message is None:
            return "An error occurred"

        return self._message

    @property
    def status_code(self):

        if self._status_code is None:
            return 500

        return self._status_code
