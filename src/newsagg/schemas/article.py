from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(AsyncAttrs, DeclarativeBase):
    pass


class ArticleORM(Base):
    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    title: Mapped[str] = mapped_column(String(512), nullable=False)
    link: Mapped[str] = mapped_column(String(1024), nullable=False, unique=True)
    published_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    source: Mapped[str] = mapped_column(String(128), nullable=False)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    retrieved_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now
    )
