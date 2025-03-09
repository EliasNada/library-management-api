import secrets

from sqlalchemy.orm import Session
from core.database.tables import User
from app.models.user import UserCreate
from core.auth.hashing import get_hash, verify_hash

class UserService:

    @staticmethod
    def generate_api_key():
        return secrets.token_urlsafe(32)

    @staticmethod
    def create_user(db: Session, user: UserCreate):
        hashed_password = get_hash(user.password)
        api_key = UserService.generate_api_key()
        hashed_api_key = get_hash(api_key)
        api_key_prefix = api_key[:10]
        db_user = User(
            username=user.username,
            password=hashed_password,
            email=user.email,
            role=user.role,
            api_key=hashed_api_key,
            api_key_prefix=api_key_prefix,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user, api_key

    @staticmethod
    def get_user(db: Session, user_id: int):
        return db.query(User).filter(User.user_id == user_id).first()

    @staticmethod
    def get_user_by_username(db: Session, username: str):
        return db.query(User).filter(User.username == username).first()

    @staticmethod
    def get_user_by_api_key(db: Session, api_key: str):
        api_key_prefix = api_key[:10]
        user = db.query(User).filter(User.api_key_prefix == api_key_prefix).first()
        if user and verify_hash(api_key, user.api_key):
            return user
        return None

    @staticmethod
    def regenerate_api_key(db: Session, user: User):
        new_api_key = UserService.generate_api_key()
        api_key_prefix = new_api_key[:10]
        hashed_api_key = get_hash(new_api_key)
        user.api_key = hashed_api_key
        user.api_key_prefix = api_key_prefix
        db.commit()
        db.refresh(user)
        return new_api_key


    @staticmethod
    def authenticate_user(db: Session, username: str, password: str):
        user = UserService.get_user_by_username(db, username)
        if not user or not verify_hash(password, user.password):
            return None
        return user

    @staticmethod
    def get_all_users(db: Session):
        return db.query(User).all()

    @staticmethod
    def update_user(db: Session, user_id: int, user: UserCreate):
        db_user = db.query(User).filter(User.user_id == user_id).first()
        if db_user:
            for key, value in user.dict().items():
                setattr(db_user, key, value)
            db.commit()
            db.refresh(db_user)
        return db_user

    @staticmethod
    def delete_user(db: Session, user_id: int):
        db_user = db.query(User).filter(User.user_id == user_id).first()
        if db_user:
            db.delete(db_user)
            db.commit()
        return db_user