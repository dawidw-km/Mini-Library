from typing import Optional
from datetime import date
from pydantic import BaseModel, field_validator
from app.validators.book_validators import title_validator, pages_validate

class BookBase(BaseModel):
    title: str
    pages: int
    author_id: Optional[int] = None
    author_name: Optional[str] = None

    @field_validator('title')
    def title_book_validator(cls, v):
        return title_validator(v)
        
    @field_validator('pages')
    def pages_book_validator(cls, v):
        return pages_validate(v)
    
class BookCreate(BookBase):
    pass

class BookUpdate(BookBase):
    pass


class BookRead(BookBase):
    id: int
    author_id: int

    class Config:
        from_attributes = True
