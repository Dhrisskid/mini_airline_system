from pydantic import BaseModel
from datetime import date, time
from models.flight import FlightStatus


class FlightResponse(BaseModel):
    id: int
    plane_id: int
    origin: str
    destination: str
    date: date
    departure_time: time
    price_per_seat: float
    status: FlightStatus
    flight_code: str

    model_config = {"from_attributes": True}