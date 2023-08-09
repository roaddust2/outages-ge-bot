import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.db.models import Chat
from settings import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT


engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')


def insert_chat(tg_chat_id: str):
    '''Insert new chat into database'''

    with Session(engine) as session:
        session.begin()
        try:
            chat = session.add(Chat(tg_chat_id=tg_chat_id,))
            session.commit()
            logging.info(f'New chat ({tg_chat_id}) was inserted to database')
            return chat
        except IntegrityError:
            session.rollback()
            logging.info(f'Chat ({tg_chat_id}) wasn\'t inserted, it already exists')
            return None


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


def insert_address(address: dict):
    '''Insert new address into database'''
    pass


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
