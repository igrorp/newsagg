from fastapi import HTTPException, status


class TokenValidationError(HTTPException):
    ERROR_MSG = "Could not validate credentials"
    STATUS = status.HTTP_401_UNAUTHORIZED
    HEADERS = {"WWW-Authenticate": "Bearer"}

    def __init__(self):
        super().__init__(
            status_code=self.STATUS, detail=self.ERROR_MSG, headers=self.HEADERS
        )


class PasswordValidationError(HTTPException):
    ERROR_MSG = ""

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST, detail=self.ERROR_MSG
        )


class ShortPasswordValidationError(HTTPException):
    ERROR_MSG = "Password must be at least 8 characters long"


class MissingUppercasePasswordValidationError(HTTPException):
    ERROR_MSG = "Password must contain at least one uppercase letter"


class MissingNumberPasswordValidationError(HTTPException):
    ERROR_MSG = "Password must contain at least one number"


class MissingSpecialPasswordValidationError(HTTPException):
    ERROR_MSG = "Password must contain at least one special character"
