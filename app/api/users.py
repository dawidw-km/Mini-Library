from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserRead

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserRead)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(
        login=user.login,
        password=user.password,
        full_name=user.full_name,
        birth_date=user.birth_date,
        city=user.city,
        street=user.street,
        postal_code=user.postal_code,
        address_email=user.address_email
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

