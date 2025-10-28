from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from scheme_out.post import PostOut

class UserGet(BaseModel):

    id: UUID
    username: str
    email: str | None = None
    full_name: str | None = None
    post: list[PostOut] = Field(default_factory=list)

    model_config = {'from_attributes': True}

class UserUpdate(BaseModel):

    username: str | None = Field(None, max_length=250)
    email: EmailStr | None = None
    full_name: str | None = None