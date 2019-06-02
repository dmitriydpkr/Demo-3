from sanic import response
from service_api.domain.contracts import *
from sanic.response import text
from sanic.views import HTTPMethodView
from service_api.resource.forms import PaymentSchema
from service_api.domain.payments import validate_id, check_values_in_db


class PaymentsContract(HTTPMethodView):
    async def get(self, request):
        get_contracts_ids = [0]
        contract_ids = request.args.get("id", "").replace(" ", "").split(",")

        if contract_ids[0]:
            check_id = await validate_id(contract_ids)

            if check_id:
                contracts_url = await get_service_contracts()

                if contracts_url != 404:
                    get_contracts_ids = await send_request_contracts(
                        contracts_url, contract_ids
                    )

        if get_contracts_ids[0]:
            check_id_db = await check_values_in_db(
                get_contracts_ids, payment.c.contract_id
            )
            if check_id_db:
                payments = await get_contracts(get_contracts_ids)
                data = PaymentSchema().dump(payments, many=True)
                return response.json(data)
        return text("Contracts not founded")
