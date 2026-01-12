from pydantic import BaseModel, EmailStr, field_validator, ConfigDict
from typing import Optional
from datetime import date
from app.validators.user_validators import validate_text

class UserBase(BaseModel):
    login: str
    password: str
    full_name: str
    birth_date: date
    city: str
    street: str
    postal_code: str
    address_email: EmailStr

    @field_validator('login')
    def login_validator(cls, v):
        return validate_text(v, field_name='login', min_length=5, max_length=18)

    @field_validator('password')
    def password_validator(cls, v):
        return validate_text(v, field_name='password', min_length=5, max_length=1000)

    @field_validator('full_name')
    def full_name_validator(cls, v):
        return validate_text(v, field_name='full_name', min_length=2, max_length=150)

    @field_validator('city')
    def city_validator(cls, v):
        return validate_text(v, field_name='city', min_length=1, max_length=150)

    @field_validator('street')
    def street_validator(cls, v):
        return validate_text(v, field_name='street', min_length=1, max_length=150)

    @field_validator('postal_code')
    def postal_code_validator(cls, v):
        return validate_text(v, field_name='postal_code', min_length=5, max_length=8)

    @field_validator('address_email')
    def address_email_validator(cls, v):
        if v is None:
            raise ValueError("Address email cannot be empty.")
        return v



class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    login: Optional[str] = None
    password: Optional[str] = None
    full_name: Optional[str] = None
    birth_date: Optional[date] = None
    city: Optional[str] = None
    street: Optional[str] = None
    postal_code: Optional[str] = None
    address_email: Optional[EmailStr] = None


class UserRead(BaseModel):
    id: int
    login: str
    full_name: str
    birth_date: date
    city: str
    street: str
    postal_code: str
    address_email: EmailStr
    role: str

    model_config = ConfigDict(
        from_attributes=True
    )