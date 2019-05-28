from sanic import response
from service_api.domain.payments import *
from sanic.response import text
from sanic.views import HTTPMethodView
from service_api.resource.forms import PaymentSchema


class Payments(HTTPMethodView):
    async def get(self, request):
        payments = await filter_payments(payment.select())
        data = PaymentSchema().dump(payments, many=True)
        return response.json(data)

    async def post(self, request):
        added_rows = await create_payments(request.json)
        data = PaymentSchema().dump(added_rows, many=True)
        return response.json(data)

    async def put(self, request):
        new_data = await update_payments(request.json)
        return response.text(f"I have updated payments: {new_data}")

    async def delete(self, request):
        request_delete = await delete_payments(request)
        if request_delete == 404:
            return text(f"ID not founded")
        else:
            return text(f"I have deleted payments: {request_delete}")


class Payment(HTTPMethodView):
    async def get(self, request, pay_id):
        query = payment.select().where(payment.c.id == pay_id)
        data_from_db = await filter_payments(query)
        checked_data = PaymentSchema().dump(data_from_db, many=True)
        return response.json(checked_data)

    async def delete(self, request, pay_id):
        request_delete = await delete_payment_by_id(request, pay_id)
        if request_delete == 404:
            return text(f"ID not founded")
        else:
            return text(f"I have deleted payments: {pay_id}")

    async def put(self, request, pay_id):
        payment_id = await update_payment_by_id(request.json, pay_id)
        return text(f"I have updated : {payment_id}")


class PaymentsFilter(HTTPMethodView):
    async def get(self, request):
        payments = await get_params(request)
        data = PaymentSchema().dump(payments, many=True)
        return response.json(data)