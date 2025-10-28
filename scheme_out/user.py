from pydantic import BaseModel
from uuid import UUID

class UserOut(BaseModel):

    id: UUID
    username: str
    full_name: str | None = None

    model_config = {'from_attributes': True}