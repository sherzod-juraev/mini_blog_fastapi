from fastapi import APIRouter, HTTPException, Depends, status, Body
from sqlalchemy.orm import Session
from typing import Annotated
from services.tags import Tags
from models.like import Like
from crud import like as like_crud
from uuid import UUID
from services.session import get_db
from schemes.like import LikeGet, LikePost
from security.jwt_token import verify_access_token

like_router = APIRouter(prefix='/like', tags=[Tags.like])

# POST
@like_router.post('/', summary='Create a like', status_code=status.HTTP_201_CREATED, response_model=LikeGet)
async def create_like(payload: Annotated[dict, Depends(verify_access_token)], post: LikePost, db: Annotated[Session, Depends(get_db)]):
    like_crud.verify(db, payload['sub'], post.post_id)
    like = Like(user_id=payload['sub'], post_id=post.post_id)
    like = like_crud.create(db, like)
    return like

# DELETE
@like_router.delete('/{like_id}', summary='Delete like', status_code=status.HTTP_204_NO_CONTENT, response_model=None, dependencies=[Depends(verify_access_token)])
async def delete_like(like_id: UUID, db: Annotated[Session, Depends(get_db)]):
    like = like_crud.delete_check(db, like_id)
    like_crud.delete(db, like)