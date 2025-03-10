from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.exceptions import NotFoundError
from core.database.database import get_db
from app.models.borrowing_history import (
    BorrowingHistoryCreate,
    BorrowingHistoryResponse,
)
from app.services.borrowing_history import BorrowingHistoryService
from core.auth.dependencies import get_current_user
from core.database.tables import User
from core.logging import logger

router = APIRouter()
borrowing_service = BorrowingHistoryService()


@router.post('/borrow/', response_model=BorrowingHistoryResponse)
def borrow_book(
    borrowing: BorrowingHistoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return borrowing_service.borrow_book(db, borrowing)
    except Exception as e:
        logger.error(f'Error borrowing book: {e}')
        raise HTTPException(status_code=500, detail='Failed to borrow book')


@router.put('/return/{borrow_id}', response_model=BorrowingHistoryResponse)
def return_book(
    borrow_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        db_borrowing = borrowing_service.return_book(db, borrow_id)
        if not db_borrowing:
            raise NotFoundError()
        return db_borrowing
    except Exception as e:
        logger.error(f'Error returning book: {e}')
        raise HTTPException(status_code=500, detail='Failed to return book')


@router.get('/history/{user_id}', response_model=list[BorrowingHistoryResponse])
def get_borrowing_history(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return borrowing_service.get_borrowing_history(db, user_id)
    except Exception as e:
        logger.error(f'Error fetching borrowing history: {e}')
        raise HTTPException(status_code=500, detail='Failed to fetch borrowing history')
