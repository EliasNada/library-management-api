from sqlalchemy.orm import Session
from core.database.tables import Category
from app.models.category import CategoryCreate


class CategoryService:
    @staticmethod
    def create_category(db: Session, category: CategoryCreate):
        db_category = Category(**category.dict())
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return db_category

    @staticmethod
    def get_category(db: Session, category_id: int):
        return db.query(Category).filter(Category.category_id == category_id).first()

    @staticmethod
    def get_all_categories(db: Session):
        return db.query(Category).all()

    @staticmethod
    def update_category(db: Session, category_id: int, category: CategoryCreate):
        db_category = db.query(Category).filter(Category.category_id == category_id).first()
        if db_category:
            for key, value in category.dict().items():
                setattr(db_category, key, value)
            db.commit()
            db.refresh(db_category)
        return db_category

    @staticmethod
    def delete_category(db: Session, category_id: int):
        db_category = db.query(Category).filter(Category.category_id == category_id).first()
        if db_category:
            db.delete(db_category)
            db.commit()
        return db_category