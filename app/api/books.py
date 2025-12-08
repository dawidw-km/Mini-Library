from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.book import BookCreate, BookRead, SoftBookDelete, BookUpdate
from app.services.token_api_services import require_admin
from app.services.books_api_services import add_book, partial_update_book_service, soft_delete_book_service
from app.services.books_api_services import read_book_service
from app.security.jwt_u import get_current_user

router = APIRouter(prefix="/books", tags=["Books"])

@router.post("/", response_model=BookRead)
def create_book(
        book_in: BookCreate,
        db: Session = Depends(get_db),
        current_user = Depends(get_current_user)
):
    require_admin(current_user)
    return add_book(db, book_in)

@router.get("/", response_model=List[BookRead])
def read_books(
        db: Session = Depends(get_db),
        current_user = Depends(get_current_user)
):
  read_book_service(db)

@router.patch("/", response_model=BookUpdate)
def partial_update_book(
        book_id: int,
        book_in: BookUpdate,
        db: Session = Depends(get_db),
        current_user = Depends(get_current_user)
):
    require_admin(current_user)
    return partial_update_book_service(db, book_id, book_in)

@router.delete("/", response_model=SoftBookDelete)
def delete_book(
        book_id: int,
        db: Session = Depends(get_db),
        current_user = Depends(get_current_user)
):
    require_admin(current_user)
    return soft_delete_book_service(db, book_id)