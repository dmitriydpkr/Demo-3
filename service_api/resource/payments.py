from sanic import response
from service_api.domain.payments import *
from sanic.response import text
from sanic.views import HTTPMethodView
from service_api.resource.forms import PaymentSchema


class Payments(HTTPMethodView):

    async def get(self, request):

        url_conditions = await get_filter_urls(request.url)
        if 'filter' in url_conditions:
            array_conditions = await get_array_conditions(url_conditions)
            form_query_to_db = payment.select().where(array_conditions[0])
            data_from_db = await query_to_db(form_query_to_db)
        else:
            data_from_db = await query_to_db(payment.select())
            if data_from_db != 404:
                validate_data = PaymentSchema().dump(data_from_db, many=True)
                return response.json(validate_data)
        return text('Not correct request')

    async def post(self, request):
        get_created_rows = await create_payments(request.json)
        get_checked_data = PaymentSchema().dump(get_created_rows, many=True)
        return response.json(get_checked_data)

    async def put(self, request):
        get_updated_rows = await update_payments(request.json)
        return text(f'Updated such IDS: {get_updated_rows}')

    async def delete(self, request):
        args_ids = request.args.get("id", "").replace(" ", "").split(",")
        check_values_db = await check_values_in_db(args_ids, payment.c.id)
        if check_values_db:
            get_deleted_rows = await delete_payments(args_ids)
            if get_deleted_rows != 404:
                return text(f"Payments deleted : {get_deleted_rows}")
        return text(f"ID or IDs not founded")


class Payment(HTTPMethodView):

    async def get(self, request, payment_id):
        query = payment.select().where(payment.c.id == payment_id)
        return_data_from_db = await query_to_db(query)
        get_checked_data_from_db = PaymentSchema().dump(return_data_from_db, many=True)
        return response.json(get_checked_data_from_db)

    async def delete(self, request, payment_id):
        check_id_db = await check_values_in_db([payment_id], payment.c.id)
        if check_id_db:
            perform_delete_id = await delete_payment_by_id(request, payment_id)
            if perform_delete_id != 404:
                return text(f"Payments deleted : {payment_id}")
        return text(f"ID is not founded")

    async def put(self, request, payment_id):

        check_id_db = await check_values_in_db([payment_id], payment.c.id)
        if check_id_db:
            query = payment.select().where(payment.c.id == payment_id)
            return_data_from_db = await query_to_db(query)
            get_checked_data_from_db = PaymentSchema().dump(return_data_from_db, many=True)
            return response.json(get_checked_data_from_db)
        return text(f"ID is not correct")

