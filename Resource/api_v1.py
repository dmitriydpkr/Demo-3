import requests
from sanic import Sanic
from .contract import PaymentsContract
from .payments import *

app = Sanic()

app.add_route(IndexView.as_view(), '/')
app.add_route(Payments.as_view(), 'payment')
app.add_route(PaymentOne.as_view(), 'payment/<pay_id:int>')
app.add_route(PaymentPeriod.as_view(), 'payment/date/<start>/<finish>')
app.add_route(PaymentPeriod.as_view(), 'payment/date/<start>/')
app.add_route(PaymentsContract.as_view(), 'payment/contract/<contract_number>')
app.add_route(PaymentsCreate.as_view(), '/payment/insert')
app.add_route(PaymentsUpdate.as_view(), '/payment/update')


def registration_sda():
    sda = "http://0.0.0.0:7000/"
    data = {"message": "Hello SDA, it is Payments!", "service": "Payments", 'host': "0.0.0.0", 'port': 8001}
    headers = {'Content-type': 'application/json'}
    try:
        requests.post(sda, json=data, headers=headers)
    except requests.exceptions.ConnectionError:
        print('Connection error occurred')
    except requests.exceptions.HTTPError:
        print('HTTP error occurred')
    except requests.exceptions.URLRequired:
        print('A valid URL is required to make a request')
    except requests.exceptions.TooManyRedirects:
        print('Too many redirects')
    except requests.exceptions.ReadTimeout:
        print('The server did not send any data in the allotted amount of time')
    except requests.exceptions.RequestException:
        print('There was an ambiguous exception that occurred while handling your request')


if __name__ == '__main__':
    # registration_sda()
    app.run(host="0.0.0.0", port=8001)

