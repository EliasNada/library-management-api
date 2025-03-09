from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.database.tables import User
from app.schemas.category import CategoryCreate, CategoryResponse
from app.services.category import CategoryService
from app.auth.dependencies import require_librarian

router = APIRouter()

@router.post("/categories/", response_model=CategoryResponse)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_librarian)  # Only librarians can create categories
):
    return CategoryService.create_category(db, category)

@router.get("/categories/{category_id}", response_model=CategoryResponse)
def read_category(category_id: int, db: Session = Depends(get_db)):
    db_category = CategoryService.get_category(db, category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

@router.get("/categories/", response_model=list[CategoryResponse])
def read_all_categories(db: Session = Depends(get_db)):
    return CategoryService.get_all_categories(db)

@router.put("/categories/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_librarian)  # Only librarians can update categories
):
    db_category = CategoryService.update_category(db, category_id, category)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

@router.delete("/categories/{category_id}", response_model=CategoryResponse)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_librarian)  # Only librarians can delete categories
):
    db_category = CategoryService.delete_category(db, category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category