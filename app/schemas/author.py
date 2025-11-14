from pydantic import BaseModel, field_validator
from datetime import date, datetime
from app.validators.general import name_validator, birth_date_name_parsed
from app.validators.author_validators import validate_birth_date


class AuthorBase(BaseModel):
    name: str
    birth_date: date

    @field_validator('name')
    def validate_name(cls, v):
        return name_validator(v)
    
    @field_validator('birth_date', mode='before')
    def parsed_b_date(cls, v):
        return birth_date_name_parsed(v)

    
    @field_validator('birth_date')
    def future_date(cls, v):
        return validate_birth_date(v)

class AuthorCreate(AuthorBase):
    pass

class AuthorRead(AuthorBase):
    id: int

    class Config:
        from_attributes = True

