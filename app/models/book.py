from sqlalchemy import ForeignKey, String, Boolean, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from datetime import date
from app.db.session import Base
from app.models.author import Author

class Book(Base):
    __tablename__ = 'books'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    pages: Mapped[int] = mapped_column(nullable=False)

    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    deleted_at: Mapped[Optional[date]] = mapped_column(Date, default=None, nullable=True)
    
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"), nullable=False)

    author: Mapped["Author"] = relationship("Author", back_populates="books")
    rentals = relationship("Rental", back_populates="book")
