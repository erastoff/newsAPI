from datetime import datetime

import httpx
from bs4 import BeautifulSoup
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import create_news, get_news_by_title
from app.database import engine
from app.schemas import NewsCreate

URL = "https://mosday.ru/news/tags.php?metro"


def fetch_news():
    response = httpx.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")
    news_items = []

    news_table = soup.find("table", {"width": "95%"})
    if not news_table:
        return news_items

    for item in news_table.find_all("tr"):

        date_font = item.find("font", color="#666666")
        if date_font and date_font.b:
            date_text = date_font.find_next(string=True)
            time_text = date_text.find_next(string=True)
            date_text = date_text.text.strip()
            date_time_str = f"{date_text}{time_text}"
            date_time = datetime.strptime(date_time_str, "%d.%m.%Y %H:%M")
        else:
            continue

        title_tag = item.find("font", size="3")
        if title_tag and title_tag.a:
            title = title_tag.a.text.strip()
            url = "http://mosday.ru/news/" + title_tag.a["href"]
        else:
            continue

        img_tag = item.find("img")
        if img_tag:
            image_url = "http://mosday.ru/news/" + img_tag["src"]
        else:
            continue
        news_item = NewsCreate(
            title=title,
            url=url,
            image_url=image_url,
            published_at=date_time,
            parsed_at=datetime.now(),
        )
        news_items.append(news_item)
    return news_items


async def save_news(db: AsyncSession, news_items: list[NewsCreate]):
    async with AsyncSession(engine) as session:
        for news in news_items:
            check = await get_news_by_title(session, title=news.title)
            if not check:
                await create_news(db, news)


async def parse_and_save_news():
    async with AsyncSession(engine) as session:
        news_items = fetch_news()
        await save_news(session, news_items)


def main():
    pass


if __name__ == "__main__":
    main()
