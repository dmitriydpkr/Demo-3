from sanic import response
from Domain.contracts import *
from sanic.response import text
from sanic.views import HTTPMethodView
from forms import PaymentSchema


class PaymentsContract(HTTPMethodView):
    @staticmethod
    async def get(request, contract_number):
        status_contract = await send_request_contracts(contract_number)

        if status_contract == 200:
            payments = await get_contract(contract_number)
            data = PaymentSchema().dump(payments, many=True)
            return response.json(data)
        else:
            return text("Contract not founded")
