from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Boolean, Date
from typing import List, Optional
from datetime import date
from app.db.base import Base

class Author(Base):
    __tablename__ = 'authors'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    birth_date: Mapped[date] = mapped_column(nullable=False)

    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    deleted_at: Mapped[Optional[date]] = mapped_column(Date, default= None, nullable=True)

    books: Mapped[List["Book"]] = relationship("Book", back_populates="author")