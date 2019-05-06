from database import *
from Domain.models import payment


async def get_all_payments():
    engine = await connect_db()
    raw_data = []
    async with engine.acquire() as conn:
        async for row in conn.execute(payment.select().where(payment.c.id < 20)):
            raw_data.append(row)
    return raw_data


async def get_one_payment(pay_id):
    engine = await connect_db()
    raw_data = []
    async with engine.acquire() as conn:
        async for row in conn.execute(payment.select().where(payment.c.id == pay_id)):
            raw_data.append(row)
    return raw_data


async def get_payment_period(start, finish):
    engine = await connect_db()
    raw_data = []
    async with engine.acquire() as conn:
        query = payment.select().where(payment.c.period > start).where(payment.c.period < finish)
        async for row in conn.execute(query):
            raw_data.append(row)
    return raw_data


async def create_payment(json):
    engine = await connect_db()
    async with engine.acquire() as conn:
        await conn.execute(payment.insert().values(contributor=json['contributor'], amount=json['amount'],
                                                   date=json['date'], period=json['period'],
                                                   contract_id=json['contract_id']))


async def update_payment(json):
    engine = await connect_db()
    async with engine.acquire() as conn:
        await conn.execute(payment.update().
                           where(payment.c.id == json['id']).
                           values(contributor=json['contributor'], amount=json['amount'],  date=json['date'],
                                  contract_id=json['contract_id'], period=json['period']))


async def delete_payment(json):
    engine = await connect_db()
    async with engine.acquire() as conn:
        await conn.execute(payment.delete().where(payment.c.id == json['id']))
