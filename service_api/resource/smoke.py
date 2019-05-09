from sanic.views import HTTPMethodView
from sanic import response
import requests


class Smoke(HTTPMethodView):
    def get(self, request):
        return response.json(
            {"message": "Hello world!"}, headers={"Service": "Payments"}, status=200
        )


async def notification():
    sda = "http://0.0.0.0:31502/"
    data = {
        "message": "Hello SDA, it is Payments!",
        "service": "Payments",
        "host": "0.0.0.0",
        "port": 8001,
    }
    headers = {"Content-type": "application/json"}
    try:
        requests.post(sda, json=data, headers=headers)
    except requests.exceptions.ConnectionError:
        print("Connection error occurred")
    except requests.exceptions.HTTPError:
        print("HTTP error occurred")
    except requests.exceptions.URLRequired:
        print("A valid URL is required to make a request")
    except requests.exceptions.TooManyRedirects:
        print("Too many redirects")
    except requests.exceptions.ReadTimeout:
        print("The server did not send any data in the allotted amount of time")
    except requests.exceptions.RequestException:
        print(
            "There was an ambiguous exception that occurred while handling your request"
        )
