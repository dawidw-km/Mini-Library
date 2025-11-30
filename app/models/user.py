from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Boolean, Date
from datetime import date
from app.db.session import Base

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    full_name: Mapped[str] = mapped_column(nullable=False)
    birth_date: Mapped[date] = mapped_column(nullable=False)
    city: Mapped[str] = mapped_column(nullable=False)
    street: Mapped[str] = mapped_column(nullable=False)
    postal_code: Mapped[str] = mapped_column(nullable=False)
    address_email: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[str] = mapped_column(nullable=False, default="reader")

    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    deleted_at: Mapped[date] = mapped_column(Date, nullable=True)

    rental_reader = relationship("Rental", back_populates="rental_reader", foreign_keys="Rental.user_reader_id")
    rental_worker = relationship("Rental", back_populates="rental_worker", foreign_keys="Rental.user_worker_id")