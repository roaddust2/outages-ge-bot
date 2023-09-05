import logging
from typing import List
from datetime import datetime, timedelta
from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError
from app.db.chat import Chat
from app.db.address import Address
from app.db.sentoutage import SentOutage
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.db.exceptions import AddressesNumExceeded, AddressAlreadyExists


# Functions that operating with Chat instances
# Selecting, inserting and removing chats from database

async def select_chats(session: AsyncSession) -> List["Chat"]:
    """Select chats"""

    async with session() as session:
        async with session.begin():

            query = await session.execute(
                select(Chat).where(Chat.state == Chat.State.active.value).options(selectinload(Chat.addresses))
            )
            chats = query.scalars().all()

    return chats


async def select_chat(tg_chat_id: str, session: AsyncSession) -> Chat:
    """Select chat"""

    query = await session.execute(
        select(Chat).where(Chat.tg_chat_id == tg_chat_id)
    )
    chat = query.scalar_one_or_none()
    return chat


async def insert_chats(chat_ids: List[str], session: AsyncSession) -> bool | None:
    """Insert or activate chats"""

    result_ids = []

    for id in chat_ids:
        chat = await select_chat(id, session)
        if chat:
            chat.state = Chat.State.active.value
        else:
            session.add(Chat(tg_chat_id=id, state=Chat.State.active.value))
        result_ids.append(id)

    if result_ids:
        try:
            await session.commit()
            logging.info(f"Total chats were activated: {len(result_ids)}. Chat ids: {result_ids}.")
            return True
        except Exception as err:
            await session.rollback()
            logging.error(f"Total chats were activated: 0. Error occured: {err}")
            return None


async def delete_chats(chat_ids: List[str], session: AsyncSession) -> bool | None:
    """Inactivate chats"""

    result_ids = []

    for id in chat_ids:
        chat = await select_chat(id, session)
        if chat:
            chat.state = Chat.State.inactive.value
        else:
            logging.info(f"Chat {id} was not found.")
        result_ids.append(id)

    if result_ids:
        try:
            await session.commit()
            logging.info(f"Total chats were inactivated: {len(result_ids)}. Chat ids: {result_ids}.")
            return True
        except Exception as err:
            await session.rollback()
            logging.error(f"Total chats were inactivated: 0. Error occured: {err}")
            return None


# Functions that operating with Addresses instances
# Inserting, removing addresses and also auxiliary functions

MAX_ADDRESSES_PER_CHAT = 2


async def is_address_num_exceeded(tg_chat_id: str, session: AsyncSession) -> None:
    """
    Check if address num count for specific chat exceeded
    if fails raises AddressesNumExceeded
    """

    stmt = select(Chat).where(Chat.tg_chat_id == tg_chat_id).options(selectinload(Chat.addresses))
    query = await session.execute(stmt)
    chat = query.scalar_one_or_none()
    if chat.addresses:
        chat_addresses_count = len(chat.addresses)
        if chat_addresses_count >= MAX_ADDRESSES_PER_CHAT:
            raise AddressesNumExceeded(f"Number of addresses exceeded for chat: {tg_chat_id}.")
    else:
        pass


async def insert_address(tg_chat_id: str, address: dict, session: AsyncSession) -> bool | None:
    """Insert new address into database"""

    city = address.get('city').lower()
    street = address.get('street')

    try:
        chat = await select_chat(tg_chat_id, session)
        session.add(
            Address(
                chat_id=chat.id,
                city=city,
                street=street,))
        await session.commit()
        logging.info(f"New address: {street, city} was inserted for chat - {tg_chat_id}.")
        return True
    except IntegrityError:
        await session.rollback()
        logging.info(f"Address {street, city} already exists for chat - {tg_chat_id}.")
        raise AddressAlreadyExists
    except Exception as err:
        await session.rollback()
        logging.error(f'Address for chat - {tg_chat_id}) wasn\'t inserted, {err}')
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
        chat = await select_chat(tg_chat_id, session)
        delete_stmt = delete(Address).where(
            (Address.chat_id == chat.id) & (Address.full_address == full_address)
        )
        await session.execute(delete_stmt)
        await session.commit()
        logging.info(f"Address {full_address} for chat - {tg_chat_id} has been successfully deleted.")
        return True
    except Exception as err:
        logging.error(f'Address for chat - {tg_chat_id} wasn\'t deleted, {err}')
        return None


# Functions that operating with SentOutage instances

async def insert_sent_outages(tg_chat_id: str, outages: List[dict], session: AsyncSession) -> bool | None:
    """Insert outage assosiated with specific chat"""

    async with session() as session:
        async with session.begin():

            chat = await select_chat(tg_chat_id, session)
            outages_count = 0
            for outage in outages:
                session.add(SentOutage(chat_id=chat.id, outage=outage))
                outages_count += 1
            try:
                await session.commit()
                logging.info(f"Total outages were inserted: {outages_count} Chat id: {chat.id}.")
                return True
            except Exception as err:
                await session.rollback()
                logging.error(f"Error occured during outages insert, {err}")
                return None


async def delete_sent_outages(session: AsyncSession) -> bool | None:
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
                return True
            except Exception as err:
                logging.error(f"Couldn't delete outdated sent outages, {err}")
                return None


async def select_chat_outages(tg_chat_id: str, session: AsyncSession) -> list:
    """Return boolean if outage already sent or not"""

    async with session() as session:
        async with session.begin():
            query = await session.execute(
                select(Chat).where(Chat.tg_chat_id == tg_chat_id)
            )
            chat = query.scalar_one_or_none()
            query = await session.execute(
                select(SentOutage).where(SentOutage.chat_id == chat.id)
            )
            sent_outages = query.scalars().all()
            result = [outage.outage for outage in sent_outages]
            return result
