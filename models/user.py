from datetime import datetime, timezone
from typing import TYPE_CHECKING
from sqlalchemy import Integer, String, DateTime, Boolean, Enum
from persistence.dB import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

if TYPE_CHECKING:
    from models.passenger import Passenger

class UserRole(enum.Enum):
    admin = 'Admin'
    passenger = 'Passenger'

class User(Base):
    __tablename__ = 'Users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(254), nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(String(225), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False, default=UserRole.passenger)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    passenger: Mapped["Passenger"] = relationship("Passenger", back_populates="user")