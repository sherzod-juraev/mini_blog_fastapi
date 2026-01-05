from datetime import datetime, timezone
from sqlalchemy import Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as db_uuid
from uuid import uuid4, UUID
from database import Base


class Comment(Base):
    __tablename__ = 'comments'

    id: Mapped[UUID] = mapped_column(db_uuid(as_uuid=True), primary_key=True, default=uuid4)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    chat_id: Mapped[UUID] = mapped_column(db_uuid(as_uuid=True), ForeignKey('chats.id', ondelete='CASCADE'), nullable=False)
    comment_id: Mapped[UUID | None] = mapped_column(db_uuid(as_uuid=True), ForeignKey('comments.id', ondelete='SET NULL'), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    chat: Mapped['Chat'] = relationship(
        'Chat',
        foreign_keys=[chat_id],
        back_populates='comments',
        lazy='noload'
    )

    comment: Mapped['Comment'] = relationship(
        'Comment',
        remote_side=[id],
        foreign_keys=[comment_id],
        lazy='selectin'
    )