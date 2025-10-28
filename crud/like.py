from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models.like import Like
from models.user import User
from models.post import Post
from uuid import UUID

def create(db: Session, obj: Like, /) -> Like:
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def delete(db: Session, obj: Like, /):
    db.delete(obj)
    db.commit()

def verify(db: Session, user_id: UUID, post_id: UUID, /):
    post = db.query(Post).filter(Post.id == post_id).one_or_none()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Post not found'
        )
    like = db.query(Like).filter(Like.user_id == user_id, Like.post_id == post_id).one_or_none()
    if like:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='like not found'
        )

def delete_check(db: Session, like_id: UUID, /) -> Like:
    like = db.query(Like).filter(Like.id == like_id).one_or_none()
    if not like:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Like not found'
        )
    return like