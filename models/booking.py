from datetime import datetime, timezone
from sqlalchemy import Integer, String, ForeignKey, Float, DateTime, UniqueConstraint, Enum
from persistence.dB import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from models.passenger import Passenger
    from models.flight import Flight
    from models.seat import Seat

class BookingStatus(enum.Enum):
    active = 'Active'
    cancelled_by_passenger = 'Cancelled By Passenger'
    cancelled_by_airline = 'Cancelled By Airline'

class Booking(Base):
    __tablename__ = 'Bookings'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    pnr: Mapped[str] = mapped_column(String(6), nullable=False, unique=True)
    passenger_id: Mapped[int] = mapped_column(Integer, ForeignKey('Passengers.id'), nullable=False)
    flight_id: Mapped[int] = mapped_column(Integer, ForeignKey('Flights.id'), nullable=False)
    seat_id: Mapped[int] = mapped_column(Integer, ForeignKey('Seats.id'), nullable=False)
    price_paid: Mapped[float] = mapped_column(Float, nullable=False)
    booking_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    booking_status: Mapped[BookingStatus] = mapped_column(Enum(BookingStatus), nullable=False, default=BookingStatus.active)

    __table_args__ = (UniqueConstraint('flight_id', 'seat_id'),)

    passenger: Mapped["Passenger"] = relationship("Passenger", back_populates="bookings")
    flight: Mapped["Flight"] = relationship("Flight", back_populates="bookings")
    seat: Mapped["Seat"] = relationship("Seat", back_populates="bookings")
