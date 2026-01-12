from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.security.jwt_u import get_current_user
from app.services.user_api_services import add_user_service, partial_update_user_service, delete_user_service
from app.services.user_api_services import read_user_service
from app.services.token_api_services import require_admin
router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserRead, status_code=201)
def register_user(
        user: UserCreate,
        db: Session = Depends(get_db),
):
    return add_user_service(db, user)

@router.get("/", response_model=List[UserRead])
def read_all_users(
        db: Session = Depends(get_db),
        current_user = Depends(get_current_user)
    ):
    require_admin(current_user)
    return read_user_service(db)

@router.patch("/{user_id}", response_model=UserRead)
def partial_update_user(
        user_id: int,
        user_data: UserUpdate,
        db: Session = Depends(get_db),
        current_user = Depends(get_current_user)
):
    require_admin(current_user)
    return partial_update_user_service(db, user_id, user_data)

@router.delete("/{user_id}", status_code=204)
def soft_user_delete(
        user_id: int,
        db: Session = Depends(get_db),
        current_user = Depends(get_current_user)
):
    require_admin(current_user)
    delete_user_service(db, user_id)

