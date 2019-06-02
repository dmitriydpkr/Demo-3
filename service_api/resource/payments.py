from sanic import response
from service_api.domain.payments import *
from sanic.response import text
from sanic.views import HTTPMethodView
from service_api.resource.forms import PaymentSchema


class Payments(HTTPMethodView):
    async def get(self, request):
        get_all_payments = await query_to_db(payment.select())
        validate_data = PaymentSchema().dump(get_all_payments, many=True)
        return response.json(validate_data)

    async def post(self, request):
        get_created_rows = await create_payments(request.json)
        if get_created_rows != 404:
            validate_data = PaymentSchema().dump(get_created_rows, many=True)
            return response.json(validate_data)
        return text(f"Json data is not valid")

    async def put(self, request):
        get_updated_rows = await update_payments(request.json)
        if get_updated_rows != 404:
            return text(f"Payments were updated : {get_updated_rows}")

        return text(f"Json data is not valid")

    async def delete(self, request):

        get_deleted_rows = await delete_payments(request)
        if get_deleted_rows == 404:
            return text(f"ID or IDs not founded")
        return text(f"Payments deleted : {get_deleted_rows}")


class Payment(HTTPMethodView):
    async def get(self, request, payment_id):
        check_id = await check_values_in_db([payment_id], payment.c.id)
        if check_id:
            query = payment.select().where(payment.c.id == payment_id)
            return_data_from_db = await query_to_db(query)
            get_checked_data = PaymentSchema().dump(return_data_from_db, many=True)
            return response.json(get_checked_data)
        return text(f"ID or IDs not founded")

    async def delete(self, request, payment_id):
        perform_delete_id = await delete_payment_by_id(request, payment_id)
        if perform_delete_id == 404:
            return text(f"ID is not correct")
        return text(f"Payments deleted : {payment_id}")

    async def put(self, request, payment_id):
        check_id = await update_payment_by_id(request.json, payment_id)
        if check_id:
            query = payment.select().where(payment.c.id == payment_id)
            return_data_from_db = await query_to_db(query)
            get_checked_data = PaymentSchema().dump(return_data_from_db, many=True)
            return response.json(get_checked_data)
        return text(f"ID is not correct")


class PaymentsFilter(HTTPMethodView):
    async def get(self, request):
        get_parameters = await get_validate_parameters(request)
        if get_parameters:
            return_data_from_db = await get_data_from_db(get_parameters)
            if return_data_from_db:
                get_checked_data = PaymentSchema().dump(return_data_from_db, many=True)
                return response.json(get_checked_data)
        return text("Incorrect parameters")
