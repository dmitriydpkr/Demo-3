from sanic import Sanic
from service_api.resource.contracts import PaymentsContract
from service_api.resource.payments import *
from service_api.resource.smoke import *

app = Sanic()

app.add_route(Smoke.as_view(), "/")
app.add_route(Smoke.as_view(), "/smoke")

app.add_route(Payments.as_view(), "payments/")  # PUT, POST, GET
app.add_route(Payments.as_view(), "payments/<start>/<finish>")
app.add_route(Payments.as_view(), "payments/<start>/")
app.add_route(Payments.as_view(), "payments//<finish>")


app.add_route(Payment.as_view(), "payment/<pay_id>")
app.add_route(Payment.as_view(), "payment/")  # PUT, POST, GET

app.add_route(PaymentsContract.as_view(), "contract/<contract_id>")  # GET


app.add_task(notification)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8002)
