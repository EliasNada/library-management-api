from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.exceptions import NotFoundError
from app.exceptions import UserBorrowingNotFound
from app.models.borrowing_history import BorrowingHistoryCreate
from app.models.borrowing_history import BorrowingHistoryResponse
from app.services.borrowing_history import BorrowingHistoryService
from core.auth.dependencies import get_current_user
from core.auth.dependencies import require_librarian
from core.database.database import get_db
from core.database.tables import User
from core.logging import logger

router = APIRouter()
borrowing_service = BorrowingHistoryService()


@router.post('/librarian/borrowing/borrow/', response_model=BorrowingHistoryResponse)
def borrow_book(
    borrowing: BorrowingHistoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return borrowing_service.borrow_book(db, borrowing)


@router.post('/user/borrow/{book_id}', response_model=BorrowingHistoryResponse)
def i_borrow_a_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    borrowing = BorrowingHistoryCreate(book_id=book_id, user_id=current_user.id)
    return borrowing_service.borrow_book(db, borrowing)


@router.post('/user/return/{borrow_id}', response_model=BorrowingHistoryResponse)
def i_return_a_book(
    borrow_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    borrowing = BorrowingHistoryService.get_borrowing_by_id(db, borrow_id)
    if not borrowing or borrowing.user_id != current_user.id:
        raise UserBorrowingNotFound()
    return borrowing_service.return_book(db, borrowing)

@router.put('/librarian/borrowing/return/{borrow_id}', response_model=BorrowingHistoryResponse)
def return_book(
    borrow_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_librarian),
):
    db_borrowing = borrowing_service.return_book(db, borrow_id)
    if not db_borrowing:
        raise NotFoundError()
    return db_borrowing


@router.get('/librarian/borrowing/history/{user_id}', response_model=list[BorrowingHistoryResponse])
def get_borrowing_history(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_librarian),
):
    try:
        return borrowing_service.get_borrowing_history(db, user_id)
    except Exception as e:
        logger.error(f'Error fetching borrowing history: {e}')
        raise HTTPException(status_code=500, detail='Failed to fetch borrowing history')


@router.get('/user/history', response_model=list[BorrowingHistoryResponse])
def get_my_borrowing_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return borrowing_service.get_borrowing_history(db, current_user.id)
    except Exception as e:
        logger.error(f'Error fetching borrowing history: {e}')
        raise HTTPException(status_code=500, detail='Failed to fetch borrowing history')
