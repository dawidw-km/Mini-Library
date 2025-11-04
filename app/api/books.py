from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.author import Author
from app.models.book import Book
from app.schemas.book import BookCreate, BookRead

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