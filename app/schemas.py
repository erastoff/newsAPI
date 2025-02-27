from datetime import datetime

from pydantic import BaseModel


class NewsBase(BaseModel):
    title: str
    url: str
    image_url: str
    published_at: datetime


class NewsCreate(NewsBase):
    parsed_at: datetime


class News(NewsBase):
    id: int

    class Config:
        from_attributes = True
