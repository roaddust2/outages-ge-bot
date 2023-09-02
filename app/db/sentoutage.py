from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import (
    ForeignKey,
    Integer,
    String,
    Text,
    Boolean,
    DateTime,
    UniqueConstraint
)
from app.db.base import Base


class SentOutage(Base):
    """Outage model"""

    __tablename__ = "sent_outages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id"))
    date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    type: Mapped[str] = mapped_column(String(255), nullable=False)
    emergency: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    geo_title: Mapped[str] = mapped_column(String(255), nullable=True)
    en_title: Mapped[str] = mapped_column(String(255), nullable=True)
    geo_info: Mapped[str] = mapped_column(Text, nullable=True)
    en_info: Mapped[str] = mapped_column(Text, nullable=True)

    __table_args__ = (
        UniqueConstraint(
            'chat_id', 'date', 'geo_title', 'geo_info', name='chat_id_date_title_info_uc'
        ),
    )
