from core.auth.api_key import get_current_user_api_key
from core.auth.jwt import get_current_user_jwt
from core.database.tables import User
from fastapi import Depends, HTTPException, status


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