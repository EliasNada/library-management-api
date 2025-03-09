from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database.database import get_db
from app.models.borrowing_history import BorrowingHistoryCreate, BorrowingHistoryResponse
from app.services.borrowing_history import BorrowingHistoryService

router = APIRouter()

@router.post("/borrow/", response_model=BorrowingHistoryResponse)
def borrow_book(borrowing: BorrowingHistoryCreate, db: Session = Depends(get_db)):
    return BorrowingHistoryService.borrow_book(db, borrowing)

@router.put("/return/{borrow_id}", response_model=BorrowingHistoryResponse)
def return_book(borrow_id: int, db: Session = Depends(get_db)):
    db_borrowing = BorrowingHistoryService.return_book(db, borrow_id)
    if db_borrowing is None:
        raise HTTPException(status_code=404, detail="Borrowing record not found")
    return db_borrowing

@router.get("/history/{user_id}", response_model=list[BorrowingHistoryResponse])
def get_borrowing_history(user_id: int, db: Session = Depends(get_db)):
    return BorrowingHistoryService.get_borrowing_history(db, user_id)