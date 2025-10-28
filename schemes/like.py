from pydantic import BaseModel
from uuid import UUID
from scheme_out.user import UserOut
from scheme_out.post import PostOut

class LikePost(BaseModel):

    post_id: UUID

    model_config = {'extra': 'forbid'}

class LikeGet(BaseModel):

    id: UUID
    user: UserOut
    post: PostOut

    model_config = {'from_attributes': True}