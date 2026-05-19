from pydantic import BaseModel
from datetime import datetime
from models.booking import BookingStatus


class BookingResponse(BaseModel):
    id: int
    pnr: str
    passenger_id: int
    flight_id: int
    seat_id: int
    price_paid: float
    booking_date: datetime
    booking_status: BookingStatus

    model_config = {"from_attributes": True}