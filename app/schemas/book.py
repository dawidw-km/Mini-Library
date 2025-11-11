from typing import Optional
from pydantic import BaseModel, field_validator

class BookBase(BaseModel):
    title: str
    pages: int

    @field_validator('title')
    def title_validator(cls, v):
        """
        Ensures that title is not empty and contains between 2 to 250 characters.
        """
        v = v.strip()
        if not v:
            raise ValueError("Title cannot be empty, please put a real title.")
        elif len(v) < 2 or len(v) > 250:
            raise ValueError("Title can contain between 2 and 250 characters.")
        return v.title()
        
    @field_validator('pages')
    def pages_validate(cls, v):
        """
        Ensures that pages are not empty and are in range 2 to 2000.
        """
        if v < 2 or v > 2000:
            raise ValueError("Pages must be between 2 to 2000.")
        return v
    
class BookCreate(BookBase):
    author_id: Optional[int] = None
    author_name: Optional[str] = None
    
class BookRead(BookBase):
    id: int
    author_id: int

    class Config:
        from_attributes = True
