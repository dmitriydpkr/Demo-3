from sanic import response
from service_api.domain.payments import *
from sanic.response import text
from sanic.views import HTTPMethodView
from service_api.resource.forms import PaymentSchema


class Payments(HTTPMethodView):

    async def get(self, request):
        url_conditions = await get_filter_urls(request.url)
        query_to_database = await combine_query_to_db(url_conditions)

        data_from_db = await query_to_db(query_to_database)
        if (url_conditions != 404 and query_to_database != 404 and data_from_db != 404) or url_conditions == 200:
            validate_data = PaymentSchema().dump(data_from_db, many=True)
            return response.json(validate_data)
        return response.json('Not correct data to db')

    async def post(self, request):
        get_created_rows = await create_payments(request.json)
        if get_created_rows != 404:
            get_checked_data = PaymentSchema().dump(get_created_rows, many=True)
            return response.json(get_checked_data)
        return response.json('JSON has wrong data')

    async def put(self, request):
        get_updated_rows = await update_payments(request.json)
        if get_updated_rows != 404:
            return text(f'Updated such IDS: {get_updated_rows}')
        return response.json('JSON has wrong data')

    async def delete(self, request):
        args_ids = request.args.get("id", "").replace(" ", "").split(",")
        get_deleted_rows = await delete_payments(args_ids)
        if get_deleted_rows != 404:
            return text(f"Payments deleted : {get_deleted_rows}")
        return response.json(f"ID or IDs not founded")


class Payment(HTTPMethodView):

    async def get(self, request, payment_id):
        query = payment.select().where(payment.c.id == payment_id)
        return_data_from_db = await query_to_db(query)
        if return_data_from_db != 404 and len(return_data_from_db) > 0:
            get_checked_data_from_db = PaymentSchema().dump(return_data_from_db, many=True)
            return response.json(get_checked_data_from_db)
        return response.json(f"Payment not founded")

    async def delete(self, request, payment_id):
        perform_delete_id = await delete_payment_by_id(payment_id)
        if perform_delete_id == 200:
            return text(f"Payment deleted : {payment_id}")
        return response.json(f"ID is not founded")

    async def put(self, request, payment_id):
        check_id_db = await check_values_in_db([payment_id], payment.c.id)
        update_row = await update_payment_by_id(request.json, payment_id)
        request_to_db = await query_to_db(payment.select().where(payment.c.id == payment_id))
        if check_id_db != 404 and update_row != 404 and request_to_db != 404:
            get_checked_data_from_db = PaymentSchema().dump(request_to_db, many=True)
            return response.json(get_checked_data_from_db)
        return response.json(f"ID is not correct")


