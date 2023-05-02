import asyncio
import logging

from sqlalchemy import Column, String, MetaData, ForeignKey 
from sqlalchemy import Integer, DateTime, BIGINT
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import declarative_base, sessionmaker, selectinload, relationship

from decouple import config

DB_USER = config("USER")
PG_PASSWORD = config("PASSWORD")
DB_NAME = config("NAME")
DB_HOST = config("HOST")

logger = logging.getLogger(__name__)

db_driver = 'postgresql+asyncpg'
db_user = DB_USER
db_password = PG_PASSWORD
db_host = DB_HOST
db_name = DB_NAME

db_string = f"{db_driver}://{db_user}:{db_password}@{db_host}/{db_name}" # Settings for connecting to database

Base = declarative_base()


class User(Base): # Init table "users" 
    __tablename__ = "users"

    user_id = Column("user_id", BIGINT, primary_key=True)
    user_name = Column("user_name", String)
    user_surname = Column("user_surname", String)
    username = Column("username", String)
    language = Column("language", String)
    date_of_joining = Column("date_of_joining", DateTime)


    def __init__(self, user_id, name, surname, username, language, date):
        self.user_id = user_id
        self.user_name = name
        self.user_surname = surname
        self.username = username
        self.language = language
        self.date_of_joining = date

    def __repr__(self):
        return f"User{(self.user_id, self.user_name, self.user_surname, self.username, self.language, self.date_of_joining)}"

async def async_main():
    global SessionMaker, engine
    engine = create_async_engine(db_string, echo=False) 

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    SessionMaker = sessionmaker(engine,
                            expire_on_commit=False, 
                            class_=AsyncSession)

    await engine.dispose()

asyncio.run(async_main())


class Database:
    """Add user to database"""
    async def add_user_to_db(user_id: int, user_name: str, user_surname: str, username: str, language: str, date: int):
        user = User(user_id=user_id, name=user_name, surname=user_surname, username=username, language=language, date=date)
        async with SessionMaker.begin() as session: 
            session.add(user)
            await session.commit()

    """Checking whether the user is in the database"""
    async def chek_user_in_db(user_id: int):
        async with SessionMaker.begin() as session:
            statement = select(User).where(User.user_id == user_id)
            result = await session.execute(statement)
            curr = result.scalars()

            for user in curr:
                return True
