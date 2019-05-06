from sanic import response
from Resource.payment_service import *
from sanic.response import text
from sanic.views import HTTPMethodView
from forms import PaymentSchema
from datetime import datetime


class IndexView(HTTPMethodView):
    def get(self, request):
        return response.json({'message': 'Hello world!'}, headers={'Service': 'SDA'}, status=200)


class Payments(HTTPMethodView):
    async def get(self, request):
        payments = await get_all_payments()
        print(payments)
        data = PaymentSchema().dump(payments, many=True)
        return response.json(data)


class PaymentOne(HTTPMethodView):
    async def get(self, request, pay_id):
        payment_one = await get_one_payment(pay_id)
        data = PaymentSchema().dump(payment_one, many=True)
        return response.json(data)


class PaymentPeriod(HTTPMethodView):
    async def get(self, request, start, finish=datetime.now().timestamp()):
        payment_period = await get_payment_period(start, finish)
        data = PaymentSchema().dump(payment_period, many=True)
        return response.json(data)


class PaymentsContract(HTTPMethodView):
    async def get(self, request, contract_number):
        status_contract = await send_request_contracts(contract_number)

        if status_contract == 200:
            payments = await get_contract(contract_number)
            data = PaymentSchema().dump(payments, many=True)
            return response.json(data)
        else:
            return text('Contract not founded')


class PaymentsCreate(HTTPMethodView):
    async def post(self, request):
        await create_payment(request.json)
        return text('I have done it')


class PaymentsUpdate(HTTPMethodView):
    async def post(self, request):
        await update_payment(request.json)
        return text('I have done it')



