from fastapi import APIRouter, Query, Depends, status
from uuid import UUID
from core.security import verify_access_token
from database import get_db
from . import schemas, crud


comment_router = APIRouter(dependencies=[Depends(verify_access_token)])


@comment_router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.CommentRead
)
async def create_comment(
        comment_schema: schemas.CommentCreate,
        db=Depends(get_db)
):
    comment_model = await crud.create(db, comment_schema)
    return comment_model


@comment_router.put(
    '/{comment_id}',
    status_code=status.HTTP_200_OK,
    response_model=schemas.CommentRead
)
async def full_update_comment(
        comment_id: UUID,
        comment_schema: schemas.CommentUpdateFull,
        db=Depends(get_db)
):
    comment_model = await crud.update(db, comment_id, comment_schema)
    return comment_model


@comment_router.patch(
    '/{comment_id}',
    status_code=status.HTTP_200_OK,
    response_model=schemas.CommentRead
)
async def partial_update_comment(
        comment_id: UUID,
        comment_schema: schemas.CommentUpdatePartial,
        db=Depends(get_db)
):
    comment_model = await crud.update(db, comment_id, comment_schema, exclude_unset=True)
    return comment_model


@comment_router.get(
    '/{chat_id}',
    status_code=status.HTTP_200_OK,
    response_model=list[schemas.CommentRead]
)
async def get_comments_by_chat_id(
        chat_id: UUID,
        skip: int = Query(0, ge=0),
        limit: int = Query(10, ge=1, le=100),
        db=Depends(get_db)
):
    comments = await crud.read_by_chat_id(db, chat_id, skip, limit)
    return comments


@comment_router.get(
    '/one/{comment_id}',
    status_code=status.HTTP_200_OK,
    response_model=schemas.CommentRead
)
async def get_comment(
        comment_id: UUID,
        db=Depends(get_db)
):
    comment_model = await crud.read(db, comment_id)
    return comment_model