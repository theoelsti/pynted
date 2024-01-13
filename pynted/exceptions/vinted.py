class UserNotFound(Exception):
    """Raised when the user is not found"""
    def __init__(self, message: str = "User not found", username: str = None):
        super().__init__(message)
        self.username = username


class NoFilterRetrieved(Exception):
    """Raised when no filter is retrieved"""
    def __init__(self, message: str = "No filter retrieved"):
        super().__init__(message)


class BrandNotFound(Exception):
    """Raised when the brand is not found"""
    def __init__(self, message: str = "Brand not found", brand: str = None):
        super().__init__(message)
        self.brand = brand
