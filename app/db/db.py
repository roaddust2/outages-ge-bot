from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.db.models import Outage

from settings import DATABASE_URL

engine = create_engine(DATABASE_URL)


def update_outages(input: dict) -> None:
    with Session(engine) as session:
        session.begin()
        try:
            session.add(
                Outage(
                    date=input['date'],
                    type='water',
                    emergency=True,
                    geo_title=input['geo_title'],
                    en_title=input['en_title'],
                    geo_info=input['geo_info'],
                    en_info=input['en_info'],
                )
            )
        except Exception:
            session.rollback()
            raise
        else:
            session.commit()
    return
