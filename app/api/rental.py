from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas.rental import RentalCreate, RentalRead, RentalPatch
from app.services.token_api_services import require_admin
from app.services.rental_api_services import rental_partial_update_services, rental_soft_delete_services
from app.services.rental_api_services import add_rental_services, read_rental_services, get_rental_by_user_name
from app.security.jwt_u import get_current_user

router = APIRouter(prefix="/rentals", tags=["Rentals"])

@router.post("/", response_model=RentalRead, status_code=201)
def create_rental(
        rental: RentalCreate,
        db: Session = Depends(get_db),
        current_user = Depends(get_current_user)
):
    require_admin(current_user)
    return add_rental_services(db, rental)

@router.get("/", response_model=List[RentalRead])
def read_all_rentals(
        db: Session = Depends(get_db),
        current_user = Depends(get_current_user)
):
    return read_rental_services(db)


### fix it
@router.get("/{user_name}", response_model=RentalRead)
def read_renta_by_name(
        user_name: str,
        db: Session = Depends(get_db),
        current_user = Depends(get_current_user)
):
    return get_rental_by_user_name(db, user_name)

@router.patch("/{rental_id}", response_model=RentalRead)
def partial_update_rental(
        rental_id: int,
        rental_data: RentalPatch,
        db: Session = Depends(get_db),
        current_user = Depends(get_current_user)
):
    require_admin(current_user)
    return rental_partial_update_services(db, rental_id, rental_data)

@router.delete("/{rental_id}", status_code=204)
def soft_delete_rental(
        rental_id: int,
        db: Session = Depends(get_db),
        current_user = Depends(get_current_user)
):
    require_admin(current_user)
    rental_soft_delete_services(db, rental_id)