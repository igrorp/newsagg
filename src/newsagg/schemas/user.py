import re

from pydantic import BaseModel, field_validator

from newsagg.schemas.exceptions import (
    EmailValidationError,
    MissingNumberPasswordValidationError,
    MissingSpecialPasswordValidationError,
    MissingUppercasePasswordValidationError,
    PasswordValidationException,
    ShortPasswordValidationError,
)


class UserBase(BaseModel):
    email: str
    username: str

    @field_validator("email", mode="before")
    def validate_email(cls, value: str) -> str:
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise EmailValidationError
        return value


class UserInput(UserBase):

    password: str

    @field_validator("password", mode="before")
    def validate_password(cls, value: str) -> str:
        errs = []

        if len(value) < 8:
            errs.append(ShortPasswordValidationError.ERROR_MSG)
        if not any(char.isupper() for char in value):
            errs.append(MissingUppercasePasswordValidationError.ERROR_MSG)
        if not any(char.isdigit() for char in value):
            errs.append(MissingNumberPasswordValidationError.ERROR_MSG)
        if not any(char in "!@#$%^&*()" for char in value):
            errs.append(MissingSpecialPasswordValidationError.ERROR_MSG)

        if errs:
            raise PasswordValidationException(detail=errs)

        return value


class UserDB(UserInput):
    is_superuser: bool = False
    is_active: bool = True
