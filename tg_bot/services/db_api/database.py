import os
import asyncio

from sqlalchemy import Column, String, MetaData, ForeignKey, update, delete
from sqlalchemy import Integer, DateTime, BigInteger
from sqlalchemy.ext.asyncio import create_async_engine, async_session, AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import declarative_base, sessionmaker, selectinload, relationship

from config import DB_DRIVER, DB_USER, DB_PASSWORD, DB_HOST, DB_NAME

# Setting up the database connection
db_string = f"{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}" 

Base = declarative_base()

# Class for creating table "users" in the database
class User(Base):  
    __tablename__ = "users"

    user_id = Column(BigInteger, primary_key=True)
    user_name = Column(String)
    user_surname = Column(String)
    username = Column(String)
    language = Column(String)
    date_of_joining = Column(DateTime)


    def __init__(self, user_id, name, surname, username, language, date):
        self.user_id = user_id
        self.user_name = name
        self.user_surname = surname
        self.username = username
        self.language = language
        self.date_of_joining = date

# Creating tables in the database
async def async_main():
    global SessionMaker, engine
    engine = create_async_engine(db_string, pool_size=30, max_overflow=30, echo=False) 

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    SessionMaker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False, future=True)

    await engine.dispose()

asyncio.run(async_main())

