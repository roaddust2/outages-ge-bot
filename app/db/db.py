import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.db.models import Chat, Address
from settings import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT


engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')


MAX_ADDRESSES_ALLOWED = 2


def insert_chat(tg_chat_id: str):
    '''Insert new chat into database'''

    with Session(engine) as session:
        session.begin()
        try:
            session.add(Chat(tg_chat_id=tg_chat_id,))
            session.commit()
            logging.info(f'New chat ({tg_chat_id}) was inserted to database')
            return True
        except IntegrityError:
            session.rollback()
            logging.info(f'Chat ({tg_chat_id}) wasn\'t inserted, it already exists')
            return False


def delete_chat(tg_chat_id: str):
    '''Delete chat from database'''

    with Session(engine) as session:
        session.begin()
        try:
            chat = session.query(Chat).filter_by(tg_chat_id=tg_chat_id).first()
            if chat:
                session.delete(chat)
                session.commit()
                logging.info(f'Chat ({tg_chat_id}) was deleted from database')
                return True
            else:
                logging.info(f'Chat ({tg_chat_id}) not found')
                return False
        except Exception as err:
            logging.error(f'Chat ({tg_chat_id}) wasn\'t deleted, {err}')
            return None


def is_address_num_exceeded(tg_chat_id: str) -> bool:
    '''Check if address num count
    for specific chat exceeded
    returns bool'''

    with Session(engine) as session:
        session.begin()
        chat = session.query(Chat).filter_by(tg_chat_id=tg_chat_id).first()
        chat_adresses_count = session.query(Address.id).filter_by(chat_id=chat.id).count()
        if chat_adresses_count < 2:
            return False
        else:
            return True


def insert_address(tg_chat_id: str, address: dict):
    '''Insert new address into database'''

    city = address.get('city').lower()
    street = address.get('street').lower()

    with Session(engine) as session:
        session.begin()
        try:
            chat = session.query(Chat).filter_by(tg_chat_id=tg_chat_id).first()
            chat_adresses_count = session.query(Address.id).filter_by(chat_id=chat.id).count()
            if chat_adresses_count < 2:
                session.add(
                    Address(
                        chat_id=chat.id,
                        city=city,
                        street=street,))
                session.commit()
                logging.info(
                    f"New address ({street, city}) added for chat ({tg_chat_id})"
                )
                return True
            else:
                logging.error(f'Address for chat ({tg_chat_id}) wasn\'t added, number of addresses exceeded')
                return False
        except Exception as err:
            session.rollback()
            logging.error(f'Address for chat ({tg_chat_id}) wasn\'t added, {err}')
            return None
        


def delete_address(address: dict):
    '''Delete address from database'''
    pass


# def insert_sent_outage(input: dict) -> None:
#     '''
#     Insert sent outages related to chats into database
#     '''
#     with Session(engine) as session:
#         session.begin()
#         try:
#             new_outage = session.add(
#                 Outage(
#                     date=input['date'],
#                     type='water',
#                     emergency=input['emergency'],
#                     geo_title=input.get('geo_title'),
#                     en_title=input.get('en_title'),
#                     geo_info=input.get('geo_info'),
#                     en_info=input.get('en_info'),
#                 )
#             )
#             session.commit()
#             logging.info(f'Added new outage - {new_outage}')
#             return new_outage
#         except IntegrityError as err:
#             session.rollback()
#             logging.error(f'{err} - outage already exists')
#             return None
