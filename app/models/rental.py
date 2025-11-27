from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.session import Base
from datetime import date
from app.models.book import Book
from app.models.user import User

class Rental(Base):
    __tablename__ = 'rentals'

    id: Mapped[int] = mapped_column(primary_key=True)
    starting_date: Mapped[date] = mapped_column(nullable=False)
    ending_date: Mapped[date] = mapped_column(nullable=False)

    user_reader_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user_worker_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    book_id: Mapped[int] = mapped_column(ForeignKey('books.id'))

    rental_reader: Mapped[User] = relationship(
        "User",
        foreign_keys=[user_reader_id],
        back_populates="rental_reader"
    )
    rental_worker: Mapped[User] = relationship(
        "User",
        foreign_keys=[user_worker_id],
        back_populates="rental_worker"
    )
    book: Mapped[Book] = relationship(
        "Book",
        back_populates="rentals"
    )