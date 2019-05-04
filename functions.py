from models import *


async def go():
    engine = await create_engine(user='myuser',
                                 database='dbprod',
                                 host='127.0.0.1',
                                 port=5432,
                                 password='mypass')
    return engine

# GET


async def get_all_payments():
    engine = await go()
    raw_data = []
    async with engine.acquire() as conn:
        async for row in conn.execute(payment.select().where(payment.c.id < 20)):
            raw_data.append(row)
    return raw_data


async def get_one_payment(pay_id):
    engine = await go()
    raw_data = []
    async with engine.acquire() as conn:
        async for row in conn.execute(payment.select().where(payment.c.id == pay_id)):
            raw_data.append(row)
    return raw_data


async def get_payment_period(start, finish):
    engine = await go()
    raw_data = []
    async with engine.acquire() as conn:
        query = payment.select().where(payment.c.date > start).where(payment.c.date < finish)
        async for row in conn.execute(query):
            raw_data.append(row)
    return raw_data


async def get_one_contragent(contr_id):
    engine = await go()
    raw_data = []
    async with engine.acquire() as conn:
        async for row in conn.execute(payment.select().where(payment.c.contragent_id == contr_id)):
            raw_data.append(row)

    return raw_data


async def get_one_contract(contract_id):
    engine = await go()
    raw_data = []
    async with engine.acquire() as conn:
        async for row in conn.execute(payment.select().where(payment.c.contract_id == contract_id)):
            raw_data.append(row)
            print(row.period)
    return raw_data


# POST


async def insert_all(json):
    engine = await go()
    async with engine.acquire() as conn:
        await conn.execute(payment.insert().values(contributor=json['contributor'], amount=json['amount'],
                                                   period=json['period'], date=json['date'],
                                                   contragent_id=json['contragent_id'], contract_id=json['contract_id']))


async def update_one(json):
    engine = await go()
    async with engine.acquire() as conn:
        await conn.execute(payment.update().
                           where(payment.c.id == json['id']).
                           values(contributor=json['contributor'], amount=json['amount'], period=json['period'],
                                  date=json['date'], contragent_id=json['contragent_id'], contract_id=json['contract_id']))










