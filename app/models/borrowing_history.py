from pydantic import BaseModel
from datetime import datetime

class BorrowingHistoryCreate(BaseModel):
    user_id: int
    book_id: int
    status: str = "borrowed"

class BorrowingHistoryResponse(BaseModel):
    borrow_id: int
    user_id: int
    book_id: int
    borrow_date: datetime
    return_date: datetime | None
    status: str

    class Config:
        from_attributes = True