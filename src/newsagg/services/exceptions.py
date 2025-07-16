from fastapi import HTTPException


class IncorretUsernameOrPasswordError(HTTPException):
    """
    Exception raised when the username or password is incorrect.
    """

    DETAIL = "Incorrect username or password"
    STATUS_CODE = 401
    HEADERS = {"WWW-Authenticate": "Bearer"}

    def __init__(self):
        super().__init__(
            status_code=self.STATUS_CODE,
            detail=self.DETAIL,
            headers=self.HEADERS,
        )


class UserNotFoundError(HTTPException):
    """
    Exception raised when the username is not located.
    """

    DETAIL = "User not found"
    STATUS_CODE = 404

    def __init__(self):
        super().__init__(
            status_code=self.STATUS_CODE,
            detail=self.DETAIL,
        )


class UsernameAlreadyExistsError(HTTPException):
    """
    Exception raised when the username already exists.
    """

    DETAIL = "Username already registered"
    STATUS_CODE = 400

    def __init__(self):
        super().__init__(
            status_code=self.STATUS_CODE,
            detail=self.DETAIL,
        )


class EmailAlreadyExistsError(HTTPException):
    """
    Exception raised when the e-mail already exists.
    """

    DETAIL = "E-mail already registered"
    STATUS_CODE = 400

    def __init__(self):
        super().__init__(
            status_code=self.STATUS_CODE,
            detail=self.DETAIL,
        )
