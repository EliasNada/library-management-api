from datetime import datetime
from datetime import UTC
from typing import List

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.exceptions import InvalidRequest
from app.exceptions import NotFoundError
from app.models.borrowing_history import BorrowingHistoryCreate
from app.services import BookService
from core.database.database import BaseRepository
from core.database.tables.borrowing_history import BorrowingHistory


class BorrowingHistoryService(BaseRepository[BorrowingHistory, BorrowingHistoryCreate]):
    def __init__(self):
        super().__init__(BorrowingHistory)

    def borrow_book(self, db: Session, borrowing: BorrowingHistoryCreate) -> BorrowingHistory:
        """
        assigns a book to a user and marks the book as unavailable
        :param db:
        :param borrowing:
        :return:
        """
        existing_borrowing = (
            db.query(self.model)
            .filter(
                BorrowingHistory.book_id == borrowing.book_id,
                BorrowingHistory.status == 'borrowed',
            )
            .first()
        )
        if existing_borrowing:
            raise InvalidRequest('Book is already borrowed')

        db_borrowing = BorrowingHistory(**borrowing.model_dump())
        db_borrowing.status = 'borrowed'
        db.add(db_borrowing)
        try:
            db.commit()
        except IntegrityError as e:
            db.rollback()
            if 'foreign key' in str(e).lower():
                raise InvalidRequest('Invalid user or book ID')
            raise InvalidRequest('Failed to borrow book')
        db.refresh(db_borrowing)
        BookService.toggle_book_availability(db, borrowing.book_id)
        return db_borrowing

    def return_book(self, db: Session, borrowing: BorrowingHistory) -> BorrowingHistory:
        """
        Marks the book as returned and available
        :param db:
        :param borrowing:
        :return BorrowingHistory:
        """
        if borrowing.status == 'returned':
            raise InvalidRequest('Book is already returned')
        borrowing.status = 'returned'
        borrowing.return_date = datetime.now(UTC)
        try:
            db.commit()
        except Exception as e:
            db.rollback()
            raise InvalidRequest('Failed to return book: ' + str(e).lower())
        db.refresh(borrowing)
        BookService.toggle_book_availability(db, borrowing.book_id)
        return borrowing

    @staticmethod
    def get_borrowing_history(db: Session, user_id: int) -> List[BorrowingHistory]:
        """
        Gets user borrowing history
        :param db:
        :param user_id:
        :return:
        """
        return db.query(BorrowingHistory).filter(BorrowingHistory.user_id == user_id).all()

    @staticmethod
    def get_borrowing_by_id(db: Session, borrowing_id: int) -> BorrowingHistory:
        """
        Gets a single borrowing by its id
        :param db:
        :param borrowing_id:
        :return:
        """
        return db.query(BorrowingHistory).filter(BorrowingHistory.id == borrowing_id).first()