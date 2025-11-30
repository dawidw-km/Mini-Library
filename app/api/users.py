from fastapi import APIRouter, Depends, HTTPException
from typing import List
from datetime import date
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserRead, SoftUserDelete
from app.services.user_services import create_user


router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserRead)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        new_user = create_user(db, user)
        return new_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[UserRead])
def read_users(db: Session = Depends(get_db)):
    users = db.query(User).filter(User.is_deleted == False).all()

    return users

@router.delete("/{id}", response_model=SoftUserDelete)
def soft_user_delete(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_deleted = True
    user.deleted_at = date.today()

    db.commit()
    db.refresh(user)
    return user