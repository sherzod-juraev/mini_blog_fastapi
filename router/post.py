from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import Annotated
from uuid import UUID
from models.post import Post
from services.session import get_db
from crud import post as post_crud
from schemes.post import PostIn, PostGet, PostUpdate
from services.tags import Tags
from security.jwt_token import verify_access_token

post_router = APIRouter(prefix='/post', tags=[Tags.post])

# GET
@post_router.get('/', summary='Get all posts', status_code=status.HTTP_200_OK, response_model=list[PostGet])
async def read_post(payload: Annotated[dict, Depends(verify_access_token)], skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    posts = post_crud.read(db, skip, limit, payload['sub'])
    return posts

# POST
@post_router.post('/', summary='Create a new post', status_code=status.HTTP_201_CREATED, response_model=PostGet)
async def create_post(payload: Annotated[dict, Depends(verify_access_token)], post: PostIn, db: Annotated[Session, Depends(get_db)]):

    post_model = Post(title=post.title, content=post.content, author_id=payload['sub'])
    post_model = post_crud.create(db, post_model)
    return post_model

# PATCH
@post_router.patch('/{post_id}', summary='Partial update of the post', status_code=status.HTTP_200_OK, response_model=PostGet, dependencies=[Depends(verify_access_token)])
async def partial_update(payload: Annotated[dict, Depends(verify_access_token)], post_id: UUID, post: PostUpdate,  db: Annotated[Session, Depends(get_db)]):
    post_model = post_crud.verify_post(db, post_id, payload['sub'])
    post_model = post_crud.update(db, post_model, post, True)
    return post_model

# DELETE
@post_router.delete('/{post_id}', summary='Delete post', status_code=status.HTTP_204_NO_CONTENT, response_model=None)
async def delete_post(payload: Annotated[dict, Depends(verify_access_token)], post_id: UUID, db: Annotated[Session, Depends(get_db)]):
    post_model = post_crud.verify_post(db, post_id, payload['sub'])
    post_crud.delete(db, post_model)