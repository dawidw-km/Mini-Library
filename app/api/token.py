from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from app.schemas.token import Token
from app.db.session import get_db
from app.services.token_api_services import user_login


router = APIRouter(prefix="/token", tags=["Token"])

@router.post("/", response_model=Token)
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: Session = Depends(get_db),
) -> Token:
    return user_login(
        db=db,
        username=form_data.username,
        password=form_data.password
    )