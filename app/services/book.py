from sqlalchemy.orm import Session
from app.database.tables.book import Book
from app.schemas.book import BookCreate, BookResponse

class BookService:
    @staticmethod
    def create_book(db: Session, book: BookCreate):
        db_book = Book(**book.dict())
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
        return db_book

    @staticmethod
    def get_book(db: Session, book_id: int):
        return db.query(Book).filter(Book.book_id == book_id).first()

    @staticmethod
    def get_all_books(db: Session):
        return db.query(Book).all()

    @staticmethod
    def update_book(db: Session, book_id: int, book: BookCreate):
        db_book = db.query(Book).filter(Book.book_id == book_id).first()
        if db_book:
            for key, value in book.dict().items():
                setattr(db_book, key, value)
            db.commit()
            db.refresh(db_book)
        return db_book

    @staticmethod
    def delete_book(db: Session, book_id: int):
        db_book = db.query(Book).filter(Book.book_id == book_id).first()
        if db_book:
            db.delete(db_book)
            db.commit()
        return db_book