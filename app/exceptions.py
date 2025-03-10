from fastapi import HTTPException
from fastapi import status

from core.logging import logger


class CustomHTTPException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)


class BookNotFound(CustomHTTPException):
    def __init__(self):
        logger.error(f'Error finding book: not found')
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Book not found',
        )


class UnauthorizedAccess(CustomHTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Unauthorized access',
        )


class InvalidRequest(CustomHTTPException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
        )


class BookBorrowingRecordNotFound(CustomHTTPException):
    def __init__(self):
        logger.error(f'Error borrowing book: record not found')
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Borrowing record not found',
        )


class BookBorrowingNotAvailable(CustomHTTPException):
    def __init__(self):
        logger.error(f'Error borrowing book: already booked')
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Book is not available for borrowing',
        )

class UserBorrowingNotFound(CustomHTTPException):
    def __init__(self):
        logger.error(f'User is not borrowing this book')
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User is not borrowing this book',
        )


class CustomHTTPException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)


class NotFoundError(CustomHTTPException):
    def __init__(self, detail: str = 'Resource not found'):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class UniqueConstraintError(CustomHTTPException):
    def __init__(self, detail: str = 'Duplicate entry'):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class ForeignKeyError(CustomHTTPException):
    def __init__(self, detail: str = 'Invalid foreign key'):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class ValueTooLongError(CustomHTTPException):
    def __init__(self, detail: str = 'Value is too long for database type'):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
