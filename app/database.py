from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from settings import Settings

cfg: Settings = Settings()

DATABASE_URL = cfg.db_uri

engine = create_async_engine(DATABASE_URL, echo=cfg.debug)
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)

Base = declarative_base()


async def get_db():
    async with SessionLocal() as session:
        yield session
