from sqlalchemy import Integer, String, ForeignKey, Time, Float, Date, Enum
from persistence.dB import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date, time
import enum
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from models.plane import Plane
    from models.booking import Booking

class FlightStatus(enum.Enum):
    on_time = 'On-Time'
    delayed = 'Delayed'
    cancelled = 'Cancelled'
    landed = 'Landed'


class Flight(Base):
    __tablename__ = 'Flights'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    plane_id: Mapped[int] = mapped_column(Integer, ForeignKey('Planes.id'), nullable=False)
    origin: Mapped[str] = mapped_column(String(100), nullable=False)
    destination: Mapped[str] = mapped_column(String(100), nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    departure_time: Mapped[time] = mapped_column(Time, nullable=False)
    price_per_seat: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[FlightStatus] = mapped_column(Enum(FlightStatus), default=FlightStatus.on_time)
    flight_code: Mapped[str] = mapped_column(String(10), nullable=False, unique=True)

    plane: Mapped["Plane"] = relationship("Plane", back_populates="flights")
    bookings: Mapped[List["Booking"]] = relationship("Booking", back_populates="flight")
