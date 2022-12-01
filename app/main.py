import fastapi
from asyncpg.connection import Connection
from fastapi import FastAPI
from app.db import database, _get_connection_from_pool, User
from app.schemas import QuerySchema
from app.utils import perform_transaction

app = FastAPI()


@app.on_event("startup")
async def startup():
    if not database.is_connected:
        await database.connect()
    await User.objects.get_or_create(name='john', email="john@test.com", balance=1500, status='')
    await User.objects.get_or_create(name='monica', email="mon@test.com", balance=500, status='')
    await User.objects.get_or_create(name='elizabeth', email="liza@test.com", balance=5000, status='')


@app.get("/")
async def get_clients():
    return await User.objects.all()


@app.post("/transaction")
async def do_transaction(
        query_serializer: list[QuerySchema],
        conn: Connection = fastapi.Depends(_get_connection_from_pool),
):
    for query in query_serializer:
        try:
            await perform_transaction(conn, query)
        except Exception:
            continue


@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()
