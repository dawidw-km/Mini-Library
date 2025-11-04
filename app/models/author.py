from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from datetime import date
from app.db.session import Base
from app.models.book import Book

class Author(Base):
    __tablename__ = 'authors'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    birth_date: Mapped[date] = mapped_column(nullable=False)

    books: Mapped[List["Book"]] = relationship(back_populates="author")