from pydantic import BaseModel
from uuid import UUID

class PostOut(BaseModel):

    id: UUID
    title: str
    content: str

    model_config = {'from_attributes': True}