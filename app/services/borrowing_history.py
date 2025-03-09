from sqlalchemy.orm import Session
from core.database.tables import BorrowingHistory
from app.models.borrowing_history import BorrowingHistoryCreate


class BorrowingHistoryService:
    @staticmethod
    def borrow_book(db: Session, borrowing: BorrowingHistoryCreate):
        db_borrowing = BorrowingHistory(**borrowing.dict())
        db.add(db_borrowing)
        db.commit()
        db.refresh(db_borrowing)
        return db_borrowing

    @staticmethod
    def return_book(db: Session, borrow_id: int):
        db_borrowing = db.query(BorrowingHistory).filter(BorrowingHistory.borrow_id == borrow_id).first()
        if db_borrowing:
            db_borrowing.status = "returned"
            db.commit()
            db.refresh(db_borrowing)
        return db_borrowing

    @staticmethod
    def get_borrowing_history(db: Session, user_id: int):
        return db.query(BorrowingHistory).filter(BorrowingHistory.user_id == user_id).all()