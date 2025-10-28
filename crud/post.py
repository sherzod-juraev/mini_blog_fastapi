from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models.post import Post
from models.user import User
from schemes.post import PostUpdate
from uuid import UUID

def create(db: Session, post: Post, /) -> dict:
    user = db.query(User).filter(User.id == post.author_id).one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    db.add(post)
    db.commit()
    db.refresh(post)
    post_dict = get_dict(post)
    print(post_dict)
    return post_dict

def update(db: Session, post: Post, scheme: PostUpdate, exclude_unset: bool = False, /) -> dict:
    for field, value in scheme.model_dump(exclude_unset=exclude_unset).items():
        setattr(post, field, value)
    db.commit()
    db.refresh(post)
    post_dict = get_dict(post)
    return post_dict

def delete(db: Session, obj: Post, /):
    db.delete(obj)
    db.commit()

def read(db: Session, skip: int, limit: int, author_id: UUID, /) -> list[dict]:
    posts = db.query(Post).filter(Post.author_id == author_id).order_by(Post.created_at.desc()).offset(skip).limit(limit).all()
    if not posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Post not found'
        )
    post_array = []
    for post in posts:
        post_array.append(get_dict(post))
    return post_array

def verify_post(db: Session, post_id: UUID, author_id: UUID, /) -> Post:
    obj = db.query(Post).filter(Post.id == post_id, Post.author_id == author_id).one_or_none()
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Post not found'
        )
    return obj

def get_dict(post: Post, /) -> dict:
    post_dict = {
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'author': {
                'id': post.author.id,
                'username': post.author.username,
                'full_name': post.author.full_name
            },
            'like': post.like.count()
    }
    return post_dict