# app/core/exceptions.py

from fastapi import HTTPException, status


class CustomException(HTTPException):
    """Base class for custom application exceptions."""

    def __init__(self, status_code: int, detail: str, code: str = "GENERIC_ERROR"):
        super().__init__(status_code=status_code, detail=detail)
        self.code = code


class UserNotFoundException(CustomException):
    def __init__(self, detail: str = "User not found."):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail, code="USER_NOT_FOUND")


class InvalidCredentialsException(CustomException):
    def __init__(self, detail: str = "Invalid authentication credentials."):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail, code="INVALID_CREDENTIALS")


class NotPermittedException(CustomException):
    def __init__(self, detail: str = "You do not have permission to perform this action."):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail, code="NOT_PERMITTED")


# class ProjectBudgetExceededException(CustomException):
#     def __init__(self, detail: str = "Adding this expense would exceed the project budget."):
#         super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail, code="BUDGET_EXCEEDED")
