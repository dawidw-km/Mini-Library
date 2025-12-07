from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.user import User
from app.schemas.user import UserCreate
from app.security.security import get_password_hash

def get_user_by_login(db: Session, login: str):
    return db.query(User).filter(User.login == login).first()

def create_user(db: Session, user_in: UserCreate):
    existing = get_user_by_login(db, user_in.login)
    if existing:
        raise ValueError("User already in the database.")
    
    hashed_password = get_password_hash(user_in.password)

    user = User(
        login = user_in.login,
        password_hash = hashed_password,
        full_name = user_in.full_name,
        birth_date = user_in.birth_date,
        city = user_in.city,
        street = user_in.street,
        postal_code = user_in.postal_code,
        address_email = user_in.address_email
    )
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ValueError("Login already exist")
    
    db.refresh(user)
    return user


