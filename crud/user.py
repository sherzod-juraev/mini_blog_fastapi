from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from models.user import User
from schemes.user import UserUpdate

def create(db: Session, user: User, /) -> User:
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def update(db: Session, user: User, scheme: UserUpdate, exclude_unset: bool = False, /) -> User:
    for field, value in scheme.model_dump(exclude_unset=exclude_unset).items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user

def delete(db: Session, obj: User, /):
    db.delete(obj)
    db.commit()

def read(db: Session, user_id: UUID, skip: int, limit: int, /) -> User:
    user = db.query(User).filter(User.id == user_id).one_or_none()
    verify(db, user_id)
    user.post = user.post.offset(skip).limit(limit).all()
    return user

def verify_user(db: Session, /, *, username: str | None = None, email: str | None = None) -> User:
    user = None
    if email:
        user = db.query(User).filter(User.email == email).first()
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='email already exists'
            )
    elif username:
        user = db.query(User).filter(User.username == username).first()
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='username already exists'
            )
    return user

def verify(db: Session, user_id: UUID, /) -> User:
    user = db.query(User).filter(User.id == user_id).one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    return user