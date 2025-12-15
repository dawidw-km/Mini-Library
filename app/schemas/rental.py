from datetime import date
from pydantic import BaseModel
from typing import Optional


class Rental(BaseModel):
    id: int
    starting_date: date
    ending_date: date
    return_date: Optional[date] = None
    user_reader_id: int
    user_worker_id: int
    book_id: int

class RentalPatch(BaseModel):
    return_date: Optional[date] = None
    user_worker_id: Optional[int] = None

class RentalCreate(BaseModel):
    user_reader_id: int
    user_worker_id: int
    book_id: int

class RentalRead(Rental):
    pass

    class Config:
        from_attributes = True