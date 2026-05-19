from sqlalchemy import Integer, String
from persistence.dB import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from models.flight import Flight
    from models.seat import Seat

class Plane(Base):
    __tablename__ = 'Planes'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    model: Mapped[str] = mapped_column(String(100), nullable=False)
    total_seats: Mapped[int] = mapped_column(Integer, nullable=False)

    flights: Mapped[List["Flight"]] = relationship("Flight", back_populates="plane")
    seats: Mapped[List["Seat"]] = relationship("Seat", back_populates="plane")

    