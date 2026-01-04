from datetime import datetime, timedelta
from typing import Annotated
from jose import JWTError, ExpiredSignatureError
from jose.jwt import encode, decode
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from uuid import UUID
from core import get_setting


settings = get_setting()
oauth2_schema = OAuth2PasswordBearer(tokenUrl='auth/signup')


def create_access_token(auth_id: UUID, /) -> str:

    data = {
        'sub': str(auth_id),
        'exp': datetime.utcnow() + timedelta(minutes=settings.at_minutes)
    }
    access_token = encode(data, settings.secret_key, algorithm=settings.algorithm)
    return access_token


def create_refresh_token(auth_id: UUID, /) -> str:

    data = {
        'sub': str(auth_id),
        'exp': datetime.utcnow() + timedelta(days=settings.rt_days)
    }
    refresh_token = encode(data, settings.secret_key, algorithm=settings.algorithm)
    return refresh_token


def verify_token(
        token: str,
        token_type: str,
        /, *,
        include_header: bool = True
) -> UUID:
    try:
        payload = decode(token, settings.secret_key, algorithms=[settings.algorithm])
        auth_id = payload.get('sub')
        if auth_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f'auth_id not found from {token_type}'
            )
        return UUID(auth_id)
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f'{token_type} expired',
            headers={
                'WWW-Authenticate': 'Bearer'
            } if include_header else None
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f'{token_type} invalid',
            headers={
                'WWW-Authenticate': 'Bearer'
            } if include_header else None
        )


def verify_access_token(access_token: Annotated[str, Depends(oauth2_schema)]) -> UUID:
    return verify_token(access_token, 'access_token')

def verify_refresh_token(refresh_token: str, /) -> UUID:
    if refresh_token is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='refresh_token not found'
        )
    return verify_token(refresh_token, 'refresh_token', include_header=False)