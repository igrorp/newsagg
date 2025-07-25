from typing import Any

from fastapi import HTTPException, status


class PasswordValidationException(HTTPException):
    STATUS = status.HTTP_400_BAD_REQUEST

    def __init__(self, detail: Any):
        super().__init__(status_code=self.STATUS, detail=detail)


class ShortPasswordValidationError(ValueError):
    ERROR_MSG = "Password must be at least 8 characters long"


class MissingUppercasePasswordValidationError(ValueError):
    ERROR_MSG = "Password must contain at least one uppercase letter"


class MissingNumberPasswordValidationError(ValueError):
    ERROR_MSG = "Password must contain at least one number"


class MissingSpecialPasswordValidationError(ValueError):
    ERROR_MSG = "Password must contain at least one special character"


class EmailValidationError(HTTPException):
    ERROR_MSG = "Invalid email address"
    STATUS = status.HTTP_400_BAD_REQUEST

    def __init__(self):
        super().__init__(status_code=self.STATUS, detail=self.ERROR_MSG)
