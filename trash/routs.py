from sanic import Sanic
from sanic.views import HTTPMethodView
from sanic.response import text
from sanic import response
from forms import *
from database import payment

app = Sanic('some_name')


class StartView(HTTPMethodView):

    def get(self, request):
        payments = Payment.select().where(Payment.id < 20)
        result = payments_schema.dump(payments)
        return response.json(result)

    def post(self, request):
        insert_all(request.json)
        return text('I have worked something')


app.add_route(StartView.as_view(), '/payment')


class SimpleView(HTTPMethodView):

    def get(self, request, pay_id):
        payment = Payment.select().where(Payment.id == pay_id)
        # Serialize the queryset
        result = payments_schema.dump(payment)
        return response.json(result)

    def post(self, request, pay_id):
        insert_one(pay_id)
        return text('I have worked something')

    def put(self, request, pay_id):
        return text('I am put method')

    def delete(self, request, pay_id):
        return text('I am delete method')


app.add_route(SimpleView.as_view(), '/<pay_id:int>')











app.run(host="0.0.0.0", port=8001)
