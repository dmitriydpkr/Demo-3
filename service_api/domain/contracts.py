from database import *
from service_api.domain.models import payment
from aiohttp_requests import requests
from sanic.exceptions import abort
import aiohttp


contract_ip = "http://0.0.0.0:10201/contract/"


async def send_request_contracts(contract_id):

    try:
        params = {"id": str(contract_id)}
        async with aiohttp.ClientSession() as session:
            r = await session.get(contract_ip, json=params)
            return r.status

    except requests.exceptions.RequestException as err:
        print(err)


async def get_contract(contract_number):
    if len(contract_number) != 36:
        abort(400, "invalid contract id")
    engine = await connect_db()
    raw_data = []
    async with engine.acquire() as conn:
        async for row in conn.execute(
            payment.select().where(payment.c.contract_id == contract_number)
        ):
            raw_data.append(row)
    return raw_data
