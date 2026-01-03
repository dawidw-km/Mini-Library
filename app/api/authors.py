from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.author import AuthorCreate, AuthorRead, AuthorUpdate
from app.services.token_api_services import require_admin
from app.services.authors_api_services import add_author_service, partial_author_update_service
from app.services.authors_api_services import read_author_service, get_author_service, soft_delete_author_service
from typing import List
from app.security.jwt_u import get_current_user
router = APIRouter(prefix="/authors", tags=["Authors"])

@router.post("/", response_model=AuthorRead, status_code=201)
def create_author(
        author: AuthorCreate
        , db: Session = Depends(get_db),
        current_user = Depends(get_current_user)
):
    require_admin(current_user)
    return add_author_service(db, author)

@router.get("/", response_model=List[AuthorRead])
def read_all_authors(
        db: Session = Depends(get_db),
        current_user = Depends(get_current_user)
):
    return read_author_service(db)

@router.get("/{author_id}", response_model=AuthorRead)
def read_one_author(
        author_id: int,
        db: Session = Depends(get_db),
        current_user = Depends(get_current_user)
):
    return get_author_service(db, author_id)

@router.patch("/{author_id}", response_model=AuthorRead)
def partial_update_author(
        author_id: int,
        author_data: AuthorUpdate,
        db: Session = Depends(get_db),
        current_user = Depends(get_current_user)
):
    require_admin(current_user)
    return partial_author_update_service(db, author_id, author_data)

@router.delete("/{author_id}", status_code=204)
def soft_delete_author(
        author_id: int,
        db: Session = Depends(get_db),
        current_user = Depends(get_current_user)
):
    require_admin(current_user)
    soft_delete_author_service(db, author_id)
