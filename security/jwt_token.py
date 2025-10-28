from fastapi import Depends, HTTPException, status, Header
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError, ExpiredSignatureError
from datetime import datetime, timedelta
from typing import Annotated
import uuid

SECRET_KEY = 'fake_super_secret_key'
ALGORITHM = 'HS256'

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='user')

def create_access_token(data: dict, /):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({'exp': expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt

def verify_access_token(access_token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='access_token expired',
            headers={'WW-Authenticate': 'Bearer'}
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='token invalid or expired',
            headers={'WW-Authenticate': 'Bearer'}
        )

def create_refresh_token():
    to_encode = {
        'sub': str(uuid.uuid4())
    }
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt

def verify_refresh_token(refresh_token: Annotated[str, Header()]):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='refresh_token expired',
            headers={'WW-Authenticate': 'Bearer'}
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='token invalid',
            headers={'WW-Authenticate': 'Bearer'}
        )