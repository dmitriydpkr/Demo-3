from sanic import Sanic
from sanic import response
from serializers import *
from payment_service import *
from sanic.response import text
import requests
from sanic.views import HTTPMethodView
from serializers import PaymentSchema

app = Sanic()


class IndexView(HTTPMethodView):
    def get(self, request):
        return response.json({'message': 'Hello world!'}, headers={'Service': 'SDA'}, status=200)


app.add_route(IndexView.as_view(), '/')


class Payments(HTTPMethodView):
    async def get(self, request):
        payments = await get_all_payments()
        data = PaymentSchema().dump(payments, many=True)
        return response.json(data)


app.add_route(Payments.as_view(), 'payment')


class PaymentOne(HTTPMethodView):
    async def get(self, request, pay_id):
        payment_one = await get_one_payment(pay_id)
        data = PaymentSchema().dump(payment_one, many=True)
        return response.json(data)


app.add_route(PaymentOne.as_view(), 'payment/<pay_id:int>')


class PaymentPeriod(HTTPMethodView):
    async def get(self, request, start, finish):
        payment_period = await get_payment_period(start, finish)
        data = PaymentSchema().dump(payment_period, many=True)
        return response.json(data)


app.add_route(PaymentPeriod.as_view(), 'payment/date/<start>/<finish>')


class PaymentsContragent(HTTPMethodView):
    async def get(self, request, contragent_id):
        payments_contragent = await get_one_contragent(contragent_id)
        data = PaymentSchema().dump(payments_contragent, many=True)
        return response.json(data)


app.add_route(PaymentsContragent.as_view(), 'payment/contragent/<contragent_id:int>')


class PaymentsContract(HTTPMethodView):
    async def get(self, request, contract_number):
        status_contract = await send_request_contracts(contract_number)

        if status_contract == 200:
            payments = await get_contract(contract_number)
            data = PaymentSchema().dump(payments, many=True)
            return response.json(data)
        else:
            return text('Contract not founded')


app.add_route(PaymentsContract.as_view(), 'payment/contract/<contract_number>')


class PaymentsCreate(HTTPMethodView):
    async def post(self, request):
        await create_payment(request.json)
        return text('I have done it')


app.add_route(PaymentsCreate.as_view(), '/payment/insert')


class PaymentsUpdate(HTTPMethodView):
    async def post(self, request):
        await update_payment(request.json)
        return text('I have done it')


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

