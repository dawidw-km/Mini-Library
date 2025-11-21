from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.author import Author
from app.schemas.author import AuthorCreate

def get_author_by_name(db: Session, name: str):
    return db.query(Author).filter(Author.name == name).first()

def create_author(db: Session, author_in: AuthorCreate):
    existing = get_author_by_name(db, author_in.name)
    if existing:
        raise ValueError("Author with that name already exists.")
    
    author = Author(
        name = author_in.name,
        birth_date = author_in.birth_date
    )
    db.add(author)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ValueError("Author already exist.")
    
    db.refresh(author)
    return author