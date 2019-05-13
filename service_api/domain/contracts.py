from service_api.database import *
from service_api.domain.models import payment
import aiohttp
import logging


contract_ip = "http://0.0.0.0:10201/contract/"


async def send_request_contracts(contract_id):

    array_id = []
    for item in contract_id:
        params = {"id": str(item)}
        try:
            async with aiohttp.ClientSession() as session:
                r = await session.get(contract_ip, params=params)
                if r.status == 200:
                    array_id.append(item)
        except Exception as exc:
            logging.error(exc)
    return array_id


async def get_contracts(contracts):
    engine = await connect_db()
    raw_data = []
    query = payment.select().where(payment.c.contract_id.in_(contracts))
    async with engine.acquire() as conn:
        selected_rows = await conn.execute(query)
        async for row in selected_rows:
            raw_data.append(row)
    return raw_data


