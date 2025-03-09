from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP, Enum, text
from app.database.database import Base

class BorrowingHistory(Base):
    __tablename__ = 'borrowing_history'
    borrow_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    book_id = Column(Integer, ForeignKey('books.book_id'), nullable=False)
    borrow_date = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    return_date = Column(TIMESTAMP)
    status = Column(Enum('borrowed', 'returned', name='borrow_status'), default='borrowed')