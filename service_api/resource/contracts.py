from sanic import response
from service_api.domain.contracts import *
from sanic.response import text
from sanic.views import HTTPMethodView
from service_api.resource.forms import PaymentSchema
from service_api.domain.payments import check_values_in_db


class PaymentsContract(HTTPMethodView):
    async def get(self, request):

        contract_ids = request.args.get("id", "").replace(" ", "").split(",")
        contracts_url = await get_service_contracts()
        if contracts_url:
            return text("Contracts service not available")

        if contracts_url != 404:
            get_contracts_ids = await send_request_contracts(
                contracts_url, contract_ids
                )
            if get_contracts_ids != 404:
                payments = await get_contracts(get_contracts_ids)
                data = PaymentSchema().dump(payments, many=True)
                return response.json(data)
        return text("Contracts not founded")
