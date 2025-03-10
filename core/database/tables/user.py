from sqlalchemy import Column, Integer, String, TIMESTAMP, Enum, text
from core.database.database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    role = Column(Enum('user', 'librarian', name='user_roles'), default='user')
    api_key = Column(String(255), unique=True, nullable=True)
    api_key_prefix = Column(String(10), unique=True, nullable=True)
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(
        TIMESTAMP,
        server_default=text('CURRENT_TIMESTAMP'),
        onupdate=text('CURRENT_TIMESTAMP'),
    )
