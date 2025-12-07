from fastapi import APIRouter, Depends, HTTPException
from typing import List
from datetime import date
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserRead, SoftUserDelete, UserUpdate
from app.security.jwt_u import get_current_user
from app.services.user_api_services import add_user, partial_update_user_service
from app.services.token_api_services import require_admin
router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserRead)
def register_user(
        user: UserCreate,
        db: Session = Depends(get_db),
        current_user = Depends(get_current_user)
):
    require_admin(current_user)
    return add_user(db, user)


@router.get("/", response_model=List[UserRead])
def read_users(
        db: Session = Depends(get_db),
        current_user = Depends(get_current_user)
    ):
    users = db.query(User).filter(User.is_deleted == False).all()
    return users

@router.patch("/{user_id}", response_model=UserRead)
def partial_update_user(
        user_id: int,
        user_data: UserUpdate,
        db: Session = Depends(get_db),
        current_user = Depends(get_current_user)
):
    require_admin(current_user)
    return partial_update_user_service(db, user_id, user_data)


@router.delete("/{id}", response_model=SoftUserDelete)
def soft_user_delete(
        id: int,
        db: Session = Depends(get_db),
        current_user = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")

    user = db.query(User).filter(User.id == id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_deleted = True
    user.deleted_at = date.today()

    db.commit()
    db.refresh(user)
    return user

