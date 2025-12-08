from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.book import Author, Book
from app.schemas.book import BookCreate

def create_book(
        db: Session,
        book_in: BookCreate
):
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