# from fastapi import FastAPI
#
# app = FastAPI()
#
#
# @app.get("/")
# async def root():
#     return {"message": "Hello World"}
#
#
# @app.get("/hello/{name}")
# async def say_hello(name: str):
#     return {"message": f"Hello {name}"}

import logging
import asyncio
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import engine, get_db
from app.models import Base
from app.parser import parse_and_save_news
from app.schemas import News as NewsSchema
from app.crud import get_news_by_days, create_news
from contextlib import asynccontextmanager

logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] %(levelname)s: %(message)s.",
    datefmt="%Y.%m.%d %H:%M:%S",
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Set up resources here
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Start background task
    task = asyncio.create_task(background_parser())

    yield

    # Clean up resources here
    task.cancel()
    await engine.dispose()


app = FastAPI(lifespan=lifespan)


async def background_parser():
    while True:
        logging.info("Starting parse_and_save_news task")
        await parse_and_save_news()
        logging.info("Completed parse_and_save_news task, sleeping for 600 seconds")
        await asyncio.sleep(600)


@app.get("/metro/news", response_model=list[NewsSchema])
async def read_news(day: int, db: AsyncSession = Depends(get_db)):
    news = await get_news_by_days(db, day)
    return news
