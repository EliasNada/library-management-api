from datetime import date
from typing import Optional

from pydantic import BaseModel


class BookCreate(BaseModel):
    title: str
    author: str
    isbn: str
    category: str
    published_date: date | None = None


class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    isbn: str
    category: str
    published_date: date | None
    is_available: bool

    class Config:
        from_attributes = True  # Allows ORM mode for SQLAlchemy models


class BookSearch(BaseModel):
    title: Optional[str] = None
    category: Optional[str] = None
    release_date_start: Optional[date] = None
    release_date_end: Optional[date] = None
    is_available: Optional[bool] = None
    limit: Optional[int] = 10
    page: Optional[int] = 1
