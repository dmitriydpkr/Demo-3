from sanic import response
from service_api.domain.contracts import *
from sanic.response import text
from sanic.views import HTTPMethodView
from service_api.resource.forms import PaymentSchema
from service_api.domain.models import payment
from service_api.resource.payments import get_filter_urls, parse_filter, parse_operator_values, \
    query_to_db, combine_query_to_db


class PaymentsContract(HTTPMethodView):
    async def get(self, request):

        url_conditions = await get_filter_urls(request.url)

        if url_conditions != 404:
            url = url_conditions[0]
            filter_contract = await parse_filter(url)
            get_array_operator_value = await parse_operator_values(url, filter_contract)
            operator, values = get_array_operator_value[0], get_array_operator_value[1]
            contracts_url = await get_service_contracts()

            if contracts_url != 404:
                try:
                    async with aiohttp.ClientSession() as session:

                        data = f"{contracts_url}?filter=id%20{operator}%20{values}"
                        print(data, 'here')
                        response_json = await session.get(data)
                        get_json = await response_json.json()
                        contracts_ids = await get_json_ids(get_json, 'id')
                        prepared_values = values.replace('(', '').replace(')', '').replace("'", '').split(',')

                        check_ids = [1]
                        for id_value in prepared_values:
                            if id_value not in contracts_ids:
                                check_ids.append(0)
                        if all(check_ids):
                            query = await combine_query_to_db(url_conditions)
                            data_from_db = await query_to_db(query)
                            validate_data = PaymentSchema().dump(data_from_db, many=True)
                            return response.json(validate_data)
                except Exception as exc:
                    logging.error('Connection to service contracts refused. ERROR')
        return text("Contract url is not correct")