from pydantic import BaseModel, field_validator
from datetime import date, datetime

class AuthorBase(BaseModel):
    name: str
    birth_date: date

    @field_validator('name')
    def name_validator(cls, v):
        """
        Validates that name is not empty and has proper lenght.
        """
        v = v.strip()
        if not v:
            raise ValueError('Name cannot be empty, please put a real name.')
        elif len(v) < 2 or len(v) > 150:
            raise ValueError('Name must be between 2 and 150 characters.')
        elif not v.replace(" ","").isalpha():
            raise ValueError("Name can contain only letters and spaces")
        return v.title()
    
    @field_validator('birth_date', mode='before')
    def birth_date_name_parsed(cls, v):
        """
        Ensures that the birth date is in the correct format 'YYYY-MM-DD'.
        """
        if isinstance(v, str):
            try:
                return datetime.strptime(v, '%Y-%m-%d').date()
            except ValueError:
                raise ValueError("Date must be in correct format YYYY-MM-DD (e.g) 1997-04-10")
        return v
    
    @field_validator('birth_date')
    def validate_birth_date(cls, v):
        """
        Ensures that birth date is not in the future.
        """
        if v > date.today():
            raise ValueError("Date cannot be in the future.")
        return v

class AuthorCreate(AuthorBase):
    pass

class AuthorRead(AuthorBase):
    id: int

    class Config:
        from_attributes = True

