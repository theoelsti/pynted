class InvalidCredentials(Exception):
    """Raised when the user credentials are invalid."""

    def __init__(self, message: str = "Invalid credentials"):
        super().__init__(message)


class TooManyAttempts(Exception):
    """Raised when the user has tried too many times to login."""

    def __init__(self, message: str = "Too many attempts"):
        super().__init__(message)


class UnknownError(Exception):
    """Raised when an unknown error occured."""

    def __init__(self, message: str = "Unknown error"):
        super().__init__(message)
