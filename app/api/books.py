from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.db.db import get_db
from app.db import crud
from app import schemas

router = APIRouter(prefix="/books", tags=["Books"])


@router.get("/", response_model=list[schemas.BookResponse])
def get_books(
    category_id: int | None = Query(default=None),
    db: Session = Depends(get_db)
):
    if category_id:
        return crud.get_books_by_category(db, category_id)
    return crud.get_books(db)


@router.get("/{book_id}", response_model=schemas.BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = crud.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.post(
    "/",
    response_model=schemas.BookResponse,
    status_code=status.HTTP_201_CREATED
)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):

    # Проверка существования категории
    category = crud.get_category(db, book.category_id)
    if not category:
        raise HTTPException(status_code=400, detail="Category does not exist")

    return crud.create_book(
        db,
        title=book.title,
        description=book.description,
        price=book.price,
        category_id=book.category_id,
        url=book.url
    )


@router.put("/{book_id}", response_model=schemas.BookResponse)
def update_book(
    book_id: int,
    book: schemas.BookUpdate,
    db: Session = Depends(get_db)
):
    # если обновляют категорию — проверяем
    if book.category_id:
        category = crud.get_category(db, book.category_id)
        if not category:
            raise HTTPException(status_code=400, detail="Category does not exist")

    updated = crud.update_book(db, book_id, **book.dict(exclude_unset=True))

    if not updated:
        raise HTTPException(status_code=404, detail="Book not found")

    return updated


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_book(db, book_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Book not found")