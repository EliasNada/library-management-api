from fastapi.security import OAuth2PasswordBearer
from app.auth.utils import decode_access_token
from app.database.tables import User
from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.services.user import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")
def get_current_user_jwt(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = decode_access_token(token)
    if not payload:
        return None
    user_id = payload.get("sub")
    if not user_id:
        return None
    user = UserService.get_user(db, user_id)
    if not user:
        return None
    return user

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
def get_current_user_api_key(api_key: str = Depends(api_key_header), db: Session = Depends(get_db)):
    if not api_key:
        return None
    user = UserService.get_user_by_api_key(db, api_key)
    if not user:
        return None
    return user

def get_current_user(
    jwt_user: User = Depends(get_current_user_jwt),
    api_key_user: User = Depends(get_current_user_api_key)
):
    if api_key_user:
        return api_key_user
    if jwt_user:
        return jwt_user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated (Valid JWT or API key required)",
    )

def require_librarian(current_user: User = Depends(get_current_user)):
    if current_user.role != "librarian":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only librarians can perform this action",
        )
    return current_user