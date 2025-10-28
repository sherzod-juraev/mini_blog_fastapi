from fastapi import APIRouter, Depends, Response, Body, status, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Annotated
from services.tags import Tags
from crud import user as user_crud
from services.session import get_db
from schemes.user import UserGet, UserUpdate
from models.user import User
from security.jwt_token import create_access_token, create_refresh_token, verify_access_token, verify_refresh_token
from security.hash_password import hash_password, verify_passwword

user_router = APIRouter(prefix='/user', tags=[Tags.user])

# GET
@user_router.get('/', summary='Get user data', status_code=status.HTTP_200_OK, response_model=UserGet)
async def read_user(payload: Annotated[dict, Depends(verify_access_token)], skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    user = user_crud.read(db, payload['sub'], skip, limit)
    return user

# POST
@user_router.post('/', summary='User registration', status_code=status.HTTP_201_CREATED, response_model=dict)
async def register(response: Response,form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Annotated[Session, Depends(get_db)]):
    user_crud.verify_user(db, username=form_data.username)
    refresh_token = create_refresh_token()
    hashed_password = hash_password(form_data.password)
    response.set_cookie(
        key='refresh_token',
        value=refresh_token,
        httponly=True
    )
    user_model = User(username=form_data.username, hashed_password=hashed_password, refresh_token=refresh_token)
    user_model = user_crud.create(db, user_model)
    user_dict = {
        'sub': str(user_model.id)
    }
    access_token = create_access_token(user_dict)
    return {'access_token': access_token, 'token_type': 'bearer'}

# PATCH
@user_router.patch('/', summary='Updating some of the user\'s information', status_code=status.HTTP_200_OK, response_model=UserGet)
async def partial_update(payload: Annotated[dict, Depends(verify_access_token)], user: UserUpdate, db: Annotated[Session, Depends(get_db)]):
    user_model = user_crud.verify(db, payload['sub'])
    user_dict = user.model_dump(exclude_unset=True)
    if user_dict.get('username') or user_dict.get('email') or (user_dict.get('username') and user_dict.get('email')):
        user_crud.verify_user(db, username=user_dict.get('username'), email=user_dict.get('email'))
    user_model = user_crud.update(db, user_model, user, True)
    return user_model

# DELETE
@user_router.delete('/', summary='delete user', status_code=status.HTTP_204_NO_CONTENT, response_model=None)
async def delete_user(payload: Annotated[dict, Depends(verify_access_token)], password: Annotated[str, Body()], db: Annotated[Session, Depends(get_db)]):
    user_model = user_crud.verify(db, payload['sub'])
    if not verify_passwword(password, user_model.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='password is invalid'
        )
    user_crud.delete(db, user_model)

# Refresh token
@user_router.post('/refresh', summary='Renew access token using refresh token', status_code=status.HTTP_200_OK, response_model=dict, dependencies=[Depends(verify_refresh_token)])
async def update_access_token(request: Request, db: Annotated[Session, Depends(get_db)]):
    refresh_token = request.cookies.get('refresh_token')
    verify_refresh_token(refresh_token)
    user = db.query(User).filter(User.refresh_token == refresh_token).one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='refresh_token not found'
        )
    access_token = create_access_token({'sub': str(user.id)})
    return {'access_token': access_token, 'token_type': 'bearer'}