from fastapi import FastAPI

# Routers
from router.comment import comment_router
from router.like import like_router
from router.post import post_router
from router.user import user_router

app = FastAPI()

# Add routers
app.include_router(comment_router)
app.include_router(like_router)
app.include_router(post_router)
app.include_router(user_router)