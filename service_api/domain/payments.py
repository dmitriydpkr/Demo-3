from database import *
from service_api.domain.models import payment
from datetime import datetime
from dateutil.parser import parse


async def get_payments(contributor, start, finish):

    transform_start_day = parse(start).date()
    transform_finish_day = parse(finish).date()
    start_day = datetime.min.time()
    finish_day = datetime.max.time()
    start = datetime.combine(transform_start_day, start_day)
    finish = datetime.combine(transform_finish_day, finish_day)

    raw_data = []
    engine = await connect_db()
    async with engine.acquire() as conn:
        if contributor:
            query = payment.select().where(payment.c.contributor == contributor)
        else:
            query = (
                payment.select()
                .where(payment.c.date > start)
                .where(payment.c.date < finish)
            )
        async for row in conn.execute(query):
            raw_data.append(row)
    return raw_data[:20]


async def get_payment(pay_id):
    engine = await connect_db()
    raw_data = []
    async with engine.acquire() as conn:
        async for row in conn.execute(payment.select().where(payment.c.id == pay_id)):
            raw_data.append(row)
    return raw_data


async def insert_one(json):
    engine = await connect_db()
    async with engine.acquire() as conn:
        values = {
            "contributor": json["contributor"],
            "amount": json["amount"],
            "date": json["date"],
            "contract_id": json["contract_id"],
        }
        await conn.execute(payment.insert().values(values))


async def insert_many(json):
    engine = await connect_db()
    async with engine.acquire() as conn:
        for row in json:
            values = {
                "contributor": row["contributor"],
                "amount": row["amount"],
                "date": row["date"],
                "contract_id": row["contract_id"],
            }
            await conn.execute(payment.insert().values(values))


async def update_one(json):
    engine = await connect_db()
    async with engine.acquire() as conn:
        await conn.execute(
            payment.update()
            .where(payment.c.id == json["id"])
            .values(
                contributor=json["contributor"],
                amount=json["amount"],
                date=json["date"],
                contract_id=json["contract_id"],
            )
        )


async def update_many(json):
    engine = await connect_db()
    async with engine.acquire() as conn:
        for row in json:
            await conn.execute(
                payment.update()
                .where(payment.c.id == row["id"])
                .values(
                    contributor=row["contributor"],
                    amount=row["amount"],
                    date=row["date"],
                    contract_id=row["contract_id"],
                )
            )


async def delete_one(json):
    engine = await connect_db()
    async with engine.acquire() as conn:
        await conn.execute(payment.delete().where(payment.c.id == json["id"]))


async def delete_many(json):
    engine = await connect_db()
    async with engine.acquire() as conn:
        for i in json["id"]:
            await conn.execute(payment.delete().where(payment.c.id == i))
