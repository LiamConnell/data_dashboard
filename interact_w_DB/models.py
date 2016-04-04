from sqlalchemy import create_engine, Column, Integer, Date, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL



DeclarativeBase = declarative_base()


def db_connect():
    engine = create_engine('postgresql://ljrconnell:rocco1!1@liamsdatabase.cbjwfk4y5vix.us-east-1.rds.amazonaws.com:5432/firstdb')
    return engine



def create_deals_table(engine):
    """"""
    DeclarativeBase.metadata.create_all(engine)


class Deals(DeclarativeBase):
    """Sqlalchemy deals model"""
    __tablename__ = "price_data"

    date = Column(Date, primary_key=True)
    Price = Column('Price', Integer)
