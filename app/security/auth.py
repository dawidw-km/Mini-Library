from sqlalchemy.orm import Session
from app.models.user import User
from app.security.security import validate_password

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.login == username, User.is_deleted == False).first()
    if not user:
        return None

    if not validate_password(password, user.password_hash):
        return None

    return user