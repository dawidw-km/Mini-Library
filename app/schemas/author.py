from pydantic import BaseModel
from datetime import date

class AuthorBase(BaseModel):
    name: str
    birth_date: date

class AuthorCreate(AuthorBase):
    pass

class AuthorRead(AuthorBase):
    id: int

    class Config:
        from_attributes = True

