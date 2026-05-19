from pydantic import BaseModel


class PlaneResponse(BaseModel):
    id: int
    model: str
    total_seats: int

    model_config = {"from_attributes": True}