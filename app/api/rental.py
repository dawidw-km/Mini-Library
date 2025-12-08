from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.rental import Rental
from app.schemas.rental import RentalCreate, RentalRead, RentalPatch
from app.services.token_api_services import require_admin
from app.services.rental_api_services import rental_partial_update_services, rental_soft_delete_services
from app.services.rental_api_services import add_rental_services
from app.security.jwt_u import get_current_user

router = APIRouter(prefix="/rental", tags=["Rental"])

@router.get("/", response_model=List[RentalRead])
def read_rentals(
        db: Session = Depends(get_db),
        current_user = Depends(get_current_user)
):
    rentals = db.query(Rental).all()

    return rentals

@router.post("/", response_model=RentalRead)
def create_rentals(
        rental: RentalCreate,
        db: Session = Depends(get_db),
        current_user = Depends(get_current_user)
):
    require_admin(current_user)
    return add_rental_services(db, rental)

@router.patch("/", response_model=RentalPatch)
def partial_update_rental(
        rental_id: int,
        rental_data: RentalPatch,
        db: Session = Depends(get_db),
        current_user = Depends(get_current_user)
):
    require_admin(current_user)
    return rental_partial_update_services(db, rental_id, rental_data)

@router.delete("/", response_model=RentalRead)
def soft_delete_rentals(
        rental_id: int,
        db: Session = Depends(get_db),
        current_user = Depends(get_current_user)
):
    require_admin(current_user)
    return rental_soft_delete_services(db, rental_id)