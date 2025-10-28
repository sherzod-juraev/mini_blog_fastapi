from services.database import Base
from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(250), unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String(200))
    refresh_token = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    post = relationship(
        'Post',
        back_populates='author',
        foreign_keys='Post.author_id',
        lazy='dynamic',
        passive_deletes=True,
        order_by='Post.created_at.desc()'
    )