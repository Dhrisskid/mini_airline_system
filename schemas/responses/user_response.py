from pydantic import BaseModel
from datetime import datetime
from models.user import UserRole


class UserResponse(BaseModel):
    id: int
    email: str
    role: UserRole
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}