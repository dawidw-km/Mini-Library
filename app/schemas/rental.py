from datetime import date
from pydantic import BaseModel
from typing import Optional


class Rental(BaseModel):
    starting_date: date
    ending_date: date
    user_reader_id: int
    user_worker_id: int
    book_id: int

class RentalPatch(Rental):
    starting_date: Optional[date] = None
    ending_date: Optional[date] = None
    user_reader_id: Optional[int] = None
    user_worker_id: Optional[int] = None
    book_id: Optional[int] = None

class RentalCreate(Rental):
    pass

class RentalUpdate(Rental):
    pass

class RentalRead(Rental):
    id: int

    class Config:
        from_attributes = True