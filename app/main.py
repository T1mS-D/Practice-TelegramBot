from fastapi import FastAPI
from app.api import books, categories
from app.db.db import create_tables

app = FastAPI(title="Book Store API")

@app.on_event("startup")
def on_startup():
    create_tables()


@app.get("/health")
def health_check():
    return {"status": "ok"}


app.include_router(categories.router)
app.include_router(books.router)