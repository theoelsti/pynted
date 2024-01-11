class UserNotFound(Exception):
    """Raised when the user is not found"""
    def __init__(self, message: str = "User not found", username: str = None):
        super().__init__(message)
        self.username = username