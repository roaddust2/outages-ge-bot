import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.db.models import Outage
from settings import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT


engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')


def update_outage(input: dict) -> None:
    '''
    Updates database with outage via INSERT in ORM style

        Parameters:
            input (dict): Outage in a dictionary type:
                [{
                    'date': '2023-07-18',
                    'type': 'water',
                    'emergency': False,
                    'geo_title': 'Title',
                    'en_title': 'Title',
                    'geo_info': 'Info',
                    'en_info': 'Info',
                }]

        Returns:
            new_outage (str): Added outage in a tring type
                (as stated in __repr__ of model Outage)
            None: if outage insert fails
    '''
    with Session(engine) as session:
        session.begin()
        try:
            new_outage = session.add(
                Outage(
                    date=input['date'],
                    type='water',
                    emergency=input['emergency'],
                    geo_title=input.get('geo_title'),
                    en_title=input.get('en_title'),
                    geo_info=input.get('geo_info'),
                    en_info=input.get('en_info'),
                )
            )
            session.commit()
            logging.info(f'Added new outage - {new_outage}')
            return new_outage
        except IntegrityError as err:
            session.rollback()
            logging.error(f'{err} - outage already exists')
            return None
