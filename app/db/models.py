from sqlalchemy import Integer, String, Text, Boolean, DateTime, UniqueConstraint
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase

from datetime import datetime


class Base(DeclarativeBase):
    """Base class reffering to MetaData"""
    pass


class Outage(Base):
    """Outage model"""

    __tablename__ = "outages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    type: Mapped[str] = mapped_column(String(255), nullable=False)
    emergency: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    geo_title: Mapped[str] = mapped_column(String(255), nullable=True)
    en_title: Mapped[str] = mapped_column(String(255), nullable=True)
    geo_info: Mapped[str] = mapped_column(Text, nullable=True)
    en_info: Mapped[str] = mapped_column(Text, nullable=True)

    __table_args__ = (
        UniqueConstraint(
            'date', 'geo_title', 'geo_info', name='date_title_info_uc'
        ),
    )

    def __repr__(self) -> str:
        return (
            "Outage("
            f"id={self.id!r},"
            f"date={self.date!r},"
            f"type={self.type!r},"
            f"emergency={self.emergency!r},"
            f"geo_title={self.geo_title!r},"
            f"en_title={self.en_title!r},"
            f"geo_info={self.geo_info!r},"
            f"en_info={self.en_info!r})"
        )
