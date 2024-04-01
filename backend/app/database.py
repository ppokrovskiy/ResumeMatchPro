import logging

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
import os

# Get the database username and password from environment variables
DB_USER = os.getenv("POSTGRES_USER", "resume_match_pro")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "resume_match_pro")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "resume_match_pro")
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


# Create an async engine instance
engine = create_async_engine(DATABASE_URL, echo=True)

# The declarative base class that our model classes will inherit from
Base = declarative_base()

# Sessionmaker factory to get database sessions. It's configured to be used with async
AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession
)


# Dependency to use in FastAPI route to get a database session
async def get_db_session():
    async with AsyncSessionLocal() as session:
        yield session


# Example function to query the database using an async session
async def get_some_data(model):
    async with AsyncSessionLocal() as session:
        async with session.begin():
            result = await session.execute(select(model))
            return result.scalars().all()
