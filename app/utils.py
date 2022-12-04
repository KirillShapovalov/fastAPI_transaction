from asyncpg.connection import Connection
import fastapi as fa
from app.db import User
from app.schemas import QuerySchema
from datetime import datetime


async def update_user(user: User, query: QuerySchema):
    user.balance += query.balance_dif
    user.status = 'Успешно'
    user.updated = datetime.now()
    await user.update(_columns=['balance', 'status', 'updated'])


async def perform_transaction(conn: Connection, user: User, query: QuerySchema):
    async with conn.transaction():
        if query.balance_dif < 0:
            if user.balance >= abs(query.balance_dif):
                await update_user(user, query)
            else:
                user.status = f'{datetime.now().replace(microsecond=0)} Недостаточно средств, запрос заблокирован: текущий баланс {user.balance}, запрашиваемая сумма {abs(query.balance_dif)}'
                await user.update(_columns=['status'])
                raise fa.HTTPException(status_code=404, detail="Недостаточно средств, запрос заблокирован")
        else:
            await update_user(user, query)
