from datetime import date
from pydantic import BaseModel


class Rental(BaseModel):
    starting_date: date
    ending_date: date
    user_reader_id: int
    user_worker_id: int
    book_id: int


class RentalCreate(Rental):
    pass

class RentalRead(Rental):
    id: int

    class Config:
        from_attributes = True