import httpx
from bs4 import BeautifulSoup
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

# from . import crud, schemas, models, database
from app.models import News
from app.crud import create_news
from app.schemas import NewsBase, NewsCreate
from app.database import get_db, engine

URL = "https://mosday.ru/news/tags.php?metro"


def fetch_news():
    response = httpx.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")
    news_items = []

    # Поиск всех таблиц и строк, содержащих новости
    news_table = soup.find("table", {"width": "95%"})
    if not news_table:
        return news_items

    for item in news_table.find_all("tr"):
        # Извлечение даты и времени публикации
        date_font = item.find("font", color="#666666")
        if date_font and date_font.b:
            date_text = date_font.find_next(string=True)
            time_text = date_text.find_next(string=True)
            date_text = date_text.text.strip()
            date_time_str = f"{date_text}{time_text}"
            date_time = datetime.strptime(date_time_str, "%d.%m.%Y %H:%M")
        else:
            continue  # Пропустить элемент, если дата или время не найдены

        # Извлечение заголовка и URL
        title_tag = item.find("font", size="3")
        if title_tag and title_tag.a:
            title = title_tag.a.text.strip()
            url = "http://mosday.ru/news/" + title_tag.a["href"]
        else:
            continue  # Пропустить элемент, если заголовок или URL не найдены

        # Извлечение URL изображения
        img_tag = item.find("img")
        if img_tag:
            image_url = "http://mosday.ru/news/" + img_tag["src"]
        else:
            continue  # Пропустить элемент, если изображение не найдено

        # Добавление новости в список
        # news_items.append(
        #     {
        #         "title": title,
        #         "url": url,
        #         "image_url": image_url,
        #         "published_at": date_time,
        #     }
        # )
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
    for news in news_items:
        await create_news(db, news)


async def parse_and_save_news():
    async with AsyncSession(engine) as session:
        news_items = fetch_news()
        await save_news(session, news_items)


def main():
    print("MAIN PARSER FUNCTION")
    items = fetch_news()
    print(items[5])


if __name__ == "__main__":
    main()
