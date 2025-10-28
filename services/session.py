from .database import SessionLocal

async def get_db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()