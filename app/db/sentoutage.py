from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy import func, ForeignKey, Integer, DateTime
from app.db.base import Base
from datetime import datetime


class SentOutage(Base):
    """Sent outages model, outage itself stored in JSON format"""

    __tablename__ = "sent_outages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id"))
    outage: Mapped[dict] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=True, default=func.now())
