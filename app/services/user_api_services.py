from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import date
from app.schemas.user import UserUpdate
from app.models.user import User
from app.services.user_services import create_user

def read_user_services(
        db: Session
):
    users = db.query(User).filter(User.is_deleted == False).all()
    return users

def add_user(
        db,
        user
):
    try:
        new_user = create_user(db, user)
        return new_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

def partial_update_user_service(
    db: Session,
    user_id: int,
    user_data: UserUpdate
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")


    for key, value in user_data.model_dump(exclude_unset=True).items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user

def delete_user(
        db: Session,
        user_id: int
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_deleted = True
    user.deleted_at = date.today()

    db.commit()
    db.refresh(user)
    return user