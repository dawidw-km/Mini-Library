from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas.rental import RentalCreate, RentalRead, RentalPatch, RentalReturn
from app.services.token_api_services import require_admin
from app.services.rental_api_services import rental_partial_update_service, rental_soft_delete_service
from app.services.rental_api_services import add_rental_service, read_rental_service, rental_return_book_service
from app.security.jwt_u import get_current_user

router = APIRouter(prefix="/rentals", tags=["Rentals"])

@router.post("/", response_model=RentalRead, status_code=201)
def create_rental(
        rental: RentalCreate,
        db: Session = Depends(get_db),
        current_user = Depends(get_current_user)
):
    return add_rental_service(db, rental)

@router.get("/", response_model=List[RentalRead])
def read_all_rentals(
        db: Session = Depends(get_db),
        current_user = Depends(get_current_user)
):
    return read_rental_service(db)


@router.patch("/{rental_id}", response_model=RentalRead)
def partial_update_rental(
        rental_id: int,
        rental_data: RentalPatch,
        db: Session = Depends(get_db),
        current_user = Depends(get_current_user)
):
    require_admin(current_user)
    return rental_partial_update_service(db, rental_id, rental_data)

@router.patch("/{rental_id}/return", response_model=RentalRead)
def rental_book_return(
        rental_id: int,
        data: RentalReturn,
        db: Session = Depends(get_db),
        current_user = Depends(get_current_user)
):
    require_admin(current_user)
    return rental_return_book_service(db, rental_id, data)

@router.delete("/{rental_id}", status_code=204)
def soft_delete_rental(
        rental_id: int,
        db: Session = Depends(get_db),
        current_user = Depends(get_current_user)
):
    require_admin(current_user)
    rental_soft_delete_service(db, rental_id)
