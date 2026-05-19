from pydantic import BaseModel, EmailStr


class PassengerRequestModel(BaseModel):
    name: str
    email: EmailStr
    phone: str

class UpdatePassengerRequest(BaseModel):
    name: str | None = None
    phone: str | None = None


