from sanic import Sanic
from Resource.contracts import PaymentsContract
from Resource.payments import *
from Resource.smoke import *

app = Sanic()

app.add_route(Main.as_view(), '/')
app.add_route(Payments.as_view(), 'payment')
app.add_route(PaymentOne.as_view(), 'payment/<pay_id:int>')
app.add_route(PaymentPeriod.as_view(), 'payment/date/<start>/<finish>')
app.add_route(PaymentPeriod.as_view(), 'payment/date/<start>/')
app.add_route(PaymentsContract.as_view(), 'payment/contract/<contract_number>')
app.add_route(PaymentsCreate.as_view(), '/payment/insert')
app.add_route(PaymentsUpdate.as_view(), '/payment/update')
app.add_route(PaymentsDelete.as_view(), '/payment/delete')

if __name__ == '__main__':
    registration_sda()
    app.run(host="0.0.0.0", port=8001)

