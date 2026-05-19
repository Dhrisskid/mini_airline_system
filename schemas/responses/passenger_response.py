from pydantic import BaseModel


class PassengerResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    user_id: int

    model_config = {"from_attributes": True}