from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database.database import get_db
from app.auth.utils import create_access_token, get_hash
from app.database.tables import User
from app.schemas import RegisterResponse, UserCreate, LoginResponse, NewApiKey
from app.services.user import UserService

router = APIRouter()

@router.post("/login", response_model=LoginResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = UserService.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": str(user.user_id)})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", response_model=RegisterResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = UserService.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    user, api_key = UserService.create_user(db, user)
    access_token = create_access_token(data={"sub": str(user.user_id)})
    return {"access_token": access_token, "token_type": "bearer", "api_key": api_key}

@router.post("/regenerate-api-key", response_model=NewApiKey)
def regenerate_api_key(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # Authenticate the user
):
    new_api_key = UserService.generate_api_key()
    hashed_api_key = get_hash(new_api_key)
    current_user.hashed_api_key = hashed_api_key
    db.commit()
    db.refresh(current_user)
    return {
        "api_key": new_api_key
    }