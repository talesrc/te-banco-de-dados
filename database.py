from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from logger import logger
import os

DATABASE = os.environ["DATABASE"]
DATABASE_USER = os.environ["DATABASE_USER"]
DATABASE_PASSWORD = os.environ["DATABASE_PASSWORD"]
DATABASE_HOST = os.environ["DATABASE_HOST"]

engine = create_engine(f"postgresql+psycopg2://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:5432/{DATABASE}")

db_session = scoped_session(
    sessionmaker(
        bind=engine,
        autocommit=False,
        autoflush=False
    )
)

Base = declarative_base()

def clean_db() -> None:
    logger.info("Cleaning database")
    Base.metadata.drop_all(bind=engine)

def init_db() -> None:
    logger.info("Initializing database")
    Base.metadata.create_all(bind=engine)

def create_record(record: any) -> None:
    db_session.add(record)
    db_session.commit()
