from datetime import datetime
from typing import List
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    ForeignKey,
    Integer,
    String,
    Text,
    Boolean,
    DateTime
)


class Base(DeclarativeBase):
    """Base class referring to MetaData"""
    pass


class Chat(Base):
    """Chat or user model in simple words"""

    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tg_chat_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True)
    addresses: Mapped[List["Address"]] = relationship("Address", cascade="all, delete")
    sent_outages: Mapped[List["SentOutage"]] = relationship("SentOutage", cascade="all, delete")


class Address(Base):
    """
    Saved addresses,
    each address connected with chat via chat_id foreign key field
    """

    __tablename__ = "addresses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id"))
    city: Mapped[str] = mapped_column(String(255), nullable=True)
    street: Mapped[str] = mapped_column(String(255), nullable=True)


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
