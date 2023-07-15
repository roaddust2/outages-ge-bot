from sqlalchemy import Integer, String, Text, DateTime
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase

from datetime import datetime


class Base(DeclarativeBase):
    """Base class reffering to MetaData"""
    pass


class Outage(Base):
    """Outages model"""

    __tablename__ = "outages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    type: Mapped[str] = mapped_column(String(255), nullable=False)
    geo_title: Mapped[str] = mapped_column(String(255), nullable=True)
    en_title: Mapped[str] = mapped_column(String(255), nullable=True)
    geo_info: Mapped[str] = mapped_column(Text, nullable=True)
    en_info: Mapped[str] = mapped_column(Text, nullable=True)
