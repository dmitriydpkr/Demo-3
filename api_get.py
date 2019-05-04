from sanic import Sanic
from sanic import response
from serializers import *
from functions import *
from sanic.response import text
import requests

app = Sanic('some_name')


# GET

@app.route('/')
async def get_handler(request):
    return response.json({'message': 'Hello world!'}, headers={'Service': 'SDA'}, status=200)


@app.route('/payment')
async def get_all(request):
    payment_rows = await get_all_payments()
    result = payments_schema.dump(payment_rows)
    return response.json(result)


@app.route('payment/<pay_id>')
async def get_all(request, pay_id):
    payment_row = await get_one_payment(pay_id)
    result = payments_schema.dump(payment_row)
    return response.json(result)


@app.route('payment/date/<start>/<finish>')
async def get_payments_for_period(request, start, finish):
    payment_rows = await get_payment_period(start, finish)
    result = payments_schema.dump(payment_rows)
    return response.json(result)


@app.route('payment/contragent/<contr_id>')
async def get_payments_contragent(request, contr_id):
    contragent_rows = await get_one_contragent(contr_id)
    result = payments_schema.dump(contragent_rows)
    return response.json(result)


@app.route('payment/contract/<contract_id>')
async def get_payments_contracts(request, contract_id):
    contract_rows = await get_one_contract(contract_id)
    result = payments_schema.dump(contract_rows)
    return response.json(result)


def registration_sda():
    sda = "http://0.0.0.0:7000/"
    data = {"message": "Hello SDA, it is Payments!", "service": "Payments", 'host': "0.0.0.0", 'port': 8001}
    headers = {'Content-type': 'application/json'}
    try:
        requests.post(sda, json=data, headers=headers)
    except requests.exceptions.RequestException as err:  # This is the correct syntax
        print(err)


if __name__ == '__main__':
    registration_sda()
    app.run(host="0.0.0.0", port=8001)

