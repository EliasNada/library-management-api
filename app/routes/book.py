from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database.database import get_db
from core.database.tables import User
from app.models.book import BookCreate, BookResponse
from app.services.book import BookService
from core.auth.dependencies import require_librarian

router = APIRouter()

@router.post("/books/", response_model=BookResponse)
def create_book(
    book: BookCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_librarian)
):
    return BookService.create_book(db, book)

@router.get("/books/{book_id}", response_model=BookResponse)
def read_book(book_id: int, db: Session = Depends(get_db)):
    db_book = BookService.get_book(db, book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@router.get("/books/", response_model=list[BookResponse])
def read_all_books(db: Session = Depends(get_db)):
    return BookService.get_all_books(db)

@router.put("/books/{book_id}", response_model=BookResponse)
def update_book(
    book_id: int,
    book: BookCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_librarian)
):
    db_book = BookService.update_book(db, book_id, book)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@router.delete("/books/{book_id}", response_model=BookResponse)
def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_librarian)
):
    db_book = BookService.delete_book(db, book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book