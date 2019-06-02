from service_api.resource.contracts import PaymentsContract
from service_api.resource.payments import *
from service_api.resource.smoke import *
from sanic import Sanic


app = Sanic()

app.add_route(Smoke.as_view(), "/")
app.add_route(Smoke.as_view(), "/smoke")
app.add_route(Payments.as_view(), "payments/")  # PUT, POST, GET, DELETE


app.add_route(PaymentsFilter.as_view(), "payments/filter")  # GET

app.add_route(Payment.as_view(), "payment/<payment_id>")  # PUT, POST, GET, DELETE


app.add_route(PaymentsContract.as_view(), "payments/contracts/")  # GET


# "payment/<pay_id:[A-Fa-f0-9]{8}-[A-Fa-f0-9]{4}-[A-Fa-f0-9]{4}-[A-Fa-f0-9]{4}-[A-Fa-f0-9]{12}>",
