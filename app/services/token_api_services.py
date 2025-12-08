from datetime import timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.security.jwt_u import create_access_token
from app.security.auth import authenticate_user
from app.schemas.token import Token
from app.core.config import settings

def user_login(db: Session, username: str, password: str) -> Token:
    user = authenticate_user(db, username, password)

    if not user:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    access_token = create_access_token(
        data={"sub": user.login}, expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type="bearer")

def require_admin(current_user):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")