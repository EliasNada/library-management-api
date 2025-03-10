from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user import UserCreate
from app.models.user import UserUpdate
from app.models.user import UserResponse
from app.services.user import UserService
from core.auth.dependencies import get_current_user
from core.database.database import get_db
from core.database.tables import User

router = APIRouter()


@router.post('/librarian/users/', response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user, api_key = UserService.create_user(db, user)
    return db_user


@router.get('/librarian/users/{user_id}', response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = UserService.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return db_user


@router.get('/librarian/users/', response_model=list[UserResponse])
def read_all_users(db: Session = Depends(get_db)):
    return UserService.get_all_users(db)


@router.get('/user/me', response_model=UserResponse)
def get_my_user(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    return current_user


@router.put('/librarian/users/{user_id}', response_model=UserResponse)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = UserService.update_user(db, user_id, user)
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return db_user


@router.delete('/librarian/users/{user_id}', response_model=UserResponse)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = UserService.delete_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return db_user
