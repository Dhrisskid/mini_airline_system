from pydantic import BaseModel, field_validator


class CreatePlaneRequest(BaseModel):
    model: str
    total_seats: int

    @field_validator('total_seats')
    @classmethod
    def seats_must_be_valid(cls, v):
        if v <= 0:
            raise ValueError('Total seats must be greater than zero')
        if v > 156:
            raise ValueError('Total seats cannot exceed 156')
        return v

    