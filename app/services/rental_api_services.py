from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import date
from app.models.rental import Rental
from app.schemas.rental import RentalPatch, RentalCreate
from app.models.user import User

def read_rental_services(
        db: Session
):
    rentals = db.query(Rental).filter(Rental.is_deleted == False).all()
    return rentals

def get_rental_by_user_name(
        db: Session,
        user_full_name: str
):
    user = db.query(User).filter(User.full_name == user_full_name, User.is_deleted == False).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return db.query(Rental).filter(Rental.user_reader_id == user.id, Rental.is_deleted == False).first()

def add_rental_services(
        db: Session,
        rental: RentalCreate
):
    new_rental = Rental(**rental.model_dump())
    db.add(new_rental)
    db.commit()
    db.refresh(new_rental)
    return new_rental

def rental_partial_update_services(
        db: Session,
        rental_id: int,
        rental_data: RentalPatch
):
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

def rental_soft_delete_services(
        db: Session,
        rental_id: int
):
    rental = db.query(Rental).filter(Rental.id == rental_id).first()

    if not rental:
        raise HTTPException(status_code=404, detail="Rental not found.")

    rental.is_deleted = True
    rental.deleted_at = date.today()

    db.commit()
    db.refresh(rental)
    return rental