import logging
from datetime import datetime, timedelta
from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError
from app.db.chat import Chat
from app.db.address import Address
from app.db.sentoutage import SentOutage
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.db.exceptions import (
    AddressesNumExceeded,
    AddressAlreadyExists,
    OutageAlreadySent
)


# Functions that operating with Chat instances
# Inserting and removing chats from database

async def insert_chat(tg_chat_id: str, session: AsyncSession) -> bool:
    """Insert new chat into database"""

    try:
        session.add(Chat(tg_chat_id=tg_chat_id))
        await session.commit()
        logging.info(f'New chat ({tg_chat_id}) was inserted to database.')
        return True
    except IntegrityError:
        await session.rollback()
        logging.info(f'Chat ({tg_chat_id}) wasn\'t inserted, it already exists.')
        return False


async def delete_chat(tg_chat_id: str, session: AsyncSession) -> bool | None:
    """Delete chat from database"""

    try:
        stmt = select(Chat).where(Chat.tg_chat_id == tg_chat_id)
        query = await session.execute(stmt)
        chat = query.scalar_one_or_none()
        if chat:
            await session.delete(chat)
            await session.commit()
            logging.info(f'Chat ({tg_chat_id}) was deleted from database.')
            return True
        else:
            logging.info(f'Chat ({tg_chat_id}) was not found.')
            return False
    except Exception as err:
        logging.error(f'Chat ({tg_chat_id}) wasn\'t deleted, {err}')
        return None


# Functions that operating with Addresses instances
# Inserting, removing addresses and also auxiliary functions

MAX_ADDRESSES_PER_CHAT = 2


async def is_address_num_exceeded(tg_chat_id: str, session: AsyncSession):
    """
    Check if address num count for specific chat exceeded
    if fails raises AddressesNumExceeded
    """

    stmt = select(Chat).where(Chat.tg_chat_id == tg_chat_id).options(selectinload(Chat.addresses))
    query = await session.execute(stmt)
    chat = query.scalar_one_or_none()
    chat_addresses_count = len(chat.addresses)
    if chat_addresses_count >= MAX_ADDRESSES_PER_CHAT:
        raise AddressesNumExceeded(f"Number of addresses exceeded for chat ({tg_chat_id}).")
    pass


async def insert_address(tg_chat_id: str, address: dict, session: AsyncSession) -> bool | None:
    """Insert new address into database"""

    city = address.get('city').lower()
    street = address.get('street')

    try:
        stmt = select(Chat).where(Chat.tg_chat_id == tg_chat_id)
        query = await session.execute(stmt)
        chat = query.scalar_one_or_none()
        session.add(
            Address(
                chat_id=chat.id,
                city=city,
                street=street,))
        await session.commit()
        logging.info(f"New address ({street, city}) inserted for chat ({tg_chat_id}).")
        return True
    except IntegrityError:
        await session.rollback()
        logging.info(f"Address ({street, city}) already exists for chat ({tg_chat_id}).")
        raise AddressAlreadyExists
    except Exception as err:
        await session.rollback()
        logging.error(f'Address for chat ({tg_chat_id}) wasn\'t inserted, {err}')
        return None


async def select_addresses(session: AsyncSession) -> list | None:
    """Select all addresses from database"""
    async with session() as session:
        async with session.begin():
            try:
                stmt = select(Address)
                query = await session.execute(stmt)
                addresses = query.scalars().all()
                return addresses
            except Exception as err:
                logging.error(f'Couldn\'t select addresses, {err}')
                return None


async def select_full_addresses(tg_chat_id: str, session: AsyncSession) -> set | None:
    """Select all full addresses from database based on chat id"""

    try:
        stmt = select(Chat).where(Chat.tg_chat_id == tg_chat_id).options(selectinload(Chat.addresses))
        query = await session.execute(stmt)
        chat = query.scalar_one_or_none()
        result = set()
        for address in chat.addresses:
            result.add(address.full_address)
        return result
    except Exception as err:
        logging.error(f'Couldn\'t select full addresses, {err}')
        return None


async def delete_address(tg_chat_id: str, full_address: str, session: AsyncSession) -> bool | None:
    """Delete address filtered by chat id and full_address field"""

    try:
        stmt = select(Chat).where(Chat.tg_chat_id == tg_chat_id)
        query = await session.execute(stmt)
        chat = query.scalar_one_or_none()

        delete_stmt = delete(Address).where(
            (Address.chat_id == chat.id) & (Address.full_address == full_address)
        )
        await session.execute(delete_stmt)
        await session.commit()
        logging.info(f"Address ({full_address}) for chat ({tg_chat_id}) has been successfully deleted.")
        return True
    except Exception as err:
        logging.error(f'Address for chat ({tg_chat_id}) wasn\'t deleted, {err}')
        return None


# Functions that operating with SentOutage instances


async def insert_sent_outage(tg_chat_id: str, outage: dict, session: AsyncSession):
    """Insert outage assosiated with specific chat"""
    async with session() as session:
        async with session.begin():

            try:
                stmt = select(Chat).where(Chat.tg_chat_id == tg_chat_id)
                query = await session.execute(stmt)
                chat = query.scalar_one_or_none()
                session.add(
                    SentOutage(
                        chat_id=chat.id,
                        date=outage.get("date"),
                        type=outage.get("type"),
                        emergency=outage.get("emergency"),
                        title=outage.get("title"),
                        info=outage.get("info")
                    )
                )
                await session.commit()
                logging.info(f"SentOutage ({outage}) inserted for chat ({tg_chat_id}).")
            except IntegrityError:
                await session.rollback()
                logging.info(f"SentOutage ({outage}) already exists for chat ({tg_chat_id}).")
                raise OutageAlreadySent


async def delete_sent_outages(session: AsyncSession):
    """Delete outdated sent outages"""

    one_week_before = datetime.now() - timedelta(days=7)

    async with session() as session:
        async with session.begin():
            try:
                stmt = select(SentOutage).where(SentOutage.date < one_week_before)
                query = await session.execute(stmt)
                sent_outages = query.scalars().all()
                for row in sent_outages:
                    await session.delete(row)
                await session.commit()
            except Exception as err:
                logging.error(f"Couldn't delete outdated sent outages, {err}")
