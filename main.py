from fastapi import FastAPI
from routes import routes_router
from core import register_exception

app = FastAPI()
app.include_router(routes_router)
register_exception(app)