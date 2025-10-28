from fastapi import APIRouter, Depends, status, Body
from sqlalchemy.orm import Session
from typing import Annotated
from uuid import UUID
from services.tags import Tags
from services.session import get_db
from crud import comment as comment_crud
from schemes.comment import CommentGet, CommentPost, CommentUpdate
from models.comment import Comment
from models.user import User
from security.jwt_token import verify_access_token

comment_router = APIRouter(prefix='/comment', tags=[Tags.comment])

# GET
@comment_router.get('/', summary='Get comments', status_code=status.HTTP_200_OK, response_model=list[CommentGet])
async def read_comments(payload: Annotated[dict, Depends(verify_access_token)], post_id: UUID, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    comments = comment_crud.read_comment(db, payload['sub'], post_id, skip, limit)
    return comments

# POST
@comment_router.post('/', summary='Add a comment', status_code=status.HTTP_201_CREATED, response_model=CommentGet)
async def create_comment(payload: Annotated[dict, Depends(verify_access_token)], comment: CommentPost, db: Annotated[Session, Depends(get_db)]):
    comment_model = Comment(content=comment.content, post_id=comment.post_id, author_id=payload['sub'])
    comment_model = comment_crud.create(db, comment_model)
    return comment_model

# PATCH
@comment_router.patch('/{comment_id}', summary='Partial update of comment', status_code=status.HTTP_200_OK, response_model=CommentGet)
async def partial_update(payload: Annotated[dict, Depends(verify_access_token)], comment_id: UUID, comment: CommentUpdate, db: Annotated[Session, Depends(get_db)]):
    comment_model = comment_crud.verify_comment(db, comment_id)
    comment_crud.update(db, comment_model, comment, True)
    return comment_model

# DELETE
@comment_router.delete('/{comment_id}', summary='Delete comment', status_code=status.HTTP_204_NO_CONTENT, response_model=None)
async def delete_comment(payload: Annotated[dict, Depends(verify_access_token)], comment_id: UUID, db: Annotated[Session, Depends(get_db)]):
    comment = comment_crud.verify_comment(db, comment_id)
    comment_crud.delete(db, comment)