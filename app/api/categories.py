from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.db import get_db
from app.db import crud
from app import schemas

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/", response_model=list[schemas.CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    return crud.get_categories(db)


@router.get("/{category_id}", response_model=schemas.CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = crud.get_category(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.post(
    "/",
    response_model=schemas.CategoryResponse,
    status_code=status.HTTP_201_CREATED
)
def create_category(
    category: schemas.CategoryCreate,
    db: Session = Depends(get_db)
):
    return crud.create_category(db, category.title)


@router.put("/{category_id}", response_model=schemas.CategoryResponse)
def update_category(
    category_id: int,
    category: schemas.CategoryUpdate,
    db: Session = Depends(get_db)
):
    updated = crud.update_category(db, category_id, category.title)
    if not updated:
        raise HTTPException(status_code=404, detail="Category not found")
    return updated


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_category(db, category_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Category not found")