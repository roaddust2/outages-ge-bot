from typing import List, TYPE_CHECKING
from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer


if TYPE_CHECKING:
    from .address import Address
    from .sentoutage import SentOutage


class Chat(Base):
    """Chat or user model in simple words"""

    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tg_chat_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True)
    addresses: Mapped[List["Address"]] = relationship("Address", cascade="all, delete")
    sent_outages: Mapped[List["SentOutage"]] = relationship("SentOutage", cascade="all, delete")


def default_full_address(context) -> str:
    """
    Context sensetive default function for full_address field
    """
    street = context.get_current_parameters().get("street")
    city = context.get_current_parameters().get("city")
    return f"{street}, {city.capitalize()}"
