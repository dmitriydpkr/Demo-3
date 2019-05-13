from sanic.views import HTTPMethodView
from sanic import response
from aiohttp_requests import requests
import aiohttp
import logging


class Smoke(HTTPMethodView):
    def get(self, request):
        return response.json(
            {"message": "Hello world!"}, headers={"Service": "Payments"}, status=200
        )


async def notification():
    sda = "http://0.0.0.0:31502/"
    parameters = '?name=Payments&host=0.0.0.0&port: 8001'
    data = {
        "message": "Hello SDA, it is Payments!",
        "service": "Payments",
        "host": "0.0.0.0",
        "port": 8001,
    }
    try:
        async with aiohttp.ClientSession() as session:
            await session.post(sda, data=parameters)

    except Exception as exc:
        logging.error(exc)
