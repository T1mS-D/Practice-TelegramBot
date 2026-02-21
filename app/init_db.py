from app.db.db import create_tables, SessionLocal
from app.db import crud


def init():
    create_tables()
    db = SessionLocal()

    try:
        #Категории
        fiction = crud.create_category(db, "Fiction")
        programming = crud.create_category(db, "Programming")


        #Fiction
        crud.create_book(
            db,
            title="1984",
            description="Dystopian novel",
            price=15.50,
            category_id=fiction.id
        )

        crud.create_book(
            db,
            title="Brave New World",
            description="Classic sci-fi dystopia",
            price=14.20,
            category_id=fiction.id
        )

        #Programming
        crud.create_book(
            db,
            title="Clean Code",
            description="Guide to writing clean code",
            price=35.00,
            category_id=programming.id
        )

        crud.create_book(
            db,
            title="Fluent Python",
            description="Advanced Python programming",
            price=42.90,
            category_id=programming.id
        )

        print("Database initialized with test data ✅")

    finally:
        db.close()


if __name__ == "__main__":
    init()