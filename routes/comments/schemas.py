from pydantic import BaseModel, ConfigDict
from uuid import UUID


class CommentCreate(BaseModel):
    model_config = ConfigDict(extra='forbid')
    text: str
    chat_id: UUID
    comment_id: UUID | None = None


class CommentUpdateFull(BaseModel):
    model_config = ConfigDict(extra='forbid')
    text: str
    chat_id: UUID
    comment_id: UUID


class CommentUpdatePartial(BaseModel):
    model_config = ConfigDict(extra='forbid')
    text: str | None = None
    chat_id: UUID | None = None
    comment_id: UUID | None = None


class CommentNestedRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    text: str


class CommentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    text: str
    comment: CommentNestedRead | None = None