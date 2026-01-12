from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Boolean, Date
from datetime import date
from app.db.base import Base

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str] = mapped_column(nullable=True)
    full_name: Mapped[str] = mapped_column(nullable=True)
    birth_date: Mapped[date] = mapped_column(nullable=True)
    city: Mapped[str] = mapped_column(nullable=True)
    street: Mapped[str] = mapped_column(nullable=True)
    postal_code: Mapped[str] = mapped_column(nullable=True)
    address_email: Mapped[str] = mapped_column(nullable=True)
    role: Mapped[str] = mapped_column(nullable=True, default="reader")

    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    deleted_at: Mapped[date] = mapped_column(Date, nullable=True)

    rental_reader = relationship("Rental", back_populates="rental_reader", foreign_keys="Rental.user_reader_id")
    rental_worker = relationship("Rental", back_populates="rental_worker", foreign_keys="Rental.user_worker_id")