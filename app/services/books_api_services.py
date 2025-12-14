from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import date
from app.models.book import Book
from app.schemas.book import BookUpdate
from app.services.books_services import create_book

def read_book_service(
        db: Session,
):
    books = db.query(Book).filter(Book.is_deleted == False).all()
    return books

def get_single_book_service(
        db: Session,
        book_id: int
):
    book = db.query(Book).filter(Book.id == book_id, Book.is_deleted == False).first()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    return book

def add_book_service(
        db,
        book
):
    try:
        new_book = create_book(db, book)
        return new_book
    except ValueError:
        return HTTPException(status_code=400, detail="Book already exists")


def partial_update_book_service(
        db: Session,
        book_id: int,
        book_in: BookUpdate,
):
    book = db.query(Book).filter(Book.id == book_id).first()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    for key, value in book_in.model_dump(exclude_unset=True).items():
        setattr(book, key, value)

    db.commit()
    db.refresh(book)
    return book

def soft_delete_book_service(
        db: Session,
        book_id: int
):
    book = db.query(Book).filter(Book.id == book_id).first()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    book.is_deleted = True
    book.deleted_at = date.today()

    db.commit()
    db.refresh(book)
    return book