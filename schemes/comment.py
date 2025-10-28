from pydantic import BaseModel
from uuid import UUID
from scheme_out.user import UserOut
from scheme_out.post import PostOut

class CommentPost(BaseModel):

    content: str
    post_id: UUID

    model_config = {'extra': 'forbid'}

class CommentGet(BaseModel):

    id: UUID
    content: str
    author: UserOut
    post: PostOut

    model_config = {'from_attributes': True}

class CommentUpdate(BaseModel):

    content: str | None = None

    model_config = {'extra': 'forbid'}