from sanic import response
from service_api.domain.contracts import *
from sanic.response import text
from sanic.views import HTTPMethodView
from forms import PaymentSchema


class PaymentsContract(HTTPMethodView):
    async def get(self, request, contract_id):
        status_contract = await send_request_contracts(contract_id)
        if status_contract == 200:
            payments = await get_contract(contract_id)
            data = PaymentSchema().dump(payments, many=True)
            return response.json(data)
        else:
            return text("Contract not founded")