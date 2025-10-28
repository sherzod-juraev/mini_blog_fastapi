from pydantic import BaseModel, Field
from scheme_out.user import UserOut
from uuid import UUID

class PostIn(BaseModel):

    title: str = Field(max_length=200)
    content: str

    model_config = {'extra': 'forbid'}

class PostGet(BaseModel):

    id: UUID
    title: str = Field(max_length=200)
    content: str
    author: UserOut
    like: int = 0
    model_config = {'from__attributes': True}

class PostUpdate(BaseModel):

    title: str | None = Field(None, max_length=200)
    content: str | None = None