from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import date
from app.schemas.author import AuthorUpdate
from app.services.author_services import create_author
from app.models.author import Author

def read_author_service(
        db: Session
):
    authors = db.query(Author).filter(Author.is_deleted == False).all()
    return authors

def add_author_service(
        db,
        author
):
    try:
        new_author = create_author(db, author)
        return new_author
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


def get_author_service(
        db: Session,
        author_id: int
):
    author = db.query(Author).filter(Author.id == author_id, Author.is_deleted == False).first()

    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    return author


def partial_author_update_service(
        db: Session,
        author_id: int,
        author_data: AuthorUpdate
):
    author = db.query(Author).filter(Author.id == author_id).first()

    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    update_data = author_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(author, key, value)

    db.commit()
    db.refresh(author)
    return author


def soft_delete_author_service(
        db: Session,
        author_id: int
):
    author = db.query(Author).filter(Author.id == author_id).first()

    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    author.is_deleted = True
    author.deleted_at = date.today()

    db.commit()
    db.refresh(author)
    return author