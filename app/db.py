import asyncpg
import databases
import ormar
import sqlalchemy
from typing import AsyncGenerator
from .config import settings
from asyncpg.connection import Connection
from typing import Optional
from datetime import datetime

database = databases.Database(settings.db_url)
metadata = sqlalchemy.MetaData()


class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


class User(ormar.Model):
    class Meta(BaseMeta):
        tablename = "users"

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=128, nullable=False)
    email: str = ormar.String(max_length=128, unique=True, nullable=False)
    balance: float = ormar.Float(minimum=0)
    status: str = ormar.String(max_length=512)
    updated: datetime = ormar.DateTime(nullable=True)


class Transaction(ormar.Model):
    class Meta(BaseMeta):
        tablename = "transaction"

    id: int = ormar.Integer(primary_key=True)
    user: Optional[User] = ormar.ForeignKey(User)
    type: str = ormar.String(max_length=128, nullable=False, choices=['increase', 'decrease'])
    amount: float = ormar.Float(minimum=0)
    status: str = ormar.String(max_length=512, choices=['success', 'fail'], nullable=True)
    created: datetime = ormar.DateTime(default=datetime.now())


async def _get_connection_from_pool() -> AsyncGenerator[Connection, None]:
    async with asyncpg.create_pool(
            dsn=settings.db_url,
    ) as pool:
        async with pool.acquire() as conn:
            yield conn


engine = sqlalchemy.create_engine(settings.db_url)
metadata.create_all(engine)
