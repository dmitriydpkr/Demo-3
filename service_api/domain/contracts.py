import aiohttp
import logging
from config import *


async def get_service_contracts():
    service_socket = []
    sda_address = f"http://{SDA_HOST}:{SDA_PORT}/contracts"
    try:
        async with aiohttp.ClientSession() as session:
            resp = await session.get(sda_address)
            decoded_socket = await resp.text()
            socket_list = decoded_socket.split(",")
            service_socket.append(socket_list[0][2:-1])
            service_socket.append(socket_list[1][2:-2])
            url = f"http://{service_socket[0]}:{service_socket[1]}/contracts"
            print(url)
            return url
    except Exception as exc:
        logging.error(f" {exc} ")
        return 404


async def get_json_ids(json, field):
    json_ids = []
    for row in json:
        json_ids.append(row[field])

    return json_ids
