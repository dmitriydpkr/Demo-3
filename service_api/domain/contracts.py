import requests
from database import *
from service_api.domain.models import payment

contract_ip = "http://0.0.0.0:10201/contract/"


async def send_request_contracts(contract_id):
    try:
        # r = requests.get(contract_ip + str(contract_id))
        return 200
        # return r.status_code
    except requests.exceptions.RequestException as err:
        print(err)


async def get_contract(contract_number):

    engine = await connect_db()
    raw_data = []
    async with engine.acquire() as conn:
        async for row in conn.execute(
            payment.select().where(payment.c.contract_id == contract_number)
        ):
            raw_data.append(row)
    return raw_data
