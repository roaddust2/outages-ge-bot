import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.db.models import Chat, Address
from settings import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT


engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')


# Functions that operating with Chat instances
# Inserting and removing chats from database

def insert_chat(tg_chat_id: str):
    """Insert new chat into database"""

    with Session(engine) as session:
        session.begin()
        try:
            session.add(Chat(tg_chat_id=tg_chat_id,))
            session.commit()
            logging.info(f'New chat ({tg_chat_id}) was inserted to database.')
            return True
        except IntegrityError:
            session.rollback()
            logging.info(f'Chat ({tg_chat_id}) wasn\'t inserted, it already exists.')
            return False


def delete_chat(tg_chat_id: str):
    """Delete chat from database"""

    with Session(engine) as session:
        session.begin()
        try:
            chat = session.query(Chat).filter_by(tg_chat_id=tg_chat_id).first()
            if chat:
                session.delete(chat)
                session.commit()
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


class AddressesNumExceeded(Exception):
    """Raises when user try to add more addresses than allowed"""
    pass


class AddressAlreadyExists(Exception):
    """Raises when user try to add existing address"""
    pass


def is_address_num_exceeded(tg_chat_id: str):
    """
    Check if address num count for specific chat exceeded
    if fails raises AddressesNumExceeded
    """

    with Session(engine) as session:
        session.begin()
        chat = session.query(Chat).filter_by(tg_chat_id=tg_chat_id).first()
        chat_adresses_count = session.query(Address.id).filter_by(chat_id=chat.id).count()
        if chat_adresses_count >= MAX_ADDRESSES_PER_CHAT:
            raise AddressesNumExceeded(f"Number of addresses exceeded for chat ({tg_chat_id}).")
        pass


def insert_address(tg_chat_id: str, address: dict):
    """Insert new address into database"""

    city = address.get('city').lower()
    street = address.get('street').lower()

    with Session(engine) as session:
        session.begin()
        try:
            chat = session.query(Chat).filter_by(tg_chat_id=tg_chat_id).first()
            session.add(
                Address(
                    chat_id=chat.id,
                    city=city,
                    street=street,))
            session.commit()
            logging.info(f"New address ({street, city}) inserted for chat ({tg_chat_id}).")
            return True
        except IntegrityError:
            session.rollback()
            logging.info(f"Address ({street, city}) already exists for chat ({tg_chat_id}).")
            raise AddressAlreadyExists
        except Exception as err:
            session.rollback()
            logging.error(f'Address for chat ({tg_chat_id}) wasn\'t inserted, {err}')
            return None


def select_addresses(tg_chat_id: str):
    """Select all addresses from database based on chat id"""

    with Session(engine) as session:
        session.begin()
        try:
            chat = session.query(Chat).filter_by(tg_chat_id=tg_chat_id).first()
            addresses = session.query(Address).filter_by(chat_id=chat.id).all()
            result = set()
            for address in addresses:
                result.add(address.full_address)
            return result
        except Exception:
            return None


def delete_address(tg_chat_id: str, full_address: str):
    """Delete address filtered by chat id and full_address field"""

    with Session(engine) as session:
        session.begin()
        try:
            chat = session.query(Chat).filter_by(tg_chat_id=tg_chat_id).first()
            address = session.query(Address).filter_by(chat_id=chat.id, full_address=full_address).first()
            session.delete(address)
            session.commit()
            logging.info(f"Address ({full_address}) for chat ({tg_chat_id}) has been successfully deleted.")
            return True
        except Exception as err:
            logging.error(f'Address for chat ({tg_chat_id}) wasn\'t deleted, {err}')
            return None
