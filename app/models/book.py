from pydantic import BaseModel
from datetime import date

class BookCreate(BaseModel):
    title: str
    author: str
    isbn: str
    category_id: int | None = None
    published_date: date | None = None

class BookResponse(BaseModel):
    book_id: int
    title: str
    author: str
    isbn: str
    category_id: int | None
    published_date: date | None
    availability_status: bool

    class Config:
        from_attributes = True  # Allows ORM mode for SQLAlchemy models