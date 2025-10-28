from sqlalchemy.orm import relationship

from services.database import Base
from sqlalchemy import Column, ForeignKey, func, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Like(Base):
    __tablename__ = 'likes'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID, ForeignKey('users.id', ondelete='CASCADE'))
    post_id = Column(UUID, ForeignKey('posts.id', ondelete='CASCADE'))
    created_at = Column(DateTime, server_default=func.now())

    user = relationship('User', foreign_keys=[user_id])
    post = relationship('Post', foreign_keys=[post_id])