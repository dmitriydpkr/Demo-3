from sanic import response
from service_api.domain.payments import *
from sanic.response import text
from sanic.views import HTTPMethodView
from forms import PaymentSchema
from datetime import datetime
from sanic.exceptions import abort


class Payments(HTTPMethodView):
    async def get(self, request, start='2016-06-29', finish=str(datetime.now())):
        contributor = request.args.get("contributor")
        payments = await get_payments(contributor, start, finish)
        data = PaymentSchema().dump(payments, many=True)
        return response.json(data)

    async def post(self, request):
        await insert_many(request.json)
        return text("I have created payment")

    async def put(self, request):
        await update_many(request.json)
        return text("I have updated payment")

    async def delete(self, request):
        print(request.json)
        await delete_many(request.json)
        return text("I have deleted payment")


class Payment(HTTPMethodView):
    async def get(self, request, pay_id):
        if len(pay_id) != 36:
            abort(400, "invalid payment id")
        payment_one = await get_payment(pay_id)
        data = PaymentSchema().dump(payment_one, many=True)
        return response.json(data)

    async def post(self, request):
        await insert_one(request.json)
        return text("I have created payment")

    async def put(self, request):
        await update_one(request.json)
        return text("I have updated payment")

    async def delete(self, request):
        await delete_one(request.json)
        return text("I have deleted payment")
