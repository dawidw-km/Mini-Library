from fastapi import APIRouter, Depends, HTTPException
from typing import List
from datetime import date
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.author import Author
from app.models.book import Book
from app.schemas.book import BookCreate, BookRead, SoftBookDelete, BookUpdate

router = APIRouter(prefix="/books", tags=["Books"])

@router.post("/", response_model=BookRead)
def create_book(book_in: BookCreate, db: Session = Depends(get_db)):

    if not book_in.author_id and not book_in.author_name:
        raise HTTPException(status_code=400, detail="Provide ID or Name of the author")

    if book_in.author_id:
        author = db.get(Author, book_in.author_id)
    elif book_in.author_name:
        author = db.query(Author).filter(Author.name == book_in.author_name).first()

    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    
    book = Book(
        title=book_in.title,
        pages=book_in.pages,
        author_id=author.id 
    )
    
    db.add(book)
    db.commit()
    db.refresh(book)
    return book

@router.get("/", response_model=List[BookRead])
def read_books(db: Session = Depends(get_db)):
    books = db.query(Book).filter(Book.is_deleted == False).all()

    return books

@router.put("/", response_model=BookUpdate)
def update_book(book_id: int, book_in: BookUpdate, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    for key, value in book_in.dict().items():
        setattr(book, key, value)

    db.commit()
    db.refresh(book)
    return book

@router.delete("/", response_model=SoftBookDelete)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    book.is_deleted = True
    book.deleted_at = date.today()

    db.commit()
    db.refresh(book)
    return book