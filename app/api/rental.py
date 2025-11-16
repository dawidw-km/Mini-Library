from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.rental import Rental
from app.schemas.rental import RentalCreate, RentalRead

router = APIRouter(prefix="/rental", tags=["Rental"])

@router.post("/", response_model=RentalRead)
def create_rentals(rental: RentalCreate, db: Session = Depends(get_db)):
    new_rental = Rental(**rental.dict())
    db.add(new_rental)
    db.commit()
    db.refresh(new_rental)
    return new_rental