import requests
from database import *
from models import payment
import datetime
contract_ip = "http://0.0.0.0:6000/contract/"


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
        print(query)
        async for row in conn.execute(query):
            raw_data.append(row)
    return raw_data


async def send_request_contracts(contract_id):
    try:
        r = requests.get(contract_ip + str(contract_id))
        return r.status_code
    except requests.exceptions.RequestException as err:
        print(err)


async def get_contract(contract_number):

    engine = await connect_db()
    raw_data = []
    async with engine.acquire() as conn:
        async for row in conn.execute(payment.select().where(payment.c.contract_id == contract_number)):
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

