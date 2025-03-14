import os
from datetime import datetime
from datetime import timedelta
from datetime import UTC

from dotenv import load_dotenv

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from jose import jwt
from sqlalchemy.orm import Session

from app.services import UserService
from core.database.database import get_db

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        return payload
    except JWTError:
        return False


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/login', auto_error=False)


def get_current_user_jwt(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    if not token:
        return None
    payload = decode_access_token(token)
    if not payload:
        return None
    user_id = payload.get('sub')
    if not user_id:
        return None
    user = UserService.get_user(db, user_id)
    if not user:
        return None
    return user
