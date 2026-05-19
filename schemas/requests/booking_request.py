from pydantic import BaseModel


class BookingRequestModel(BaseModel):
    user_id: int
    name: str
    phone: str
    flight_id: int
    seat_id: int


class CancelBookingRequest(BaseModel):
    cancelled_by_airline: bool = False

    