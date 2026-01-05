from fastapi import APIRouter


from .users import user_router
from .chats import chat_router
from .comments import comment_router


routes_router = APIRouter()


routes_router.include_router(
    user_router,
    prefix='/auth',
    tags=['Authenticate']
)

routes_router.include_router(
    chat_router,
    prefix='/chat',
    tags=['Chat']
)

routes_router.include_router(
    comment_router,
    prefix='/comment',
    tags=['Comment']
)