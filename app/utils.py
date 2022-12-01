from asyncpg.connection import Connection
import fastapi as fa
from app.db import User
from app.schemas import QuerySchema
from datetime import datetime


async def perform_transaction(conn: Connection, query: QuerySchema):
    async with conn.transaction():
        user: User = await User.objects.get(id=query.user_id)
        if query.balance_dif < 0:
            if user.balance >= abs(query.balance_dif):
                user.balance += query.balance_dif
                user.status = 'Успешно'
                await user.update(_columns=["balance", "status"])
            else:
                user.status = f'{datetime.now().replace(microsecond=0)} Недостаточно средств, запрос заблокирован: текущий баланс {user.balance}, запрашиваемая сумма {abs(query.balance_dif)}'
                await user.update(_columns=["status"])
                raise fa.HTTPException(status_code=404, detail="Недостаточно средств, запрос заблокирован")
        else:
            user.balance += query.balance_dif
            user.status = 'Успешно'
            await user.update(_columns=["balance", "status"])
