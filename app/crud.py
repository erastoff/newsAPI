from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from app.database import get_db, engine

# from . import models, schemas
from app.schemas import NewsCreate
from app.models import News


async def get_news_by_days(db: AsyncSession, days: int):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    result = await db.execute(select(News).filter(News.published_at >= start_date))
    return result.scalars().all()


async def create_news(db: AsyncSession, news: NewsCreate):
    db_news = News(**news.dict())
    db.add(db_news)
    await db.commit()
    await db.refresh(db_news)
    return db_news


async def main():
    async with AsyncSession(engine) as session:
        new_1 = NewsCreate(
            published_at=datetime(2024, 7, 16, 14, 9),
            title="title",
            url="https://mosday.ru/news",
            image_url="https://cdn.mosday.ru/images/logo.png",
            parsed_at=datetime.now(),
        )
        # Create News
        # new_item = await create_news(session, new_1)

        # Read News
        res = await get_news_by_days(session, 200)
        print(res[0].parsed_at, res[0].url)
        print(res[1].parsed_at, res[1].url)
        print(res[2].parsed_at, res[2].url)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
