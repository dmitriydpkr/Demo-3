import requests
from database import *


contract_ip = "http://0.0.0.0:6000/contract/"


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


async def send_request_contracts(contract_id):
    try:
        r = requests.get(contract_ip + str(contract_id))
        return r.status_code
    except requests.exceptions.RequestException as err:
        print(err)


async def get_contract(contract_number):

    engine = await go()
    raw_data = []
    async with engine.acquire() as conn:
        async for row in conn.execute(payment.select().where(payment.c.contract_id == contract_number)):
            raw_data.append(row)
    return raw_data


async def create_payment(json):
    engine = await go()
    async with engine.acquire() as conn:
        await conn.execute(payment.insert().values(contributor=json['contributor'], amount=json['amount'],
                                                   period=json['period'], date=json['date'],
                                                   contragent_id=json['contragent_id'],
                                                   contract_id=json['contract_id']))


async def update_payment(json):
    engine = await go()
    async with engine.acquire() as conn:
        await conn.execute(payment.update().
                           where(payment.c.id == json['id']).
                           values(contributor=json['contributor'], amount=json['amount'], period=json['period'],
                                  date=json['date'], contragent_id=json['contragent_id'],
                                  contract_id=json['contract_id']))


