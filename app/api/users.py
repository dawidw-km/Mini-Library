from fastapi import APIRouter, Depends, HTTPException
from typing import List
from datetime import date
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserRead, SoftUserDelete, UserUpdate
from app.services.user_services import create_user
from app.security.jwt_u import get_current_user

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserRead)
def register_user(
        user: UserCreate,
        db: Session = Depends(get_db),
        current_user = Depends(get_current_user)
):
    if current_user != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")

    try:
        new_user = create_user(db, user)
        return new_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[UserRead])
def read_users(
        db: Session = Depends(get_db),
        current_user = Depends(get_current_user)
    ):
    users = db.query(User).filter(User.is_deleted == False).all()
    return users

@router.put("/", response_model=UserUpdate)
def partial_update_user(
        user_id: int,
        user_data: UserUpdate,
        db: Session = Depends(get_db),
        current_user = Depends(get_current_user)
):
    if current_user != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in user_data.model_dump().items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user


@router.delete("/{id}", response_model=SoftUserDelete)
def soft_user_delete(
        id: int,
        db: Session = Depends(get_db),
        current_user = Depends(get_current_user)
):
    if current_user != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")

    user = db.query(User).filter(User.id == id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_deleted = True
    user.deleted_at = date.today()

    db.commit()
    db.refresh(user)
    return user

