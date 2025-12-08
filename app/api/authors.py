from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.author import  Author
from app.schemas.author import AuthorCreate, AuthorRead, AuthorUpdate, SoftDeleteAuthor
from app.services.token_api_services import require_admin
from app.services.authors_api_services import add_author, get_author, partial_author_update_service, soft_delete_author
from typing import List
from app.security.jwt_u import get_current_user
router = APIRouter(prefix="/authors", tags=["Authors"])

@router.post("/", response_model=AuthorRead)
def add_author(
        author: AuthorCreate
        , db: Session = Depends(get_db),
        current_user = Depends(get_current_user)
):
    require_admin(current_user)
    return add_author(db, author)

@router.get("/", response_model=List[AuthorRead])
def read_all_authors(
        db: Session = Depends(get_db),
        current_user = Depends(get_current_user)
):
    authors = db.query(Author).filter(Author.is_deleted == False).all()

    return authors

@router.get("/{author_id}", response_model=AuthorRead)
def read_one_author(
        author_id: int,
        db: Session = Depends(get_db),
        current_user = Depends(get_current_user)
):
    return get_author(db, author_id)

@router.patch("/{author_id}", response_model=AuthorRead)
def partial_update_author(
        author_id: int,
        author_data: AuthorUpdate,
        db: Session = Depends(get_db),
        current_user = Depends(get_current_user)
):
    require_admin(current_user)
    return partial_author_update_service(db, author_id, author_data)

@router.delete("/{author_id}", response_model=SoftDeleteAuthor)
def soft_delete_author(
        author_id: int,
        db: Session = Depends(get_db),
        current_user = Depends(get_current_user)
):
    require_admin(current_user)
    return soft_delete_author(db, author_id)

