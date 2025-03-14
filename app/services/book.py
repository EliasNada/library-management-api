from typing import List

from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.models.book import BookCreate
from app.models.book import BookSearch
from core.database.database import BaseRepository
from core.database.tables import Book


class BookService(BaseRepository[Book, BookCreate]):
    def __init__(self):
        super().__init__(Book)

    def search_books(self, db: Session, search: BookSearch) -> List[Book]:
        """
        Search books by various filters
        :param db:
        :param search:
        :return List[Book]:
        """
        query = db.query(self.model)
        # apply any provided filters
        if search.title:
            query = query.filter(Book.title.ilike(f'%{search.title}%'))
        if search.author:
            query = query.filter(Book.author.ilike(f'%{search.author}%'))
        if search.category:
            query = query.filter(Book.category == search.category)
        if search.release_date_start and search.release_date_end:
            query = query.filter(
                and_(
                    Book.published_date >= search.release_date_start,
                    Book.published_date <= search.release_date_end,
                )
            )
        elif search.release_date_start:
            query = query.filter(Book.published_date >= search.release_date_start)
        elif search.release_date_end:
            query = query.filter(Book.published_date <= search.release_date_end)
        if search.is_available is not None:
            query = query.filter(Book.is_available == search.is_available)
        offset = (search.page - 1) * search.limit
        return query.offset(offset).limit(search.limit).all()

    @staticmethod
    def toggle_book_availability(db: Session, book_id: int) -> Book:
        """
        Toggle book availability, changes to true once book is returned, and to false when it's borrowed
        :param db:
        :param book_id:
        :return Book:
        """
        book = db.query(Book).filter(Book.id == book_id).first()
        print(book.is_available)
        if book:
            setattr(book, 'is_available', not book.is_available)
            db.commit()
            db.refresh(book)
        return book

