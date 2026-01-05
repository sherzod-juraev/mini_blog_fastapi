# Comment Router Package

This package provides CRUD
functionality for managing
comments in the application.
It supports nested comments
(reply-to-comment) and integrates
with FastAPI, Async SQLAlchemy,
and Pydantic for validation and
serialization.

## Features

- Create, read, update, and delete comments.
- Nested comments support (reply-to-comment).
- Pagination support when retrieving comments by chat.
- Async support with AsyncSession from SQLAlchemy.
- Input validation via Pydantic models
- FastAPI dependency injection for authentication.

## Model

### Represents a comment in the system.

1. Fields
    - `id` (UUID): Primary key.
    - `text` (str): Comment content.
    - `chat_id` (UUID): Reference to the associated chat.
    - `comment_id` (UUID | None): Optional reference to a parent comment (for replies).
    - `created_at` (datetime): Timestamp of creation.
2. Relationships
    - `chat:` Links to the parent chat (noload by default).
    - `comment:` Self-referential link to parent comment (selectin for nested loading).

## Schemas

- **CommentCreate:** Input schema for creating a comment.
- **CommentUpdateFull:** Input schema for full updates.
- **CommentUpdatePartial:** Input schema for partial updates.
- **CommentNestedRead:** Nested read schema for parent comments.
- **CommentRead:** Main read schema with optional nested comment included.

### Validation & security

- Extra fields are forbidden `(extra='forbid')` to ensure only expected data is processed.

## CRUD Operations

- `create(db, comment_schema) → Comment`
Creates a new comment. Commits to the database
and returns the saved model including nested relationships.
- `read(db, comment_id) → Comment`
Retrieves a single comment by its ID, including parent
comment if available (`selectinload`).
- `read_by_chat_id(db, chat_id, skip, limit) → list[Comment]`
Returns a list of comments for a specific chat
with pagination. Nested parent comments
are loaded with selectinload.
- `update(db, comment_id, comment_schema, exclude_unset=False) → Comment`
Updates a comment partially or fully. Returns the updated model.
- `delete(db, comment_id)`
Deletes a comment by ID, with database commit and rollback handling.

### Error Handling

- `HTTPException` with status codes `400`, `404` are used for invalid operations or missing records.

## Endpoints

### Create Comment

- POST `/comments/`
- Request body: `CommentCreate`
- Response: `CommentRead`
- Requires authentication.

### Full Update Comment

- PUT `/comments/{comment_id}`
- Request body: `CommentUpdateFull`
- Response: `CommentRead`
- Requires authentication.

### Partial Update Comment

- PATCH `/comments/{comment_id}`
- Request body: `CommentUpdatePartial`
- Response: `CommentRead`
- Requires authentication.

### Get Comments by Chat

- GET `/comments/{chat_id}`
- Query params: `skip` (default=0), `limit` (default=10, max=100)
- Response: `List[CommentRead]`
- Requires authentication.

### Get Single Comment

- GET `/comments/one/{comment_id}`
- Response: `CommentRead`
- Requires authentication.

## Authentication & Security

- All endpoints are protected via OAuth2 access token.
- Dependency injection via `verify_access_token` ensures only authorized users can access or modify comments.
- Nested comments (replies) are loaded efficiently with `selectinload` to avoid N+1 queries.

## Notes

- Nested comments are loaded only when needed; `selectinload` ensures minimal database queries.
- Self-referential relationship (`comment_id`) allows reply chains but may require careful handling for deeply nested comments.
- Pagination parameters (`skip`, `limit`) prevent excessive data loading for large chats.
- The package follows async best practices with `AsyncSession`.