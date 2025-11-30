from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from app.db.session import get_db
from app.models.author import  Author
from app.schemas.author import AuthorCreate, AuthorRead, AuthorUpdate, SoftDeleteAuthor
from app.services.author_services import create_author
from typing import List
router = APIRouter(prefix="/authors", tags=["Authors"])

@router.post("/", response_model=AuthorRead)
def add_author(author: AuthorCreate, db: Session = Depends(get_db)):
    try:
        new_author = create_author(db, author)
        return new_author
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[AuthorRead])
def read_authors(db: Session = Depends(get_db)):
    authors = db.query(Author).filter(Author.is_deleted == False).all()

    return authors

@router.get("/{author_id}", response_model=AuthorRead)
def read_author(author_id: int, db: Session = Depends(get_db)):
    author = db.query(Author).filter(Author.id == author_id).first()

    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    return author

@router.put("/{author_id}", response_model=AuthorRead)
def full_update_author(author_id: int, author_data: AuthorUpdate, db: Session = Depends(get_db)):
    author = db.query(Author).filter(Author.id == author_id).first()

    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    for key, value in author_data.dict().items():
        setattr(author, key, value)

    db.commit()
    db.refresh(author)
    return author

@router.delete("/{author_id}", response_model=SoftDeleteAuthor)
def soft_delete_author(author_id: int, db: Session = Depends(get_db)):
    author = db.query(Author).filter(Author.id == author_id).first()

    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    author.is_deleted = True
    author.deleted_at = date.today()

    db.commit()
    db.refresh(author)
    return author

