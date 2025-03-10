import os
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError, DataError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Type, TypeVar, Generic, Optional
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.exceptions import (
    NotFoundError,
    InvalidRequest,
    UniqueConstraintError,
    ForeignKeyError,
    ValueTooLongError,
)

DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class BaseRepository(Generic[ModelType, CreateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, id: int) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> list[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, obj_in: CreateSchemaType) -> ModelType:
        db_obj = self.model(**obj_in.model_dump())
        db.add(db_obj)
        try:
            db.commit()
        except IntegrityError as e:
            db.rollback()
            if 'unique constraint' in str(e).lower():
                raise UniqueConstraintError()
            elif 'foreign key' in str(e).lower():
                raise ForeignKeyError()
            raise InvalidRequest('Database error')
        except DataError as e:
            db.rollback()
            if 'value too long' in str(e).lower():
                raise ValueTooLongError()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, id: int, obj_in: UpdateSchemaType) -> Optional[ModelType]:
        db_obj = self.get(db, id)
        if not db_obj:
            raise NotFoundError()
        for key, value in obj_in.dict().items():
            setattr(db_obj, key, value)
        try:
            db.commit()
        except IntegrityError as e:
            db.rollback()
            if 'unique constraint' in str(e).lower():
                raise UniqueConstraintError()
            elif 'foreign key' in str(e).lower():
                raise ForeignKeyError()
            raise InvalidRequest('Database error')
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, id: int) -> Optional[ModelType]:
        db_obj = self.get(db, id)
        if not db_obj:
            raise NotFoundError()
        db.delete(db_obj)
        db.commit()
        return db_obj
