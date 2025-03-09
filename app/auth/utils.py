from datetime import datetime, timedelta

import bcrypt
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status

# Secret key for JWT encoding/decoding
SECRET_KEY = "your-secret-key"  # Replace with a secure secret key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_hash(plain_secret: str, hashed_secret: str):
    secret_byte_enc = plain_secret.encode('utf-8')
    hashed_secret = hashed_secret.encode('utf-8')
    return bcrypt.checkpw(password=secret_byte_enc, hashed_password=hashed_secret)

def get_hash(secret: str):
    secret_bytes = secret.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(password=secret_bytes, salt=salt)
    return hash.decode('utf-8')


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        return payload
    except JWTError:
        return False
