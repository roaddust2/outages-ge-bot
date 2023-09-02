from typing import TYPE_CHECKING
from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint
)


if TYPE_CHECKING:
    from .chat import Chat


class Address(Base):
    """
    Saved addresses,
    each address connected with chat via chat_id foreign key field
    """

    __tablename__ = "addresses"

    def _default_full_address(context) -> str:
        """Context sensetive default function for full_address field"""
        street = context.get_current_parameters().get("street")
        city = context.get_current_parameters().get("city")
        return f"{street}, {city.capitalize()}"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    chat: Mapped["Chat"] = relationship("Chat", lazy="subquery", back_populates="addresses")
    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id"))
    city: Mapped[str] = mapped_column(String(255), nullable=True)
    street: Mapped[str] = mapped_column(String(255), nullable=True)
    full_address: Mapped[str] = mapped_column(Text, nullable=True, default=_default_full_address)

    __table_args__ = (
        UniqueConstraint(
            'chat_id', 'city', 'street', name='chat_id_city_street_uc'
        ),
    )
