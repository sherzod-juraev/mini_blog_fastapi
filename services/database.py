from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

url = URL.create(
    drivername='postgresql',
    username='postgres',
    password='9943',
    host='localhost',
    port=5432,
    database='blog'
)

engine = create_engine(url)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()