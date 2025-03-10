from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.exceptions import InvalidRequest
from app.exceptions import NotFoundError
from app.models.borrowing_history import BorrowingHistoryCreate
from core.database.database import BaseRepository
from core.database.tables.borrowing_history import BorrowingHistory


class BorrowingHistoryService(BaseRepository[BorrowingHistory, BorrowingHistoryCreate]):
    def __init__(self):
        super().__init__(BorrowingHistory)

    def borrow_book(self, db: Session, borrowing: BorrowingHistoryCreate):
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
        return db_borrowing

    def return_book(self, db: Session, borrowing: BorrowingHistory):
        if borrowing.status == 'returned':
            raise InvalidRequest('Book is already returned')
        borrowing.status = 'returned'
        try:
            db.commit()
        except Exception as e:
            db.rollback()
            raise InvalidRequest('Failed to return book: ' + str(e).lower())
        db.refresh(borrowing)
        return borrowing

    @staticmethod
    def get_borrowing_history(db: Session, user_id: int):
        return db.query(BorrowingHistory).filter(BorrowingHistory.user_id == user_id).all()

    @staticmethod
    def get_borrowing_by_id(db: Session, borrowing_id: int):
        return db.query(BorrowingHistory).filter(BorrowingHistory.id == borrowing_id).first()