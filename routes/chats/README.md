# Chat Router Package

This package provides the Chat
functionality for a FastAPI 
application using async SQLAlchemy.
It allows users to create, read, update,
and delete chat records, as well as fetch
chats by user. The package is designed
with async endpoints, proper validation,
and security in mind.

## Model

`Chat` model represents a chat created by a user.
### Fields:

- `id:` UUID, primary key
- `title:` str, chat title
- `description:` Optional[str], chat description
- `user_id:` UUID, foreign key referencing User
- `created_at:` datetime, timestamp of creation

### Relationships:

- `user:` Links to the user who created the chat
- `comments:` List of comments associated with this chat

`lazy='noload'` is used for relationships to avoid
unnecessary loading. Use `selectinload` if nested 
data is required.

## Schemas

- **ChatCreate** – Fields required to create a chat (`title`, `description`)
- **ChatUpdateFull** – All fields required for full update
- **ChatUpdatePartial** – Optional fields for partial update (PATCH)
- **ChatRead** – Fields returned in responses (`id`, `title`, `description`)

All schemas use `ConfigDict` with `extra='forbid'` to prevent extra fields.

## CRUD Functions

- `create(db, user_id, chat_schema)` – Creates a new chat for a user
- `read(db, chat_id)` – Fetches a chat by its ID
- `read_by_user_id(db, user_id, skip, limit)` – Fetches a paginated list of chats for a user
- `update(db, chat_id, chat_schema, exclude_unset)` – Updates a chat (full or partial)
- `delete(db, chat_id)` – Deletes a chat

### Notes:

- `save()` function handles commit and rollback, with proper HTTPException for errors.
- `exclude_unset=True` ensures PATCH only updates fields provided.

## Endpoints

| Method  | Path         |                 Description                  |
|:--------|:-------------|:--------------------------------------------:|
| POST    | `/`          |                Create a chat                 |
| PUT     | `/{chat_id}` |            Full update of a chat             |
| PATCH   | `/{chat_id}` |           Partial update of a chat           |
| GET     | `/{chat_id}` |                Get chat by id                |
| GET     | `/`          |   Get chats by user's id (with pagination)   |
| DELETE  | `/{chat_id}` |                Delete a chat                 |

### Security:
Most endpoints require user authentication via verify_access_token dependency.