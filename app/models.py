from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base


class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    url = Column(String)
    image_url = Column(String)
    published_at = Column(DateTime)
    parsed_at = Column(DateTime)
