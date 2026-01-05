from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from fastapi import HTTPException, status
from uuid import UUID
from . import schemas
from .model import Comment


async def save(
        db: AsyncSession,
        err_name: str,
        /
):
    try:
        await db.commit()
    except IntegrityError as ex:
        await db.rollback()
        err_msg = str(ex.orig)
        if 'comments_chat_id_fkey' in err_msg:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Chat not found'
            )
        elif 'comments_comment_id_fkey' in err_msg:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Comment not found'
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Error {err_name} comment'
        )


async def create(
        db: AsyncSession,
        comment_schema: schemas.CommentCreate,
        /
) -> Comment:
    comment_model = Comment(
        text=comment_schema.text,
        chat_id=comment_schema.chat_id,
        comment_id=comment_schema.comment_id
    )
    db.add(comment_model)
    await save(db, 'creating')
    comment_model = await read(db, comment_model.id)
    return comment_model


async def read(
        db: AsyncSession,
        comment_id: UUID,
        /
) -> Comment:
    query = select(Comment).options(
        selectinload(Comment.comment)
    ).where(Comment.id == comment_id)
    result = await db.execute(query)
    comment_model = result.scalars().one_or_none()
    if comment_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Comment not found'
        )
    return comment_model


async def read_by_chat_id(
        db: AsyncSession,
        chat_id: UUID,
        skip: int,
        limit: int,
        /
) -> list[Comment]:
    query = select(Comment).where(
        Comment.chat_id == chat_id
    ).order_by(
        Comment.created_at.desc()
    ).offset(skip).limit(limit)
    result = await db.execute(query)
    comments = result.scalars().all()
    return comments


async def update(
        db: AsyncSession,
        comment_id: UUID,
        comment_schema: schemas.CommentUpdateFull | schemas.CommentUpdatePartial,
        /, *,
        exclude_unset: bool = False
) -> Comment:
    comment_model = await read(db, comment_id)
    for field, value in comment_schema.model_dump(exclude_unset=exclude_unset).items():
        setattr(comment_model, field, value)
    await save(db, 'updating')
    comment_model = await read(db, comment_model.id)
    return comment_model


async def delete(
        db: AsyncSession,
        comment_id: UUID,
        /
):
    comment_model = await read(db, comment_id)
    await db.delete(comment_model)
    await save(db, 'deleting')