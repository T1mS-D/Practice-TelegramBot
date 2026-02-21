from sqlalchemy.orm import Session
from app.db.models import Category, Book

#CATEGORY CRUD
def create_category(db: Session, title: str) -> Category:
    category = Category(title=title)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def get_category(db: Session, category_id: int) -> Category | None:
    return db.query(Category).filter(Category.id == category_id).first()


def get_categories(db: Session):
    return db.query(Category).all()


def update_category(db: Session, category_id: int, title: str):
    category = get_category(db, category_id)
    if not category:
        return None
    category.title = title
    db.commit()
    db.refresh(category)
    return category


def delete_category(db: Session, category_id: int):
    category = get_category(db, category_id)
    if not category:
        return None
    db.delete(category)
    db.commit()
    return category

#BOOK CRUD
def create_book(
    db: Session,
    title: str,
    description: str,
    price,
    category_id: int,
    url: str | None = None
) -> Book:
    book = Book(
        title=title,
        description=description,
        price=price,
        category_id=category_id,
        url=url
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def get_book(db: Session, book_id: int) -> Book | None:
    return db.query(Book).filter(Book.id == book_id).first()


def get_books(db: Session):
    return db.query(Book).all()


def get_books_by_category(db: Session, category_id: int):
    return db.query(Book).filter(Book.category_id == category_id).all()


def update_book(
    db: Session,
    book_id: int,
    **kwargs
):
    book = get_book(db, book_id)
    if not book:
        return None

    for key, value in kwargs.items():
        if hasattr(book, key):
            setattr(book, key, value)

    db.commit()
    db.refresh(book)
    return book


def delete_book(db: Session, book_id: int):
    book = get_book(db, book_id)
    if not book:
        return None
    db.delete(book)
    db.commit()
    return book