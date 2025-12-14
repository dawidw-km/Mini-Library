from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.book import BookCreate, BookRead, BookUpdate
from app.services.token_api_services import require_admin
from app.services.books_api_services import add_book_service, partial_update_book_service, soft_delete_book_service
from app.services.books_api_services import read_book_service, get_single_book_service
from app.security.jwt_u import get_current_user

router = APIRouter(prefix="/books", tags=["Books"])

@router.post("/", response_model=BookRead, status_code=201)
def create_book(
        book_in: BookCreate,
        db: Session = Depends(get_db),
        current_user = Depends(get_current_user)
):
    require_admin(current_user)
    return add_book_service(db, book_in)

@router.get("/", response_model=List[BookRead])
def read_all_books(
        db: Session = Depends(get_db),
        current_user = Depends(get_current_user)
):
    return read_book_service(db)

@router.get("/{book_id}", response_model=BookRead)
def read_one_book(
        book_id: int,
        db: Session = Depends(get_db),
        current_user = Depends(get_current_user)
):
    return get_single_book_service(db, book_id)

@router.patch("/{book_id}", response_model=BookRead)
def partial_update_book(
        book_id: int,
        book_in: BookUpdate,
        db: Session = Depends(get_db),
        current_user = Depends(get_current_user)
):
    require_admin(current_user)
    return partial_update_book_service(db, book_id, book_in)

@router.delete("/{book_id}", status_code=204)
def soft_delete_book(
        book_id: int,
        db: Session = Depends(get_db),
        current_user = Depends(get_current_user)
):
    require_admin(current_user)
    soft_delete_book_service(db, book_id)