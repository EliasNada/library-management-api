from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.models import LoginResponse
from app.models import NewApiKey
from app.models import RegisterResponse
from app.models import UserCreate
from app.services.user import UserService
from core.auth.dependencies import get_current_user
from core.auth.jwt import create_access_token
from core.database.database import get_db
from core.database.tables import User

router = APIRouter()


@router.post('/common/auth/login', response_model=LoginResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = UserService.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    access_token = create_access_token(data={'sub': str(user.id)})
    return {'access_token': access_token, 'token_type': 'bearer'}


@router.post('/common/auth/register', response_model=RegisterResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = UserService.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail='Username already registered')
    user, api_key = UserService.create_user(db, user)
    access_token = create_access_token(data={'sub': str(user.id)})
    return {'access_token': access_token, 'token_type': 'bearer', 'api_key': api_key}


@router.post('/common/auth/regenerate-api-key', response_model=NewApiKey)
def regenerate_api_key(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return {'api_key': UserService.regenerate_api_key(db, current_user)}
