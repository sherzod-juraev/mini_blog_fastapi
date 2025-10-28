from services.database import Base
from sqlalchemy import Column, String, ForeignKey, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

class Post(Base):
    __tablename__ = 'posts'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(200), index=True, nullable=False)
    content = Column(String, nullable=False)
    author_id = Column(UUID, ForeignKey('users.id', ondelete='CASCADE'))
    created_at = Column(DateTime, server_default=func.now(), index=True)

    author = relationship('User', back_populates='post', foreign_keys=[author_id])
    like = relationship('Like', back_populates='post', foreign_keys='Like.post_id', lazy='dynamic', passive_deletes=True)
    comment = relationship('Comment', back_populates='post', foreign_keys='Comment.post_id', lazy='noload', passive_deletes=True)