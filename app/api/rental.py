from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.rental import Rental
from app.schemas.rental import RentalCreate, RentalRead, RentalUpdate, RentalPatch
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
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions.")

    new_rental = Rental(**rental.model_dump())
    db.add(new_rental)
    db.commit()
    db.refresh(new_rental)
    return new_rental

@router.put("/", response_model=RentalUpdate)
def full_update_rental(
        rental_id: int,
        rental_data: RentalUpdate,
        db: Session = Depends(get_db),
        current_user = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions.")

    rental = db.query(Rental).filter(Rental.id == rental_id).first()

    if not rental:
        raise HTTPException(
            status_code=404,
            detail="Rental not found."
        )
    
    for key, value, in rental_data.model_dump().items():
        setattr(rental, key, value)
    
    db.commit()
    db.refresh(rental)
    return rental

@router.patch("/", response_model=RentalPatch)
def partial_update_rental(
        rental_id: int,
        rental_data: RentalPatch,
        db: Session = Depends(get_db),
        current_user = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions.")

    rental = db.query(Rental).filter(Rental.id == rental_id).first()

    if not rental:
        raise HTTPException(
            status_code=404,
            detail="Rental not found."
        )

    update_data = rental_data.model_dump(exclude_unset=True)

    if "ending_date" in update_data and update_data["ending_date"] < rental.starting_date:
        raise HTTPException(
            status_code=400,
            detail="Ending date cannot be earlier than starting date."
        )
    
    for key, value in update_data.items():
        setattr(rental, key, value)
        
    db.commit()
    db.refresh(rental)
    return rental
    