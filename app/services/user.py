import secrets
from typing import Tuple, Union, List

from sqlalchemy.orm import Session

from app.exceptions import InvalidRequest
from app.models.user import UserCreate
from app.models.user import UserUpdate
from core.auth.hashing import get_hash
from core.auth.hashing import verify_hash
from core.database.tables import User


class UserService:
    @staticmethod
    def generate_api_key() -> str:
        """
        Generates a random API key
        :return str:
        """
        return secrets.token_urlsafe(32)

    @staticmethod
    def create_user(db: Session, user: UserCreate) -> Tuple[User, str]:
        """
        Creates a new user, stores hashed password, and api key
        :param db:
        :param user:
        :return:
        """
        hashed_password = get_hash(user.password)
        api_key = UserService.generate_api_key()
        hashed_api_key = get_hash(api_key)
        api_key_prefix = api_key[:10] # expose the first 10 characters of key to speed up lookups
        db_user = User(
            username=user.username,
            password=hashed_password,
            email=user.email,
            role=user.role,
            api_key=hashed_api_key,
            api_key_prefix=api_key_prefix,
        )
        db.add(db_user)
        try:
            db.commit()
        except Exception as e:
            db.rollback()
            raise InvalidRequest(str(e))
        db.refresh(db_user)
        return db_user, api_key

    @staticmethod
    def get_user(db: Session, user_id: int) -> User:
        """
        Retrieves a user from the database by id
        :param db:
        :param user_id:
        :return:
        """
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_user_by_username(db: Session, username: str) -> User:
        """
        Retrieves a user from the database by username
        :param db:
        :param username:
        :return:
        """
        return db.query(User).filter(User.username == username).first()

    @staticmethod
    def get_user_by_api_key(db: Session, api_key: str) -> Union[User, None]:
        """
        Retrieves a user from the database by api key
        :param db:
        :param api_key:
        :return:
        """
        api_key_prefix = api_key[:10]
        user = db.query(User).filter(User.api_key_prefix == api_key_prefix).first()
        if user and verify_hash(api_key, user.api_key):
            return user
        return None

    @staticmethod
    def regenerate_api_key(db: Session, user: User) -> str:
        """
        regenerates a new API key
        :param db:
        :param user:
        :return:
        """
        new_api_key = UserService.generate_api_key()
        api_key_prefix = new_api_key[:10]
        hashed_api_key = get_hash(new_api_key)
        user.api_key = hashed_api_key
        user.api_key_prefix = api_key_prefix
        db.commit()
        db.refresh(user)
        return new_api_key

    @staticmethod
    def authenticate_user(db: Session, username: str, password: str) -> Union[User, None]:
        """
        performs check of user password to facilitate authentication
        :param db:
        :param username:
        :param password:
        :return:
        """
        user = UserService.get_user_by_username(db, username)
        if not user or not verify_hash(password, user.password):
            return None
        return user

    @staticmethod
    def get_all_users(db: Session) -> List[User]:
        """
        Lists all users in the database
        :param db:
        :return:
        """
        return db.query(User).all()

    @staticmethod
    def update_user(db: Session, user_id: int, user: UserUpdate) -> User:
        """
        Updates a user in the database
        :param db:
        :param user_id:
        :param user:
        :return:
        """
        db_user = db.query(User).filter(User.id == user_id).first()
        if db_user:
            for key, value in user.model_dump().items():
                if value:
                    setattr(db_user, key, value)
            db.commit()
            db.refresh(db_user)
        return db_user

    @staticmethod
    def delete_user(db: Session, user_id: int) -> User:
        """
        Deletes a user from the database
        :param db:
        :param user_id:
        :return:
        """
        db_user = db.query(User).filter(User.id == user_id).first()
        if db_user:
            db.delete(db_user)
            db.commit()
        return db_user
