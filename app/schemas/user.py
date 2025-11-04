from pydantic import BaseModel, EmailStr, Field
from datetime import date

class UserBase(BaseModel):
    login: str
    password: str
    full_name: str
    birth_date: date
    city: str
    street: str
    postal_code: str
    address_email: EmailStr

class UserCreate(UserBase):
    pass

class UserRead(UserBase):
    id: int
    
    class Config:
        from_attributes = True
a