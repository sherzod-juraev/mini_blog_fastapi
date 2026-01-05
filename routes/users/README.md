# User Management Package

## Overview

This package provides user management
functionality for a FastAPI application
using asynchronous SQLAlchemy 
(AsyncSession).

### It supports:

- User signup with password hashing
- Access and refresh tokens (JWT-based)
- CRUD operations on users
- Validation of fields via Pydantic
- Token-based authentication with cookie support

## Features

1. Authentication
    - Sign up with username and password
    - JWT access token
    - Refresh token stored in HTTP-only cookie
2. User CRUD
    - Create, read, update (full/partial), delete users
    - Secure password hashing and verification
    - Field validation using regex (username, password, full name)
    - Only authenticated users can update or delete their own data
3. Database
    - Async PostgreSQL via SQLAlchemy
    - UUID primary keys
    - Automatic timestamp (`created_at`)
    - `noload` lazy loading for related `chats` to optimize queries

## Endpoints

| Method    |    Path    |            Description             |
|:----------|:----------:|:----------------------------------:|
| POST      | `/signup`  |   Create user and return tokens    |
| POST      | `/refresh` |      Refresh JWT access token      |
| GET       |   `/me`    |   Get current authenticated user   |
| PUT       |    `/`     |      Full update of user data      |
| PATCH     |    `/`     |    Partial update of user data     |
| DELETE    |    `/`     |        Delete user account         |

## Schemas

- `UserCreate` – for signup
- `UserUpdateFull` – full update
- `UserUpdatePartial` – partial update (PATCH)
- `UserRead` – read-only user info
- `Token` – access token response
### Validation patterns are applied to:

- Username (upper/lowercase, digit, length ≤50)
- Password (upper/lowercase, digit, symbol, length 8–25)
- Full name (letters and hyphen only, length ≤100)

## Security

- Passwords are hashed before storing in the database
- Access tokens expire after a short time (e.g., minutes)
- Refresh tokens stored in HTTP-only cookies and can be rotated

## Notes

- chats relationship in the User model is lazy-loaded with noload, so related chats are not fetched unless explicitly requested.
- All database operations are async for better concurrency.
- Error handling uses HTTPException with proper status codes.