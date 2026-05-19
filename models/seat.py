from sqlalchemy import Integer, String, ForeignKey, UniqueConstraint
from persistence.dB import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from models.booking import Booking
    from models.plane import Plane

class Seat(Base):
    __tablename__ = 'Seats'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    plane_id: Mapped[int] = mapped_column(Integer, ForeignKey('Planes.id'), nullable=False)
    seat_no: Mapped[str] = mapped_column(String(5), nullable=False)

    __table_args__ = (UniqueConstraint('plane_id', 'seat_no'),)

    bookings: Mapped[List["Booking"]] = relationship("Booking", back_populates="seat")
    plane: Mapped["Plane"] = relationship("Plane", back_populates="seats")

