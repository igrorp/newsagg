from typing import List

from fastapi import HTTPException

from .exceptions import (
    MissingNumberPasswordValidationError,
    MissingSpecialPasswordValidationError,
    MissingUppercasePasswordValidationError,
    ShortPasswordValidationError,
)


def validate_password(password: str) -> List[HTTPException]:

    violations = []

    if len(password) < 8:
        violations.append(ShortPasswordValidationError)

    if not any(char.isupper() for char in password):
        violations.append(MissingUppercasePasswordValidationError)

    if not any(char.isdigit() for char in password):
        violations.append(MissingNumberPasswordValidationError)

    if not any(char in "!@#$%^&*()" for char in password):
        violations.append(MissingSpecialPasswordValidationError)

    return violations
