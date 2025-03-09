from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, TIMESTAMP, text
from core.database.database import Base

class Book(Base):
    __tablename__ = 'books'
    book_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    author = Column(String(255), nullable=False)
    isbn = Column(String(13), unique=True, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.category_id'), nullable=True)
    published_date = Column(Date)
    availability_status = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), onupdate=text('CURRENT_TIMESTAMP'))