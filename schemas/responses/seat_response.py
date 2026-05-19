from pydantic import BaseModel


class SeatResponse(BaseModel):
    id: int
    plane_id: int
    seat_no: str

    model_config = {"from_attributes": True}