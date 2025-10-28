from services.database import Base
from sqlalchemy import Column, String, DateTime, func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

class Comment(Base):
    __tablename__ = 'comments'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content = Column(String, nullable=False)
    author_id = Column(UUID, ForeignKey('users.id', ondelete='SET NULL'))
    post_id = Column(UUID, ForeignKey('posts.id', ondelete='CASCADE'))
    created_at = Column(DateTime, server_default=func.now())

    author = relationship('User', foreign_keys=[author_id])
    post = relationship('Post', foreign_keys=[post_id])