from pydantic import BaseModel, field_validator
from datetime import date, time
from models.flight import FlightStatus


class CreateFlightRequest(BaseModel):
    plane_id: int
    origin: str
    destination: str
    date: date
    departure_time: time
    price_per_seat: float

    @field_validator('price_per_seat')
    @classmethod
    def price_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Price must be greater than zero')
        return v

    @field_validator('origin', 'destination')
    @classmethod
    def not_empty(cls, v):
        if not v.strip():
            raise ValueError('Field cannot be empty')
        return v.strip()


class UpdateFlightStatusRequest(BaseModel):
    status: FlightStatus


class UpdateFlightPriceRequest(BaseModel):
    price: float

    @field_validator('price')
    @classmethod
    def price_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Price must be greater than zero')
        return v


    