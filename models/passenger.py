from typing import TYPE_CHECKING, List
from sqlalchemy import Integer, String, ForeignKey
from persistence.dB import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from models.user import User
    from models.booking import Booking

class Passenger(Base):
    __tablename__ = 'Passengers'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(254), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(String(15), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('Users.id'), unique=True)

    user: Mapped["User"] = relationship("User", back_populates="passenger")
    bookings: Mapped[List["Booking"]] = relationship("Booking", back_populates="passenger")
