import os
from sqlalchemy import create_engine

def get_engine():
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise Exception("DATABASE_URL is missing")
    return create_engine(database_url)
    
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)