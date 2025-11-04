from pydantic import BaseModel

class BookBase(BaseModel):
    title: str
    pages: int

class BookCreate(BookBase):
    author_id: int | None = None
    author_name: str  | None = None
    
class BookRead(BookBase):
    id: int
    author_id: int

    class Config:
        from_attributes = True
