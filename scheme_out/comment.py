from pydantic import BaseModel
from uuid import UUID

class CommentOut(BaseModel):

    id: UUID
    content: str

    model_config = {'from_attributes': True}