from fastapi import Depends
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session

from app.services import UserService
from core.database.database import get_db

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
def get_current_user_api_key(api_key: str = Depends(api_key_header), db: Session = Depends(get_db)):
    if not api_key:
        return None
    user = UserService.get_user_by_api_key(db, api_key)
    if not user:
        return None
    return user