from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models.comment import Comment
from models.user import User
from models.post import Post
from schemes.comment import CommentUpdate
from uuid import UUID

def create(db: Session, comment: Comment, /) -> Comment:
    user = db.query(User).filter(User.id == comment.author_id).one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    post = db.query(Post).filter(Post.id == comment.post_id).one_or_none()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Post not found'
        )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment

def update(db: Session, comment: Comment, scheme: CommentUpdate, exclude_unset: bool = False, /) -> Comment:
    for field, value in scheme.model_dump(exclude_unset=exclude_unset).items():
        setattr(comment, field, value)
    db.commit()
    db.refresh(comment)
    return comment

def delete(db: Session, obj: Comment, /):
    db.delete(obj)
    db.commit()

def read_comment(db: Session, author_id: UUID, post_id: UUID, skip: int, limit: int, /) -> list[Comment]:
    comments = db.query(Comment).filter(Comment.author_id == author_id, Comment.post_id == post_id).order_by(Comment.created_at.desc()).offset(skip).limit(limit).all()
    if not comments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Comment not found'
        )
    return comments

def verify_comment(db: Session, comment_id: UUID, /) -> Comment:
    comment = db.query(Comment).filter(Comment.id == comment_id).one_or_none()
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Comment not found'
        )
    return comment