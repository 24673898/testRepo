from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


#move to keycloack intergation  no need to hash password handled by keycloack
class TokenData(BaseModel):
    sub: str
    email: str
    name: str | None = None
    preferred_username: str | None = None


class UserResponse(BaseModel):
    id: UUID
    email: str
    full_name: str | None
    role: str
    created_at: datetime

    model_config = {"from_attributes": True}
