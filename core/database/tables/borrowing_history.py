from sqlalchemy import Index
from sqlalchemy import TIMESTAMP
from sqlalchemy import Column
from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import text

from core.database.database import Base


class BorrowingHistory(Base):
    __tablename__ = 'borrowing_history'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    borrow_date = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    return_date = Column(TIMESTAMP)
    status = Column(Enum('borrowed', 'returned', name='borrow_status'), default='borrowed')


Index('user_id_index', BorrowingHistory.user_id)
Index('book_id_index', BorrowingHistory.book_id)
