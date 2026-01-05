# Mini Blog FastAPI

Mini Blog FastAPI is an asynchronous
blog application built with FastAPI,
SQLAlchemy (async), and PostgreSQL.

It provides user authentication, chat
rooms, and nested comment functionality,
following modern async patterns and
secure password/token handling.

## Features

- User management: sign-up, access tokens, refresh tokens, profile update.
- Chat rooms: create, update, list, delete chats.
- Nested comments: comments and replies with pagination support.
- JWT authentication with access and refresh tokens.
- Async database operations with SQLAlchemy AsyncSession.
- Input validation using Pydantic schemas.
- Centralized exception handling and consistent HTTP responses.

## Routers

1. Users [More info](./routes/users/README.md#user-management-package)
2. Chats [More info](./routes/chats/README.md#chat-router-package)
3. Comments [More info](./routes/comments/README.md#comment-router-package)

## Authentication

- All endpoints are secured via OAuth2 access tokens.
- Refresh tokens are stored in cookies.
- Passwords are securely hashed using industry-standard algorithms.

## Database

- Uses PostgreSQL.
- Async session management with SQLAlchemy.
- Supports foreign key relationships between users, chats, and comments.

## Notes

- Async-first design ensures non-blocking operations.
- Nested comment relationships are loaded efficiently using selectinload.
- Pagination prevents large query loads.
- Centralized CRUD and exception handling ensures consistency across the application.