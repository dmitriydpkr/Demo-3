from sanic import response
from Domain.payments import *
from sanic.response import text
from sanic.views import HTTPMethodView
from forms import PaymentSchema
from datetime import datetime


class Payments(HTTPMethodView):
    async def get(self, request):
        payments = await get_all_payments()
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


class PaymentsCreate(HTTPMethodView):
    async def post(self, request):
        await create_payment(request.json)
        return text("I have created payment")


class PaymentsUpdate(HTTPMethodView):
    async def put(self, request):
        await update_payment(request.json)
        return text("I have updated payment")


class PaymentsDelete(HTTPMethodView):
    async def delete(self, request):
        await delete_payment(request.json)
        return text("I have deleted payment")
