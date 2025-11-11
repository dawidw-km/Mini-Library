from pydantic import BaseModel, EmailStr, field_validator
from datetime import date, datetime

def ensure_not_empty(value: str, field_name: str):
    value = value.strip()
    if not value:
        raise ValueError(f"Field {field_name} cannot be empty.")
    return value

def ensure_min_length(value: str, field_name: str, *, min_length: int = None):
    if min_length and len(value) < min_length:
        raise ValueError(f"Field {field_name} must contain at least {min_length} characters.")
    return value

def ensure_max_length(value: str, field_name: str, *, max_length: int = None):
    if max_length and len(value) > max_length:
        raise ValueError(f"Field {field_name} must contain at most {max_length} characters.")
    return value

def ensure_alnum(value: str, field_name: str, *, alnum: bool = False) -> str:
    if alnum and not value.isalnum():
        raise ValueError(f"Field {field_name} can contain only alphanumeric characters.")
    return value

def validate_text(value: str, field_name: str, *,
                 min_length: int = None,
                 max_length: int = None,
                 alnum: bool = False) -> str:
    value = ensure_not_empty(value, field_name)
    value = ensure_min_length(value, field_name, min_length=min_length)
    value = ensure_max_length(value, field_name, max_length=max_length)
    value = ensure_alnum(value, field_name, alnum=alnum)
    return value

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
        return validate_text(v, field_name='login', min_length=6, max_length=18, alnum=False)
    
    @field_validator('password')
    def password_validator(cls, v):
        return validate_text(v, field_name='password', min_length=6, max_length=18, alnum=False)

    @field_validator('full_name')
    def full_name_validator(cls, v):
        return validate_text(v, field_name='full_name', min_length=6, max_length=150, alnum=False)
    
    @field_validator('birth_date', mode='before')
    def birth_date_validator(cls, v):
        if isinstance(v, str):
            try:
                v = datetime.strptime(v.strip(), "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("Wrong format, try again. (e.g 2000-12-31)")
        elif not isinstance(v, date):
            raise ValueError("Birth date must be a valid date.")

        if v > date.today():
            raise ValueError("Date cannot be in the future.")
        if v < date(1900, 1, 1):
            raise ValueError("Birth date seems too old, please try again.")

        return v
    
    @field_validator('city')
    def city_validator(cls, v):
        return validate_text(v, field_name='city', min_length=1, max_length=150, alnum=False)

    @field_validator('street')
    def street_validator(cls, v):
        return validate_text(v, field_name='street', min_length=1, max_length=150, alnum=False)

    @field_validator('postal_code')
    def postal_code_validator(cls, v):
        return validate_text(v, field_name='postal_code', min_length=5, max_length=8, alnum=True)

    @field_validator('address_email')
    def address_email_validator(cls, v):
        if v is None:
            raise ValueError("Address email cannot be empty.")
        return v



class UserCreate(UserBase):
    pass

class UserRead(UserBase):
    id: int
    
    class Config:
        from_attributes = True