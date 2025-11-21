from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.author import AuthorCreate, AuthorRead
from app.services.author_services import create_author

router = APIRouter(prefix="/authors", tags=["Authors"])

@router.post("/", response_model=AuthorRead)
def add_author(author: AuthorCreate, db: Session = Depends(get_db)):
    try:
        new_author = create_author(db, author)
        return new_author
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))