from app.db.db import SessionLocal
from app.db import crud

def main():
    db = SessionLocal()

    try:
        categories = crud.get_categories(db)

        for category in categories:
            print(f"\nCATEGORY: {category.title}")

            books = crud.get_books_by_category(db, category.id)
            for book in books:
                print(f"  - {book.title}")
                print(f"    description: {book.description}")
                print(f"    price: {book.price}")
                print(f"    url: {book.url}")
    finally:
        db.close()

if __name__ == "__main__":
    main()