from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.orm import Session
from starlette.requests import Request

from app.exceptions import NotFoundError
from app.models.book import BookCreate
from app.models.book import BookUpdate
from app.models.book import BookResponse
from app.models.book import BookSearch
from app.services.book import BookService
from core.auth.dependencies import get_current_user
from core.database.database import get_db
from core.database.tables import User
from core.logging import logger

router = APIRouter()
book_service = BookService()

limiter = Limiter(key_func=get_remote_address)


@router.post('/books/', response_model=BookResponse)
@limiter.limit('5/minute')
def create_book(
    request: Request,
    book: BookCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return book_service.create(db, book)


@router.get('/books/{book_id}', response_model=BookResponse)
def read_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        db_book = book_service.get(db, book_id)
        if not db_book:
            raise NotFoundError()
        return db_book
    except Exception as e:
        logger.error(f'Error fetching book: {e}')
        raise HTTPException(status_code=500, detail='Failed to fetch book')


@router.get('/books/', response_model=list[BookResponse])
def read_all_books(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    try:
        return book_service.get_all(db)
    except Exception as e:
        logger.error(f'Error fetching books: {e}')
        raise HTTPException(status_code=500, detail='Failed to fetch books')


@router.put('/books/{book_id}', response_model=BookResponse)
def update_book(
    book_id: int,
    book: BookUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_book = book_service.update(db, book_id, book)
    if not db_book:
        raise NotFoundError()
    return db_book


@router.delete('/books/{book_id}', response_model=BookResponse)
def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        db_book = book_service.delete(db, book_id)
        if not db_book:
            raise NotFoundError()
        return db_book
    except Exception as e:
        logger.error(f'Error deleting book: {e}')
        raise HTTPException(status_code=500, detail='Failed to delete book')


@router.post('/books/search', response_model=list[BookResponse])
def search_books(
    search: BookSearch,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return book_service.search_books(db, search)
    except Exception as e:
        logger.error(f'Error searching books: {e}')
        raise HTTPException(status_code=500, detail='Failed to search books')
