from pydantic import BaseModel, field_validator, ConfigDict, model_validator
from datetime import date
from typing import Optional
from app.validators.general import name_validator, update_validator
from app.validators.author_validators import validate_birth_date



class AuthorBase(BaseModel):
    name: str
    birth_date: date

    @field_validator('name')
    def validate_name(cls, v):
        return name_validator(v)

    @field_validator('birth_date')
    def future_date(cls, v):
        return validate_birth_date(v)


class AuthorCreate(AuthorBase):
    pass


class AuthorUpdate(BaseModel):
    name: Optional[str] = None
    birth_date: Optional[date] = None

    @field_validator('name')
    def validate_name(cls, v):
        return name_validator(v)

    @field_validator('birth_date')
    def future_date(cls, v):
        return validate_birth_date(v)

    @model_validator(mode="after")
    def validate_model(self):
        update_validator(self)
        return self


class AuthorRead(AuthorBase):
    id: int
    name: str
    birth_date: date

    model_config = ConfigDict(
        from_attributes=True
    )