from enum import unique
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from datetime import date
from app.db.session import Base

class Author(Base):
    __tablename__ = 'authors'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    birth_date: Mapped[date] = mapped_column(nullable=False)

    books: Mapped[List["Book"]] = relationship("Book", back_populates="author")